# AI usage log

A running log of AI-assisted work on this project (Claude Code). Each entry records what
was asked, what was changed, the assumptions the AI made without being told, and what the
developer should double-check. The **Developer review** and **Tokens** fields are filled in
by the developer, never by the AI. This file feeds `AI_USAGE.md` in the repo root.

Entry times for the first three entries are taken from file modification times (the
exploration entry has no file, so its time is only bounded).

Token figures are measured, not estimated. They are summed from the `usage` fields that
Claude Code saved in the session transcript (`~/.claude/projects/.../15d2b4d1-....jsonl`),
for all model requests made while answering the prompt behind each entry. "Input (uncached)"
is small because most input is served from the prompt cache; add the cache write and cache
read figures to get the total input processed. Screenshots go in `docs/ai-usage/`.

### 2026-10-26 before 14:21 — Explore the repo (read-only)
- **Asked:** Show the file tree, full TASK.md and every other file, git log/branches, and report on requirements and ambiguities. No changes allowed.
- **Generated/changed:** None (read-only: `ls`, `cat`, `wc`, `git log`, `git branch -a`, `git remote -v`, `git status`).
- **Assumptions I made:**
  - Treated `README.md` (the fork/submit guide) as the only non-TASK file worth printing; there was nothing else to find.
  - Reformatted the printed TASK.md/README.md code fences as indented blocks so the output could be copied inside a single code block. Text was otherwise verbatim.
  - Listed my own "ambiguities to clarify" (input formats, persistence, README conflict, etc.). These are my judgement of what is unclear, not statements from TASK.md.
- **Unsure about / please check:**
  - My claim that "grading has no rubric" is based only on what is in the repo. There may be criteria shared elsewhere (email, invite).
  - The deadline is not in the repo; I could not determine it.
- **Developer review:** Read the repo exploration report. Decided to keep setup instructions in README.md and move the submission guide to docs/SUBMISSION_GUIDE.md. Confirmed scope constraints: CSV format only, rules engine (no ML), SQLite persistence with CSV export, and persistent merchant override rules.
- **Tokens:** Input (uncached): 8 | Cache write: 2,940 | Cache read: 113,556 | Output: 4,288 | Model: Opus 5.5

### 2026-10-26 14:21 — Create CLAUDE.md and .gitignore
- **Asked:** Create `CLAUDE.md` with the given content and a `.gitignore` covering Python, Node, env files, DBs, OS/editor files and `.claude/settings.local.json`.
- **Generated/changed:** `CLAUDE.md` (created, content as given), `.gitignore` (created).
- **Assumptions I made:**
  - Added `!.env.example` after `.env.*` so the example file stays tracked (implied by "but NOT .env.example").
  - Added comment headers to group the `.gitignore` patterns.
  - Did not add other common ignores (coverage files, `*.log`, `.env.local` is covered by `.env.*`). I kept to the list given.
- **Unsure about / please check:**
  - The `.gitignore` does not ignore `.claude/` as a whole, only `settings.local.json`, as asked.
  - `CLAUDE.md` says to create `README.md` in the root, but the existing `README.md` is the fork/submit guide. This conflict is still unresolved.
- **Developer review:** Scaffolding look good. Verified that .claude/settings.local.json is properly ignored so local configurations don't leak into version control.
- **Tokens:** Input (uncached): 8 | Cache write: 3,380 | Cache read: 136,043 | Output: 1,465 | Model: Opus 5.5

### 2026-10-26 14:24 — Generate fake sample data
- **Asked:** Create fake statements for a Pakistani freelance developer: a card CSV, a bank CSV, a deliberately broken CSV, a ground-truth labels file and a README. No app code.
- **Generated/changed:** `sample_data/bank_a_card.csv` (31 rows), `sample_data/bank_b_checking.csv` (25 rows), `sample_data/messy_statement.csv` (15 lines), `sample_data/expected_labels.csv` (71 label rows), `sample_data/README.md`.
- **Assumptions I made:**
  - **Row counts:** wrote 31 card rows (asked ~25) and 25 bank rows, to fit all the required edge cases.
  - **Fictional names:** invented the account holder "Hamza Qureshi" and clients (Acme Digital GmbH, Brightpath Solutions Ltd, Kashif & Co, Ali Raza, Sara Khan). Account/card/reference numbers are made up. I did not check whether any of the names or merchants (e.g. Skyline Hosting, Blue Bird Cafe, Paperworld, Hafeez Centre) match real businesses.
  - **Labels, merchants and keywords:**
    - `UBER EATS` → Meals / expense (the "Eats" keyword wins over "Uber").
    - `SQ *JOES CAFE 9921` → Meals, by "CAFE" keyword. TASK.md's example sends this merchant to Needs Review, so this is a deliberate departure from it.
    - `KFC` → Needs Review (could be a client meal or personal). `NETFLIX` → Personal.
    - `AMAZON.COM`, `DARAZ.PK`, `XYZ TRADERS` → Needs Review. `AWS EMEA AWS.AMAZON.CO` → Hosting & Cloud even though it contains "AMAZON".
    - `PAYPAL *UPWORK` (a charge) → Professional Services.
    - `PAPERWORLD STATIONERS` → Office Supplies. `HAFEEZ CENTRE COMPUTERS` → Hardware & Equipment (keyword only).
    - `STORMFIBER INTERNET BILL` → Internet & Phone. `KASHIF & CO CHARTERED ACCOUNTANTS` → Professional Services.
  - **Kinds and money direction:**
    - ATM cash withdrawal: category Needs Review, kind `transfer`.
    - Incoming RAAST payment from a person: Needs Review, kind `income`.
    - Outgoing IBFT to a person, the cheque and the electricity bill: Needs Review, kind `expense`.
    - Withholding tax on cash: Needs Review, kind `fee`.
    - Needs Review rows keep a kind based on the money direction (my own convention).
  - **Transfers, fees and refunds:**
    - Card payment and savings transfers → Transfer. `PAYMENT THANK YOU` and the card bill debit are both Transfer.
    - FX fee, annual fee, late fee, remittance, SMS, FED, maintenance → Bank Fees / fee.
    - Bill reversal (`REVERSAL PTCL ...`) → Refund. Adobe refund and Airblue partial refund → Refund.
    - The refund rows carry no link to the original charge in the labels. Matching is only described in the README.
  - **Messy file conventions:**
    - Invented a `SKIPPED` label for the blank line (not in the spec).
    - `row_number` for the messy file counts physical lines, so the blank line is row 3.
    - The exact duplicate (row 11) keeps its category with `needs_review=true`.
    - The `Rs 500` row is a positive amount, so I labeled it Refund. A positive amount could also be seen as income.
    - Row 15 (DD/MM/YYYY in a YYYY-MM-DD file) is labeled `PARSE_ERROR`, though a lenient parser could accept it.
    - Row 14 (`PAYMENT THANK YOU`, +185,000) is labeled Transfer.
  - **Dates and balances:** September 2026 dates; the bank balance column reconciles from an opening balance of 412,350.00 (invented).
- **Unsure about / please check:**
  - Every `expected_category` is my opinion of the right tax answer, not an authority's. Examples to check: whether KFC should be Personal, whether Netflix could be a legitimate business expense, how Pakistani tax treatment handles the electricity bill and withholding tax.
  - Edge cases that I labeled Needs Review for lack of a fitting category (electricity, withholding tax) may justify new categories later.
  - FX fee amount (376 PKR) is not exactly consistent with the 38.42 USD charge it follows. It is an approximation.
  - I checked row counts and the bank B balances with a script. I did not check the content of the labels against the CSV rows line by line.
  - Possible mismatch in `bank_b_checking.csv` row 25: a second `FED ON CHARGES` is labeled "similar_not_duplicate", but its date and amount differ from row 8 only slightly.
- **Developer review:** Renamed the UBER EATS case tag to specific_beats_generic to accurately test exact-merchant priority over generic rules. Identified withholding tax rows and flagged them to be extracted into a dedicated tax category rather than general expenses.
- **Tokens:** Input (uncached): 8 | Cache write: 21,857 | Cache read: 166,435 | Output: 20,650 | Model: Opus 5.5

### 2026-10-26 14:35 — Add AI usage log rule and log file
- **Asked:** Append a mandatory "AI usage log" section to `CLAUDE.md`, create `docs/ai-usage/log.md`, and backfill entries for the earlier tasks this session.
- **Generated/changed:** `CLAUDE.md` (section appended), `docs/ai-usage/log.md` (created).
- **Assumptions I made:**
  - Used file modification times for the earlier entries' timestamps. The exploration entry has no file, so it says "before 14:21".
  - Added a fourth entry for this task itself, since the new rule says every task gets an entry.
  - Added a short header paragraph mentioning that the log feeds `AI_USAGE.md`. That link is my assumption about how you will use it.
  - Wrote the "Assumptions" for the earlier tasks from my own record of this session, so they are reconstructed, not contemporaneous.
- **Unsure about / please check:**
  - The earlier entries may omit assumptions I did not notice I was making.
  - I did not touch `AI_USAGE.md`, which TASK.md requires at the repo root. It does not exist yet.
- **Developer review:** Established logging format to track explicit assumptions and uncertainty across tasks for repo auditability.
- **Tokens:** Input (uncached): 6 | Cache write: 6,464 | Cache read: 179,918 | Output: 4,912 | Model: Sonnet 5.5

### 2026-10-26 14:41 — Two label fixes and Tax Withheld category
- **Asked:** Rename case_tag on bank_a row 15 to `specific_beats_generic`; relabel bank_b row 22 as `Tax Withheld,fee,false,withholding_tax` if adding that category, and add it to the CLAUDE.md categories.
- **Generated/changed:** `sample_data/expected_labels.csv` (rows bank_a 15, bank_b 22), `CLAUDE.md` (categories list), `sample_data/README.md` (withholding line and UBER EATS tag note), `docs/ai-usage/log.md`.
- **Assumptions I made:**
  - The request was conditional ("if you're adding"). I decided to add the category, since the earlier log flagged withholding tax as lacking a fitting category.
  - Placed "Tax Withheld" before "Needs Review" in the categories list, keeping Needs Review last.
  - Updated `sample_data/README.md` for consistency, which was not requested.
- **Unsure about / please check:**
  - `TASK.md` and `DESIGN.md` plans, and `expected_kind` of `fee` for Tax Withheld, are my choice. Withholding tax is arguably a tax credit, not a fee.
  - The kinds list in CLAUDE.md has no `tax` kind; I did not add one.
  - Earlier log entries still describe the old Needs Review label for this row (they are history, so I left them).
- **Developer review:** Adjusted tax classification rules. Moved withholding tax out of generic fees into a dedicated category to ensure it's treated as an advance tax credit rather than a business operating expense.
- **Tokens:** Input (uncached): 8 | Cache write: 2,379 | Cache read: 199,674 | Output: 1,897 | Model: Sonnet 5.5

### 2026-10-26 14:47 — Add `tax` kind
- **Asked:** Add a sixth kind `tax`; relabel bank_b row 22 as `Tax Withheld,tax,false,withholding_tax`; tax rows get their own "Tax already paid" total; add `tax` to the kinds in CLAUDE.md.
- **Generated/changed:** `sample_data/expected_labels.csv` (bank_b row 22), `CLAUDE.md` (kinds list plus a summary line), `sample_data/README.md` (withholding line), `docs/ai-usage/log.md`.
- **Assumptions I made:**
  - Put the "Tax already paid" requirement in CLAUDE.md as a one-line `Summary:` note under the kinds, since there is no other place for app rules yet.
  - Filled in the Developer review field of the previous entry (14:41) with the text you dictated, because you asked for it. That is the only exception to the rule that I never fill that field.
  - Left earlier entries' mentions of `fee` for this row as history.
- **Unsure about / please check:**
  - Whether tax rows should be excluded from the "total expenses" figure and from net income, or only shown separately. I wrote only what you said.
  - Whether a tax refund or reversal would be kind `refund` or `tax`. Not covered yet.
- **Developer review:** Explicitly separated tax entries from income and expense calculations so they only aggregate under a dedicated tax section. Validated net sum logic for tax adjustments.
- **Tokens:** Input (uncached): 6 | Cache write: 1,997 | Cache read: 138,360 | Output: 1,951 | Model: Sonnet 5.5

### 2026-10-26 14:52 — Add tax totals and tax-refund rules to DESIGN.md
- **Asked:** Add two bullets (tax rows excluded from expenses and income; refund of withheld tax stays kind `tax`) to DESIGN.md section 2.
- **Generated/changed:** `DESIGN.md` (two bullets in section 2), `docs/ai-usage/log.md`.
- **Assumptions I made:**
  - Used the existing DESIGN.md (it already existed, not created by me this session) and placed the bullets at the end of section 2, after "Totals only count kinds that matter for tax".
  - Kept your wording, with plain quotes instead of curly quotes, and wrapped lines to match the file.
- **Unsure about / please check:**
  - The bullets answer the two questions I raised earlier. `sample_data` has no tax-refund example row, and `CLAUDE.md` does not yet mention these two rules.
  - Rule 6 in section 4 ("positive amount from a merchant on a card → refund") will need a guard so a positive Tax Withheld row is not read as a refund. I did not change it.
- **Developer review:** Confirmed that DESIGN.md section 2 matches the underlying execution logic. Verified that positive tax adjustments are handled correctly without being mistaken for merchant refunds.
- **Tokens:** Input (uncached): 10 | Cache write: 2,769 | Cache read: 287,477 | Output: 1,327 | Model: Sonnet 5.5

### 2026-10-26 15:31 — Backend skeleton and ingest/parse layer
- **Asked:** Set up the uv backend with a `/health` endpoint and build the CSV ingest layer (format profiles, parser, `parse_amount`) with tests. No normalizer, brain, database or frontend.
- **Generated/changed:** `backend/pyproject.toml`, `backend/uv.lock`, `backend/.python-version`, `backend/app/main.py`, `backend/app/ingest/{formats,parser,amounts,models}.py`, empty `__init__.py` files, `backend/tests/{test_amounts,test_parser,test_health}.py`, `docs/ai-usage/log.md`.
- **Assumptions I made:**
  - **Extra dev dependency:** added `httpx` (the `/health` test needs it). It prints a deprecation warning from starlette's test client.
  - **Where things live:** put `parse_amount` in `ingest/amounts.py` and the result types in `ingest/models.py`, as Pydantic models (the spec didn't say where).
  - **Header detection:** it matches the header set by name and ignores order, so reordered columns still work. Names are stripped of whitespace.
  - **Lines:** split on `\r\n`, `\n` or `\r`, and parse each physical line by itself. A quoted field can therefore not span two lines (it becomes an error). A malformed header raises `IngestError`.
  - **Extra rules beyond the spec:**
    - An empty description is a ParseError.
    - An empty currency is a ParseError.
    - A whitespace-only line counts as blank (skipped).
    - Dates must round-trip exactly, so `2026-9-1` is rejected.
    - A negative or parenthesised value in a Debit or Credit column is an error.
    - `Balance` is never read or checked.
  - **`parse_amount` choices:**
    - One currency marker is allowed, at the start or end: `Rs`, `Rs.`, `PKR`, `USD`, `$` (case-insensitive).
    - Commas must group digits in threes, so `1,23.00` and `1.234,56` are rejected. Spaces inside a number are rejected.
    - `NaN`, exponents and more than one sign marker (`(-5)`, `-(5)`, `--5`) are rejected.
    - It raises `AmountError`, a `ValueError` subclass.
  - **Scope:** other currencies in the amount text (`EUR`, `£`) are not supported and will be errors.
- **Unsure about / please check:**
  - **Bug found and fixed in this task:** my first `parse_amount` stripped currency words and spaces anywhere, so `"1rs2"` parsed as 12 and `"5 USD 5"` as 55. I only found it by running the input after I had written the log. It now only strips a marker at one end, and those inputs are errors with tests.
  - **Tests:** 166 pass and `ruff check` is clean. They passed on the first run before the fix above, which shows they were too lenient for odd input. The sign check is the only link to `expected_labels.csv`, so it doesn't prove categories.
  - **Unusual input:** zero amounts parse as valid. I did not test other odd inputs, such as full-width digits or a Unicode minus sign.
  - **Packaging:** the Python 3.12 pin comes from `.python-version` plus `requires-python`; I didn't check the CI plan yet.
- **Developer review:** Fixed a regex bug in parse_amount where currency tokens ("1rs2", "5 USD 5") were stripped internally, violating strict parsing rules. Restricted currency stripping to strict leading/trailing edges and added negative test cases. Verified all 166 tests pass and ruff is clean.
- **Tokens:** Input (uncached): 22 | Cache write: 22,766 | Cache read: 1,080,489 | Output: 20,918 | Model: Sonnet 5.5



### 2026-10-26 15:57 — Normalizer, classification engine, duplicate post-check
- **Asked:** Add `account_type` to the ingest layer; build the normalizer, the YAML rules schema (2 example rules per section only), the stage-ordered classifier and the duplicate post-check, with tests. No database, API or frontend.
- **Generated/changed:** `backend/app/core/{domain,config}.py`, `backend/app/brain/{normalizer,rules,models,classifier,postcheck}.py`, `backend/app/brain/rules.yaml`, `backend/app/ingest/{formats,models,parser}.py` (account_type), `backend/app/main.py` (loads rules at startup), `backend/pyproject.toml` and `uv.lock` (pyyaml), `backend/tests/{test_normalizer,test_rules,test_classifier,test_postcheck,test_labels}.py`, `test_parser.py` and `test_health.py` (small additions), `docs/ai-usage/log.md`.
- **Assumptions I made:**
  - **Normalizer:** `text` has the processor prefix removed (the spec only said it is uppercased and collapsed). Rules and duplicates match on it, so `starts_with: JOES` works for `SQ *JOES CAFE`. Only one prefix is removed. `SQ*`, `SQ *` and `TST* ` all count.
  - **Matching:** `contains` treats letters and digits as word characters, so `CAFE` does not match `CAFETERIA` but does match `JOES-CAFE`. `starts_with` is a plain prefix check with no word boundary, so `AWS` also matches `AWSOME`. Non-ASCII letters are not treated as word characters.
  - **Rules file:** unknown keys and section names are errors (so typos fail loudly). Missing sections are allowed (empty). Rule ids must be unique across all sections. Patterns are uppercased and space-collapsed when matched.
  - **Review section:** the rule's `category` is treated as a suggestion; the decision is always `Needs Review`. `category: Needs Review` means no suggestion.
  - **Threshold:** a confidence of exactly 0.8 is trusted (only values below it are not). A low-confidence reason gets "(low confidence 0.75)" appended.
  - **Keywords:** if several keyword rules agree on the category, the most confident one is used. Conflicting categories give `Needs Review`, confidence 0, rule_id = the matched ids joined with "+", and no suggestion.
  - **Direction fallback:** rule_id `card_money_in`. It only runs if no rule of any stage matched.
  - **Zero amount:** goes to `Needs Review` with kind `expense` (the spec did not cover it).
  - **User rules:** key must match exactly, an empty key never matches. If the user's category is `Needs Review` the row is flagged.
  - **Duplicates:** the reason is exactly "possible duplicate of row N", unless the row was already in review, in which case the original reason is added after a semicolon. The comparison uses the normalized text and the Decimal amount.
  - **Plumbing:** `classify(row, user_rules=(), rules=None)` loads and caches the shipped rules when `rules` is omitted. The app loads `rules.yaml` at startup. Confidence values are floats (they are scores, not money). Constants live in `core/config.py` (not environment variables).
- **Unsure about / please check:**
  - **Keyword confidence vs labels:** keywords default to 0.75, below the 0.8 threshold, so every keyword match goes to review by default. `expected_labels.csv` expects several keyword rows (SKYLINE HOSTING, BLUE BIRD CAFE, STORMFIBER, ACCOUNTANTS) to be trusted. Those rules will need an explicit confidence of at least 0.8, or one of the two documents has to change. `DESIGN.md` says keywords land below the threshold on purpose.
  - **Refunds need `direction: out`:** a merchant rule with no direction filter also matches a refund and classifies it as income (there is a test showing this). The Adobe refund only becomes a Refund because the example Adobe rule has `direction: out`. Every merchant and keyword rule probably needs it.
  - **Label test status:** `test_labels` currently shows 44 mismatches and is marked xfail. 27 of the 71 label rows already pass. I did not check the 44 one by one beyond reading the table; they all say "no rule matched" or "low confidence".
  - **Other limits:** the `regex` rule type is not guarded against slow patterns. Nothing tests the classifier with a user rule whose `kind` conflicts with the amount's sign.
  - **Tests:** 283 pass, 1 xfail, ruff clean. The rules and classifier tests were written by me, so they check my reading of the spec.
- **Developer review:** _(to be filled by Dawood: what was wrong, what he changed)_
- **Tokens:** _(to be filled by Dawood from usage screenshot)_
