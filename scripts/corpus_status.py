"""Report which corpus papers have a local PDF in corpus/ (git-ignored).

Name each file <paper_id>.pdf, e.g. corpus/etbert.pdf. The paper id is the ?paper= value in
the atlas URL. Writes corpus/STATUS.md (have / missing with source links / unmatched files)
and prints a one-line summary.

Usage: python3 scripts/corpus_status.py
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / 'corpus'


def main():
    papers = json.load(open(ROOT / 'public/data/papers.json'))
    CORPUS.mkdir(exist_ok=True)
    files = {f.stem: f for f in CORPUS.iterdir() if f.suffix.lower() == '.pdf'}
    ids = {p['id'] for p in papers}
    have = [p for p in papers if p['id'] in files]
    missing = sorted((p for p in papers if p['id'] not in files), key=lambda p: (p.get('reviewDepth') != 'Metadata and abstract', p['year']))
    unmatched = sorted(s for s in files if s not in ids)
    lines = ['# Corpus PDFs', '', f'{len(have)} of {len(papers)} papers have a PDF. Name files `<paper_id>.pdf`.', '',
             '## Missing', '', '| paper_id | year | paper | review depth | source |', '|---|---|---|---|---|']
    lines += [f"| `{p['id']}` | {p['year']} | {p['short']} | {p.get('reviewDepth', '')} | {p['url']} |" for p in missing]
    if unmatched:
        lines += ['', '## Files that match no paper id', ''] + [f'- `{s}.pdf`' for s in unmatched]
    lines += ['', '## Have', ''] + [f"- `{p['id']}` {p['short']}" for p in have]
    (CORPUS / 'STATUS.md').write_text('\n'.join(lines) + '\n')
    print(f'{len(have)}/{len(papers)} PDFs present, {len(missing)} missing, {len(unmatched)} unmatched -> corpus/STATUS.md')


if __name__ == '__main__':
    main()
