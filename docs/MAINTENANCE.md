# Maintenance

How the atlas is kept current. The corpus is curated by hand. Automation only proposes leads; nothing enters `public/data/` without a human check against a primary source.

## Weekly discovery review

`.github/workflows/discovery.yml` runs every Monday at 06:00 UTC and can be started by hand under **Actions → Weekly discovery → Run workflow** (the `days` input sets the look-back window, default 7).

It runs `scripts/discover.py`, which:

1. Queries OpenAlex, arXiv (cs.NI, cs.CR, cs.LG, three seconds between calls) and Crossref with eight queries covering the atlas scope: encrypted traffic classification, deep-learning traffic classification, traffic foundation models, website and app fingerprinting, in-network (P4, SmartNIC) classification, open-world and zero-day traffic, and datasets, benchmarks, shortcuts and leakage.
2. Merges duplicates by DOI, arXiv id and normalised title, and drops anything already in `public/data/papers.json` (same normalised title, DOI or arXiv id in the paper URL).
3. Scores each remaining record by keyword hits in the title and abstract. A record needs at least one core phrase such as "traffic classification" or "encrypted traffic" and a score of 5. Each core phrase scores 3, a core phrase in the title adds 3, and extra terms (encrypted, TLS/QUIC/VPN/Tor, fingerprint, pretraining, open-world, P4/SmartNIC, shortcut, leakage and similar) add 1 or 2. The thresholds and word lists are at the top of the script.
4. Keeps the top 30 and writes a Markdown checklist: title, first three authors, venue and date, link, sources, matched keywords and a two-sentence abstract snippet.

The workflow opens one issue titled `Discovery review YYYY-MM-DD` with the label `discovery`. With zero candidates it opens nothing. If one source is down, the issue names it under "Failed sources" and the other sources still run. The workflow has `contents: read` and `issues: write` permissions only. It never commits and never touches `public/data/`.

Set the repository variable `DISCOVERY_MAILTO` to a contact address to use the polite pools of OpenAlex and Crossref. It is optional. To try the script locally:

```bash
python3 scripts/discover.py --days 30 --out /tmp/discovery.md   # add --json for JSON
```

The score is a keyword count and nothing more. Expect some off-topic records (intrusion detection, 5G management) and some deposits that are not papers. Skip them.

## Triaging a discovery issue

Work through the checklist. For each candidate, open the link and decide.

**Accept.** Verify first (see the rules below). Then add the paper to `scripts/curate.py` with `add(id, short, title, authors, year, venue, url, family, unit, summary, contribution, risk, gap, **kw)`:

- `id` is a short unique slug (it becomes the `?paper=` value) and `short` is the label shown on cards.
- `authors` is one string with names joined by `|`, in byline order, as printed by the source.
- `url` is the publisher, DOI or arXiv record you checked. `venue` and `year` come from the same record.
- `family` and `unit` use the existing family and unit values already used by other `add()` calls.
- `summary`, `contribution`, `risk` and `gap` are short paraphrases of what the abstract states plus the curator's open question.

`add()` creates a bibliography evidence record, a paper-claim record and a curator-interpretation record for you, sets every comparison field to "Needs verification" and every gap column to "Not addressed/not reported" (scoped to the reviewed abstract). Record full-text findings later with `detail()`, relationships with `rel()` and datasets with `ds()`, each with its own source and locator. Add authors through their verified byline only.

Then regenerate and check:

```bash
python3 scripts/curate.py
pnpm counts
pnpm check
```

Commit the change in a pull request, tick the box in the issue and reference the paper id.

**Reject.** Close the checklist item with a reason in a comment (off scope, not a paper, duplicate or new version of a paper already present, not verifiable). A candidate that may fit but cannot be verified yet goes to the pending queue in `scripts/curate.py` (the `pending=[...]` list). Close the issue when every item is resolved.

## Verification rules

These repeat [CONTRIBUTING.md](../CONTRIBUTING.md).

- The bibliographic record comes from the publisher, DOI record, proceedings or the arXiv record. Discovery output, OpenAlex, Crossref and Google Scholar are leads, never sources.
- Every field has a locator (section, table, page or "Abstract / bibliographic record") and a source URL. Nothing is filled from memory.
- No invented metadata. Use the qualified NA forms (`not reported in reviewed sections`, `not applicable`, `not yet extracted`) when a value is missing.
- Record whether the version checked is a preprint or the peer-reviewed paper. Keep distinct follow-up models as separate records.
- A relationship (extension, critique, comparison) needs a source that states it.

## Other recurring upkeep

- **Author identities.** Links to ORCID, homepage, Scholar and publication pages are confirmed by the process in [AUTHOR-IDENTITY.md](AUTHOR-IDENTITY.md): run `python3 scripts/author_candidates.py`, review `curation/author-candidates.csv`, and rebuild with `python3 scripts/curate.py`.
- **Corpus PDFs.** PDFs live in the git-ignored `corpus/` folder, named `<paper_id>.pdf`. `python3 scripts/corpus_status.py` writes `corpus/STATUS.md` (have, missing, unmatched). Use `--rename` to name downloads by paper id and `--import DIR` to copy matching PDFs from a folder such as Zotero storage.
- **README counts.** After any data change run `pnpm counts` to rewrite the counts table. `pnpm validate` (part of `pnpm check`) fails on a stale table.
- **Cloudflare token.** The deploy workflow uses the secrets `CLOUDFLARE_API_TOKEN` (Account → Cloudflare Pages → Edit) and `CLOUDFLARE_ACCOUNT_ID`. Roll the API token once a year: create a new token with the same scope, replace the repository secret, trigger **Check and deploy** by hand to confirm, then delete the old token.
