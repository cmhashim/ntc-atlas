"""Report which corpus papers have a local PDF in corpus/ (git-ignored).

Files are named <paper_id>.pdf, e.g. corpus/etbert.pdf (the ?paper= value in the atlas URL).
Downloads can keep their original names: with --rename, a PDF whose first two pages contain
exactly one corpus paper's title is renamed to that paper's id. Writes corpus/STATUS.md
(have / missing with source links / unmatched files) and prints a one-line summary.

Usage: python3 scripts/corpus_status.py [--rename]
"""
import json, re, subprocess, sys, unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / 'corpus'


def norm(s):
    return re.sub(r'[^a-z0-9]+', ' ', unicodedata.normalize('NFKC', s).lower()).strip()


def match_by_title(pdf, papers):
    """Paper ids whose title appears in the PDF's first two pages (pdftotext)."""
    try:
        text = subprocess.run(['pdftotext', '-l', '2', str(pdf), '-'], capture_output=True, text=True, timeout=60).stdout
    except (OSError, subprocess.TimeoutExpired):
        return []
    flat = norm(text)
    return [p['id'] for p in papers if len(norm(p['title'])) > 15 and norm(p['title']) in flat]


def main():
    papers = json.load(open(ROOT / 'public/data/papers.json'))
    CORPUS.mkdir(exist_ok=True)
    ids = {p['id'] for p in papers}
    for f in sorted(CORPUS.glob('*.pdf')):
        if f.stem in ids:
            continue
        hits = match_by_title(f, papers)
        if len(hits) == 1 and not (CORPUS / f'{hits[0]}.pdf').exists():
            if '--rename' in sys.argv:
                f.rename(CORPUS / f'{hits[0]}.pdf')
                print(f'renamed {f.name} -> {hits[0]}.pdf')
            else:
                print(f'{f.name} looks like {hits[0]} (run with --rename)')
        else:
            print(f'{f.name}: {"no title match" if not hits else "ambiguous " + ", ".join(hits)}')
    files = {f.stem: f for f in CORPUS.iterdir() if f.suffix.lower() == '.pdf'}
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
