"""Build a review sheet of author identity candidates.

For every corpus paper this looks up the work in OpenAlex (DOI, arXiv DOI or
exact title), aligns OpenAlex authorships with the verified byline, and reads
the public ORCID record of each matched author. An ORCID counts as confirmed
only when that ORCID record lists a corpus paper by the same author. Google
Scholar is never queried: the sheet carries an author-search link for a
manual check.

Output: curation/author-candidates.csv (review sheet, committed) and
curation/.cache/ (raw API responses, ignored by git).

Usage: python3 scripts/author_candidates.py [--accept]

--accept merges values that meet the confirmation rules into
curation/author-identities.json without overwriting existing entries:
  orcid       the ORCID record lists a corpus paper and the name matches
  homepageUrl first non-social URL in that confirmed ORCID record
  scholarUrl  listed in the confirmed ORCID record, or the only Scholar
              profile linked from the author's own homepage or publication
              page; never accepted when the two sources disagree
"""
import csv, datetime, hashlib, json, re, sys, time, unicodedata, urllib.parse, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / 'curation/.cache'
OUT = ROOT / 'curation/author-candidates.csv'
IDENTITIES = ROOT / 'curation/author-identities.json'
UA = 'ntc-atlas-curation (+https://github.com/cmhashim/ntc-atlas)'


def get_json(url, headers=None):
    CACHE.mkdir(parents=True, exist_ok=True)
    path = CACHE / (hashlib.sha1(url.encode()).hexdigest() + '.json')
    if path.exists():
        return json.loads(path.read_text())
    req = urllib.request.Request(url, headers={'User-Agent': UA, 'Accept': 'application/json', **(headers or {})})
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                data = json.load(r)
            break
        except urllib.error.HTTPError as e:
            if e.code == 404:
                data = None
                break
            if e.code != 429 or attempt == 3:
                raise
        except urllib.error.URLError:
            if attempt == 3:
                raise
        time.sleep(2 ** attempt)
    time.sleep(0.2)
    path.write_text(json.dumps(data))
    return data


def norm(s):
    s = unicodedata.normalize('NFKD', s or '').encode('ascii', 'ignore').decode().lower()
    return re.sub(r'[^a-z0-9]+', ' ', s).strip()


def name_tokens(s):
    return norm(s.replace('-', '')).split()


def same_person_name(a, b):
    ta, tb = name_tokens(a), name_tokens(b)
    if not ta or not tb:
        return False
    if sorted(ta) == sorted(tb) or ''.join(ta) == ''.join(tb):
        return True
    return ta[-1] == tb[-1] and ta[0][0] == tb[0][0]


def identifiers(url):
    doi = re.search(r'(10\.\d{4,9}/[^\s?#]+)', url)
    arxiv = re.search(r'arxiv\.org/(?:abs|pdf|html)/(\d{4}\.\d{4,5})', url)
    return (doi.group(1).rstrip('/').lower() if doi else None,
            arxiv.group(1) if arxiv else None)


def openalex_work(paper):
    doi, arxiv = identifiers(paper['url'])
    for d in [doi, f'10.48550/arxiv.{arxiv}' if arxiv else None]:
        if d:
            w = get_json(f'https://api.openalex.org/works/doi:{urllib.parse.quote(d)}')
            if w and norm(w.get('title')) == norm(paper['title']):
                return w, 'DOI' if d == doi else 'arXiv DOI'
    q = urllib.parse.quote(re.sub(r'[:,]', ' ', paper['title']))
    res = get_json(f'https://api.openalex.org/works?filter=title.search:{q}&per-page=10')
    for w in (res or {}).get('results', []):
        if norm(w.get('title')) == norm(paper['title']):
            return w, 'exact title'
    return None, 'not found'


SOCIAL = ('linkedin.com', 'researchgate.net', 'twitter.com', 'x.com/', 'facebook.com', 'qa.elsevierpure.com',
          'scholar.google', 'orcid.org', 'github.com/')


def scholar_id(url):
    m = re.search(r'[?&]user=([A-Za-z0-9_-]{12})', url)
    return m.group(1) if m else None


def scholar_on_page(url):
    """Scholar profile IDs linked from an author's own page (one HTTP GET, no crawling)."""
    CACHE.mkdir(parents=True, exist_ok=True)
    path = CACHE / (hashlib.sha1(('page:' + url).encode()).hexdigest() + '.html')
    if not path.exists():
        try:
            req = urllib.request.Request(url, headers={'User-Agent': UA})
            with urllib.request.urlopen(req, timeout=20) as r:
                path.write_text(r.read(2_000_000).decode('utf-8', 'replace'))
        except Exception:
            path.write_text('')
        time.sleep(0.5)
    html = path.read_text().replace('&amp;', '&')
    return sorted(set(m for m in re.findall(r'scholar\.google\.[a-z.]+/citations\?[^"\'<> ]*?user=([A-Za-z0-9_-]{12})', html)))


def orcid_record(orcid):
    oid = orcid.rsplit('/', 1)[-1]
    person = get_json(f'https://pub.orcid.org/v3.0/{oid}/person') or {}
    works = get_json(f'https://pub.orcid.org/v3.0/{oid}/works') or {}
    titles, dois = set(), set()
    for g in works.get('group', []):
        for s in g.get('work-summary', []):
            titles.add(norm(((s.get('title') or {}).get('title') or {}).get('value')))
        for x in (g.get('external-ids') or {}).get('external-id', []):
            if x.get('external-id-type') == 'doi':
                dois.add(x['external-id-value'].lower())
    urls = [u['url']['value'] for u in (person.get('researcher-urls') or {}).get('researcher-url', [])]
    name = person.get('name') or {}
    full = ' '.join(filter(None, [((name.get('given-names') or {}).get('value')), ((name.get('family-name') or {}).get('value'))]))
    return dict(id=oid, name=full, titles=titles, dois=dois, urls=urls)


def auto_identity(confirmed, best, scholar, from_page, homepage, author, papers):
    if not confirmed:
        best = None
    out, today = {}, datetime.date.today().isoformat()
    if best:
        out['orcid'] = best[0]
        out['orcidSource'] = 'ORCID record lists ' + ', '.join(best[1])
    if homepage:
        out['homepageUrl'] = homepage
        out['homepageSource'] = 'Linked from the confirmed ORCID record'
    page_ids = from_page if len(from_page) == 1 else []
    ids = set(scholar) | set(page_ids)
    if len(ids) == 1 and (not scholar or not page_ids or scholar == page_ids):
        sid = ids.pop()
        out['scholarUrl'] = f'https://scholar.google.com/citations?user={sid}&hl=en'
        out['scholarSource'] = ' and '.join(filter(None, [
            'listed in the confirmed ORCID record' if scholar else '',
            'linked from the author\'s own page' if page_ids else '']))
    if out:
        out['identityChecked'] = today
    return out


def accept(rows):
    current = json.loads(IDENTITIES.read_text()) if IDENTITIES.exists() else {}
    added, conflicts = 0, []
    for r in rows:
        auto = r['_auto']
        entry = current.setdefault(r['id'], {})
        for key in ['orcid', 'homepageUrl', 'scholarUrl']:
            if key not in auto:
                continue
            if key in entry:
                same = entry[key] == auto[key] or (key == 'scholarUrl' and scholar_id(entry[key]) == scholar_id(auto[key]))
                if not same:
                    conflicts.append(f"{r['id']}.{key}: kept {entry[key]}, candidate {auto[key]}")
                continue
            entry[key] = auto[key]
            entry[key.replace('Url', '') + 'Source'] = auto[key.replace('Url', '') + 'Source']
            entry['identityChecked'] = auto['identityChecked']
            added += 1
        if not entry:
            del current[r['id']]
    IDENTITIES.write_text(json.dumps(dict(sorted(current.items())), ensure_ascii=False, indent=2) + '\n')
    print(f'accepted {added} new links into {IDENTITIES.relative_to(ROOT)}')
    for c in conflicts:
        print('CONFLICT', c)


def main():
    P = json.load(open(ROOT / 'public/data/papers.json'))
    A = json.load(open(ROOT / 'public/data/authors.json'))
    by_name = {a['name']: a for a in A}
    found = {a['id']: dict(openalex=set(), orcid=set(), via=set()) for a in A}
    lookup = []
    for p in P:
        work, how = openalex_work(p)
        lookup.append((p['id'], how))
        if not work:
            continue
        ships = work.get('authorships', [])
        for i, name in enumerate(p['authors']):
            cands = [ships[i]] if i < len(ships) else []
            cands += [s for s in ships if s not in cands]
            for s in cands:
                if any(same_person_name(name, n) for n in [s.get('raw_author_name'), s['author'].get('display_name')]):
                    f = found[by_name[name]['id']]
                    if s['author'].get('id'):
                        f['openalex'].add(s['author']['id'].rsplit('/', 1)[-1])
                    if s['author'].get('orcid'):
                        f['orcid'].add(s['author']['orcid'].rsplit('/', 1)[-1])
                    f['via'].add(p['id'])
                    break

    paper_by_id = {p['id']: p for p in P}
    rows = []
    for a in A:
        f = found[a['id']]
        papers = [paper_by_id[x] for x in a['papers']]
        first_last = any(p['authors'][0] == a['name'] or p['authors'][-1] == a['name'] for p in papers)
        priority = 1 if len(papers) > 1 else 2 if first_last else 3
        orcid_rows = []
        for oid in sorted(f['orcid']):
            rec = orcid_record(oid)
            hits = [p['short'] for p in papers
                    if norm(p['title']) in rec['titles'] or (identifiers(p['url'])[0] or '#') in rec['dois']]
            name_ok = same_person_name(a['name'], rec['name']) if rec['name'] else False
            orcid_rows.append((oid, hits, name_ok, rec['urls']))
        confirmed = [o for o in orcid_rows if o[1] and o[2]]
        best = confirmed[0] if confirmed else (orcid_rows[0] if orcid_rows else None)
        urls = best[3] if best else []
        scholar = sorted(set(filter(None, (scholar_id(u) for u in urls if 'scholar.google' in u))))
        other = [u for u in urls if not scholar_id(u) and 'scholar.google' not in u]
        homepage = next((u for u in other if not any(x in u for x in SOCIAL)), '') if confirmed else ''
        pages = [u for u in [homepage, a.get('publicationsUrl')] if u]
        from_page = sorted(set(i for u in pages for i in scholar_on_page(u)))
        rows.append({
            'priority': priority,
            'id': a['id'],
            'name': a['name'],
            'corpus_papers': '; '.join(p['short'] for p in papers),
            'current_scholar': a.get('scholarUrl', ''),
            'openalex_ids': ' '.join(sorted(f['openalex'])),
            'orcid': best[0] if best else '',
            'orcid_status': ('confirmed: lists ' + ', '.join(best[1])) if confirmed else
                            ('unconfirmed: ORCID record does not list a corpus paper' if best else ''),
            'orcid_conflict': 'yes' if len(f['orcid']) > 1 else '',
            'scholar_from_orcid': ' '.join(scholar) if confirmed else '',
            'homepage_from_orcid': homepage,
            'scholar_from_homepage': ' '.join(from_page),
            'urls_from_orcid': ' '.join(other) if confirmed else '',
            'scholar_search': 'https://scholar.google.com/citations?view_op=search_authors&mauthors='
                              + urllib.parse.quote(a['name']),
        })
        rows[-1]['_auto'] = auto_identity(confirmed, best, scholar, from_page, homepage, a, papers)
    rows.sort(key=lambda r: (r['priority'], r['name']))
    if '--accept' in sys.argv:
        accept(rows)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT, 'w', newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=[k for k in rows[0] if k != '_auto'], extrasaction='ignore')
        w.writeheader()
        w.writerows(rows)
    missing = [pid for pid, how in lookup if how == 'not found']
    print(f'papers matched in OpenAlex: {len(P) - len(missing)}/{len(P)}')
    print(f'authors with an OpenAlex ID: {sum(bool(r["openalex_ids"]) for r in rows)}/{len(rows)}')
    print(f'authors with an ORCID candidate: {sum(bool(r["orcid"]) for r in rows)}')
    print(f'ORCID confirmed by a corpus paper: {sum(r["orcid_status"].startswith("confirmed") for r in rows)}')
    print(f'Scholar links found in confirmed ORCID records: {sum(bool(r["scholar_from_orcid"]) for r in rows)}')
    print(f'homepages found in confirmed ORCID records: {sum(bool(r["homepage_from_orcid"]) for r in rows)}')
    print(f'Scholar links found on author homepages: {sum(bool(r["scholar_from_homepage"]) for r in rows)}')
    print('papers not found in OpenAlex:', ', '.join(missing) or 'none')
    print(f'wrote {OUT.relative_to(ROOT)}')


if __name__ == '__main__':
    main()
