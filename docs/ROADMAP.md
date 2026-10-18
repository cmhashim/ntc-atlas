# Roadmap

What still needs doing to make NTC Atlas a dependable reference for researchers. Counts were taken from `public/data/` on 2026-10-13; re-check them with the snippet at the bottom before starting a section.

Priorities: **P1** blocks trust in the atlas, **P2** makes it useful day to day, **P3** grows reach.

## P1. Author identity and profile links

Currently: 274 authors; **171** have a confirmed Google Scholar profile (147 of them from browser checks on 2026-10-13, 2026-10-14 and 2026-10-16, automated profile re-check pending), **83** a confirmed ORCID iD, **23** a homepage, **3** a publication page; **86** have a verified (dated) affiliation, **188** still "Needs verification". Rules and workflow: [AUTHOR-IDENTITY.md](AUTHOR-IDENTITY.md).

- [x] Add schema fields to `Author`: `orcid`, `homepageUrl`, each with its own source and check date (`identityChecked`).
- [x] Semi-automate the candidate step: `scripts/author_candidates.py` aligns OpenAlex authorships with the bylines, confirms ORCID iDs against the ORCID record's works, and writes `curation/author-candidates.csv`. Google Scholar is checked by hand only (no scraping).
- [ ] Re-check the 147 browser-checked Scholar profiles against their profile pages (Scholar was rate-limiting on 2026-10-13).
- [ ] Check Google Scholar for the remaining 103 authors (80 of 81 papers have had at least one browser pass, the CNSM 2023 few-shot study added 2026-10-18 has not; these authors had no profile that lists a corpus paper, so the next pass is name-first search with the confirmation rule below). Order of work: authors with 2+ corpus papers first (priority 1 in the sheet), then first and last authors, then the rest. Confirmation rule: the profile lists at least one corpus paper with the same byline. Record "no confirmed profile" rather than guessing.
- [ ] Six papers are not found in OpenAlex (BLINC, DeepMAL, Refinery, LEO, AKEM, Trustee); check their authors by hand.
- [ ] Add DBLP person pages (`dblpUrl`); DBLP's API currently sits behind a bot check, so this needs manual links or a later API route.
- [ ] Add an institutional page where no homepage exists. Keep affiliation (dated, with source) separate from byline verification.
- [x] Validator: Scholar links must be direct `user=` profiles, no profile or ORCID shared by two authors, ORCID checksum, every link has a source and check date.
- [ ] Author identity correction issues are answered within two weeks.

## P1. Paper metadata and evidence quality

Currently: 81 papers, all bibliographically verified, **all** with technical status "Needs verification". **83** of 379 evidence records are "Needs verification". **51** papers have no verified code link.

- [ ] Add explicit `doi` and `arxivId` fields to every paper (today the identifier is only in the URL). Validator: no duplicate DOI or arXiv ID.
- [ ] Re-check the 82 unverified evidence records against their primary sources.
- [ ] Find official code/artefact links for the 50 papers without one, or record "no public artefact found (checked YYYY-MM-DD)".
- [ ] Audit the two `Precedes` relationships: an edge needs a source that states the link; chronology alone is not evidence.
- [ ] Close the five evidence boundaries listed on the Methodology page (TrafficFormer, PERT, Flow-MAE, App-Time/App-Ver, BiasSeeker proceedings). See [RESEARCH-BACKLOG.md](RESEARCH-BACKLOG.md).
- [ ] Derive the site's "Updated" date from the newest evidence access date instead of the hand-set `meta.updated` (shows 2026-09-23; records changed 2026-10-04).

## P2. Technical extraction (what researchers come for)

Currently: **64** of 81 papers are reviewed from metadata and abstract only; **1,868** comparison fields read "NA — not extracted".

- [ ] Full-text extraction for the most-used models first (ET-BERT, YaTC, NetMamba, NetMamba+, TrafficFormer, netFound, PERT, Flow-MAE), then all 2025-2026 papers.
- [ ] Priority fields: datasets with version, split unit, class count, metric, reported result, throughput/latency with hardware and scope, open-world and cross-dataset setup.
- [ ] Pretraining/evaluation overlap: record which datasets each pretrained model saw, and flag evaluations on the same data (possible leakage).
- [ ] Each extracted value keeps unit, scope and locator; offline inference rates are never shown as live throughput.

## P2. Researcher features

- [ ] **Comparable results view**: results grouped only when dataset version, split unit, task and metric all match; everything else shown as "not comparable" with the reason.
- [ ] **Dataset usage page**: how many papers use each dataset, known caveats, label provenance, and which results share a dataset.
- [x] **Review-depth badge** on every Paper library row ("In depth" for the 16 papers with full-text sections, "Abstract only" for the rest), an "In-depth only" switch, and a Compare picker that lists in-depth papers unless abstract-only papers are switched on. Prevents comparisons that are mostly NA. (From an external critique, 2026-10-14.)
- [x] **"Start here" preset** in the Paper library: the curator-flagged seminal papers, oldest first.
- [ ] Trim "Start here" to a short curated reading path (about 15 papers, foundations plus key critiques), each linked to its explainer once one exists. The curator outlook itself is published separately as research briefings.
- [ ] **What's new** page and an RSS/Atom feed of additions and corrections, fed by the weekly discovery review.
- [ ] Search by DOI or arXiv ID; copy BibTeX from every paper card.
- [ ] Shareable link previews (Open Graph title, description and image) for paper, author and dataset URLs.

## P2. Engineering and quality

- [ ] Strengthen `scripts/validate-data.mjs`: duplicate DOI/arXiv, normalised-title duplicates, reciprocal author and dataset links, edges without evidence, placeholder text marked verified, unqualified NA, invalid URLs, stale README counts.
- [ ] Playwright tests in CI: query-string navigation, search and filters, sorting and pagination, comparison, author profile links, exports (CSV/JSON/BibTeX), one graph, mobile layout.
- [ ] Weekly discovery workflow (Crossref, OpenAlex, arXiv, DBLP) that opens one review issue; nothing enters `public/data/` without human verification. Document it in `docs/MAINTENANCE.md`.
- [ ] Fix the tab row: the last tab is clipped at 1440 px width; make it scroll or wrap visibly.
- [ ] Add a `404.html` so mistyped data URLs return an error instead of the home page.
- [ ] Split the 500 kB+ JavaScript chunk (load graph views on demand).
- [ ] Accessibility pass: keyboard navigation of every view, focus order, colour contrast in both themes.
- [ ] Privacy-friendly usage statistics (Cloudflare Web Analytics, no cookies) to see which views researchers use.

## P3. Coverage and reach

Currently: 26 papers from 2025-2026.

- [ ] Run the weekly discovery review and add verified papers, especially on calibration, energy, edge/cloud cascades, open-world detection and LLM-based traffic models.
- [ ] Biweekly paper explainers ("One NTC paper, explained"), each linking to the paper's atlas page.
- [ ] Zenodo integration: a DOI for every tagged release of the atlas.
- [ ] Custom domain.

## Re-counting

```bash
python3 - <<'EOF'
import json
A=json.load(open('public/data/authors.json')); P=json.load(open('public/data/papers.json')); E=json.load(open('public/data/evidence.json'))
print('direct scholar', sum('user=' in (a.get('scholarUrl') or '') for a in A), '/', len(A))
print('orcid', sum(bool(a.get('orcid')) for a in A), 'homepage', sum(bool(a.get('homepageUrl')) for a in A))
print('affiliation verified', sum(a['status']=='Verified' for a in A))
print('evidence needing verification', sum(e['status']!='Verified' for e in E))
print('no code link', sum(not p['code'] for p in P))
print('abstract-only papers', sum(p['reviewDepth']=='Metadata and abstract' for p in P))
print('NA not extracted', sum(str(v).startswith('NA — not extracted') for p in P for v in p['details'].values()))
EOF
```
