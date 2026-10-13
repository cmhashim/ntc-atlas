# Roadmap

What still needs doing to make NTC Atlas a dependable reference for researchers. Counts were taken from `public/data/` on 2026-10-13; re-check them with the snippet at the bottom before starting a section.

Priorities: **P1** blocks trust in the atlas, **P2** makes it useful day to day, **P3** grows reach.

## P1. Author identity and profile links

Currently: 272 authors; **4** have a direct Google Scholar profile, **3** a publication page, **77** a verified (dated) affiliation, **195** still "Needs verification".

- [ ] Add schema fields to `Author`: `orcid`, `dblpUrl`, `homepageUrl`, `institutionUrl`, each with its own source and check date.
- [ ] For every author, link the **direct** Google Scholar profile when the identity is confirmed. Confirmation rule: the profile lists at least one corpus paper with the same byline, and the name/affiliation match. Never substitute a name search for a confirmed profile, and record "no confirmed profile" rather than guessing.
- [ ] Add a personal homepage or institutional page where one exists. Keep affiliation (dated, with source) separate from byline verification.
- [ ] Order of work: authors with 2+ corpus papers first, then first and last authors, then the rest.
- [ ] Semi-automate the candidate step: look up OpenAlex author IDs, ORCID and DBLP for each byline and write a review sheet. A human confirms every match. Google Scholar is checked by hand only (no scraping).
- [ ] Validator: fail on a Scholar link that is a search URL when `scholarUrl` with `user=` exists; fail on malformed ORCID iDs (checksum).
- [ ] Author identity correction issues are answered within two weeks.

## P1. Paper metadata and evidence quality

Currently: 80 papers, all bibliographically verified, **all** with technical status "Needs verification". **82** of 373 evidence records are "Needs verification". **50** papers have no verified code link.

- [ ] Add explicit `doi` and `arxivId` fields to every paper (today the identifier is only in the URL). Validator: no duplicate DOI or arXiv ID.
- [ ] Re-check the 82 unverified evidence records against their primary sources.
- [ ] Find official code/artefact links for the 50 papers without one, or record "no public artefact found (checked YYYY-MM-DD)".
- [ ] Audit the two `Precedes` relationships: an edge needs a source that states the link; chronology alone is not evidence.
- [ ] Close the five evidence boundaries listed on the Methodology page (TrafficFormer, PERT, Flow-MAE, App-Time/App-Ver, BiasSeeker proceedings). See [RESEARCH-BACKLOG.md](RESEARCH-BACKLOG.md).
- [ ] Derive the site's "Updated" date from the newest evidence access date instead of the hand-set `meta.updated` (shows 2026-09-23; records changed 2026-10-04).

## P2. Technical extraction (what researchers come for)

Currently: **64** of 80 papers are reviewed from metadata and abstract only; **1,846** comparison fields read "NA — not extracted".

- [ ] Full-text extraction for the most-used models first (ET-BERT, YaTC, NetMamba, NetMamba+, TrafficFormer, netFound, PERT, Flow-MAE), then all 2025-2026 papers.
- [ ] Priority fields: datasets with version, split unit, class count, metric, reported result, throughput/latency with hardware and scope, open-world and cross-dataset setup.
- [ ] Pretraining/evaluation overlap: record which datasets each pretrained model saw, and flag evaluations on the same data (possible leakage).
- [ ] Each extracted value keeps unit, scope and locator; offline inference rates are never shown as live throughput.

## P2. Researcher features

- [ ] **Comparable results view**: results grouped only when dataset version, split unit, task and metric all match; everything else shown as "not comparable" with the reason.
- [ ] **Dataset usage page**: how many papers use each dataset, known caveats, label provenance, and which results share a dataset.
- [ ] **Free "Start here" reading path** for newcomers (the curator outlook itself is published separately as research briefings).
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
print('affiliation verified', sum(a['status']=='Verified' for a in A))
print('evidence needing verification', sum(e['status']!='Verified' for e in E))
print('no code link', sum(not p['code'] for p in P))
print('abstract-only papers', sum(p['reviewDepth']=='Metadata and abstract' for p in P))
print('NA not extracted', sum(str(v).startswith('NA — not extracted') for p in P for v in p['details'].values()))
EOF
```
