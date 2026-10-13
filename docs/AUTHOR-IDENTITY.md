# Author identity links

Every author page links Google Scholar. Where an identity is confirmed, the page also links ORCID, a homepage and the author's publication page. This file explains where those links come from and how to add more.

## Files

| File | Role |
| --- | --- |
| `curation/author-identities.json` | The reviewed links. Single source of truth; `scripts/curate.py` copies it into `public/data/authors.json`. |
| `curation/author-candidates.csv` | Review sheet produced by `scripts/author_candidates.py`, sorted by priority. |
| `curation/.cache/` | Raw API responses (not committed). Delete it to force a fresh lookup. |

## Confirmation rules

A link is published only with a source and a check date.

- **ORCID.** OpenAlex aligns each corpus paper's authorships with the verified byline. The ORCID that OpenAlex attaches to the matched author is a candidate only, because OpenAlex sometimes merges people with the same name. It is confirmed when the public ORCID record lists a corpus paper (by DOI or exact title) and the record's name matches the byline.
- **Homepage.** The first non-social URL in a confirmed ORCID record.
- **Google Scholar.** Accepted automatically when the confirmed ORCID record lists the profile, or when the author's own homepage or publication page links exactly one Scholar profile. When the two sources disagree, nothing is accepted. Otherwise a curator checks by hand that the profile lists a corpus paper under the same byline. Scholar is never queried by script.
- No link is guessed from a name search. An author without a confirmed profile keeps the exact-name Scholar search link.

## Refresh the candidates

```bash
python3 scripts/author_candidates.py            # rewrite the review sheet only
python3 scripts/author_candidates.py --accept   # also merge links that meet the rules above
python3 scripts/curate.py                       # copy links into public/data
pnpm check
```

`--accept` never overwrites an existing entry. A differing candidate is printed as `CONFLICT` for a curator to resolve.

## Add a Scholar profile by hand

1. Open `curation/author-candidates.csv` and pick an author with priority 1 (two or more corpus papers) and no `current_scholar`.
2. Open the `scholar_search` link and find the profile that lists one of the `corpus_papers` under the same byline.
3. Add the profile to `curation/author-identities.json` under the author ID:

   ```json
   "author-id": {
     "scholarUrl": "https://scholar.google.com/citations?user=XXXXXXXXXXXX&hl=en",
     "scholarSource": "Curator check: profile lists <paper short name>",
     "identityChecked": "YYYY-MM-DD"
   }
   ```

4. If two people share the name and the right profile is unclear, leave the entry out. The review sheet is regenerated on every run, so do not keep notes in it.
5. Run `python3 scripts/curate.py` and `pnpm check`.

## Import a browser-check CSV

A curator-run browser check (for example an AI browsing agent following the paper-first steps above) returns a CSV with `author_id, paper_id, status, scholar_user_id, profile_name, profile_affiliation, paper_listed, other_papers_listed, note`. Import the confirmed rows with:

```bash
python3 scripts/import_scholar_review.py path/to/results.csv --label 'how it was checked'
```

Rows are rejected when the author is not on the paper, the ID is malformed, the profile name differs from the byline, the author already has a link, or the ID belongs to another author.

The validator rejects Scholar URLs without a `user=` ID, a Scholar profile or ORCID used for two authors, invalid ORCID checksums, and links without a source or check date.
