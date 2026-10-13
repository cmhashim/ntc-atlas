# Validation record — 22 September 2026

## Original publication (51-paper corpus)

- Data integrity: PASS. 51 papers, 18 datasets, 214 bylines, 60 verified affiliations, 28 relationships, 239 evidence records. No orphan source/target/evidence IDs; 16 gap states per paper; dataset reverse references; duplicate/version invariants.
- TypeScript: PASS before packaging; repeated by publication workflow after final edits.
- Browser: timeline point opens paper, search, year zoom/pan/reset, seminal toggle, comparison of ET-BERT/YaTC/NetMamba, author-to-paper filtering, dataset-to-paper filtering, connection focus, gap evidence panel, table sorting and pagination, theme switch, share URL and reload restoration.
- Mobile: 390px iframe, actual content width 373px including scrollbar; no page-level horizontal overflow. Charts and wide tables scroll within their sections. Search and theme switch tested.
- Scale: temporary 200-record display fixture rendered all 200 timeline marks, 12 paper rows and 25 gap rows per page. Synthetic fixture removed before publication. Filtering/sorting microbenchmark also checks 200 records; this is not a production load benchmark.
- CSV/JSON: downloaded eight-paper exports parsed successfully; CSV has 64 columns; JSON includes authors, datasets and evidence.
- BibTeX: clipboard export validated at 51 entries. The automation browser held .bib downloads as unconfirmed files, so final browser download completion is unverified. Copy BibTeX and inline citations provide usable alternatives.
- No application console errors observed; browser extension metadata errors are unrelated to the application.
- Optional WebMCP invocation could not be tested because navigator.modelContext was unavailable.
- External source checks are bibliographic research checks, not an automated guarantee of ongoing HTTP availability. Some publishers restrict full-text extraction.
- No machine-learning experiment was independently reproduced. Technical extraction remains explicitly incomplete.

## Publication-driven corpus update

- Data integrity: PASS. 55 papers, 19 datasets, 221 bylines, 67 verified affiliations, 38 relationships, 272 evidence records. Every author has at least one supported publication; all references and gap evidence resolve.
- Both requested papers have technical extraction, evidence, related authors, dataset links, gap judgements and directed relationships. Trustee, NTC Enigma and CipherSpectrum expand the relevant research context.
- Earlier evidence IDs, contents and access dates are unchanged. BibTeX now uses each paper’s bibliographic-source access date.
- TypeScript: PASS after data and interface updates. The publication workflow builds the updated application and source download.
- No new browser interaction run for this data/text update; browser results above apply to the original publication. No model experiment was rerun.
- Bias in the Shadows is reviewed from arXiv v1; proceedings status remains explicitly pending primary confirmation.

## 23 September interface and comparison update

- Integrity: PASS, 55 papers, 19 datasets, 221 authors, 67 resolved affiliations, 38 relationships and 285 evidence records. Added field-source and research-outlook reference checks and NetMamba+ extension invariant.
- Browser: labelled Transformer timeline and zoom/reset; NetMamba all-relations view and successors/foundations filter; absent graph mini-map; research outlook reading links and five-paper comparison action; populated throughput rows and qualified NA/source links. Desktop comparison stays within page width (1348px content / 1363px viewport).
- Console: no application errors observed; browser-extension metadata errors excluded.
- TypeScript passed after schema/UI edits; final workflow repeats integrity, typecheck and production build.
- Thirteen records now have selected full-text/artifact review; 14 records receive technical/comparison enrichment, including existing reported results. Remaining fields explicitly distinguish unextracted evidence from unreported measurements. No model experiments rerun.
- Prior mobile/200-mark browser checks remain historical; this update has focused desktop browser QA and the 200-record data benchmark.

## 23 September author-led expansion

- Integrity: PASS, 72 papers, 254 authors, 68 resolved affiliations, 19 datasets, 42 relationships, 344 evidence records. All 17 additions are dated 2023 or later. All 285 earlier evidence records remain unchanged.
- Browser: Nimesha search and selection show both NTC Enigma and LiM; ISCX label provenance panel exposes evidence/assignment/meaning and audit source; research outlook displays three review lenses and nine directions; selecting label provenance changes the study proposal. No page-level desktop overflow.
- No application console errors observed; browser extension metadata errors excluded.
- TypeScript, integrity and production build run in the publication workflow. Earlier mobile checks remain historical. Research extraction is scoped and no model experiments were rerun.

## 23 September verification closeout

- Official NeurIPS Datasets and Benchmarks 2025 proceedings verified for Demystifying Network Foundation Models, including title, five names and DOI. Technical details remain tied to the reviewed arXiv v3.
- Three papers were added from primary publisher, conference or author records: PTU (ICNP 2024), MM4flow (CCS 2025), Mean MAE (arXiv 2026). Mean MAE Section IV and Table VI support datasets, metrics, hardware, training resources and offline inference rate. Publication and review depth remain explicit.
- Five targeted evidence boundaries replace the nine-item mixed queue; no unresolved field has been silently filled.
- Integrity: 75 papers, 267 authors, 75 resolved affiliations, 19 datasets, 42 relationships, 354 evidence records. Final TypeScript and build run through the publication workflow.
- Author identity UX: Zhuotao Liu is resolved to the Tsinghua institutional profile, personal publication list and supplied Google Scholar profile. The author view no longer describes an unverified affiliation as an unverified identity; all 267 author pages expose a Scholar profile or exact-name search.
- Luming Yang audit: supplied Scholar ID matched to publisher metadata and author repositories. PASS with six linked papers (five newly added), 80 total papers, 272 authors, 77 resolved affiliations, 46 relationships and 373 evidence records.
- Xiaohui Xie identity link: direct Google Scholar ID `j0yTuxoAAAAJ` and official Tsinghua publication homepage stored; regression assertions prevent fallback to a generic name search.
