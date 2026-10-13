# Contributing to NTC Atlas

Thank you for helping keep the atlas accurate. The corpus is curated by hand, so every change needs a source that a reviewer can check.

## Ways to help

| You want to | Use |
| --- | --- |
| Suggest a paper | Issue form **New paper suggestion** |
| Fix a title, author list, year, venue or link | **Incorrect metadata** |
| Fix an author identity, alias or profile link | **Author identity correction** |
| Ask for technical details from a paper | **Technical extraction request** |
| Report a problem with the site | **Bug report** |

Pull requests are welcome for small, sourced data fixes and for code. Please open an issue first for larger changes.

## Evidence rules

- **Primary sources.** Verify title, full author list and order, year and venue against the original paper, DOI record, publisher, proceedings or official repository. Secondary indexes and Google Scholar are leads only.
- **Preprint or peer-reviewed.** Record which version you checked. Do not merge distinct follow-up models into one record.
- **Evidence records.** Each analytical statement needs a source URL, source type, locator (section, table or page), verification status and access date.
- **Relationships.** Add an extension, critique or comparison edge only when a source states it. Chronology is not evidence of succession, and a baseline comparison is not a successor.
- **Authors.** A byline on a relevant paper is the only route into the author list. An old byline does not establish a current affiliation. Committee membership is not a publication.
- **Missing values.** Use a qualified NA: `not reported in reviewed sections`, `not applicable` or `not yet extracted`.
- **Results.** Keep dataset, split, task, metric and unit with every number. Offline samples per second are not live throughput.
- **Interpretation.** Label curator synthesis as such and link it to evidence. Absence from this corpus is not absence from the field.

## Making a change locally

```bash
corepack enable
pnpm install --frozen-lockfile
# edit scripts/curate.py (or the relevant JSON), then:
python3 scripts/curate.py
pnpm counts
pnpm check
```

`pnpm check` runs data validation, type-checking, linting and the production build, the same steps as CI. Please do not weaken a validation rule to make a change pass. Explain the case in the pull request instead.

## Weekly discovery candidates

A scheduled workflow lists possible new papers in a weekly issue. Candidates are leads only. They enter `public/data/` after a human has verified them against primary sources. See [docs/MAINTENANCE.md](docs/MAINTENANCE.md).

## Licence of contributions

Code contributions are accepted under the MIT licence and data contributions under CC BY 4.0, matching [LICENSE](LICENSE) and [LICENSE-DATA](LICENSE-DATA).
