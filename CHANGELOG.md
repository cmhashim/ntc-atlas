# Changelog

Corpus and interface changes before the GitHub repository was created (source v10). Counts quoted below were correct at the time of each entry; current counts come from `public/data/` and are shown in the README and on the site. Later changes are recorded in the git history.

## 2026-09-22: publication-driven update

Added **ShortcutCatcher** (Yuqi Zhao et al., DOI 10.1145/3808671), **Bias in the Shadows / BiasSeeker** (Chuyi Wang et al.), **Trustee**, and **SoK: Decoding the Enigma of Encrypted Network Traffic Classifiers**, plus CipherSpectrum and ten supported relationships. Added seven authors and updated the relevant existing profiles. Removed the fixed example-author checklist; every displayed author must have a verified publication in scope.

ShortcutCatcher’s simulated network shifts are distinguished from independent cross-organisation evaluation. BiasSeeker’s statistical screening is distinguished from causal proof and retains its need for expert interpretation. Both paper records expose the reviewed version, experimental setup, limitations and gap evidence. Reported scores are not independently reproduced.

## 2026-09-23: usability and research update

Timeline labels use collision-aware lanes; graph mini-maps are removed. Connections show all relationships by default, with a successors/foundations filter distinguishing documented extensions from baseline comparisons. NetMamba+ extends NetMamba.

Comparison enrichment covers 14 core model and systems records, with 33 technical fields, field-level sources, hardware, batch size and measurement scope. All 55 papers use qualified NA where extraction is incomplete; this is not a completed audit of every experimental field. Throughput retains its reported unit and boundary.

Research outlook offers six evidence-scoped directions, concrete experiments, metrics, feasibility notes, a reading path and a performance-unit guide. It does not infer field-wide saturation or novelty from missing corpus evidence.

## 2026-09-23 to 2026-10-04: author-led expansion

Added 20 relevant papers from 2023 onward, including LiM / NetMatrix, the flow-label provenance SoK and both requested 2026 surveys. The corpus now links 267 authors to 75 papers. This is a scoped author-led search, not a complete audit of every author’s bibliography.

Author pages now distinguish a verified publication byline from a separately verified affiliation. Every page links either a confirmed Google Scholar profile or an exact-name Scholar search. Zhuotao Liu’s Tsinghua profile, publication page and Scholar identity are explicitly linked.

Audited Luming Yang’s supplied Scholar identity against publisher records and author repositories. Added EVS2vec (2023), ExpMD (2024), unFlowS (2025), Robustness Matters (2025) and SemiAF (2025), alongside the existing MM4flow record. The corpus now contains 80 papers and 272 verified paper bylines.

Replaced Xiaohui Xie’s generic Scholar search with the supplied direct Scholar profile and added his official Tsinghua publication homepage (checked 2026-10-04).

Seven dataset panels separate label evidence, assignment units and semantic targets, with version caveats and an audit checklist. Research outlook now has nine directions, three review lenses and an expanded reading path. Reported measurements retain units and experimental boundaries; survey-only and unextracted fields retain explicit NA reasons. Publisher abstracts/previews support the two survey records; their full experimental tables were not reviewed.

The final three additions in this review are PTU (IEEE ICNP 2024), MM4flow (ACM CCS 2025), and Mean MAE (2026 arXiv v1). Mean MAE reports 5,343 offline inference samples/s in its Table VI on one RTX 4080; that number is not live network throughput. The official NeurIPS 2025 proceedings now confirm Demystifying Network Foundation Models. Five narrowly scoped evidence boundaries remain visible in Methodology; their source links and per-paper NA reasons explain what has not been extracted.

## 2026-10-12: repository created

Imported source v10 into git, replaced the Cloudflare Worker build with a static export, and added CI deployment to Cloudflare Pages. The research outlook moved out of the public atlas into subscriber research briefings; its view now shows a placeholder.
