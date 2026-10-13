"""Import confirmed rows from a Scholar review CSV into curation/author-identities.json.

The CSV comes from a curator-run browser check (header: author_id, paper_id,
status, scholar_user_id, profile_name, profile_affiliation, paper_listed,
other_papers_listed, note). Only status=confirmed rows with paper_listed=yes are
used. Rows are rejected when the author is not on the paper, the ID is malformed,
the profile name does not match the byline, or the author already has a link.

Usage: python3 scripts/import_scholar_review.py <review.csv> [--label TEXT]
"""
import csv, datetime, json, re, sys
from collections import defaultdict
from pathlib import Path
from author_candidates import same_person_name

ROOT = Path(__file__).resolve().parents[1]
IDENTITIES = ROOT / 'curation/author-identities.json'


def main():
    path = Path(sys.argv[1])
    label = sys.argv[sys.argv.index('--label') + 1] if '--label' in sys.argv else 'curator browser check'
    P = {p['id']: p for p in json.load(open(ROOT / 'public/data/papers.json'))}
    A = {a['id']: a for a in json.load(open(ROOT / 'public/data/authors.json'))}
    current = json.loads(IDENTITIES.read_text())
    used = {m.group(1): aid for aid, e in current.items()
            if (m := re.search(r'user=([A-Za-z0-9_-]{12})', e.get('scholarUrl', '')))}
    found, rejected = defaultdict(lambda: {'ids': set(), 'papers': set()}), []
    for r in csv.DictReader(open(path)):
        if r['status'] != 'confirmed':
            continue
        a, p, sid = A.get(r['author_id']), P.get(r['paper_id']), r['scholar_user_id'].strip()
        why = ('unknown author or paper' if not a or not p else
               'author not on paper' if a['name'] not in p['authors'] else
               'paper not listed' if r['paper_listed'] != 'yes' else
               'malformed ID' if not re.fullmatch(r'[A-Za-z0-9_-]{12}', sid) else
               'profile name differs' if not same_person_name(a['name'], re.sub(r',.*', '', r['profile_name'])) else
               'author already linked' if current.get(a['id'], {}).get('scholarUrl') else
               'ID already used by ' + used[sid] if sid in used and used[sid] != a['id'] else '')
        if why:
            rejected.append(f"{r['author_id']} ({r['paper_id']}): {why}")
            continue
        f = found[a['id']]
        f['ids'].add(sid)
        f['papers'] |= {r['paper_id']} | {x for x in r['other_papers_listed'].split() if x in a['papers']}
    today, added = datetime.date.today().isoformat(), 0
    for aid, f in sorted(found.items()):
        if len(f['ids']) > 1:
            rejected.append(f'{aid}: conflicting IDs {sorted(f["ids"])}')
            continue
        sid = f['ids'].pop()
        shorts = ', '.join(P[x]['short'] for x in sorted(f['papers']))
        current.setdefault(aid, {}).update(
            scholarUrl=f'https://scholar.google.com/citations?user={sid}&hl=en',
            scholarSource=f'Profile lists {shorts} ({label})',
            identityChecked=today)
        used[sid] = aid
        added += 1
    IDENTITIES.write_text(json.dumps(dict(sorted(current.items())), ensure_ascii=False, indent=2) + '\n')
    print(f'added {added} Scholar profiles')
    for x in rejected:
        print('REJECTED', x)


if __name__ == '__main__':
    main()
