#!/usr/bin/env python3
"""Weekly candidate discovery for the NTC Atlas (stdlib only).

Queries OpenAlex, arXiv and Crossref for recent works in the atlas scope, removes duplicates and
anything already in public/data/papers.json, scores the rest by keyword hits and prints a Markdown
checklist for human review. It only reads papers.json and never writes to public/data/.

Usage: python3 scripts/discover.py [--days 7] [--top 30] [--out FILE] [--json]
Env:   DISCOVERY_MAILTO  optional contact address for the OpenAlex/Crossref polite pool.
"""
import argparse, datetime as dt, html, json, os, re, sys, time, unicodedata
import urllib.error, urllib.parse, urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT / 'public/data/papers.json'
MAILTO = os.environ.get('DISCOVERY_MAILTO', '').strip()
UA = 'ntc-atlas-discovery/1.0 (https://github.com/cmhashim/ntc-atlas' + (f'; mailto:{MAILTO})' if MAILTO else ')')

QUERIES = [
    'encrypted traffic classification',
    'network traffic classification deep learning',
    'traffic foundation model pretrained traffic representation',
    'website fingerprinting machine learning',
    'mobile app fingerprinting encrypted traffic',
    'in-network traffic classification programmable switch P4 SmartNIC',
    'open-world traffic classification unknown applications zero-day',
    'traffic classification dataset benchmark shortcut data leakage',
]

# Transparent scoring. A candidate needs at least one CORE phrase hit and score >= MIN_SCORE.
# Each CORE phrase adds CORE_W, a core phrase in the title adds 3, EXTRA terms add their weight once.
CORE = [r'traffic classification', r'traffic classifier', r'encrypted traffic', r'network traffic',
        r'traffic identification', r'traffic fingerprint', r'website fingerprint', r'app fingerprint', r'application fingerprint',
        r'traffic analysis', r'flow classification', r'packet classification', r'traffic recognition',
        r'traffic foundation model', r'traffic representation', r'traffic transformer']
EXTRA = [(r'encrypted', 2), (r'\btls\b|\bquic\b|\bvpn\b|\btor\b', 2), (r'fingerprint', 2),
         (r'pre-?train|foundation model|self-supervised|contrastive|transformer|\bllm\b', 2),
         (r'open-world|open set|zero-day|unknown (?:class|application|traffic)|novelty', 2),
         (r'\bp4\b|smartnic|programmable (?:switch|data ?plane)|in-network|\bebpf\b|\bfpga\b', 2),
         (r'shortcut|data leakage|leakage|benchmark|dataset|concept drift|robustness|calibration', 1),
         (r'\bflow\b|\bpacket\b|\bpcap\b', 1), (r'deep learning|neural|machine learning', 1)]
CORE_W, MIN_SCORE = 3, 5
# Off-topic matches that look relevant by keywords (road traffic, air traffic, ...).
NEGATIVE = re.compile(r'road traffic|vehicle|vehicular|traffic (?:flow|light|signal) (?:predict|forecast)|traffic sign|'
                      r'air traffic|urban traffic|traffic congestion|pedestrian', re.I)


def norm(s):
    return re.sub(r'[^a-z0-9]+', ' ', unicodedata.normalize('NFKC', html.unescape(s or '')).lower()).strip()


def norm_doi(d):
    d = (d or '').lower().strip()
    return re.sub(r'^(?:https?://(?:dx\.)?doi\.org/|doi:)', '', d) or None


ARXIV_RE = re.compile(r'arxiv\.org/(?:abs|pdf)/([a-z\-]+/\d{7}|\d{4}\.\d{4,5})', re.I)


def arxiv_id(s):
    m = ARXIV_RE.search(s or '')
    return m.group(1).lower() if m else None


def fetch(url, retries=2):
    last = None
    for i in range(retries + 1):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': UA})
            with urllib.request.urlopen(req, timeout=40) as r:
                return r.read()
        except (urllib.error.URLError, TimeoutError, OSError) as e:
            last = e
            time.sleep(2 * (i + 1))
    raise last


def clean(s):
    return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', html.unescape(s or ''))).strip()


# ---- sources -------------------------------------------------------------------------------
def from_openalex(since):
    out = []
    for q in QUERIES:
        p = {'search': q, 'filter': f'from_publication_date:{since}', 'per-page': 50}
        if MAILTO:
            p['mailto'] = MAILTO
        data = json.loads(fetch('https://api.openalex.org/works?' + urllib.parse.urlencode(p, safe=':,|')))
        for w in data.get('results', []):
            inv = w.get('abstract_inverted_index') or {}
            words = sorted((pos, t) for t, ps in inv.items() for pos in ps)
            loc = w.get('primary_location') or {}
            links = ' '.join(str(l.get('landing_page_url')) for l in w.get('locations', []) if l)
            out.append(dict(source='OpenAlex', title=clean(w.get('title')), doi=norm_doi(w.get('doi')),
                            arxiv=arxiv_id(links),
                            authors=[a['author']['display_name'] for a in w.get('authorships', [])],
                            venue=((loc.get('source') or {}).get('display_name') or ''),
                            date=w.get('publication_date') or '',
                            url=w.get('doi') or loc.get('landing_page_url') or w.get('id'),
                            abstract=' '.join(t for _, t in words)))
        time.sleep(1)
    return out


def from_arxiv(since):
    out = []
    cats = '(cat:cs.NI OR cat:cs.CR OR cat:cs.LG)'
    ns = {'a': 'http://www.w3.org/2005/Atom'}
    start = since.replace('-', '') + '0000'
    end = dt.date.today().strftime('%Y%m%d') + '2359'
    for q in QUERIES:
        terms = ' AND '.join(f'all:{w}' for w in re.findall(r'[A-Za-z0-9\-]+', q)[:3])
        sq = f'{cats} AND ({terms}) AND submittedDate:[{start} TO {end}]'
        url = 'http://export.arxiv.org/api/query?' + urllib.parse.urlencode(
            {'search_query': sq, 'max_results': 50, 'sortBy': 'submittedDate', 'sortOrder': 'descending'})
        root = ET.fromstring(fetch(url))
        for e in root.findall('a:entry', ns):
            link = e.findtext('a:id', '', ns)
            doi = e.find('{http://arxiv.org/schemas/atom}doi')
            out.append(dict(source='arXiv', title=clean(e.findtext('a:title', '', ns)),
                            doi=norm_doi(doi.text if doi is not None else None), arxiv=arxiv_id(link),
                            authors=[clean(a.findtext('a:name', '', ns)) for a in e.findall('a:author', ns)],
                            venue='arXiv', date=(e.findtext('a:published', '', ns) or '')[:10], url=link,
                            abstract=clean(e.findtext('a:summary', '', ns))))
        time.sleep(3)  # arXiv API etiquette: one call per 3 s
    return out


def from_crossref(since):
    out = []
    for q in QUERIES:
        p = {'query': q, 'filter': f'from-pub-date:{since}', 'rows': 40,
             'select': 'DOI,title,author,container-title,issued,URL,abstract,type'}
        if MAILTO:
            p['mailto'] = MAILTO
        data = json.loads(fetch('https://api.crossref.org/works?' + urllib.parse.urlencode(p, safe=':,')))
        for w in data['message'].get('items', []):
            parts = (w.get('issued') or {}).get('date-parts') or [[]]
            date = '-'.join(f'{x:02d}' if i else str(x) for i, x in enumerate(parts[0] or []))
            out.append(dict(source='Crossref', title=clean((w.get('title') or [''])[0]), doi=norm_doi(w.get('DOI')),
                            arxiv=None,
                            authors=[' '.join(filter(None, [a.get('given'), a.get('family')])) for a in w.get('author', [])],
                            venue=clean((w.get('container-title') or [''])[0]), date=date, url=w.get('URL'),
                            abstract=clean(w.get('abstract'))))
        time.sleep(1)
    return out


SOURCES = [('OpenAlex', from_openalex), ('arXiv', from_arxiv), ('Crossref', from_crossref)]


# ---- processing ----------------------------------------------------------------------------
def load_known():
    titles, dois, arx = set(), set(), set()
    for p in json.loads(PAPERS.read_text()):
        titles.add(norm(p['title']))
        u = p.get('url') or ''
        a = arxiv_id(u)
        if a:
            arx.add(a)
        m = re.search(r'10\.\d{4,9}/\S+', u)
        if m:
            dois.add(m.group(0).lower().rstrip('/'))
    return titles, dois, arx


SUPPLEMENT = re.compile(r'dataset and|artifacts?\b|checkpoints|supplementary|replication package|per-flow', re.I)


def score(c):
    raw = c['title'] + ' ' + c['abstract']
    # Zenodo data/artifact deposits of papers are not papers themselves.
    if NEGATIVE.search(raw) or ('zenodo' in c['venue'].lower() and SUPPLEMENT.search(c['title'])):
        return 0, []
    text, title = norm(raw), norm(c['title'])
    core = [p for p in CORE if re.search(p, text)]
    if not core:
        return 0, []
    kws = [p.replace('(?:', '').replace(')', '').replace('\\', '') for p in core]
    s = CORE_W * len(core)
    for pat, w in EXTRA:
        m = re.search(pat, text)
        if m:
            s += w
            kws.append(m.group(0))
    if any(re.search(p, title) for p in CORE):
        s += 3
    return s, sorted(set(kws))


def merge(cands):
    out, index = [], {}

    def keys(c):
        k = [('t', norm(c['title']))]
        if c['doi']:
            k.append(('d', c['doi']))
        if c['arxiv']:
            k.append(('a', c['arxiv']))
        return k

    for c in cands:
        if not c['title']:
            continue
        hit = next((index[k] for k in keys(c) if k in index), None)
        if hit is None:
            hit = dict(c, sources=[c['source']])
            out.append(hit)
        else:
            if c['source'] not in hit['sources']:
                hit['sources'].append(c['source'])
            for f in ('doi', 'arxiv', 'url', 'date'):
                hit[f] = hit.get(f) or c[f]
            if not hit['venue'] or (hit['venue'] == 'arXiv' and c['venue']):
                hit['venue'] = c['venue'] or hit['venue']
            if len(c['abstract']) > len(hit['abstract']):
                hit['abstract'] = c['abstract']
            if len(c['authors']) > len(hit['authors']):
                hit['authors'] = c['authors']
        for k in keys(c):
            index[k] = hit
    return out


def snippet(a, n=2, width=260):
    s = ' '.join(re.split(r'(?<=[.!?])\s+', clean(a))[:n])
    return (s[:width].rsplit(' ', 1)[0] + '...') if len(s) > width else s


def render(cands, today, since, failed, total):
    L = [f'# Discovery review {today}', '',
         f'Window: {since} to {today}. {len(cands)} candidates from {total} raw hits. '
         'Relevance is a keyword score, not a judgement.',
         'Nothing here is verified. Check every field against the publisher or arXiv record before adding anything.', '']
    if failed:
        L += ['**Failed sources:** ' + '; '.join(f'{n} ({e})' for n, e in failed), '']
    for c in cands:
        au = ', '.join(c['authors'][:3]) + (' et al.' if len(c['authors']) > 3 else '')
        L += [f"- [ ] **{c['title']}**",
              f"  - Authors: {au or 'not listed'}",
              f"  - Venue / date: {c['venue'] or 'unknown'}, {c['date'] or 'undated'}",
              f"  - Link: {c['url']}",
              f"  - Sources: {', '.join(c['sources'])}; score {c['score']}; keywords: {', '.join(c['keywords'])}"]
        if c['abstract']:
            L.append(f"  - Abstract: {snippet(c['abstract'])}")
    return '\n'.join(L) + '\n'


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--days', type=int, default=7)
    ap.add_argument('--top', type=int, default=30)
    ap.add_argument('--out')
    ap.add_argument('--json', action='store_true', help='emit JSON instead of Markdown')
    a = ap.parse_args()
    today = dt.date.today()
    since = (today - dt.timedelta(days=a.days)).isoformat()
    raw, failed = [], []
    for name, fn in SOURCES:
        try:
            r = fn(since)
            raw += r
            print(f'{name}: {len(r)} hits', file=sys.stderr)
        except Exception as e:  # one failing source must not stop the others
            failed.append((name, f'{type(e).__name__}: {e}'))
            print(f'{name}: FAILED {e}', file=sys.stderr)
    kt, kd, ka = load_known()
    cands = []
    for c in merge(raw):
        if norm(c['title']) in kt or (c['doi'] and c['doi'] in kd) or (c['arxiv'] and c['arxiv'] in ka):
            continue
        c['score'], c['keywords'] = score(c)
        if c['score'] >= MIN_SCORE:
            cands.append(c)
    cands.sort(key=lambda c: (-c['score'], -len(c['sources']), c['title']))
    cands = cands[:a.top]
    if a.json:
        body = json.dumps(dict(date=today.isoformat(), since=since, failed=failed,
                               candidates=[{k: v for k, v in c.items() if k != 'source'} for c in cands]),
                          indent=2, ensure_ascii=False)
    else:
        body = render(cands, today.isoformat(), since, failed, len(raw))
    if a.out:
        Path(a.out).write_text(body)
    else:
        print(body)
    print(f'{len(cands)} candidates', file=sys.stderr)
    return 1 if len(failed) == len(SOURCES) else 0


if __name__ == '__main__':
    sys.exit(main())
