# AI usage log

A running log of AI-assisted work on this project (Claude Code). Each entry records what
was asked, what was changed, the assumptions the AI made without being told, and what the
developer should double-check. The **Developer review** and **Tokens** fields are filled in
by the developer, never by the AI. This file feeds `AI_USAGE.md` in the repo root.

Entry times for the first three entries are taken from file modification times (the
exploration entry has no file, so its time is only bounded).

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
- **Tokens:** Input: 2,410 | Output: 850

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
- **Tokens:** Input: 1,850 | Output: 420

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
- **Tokens:** Input: 4,120 | Output: 1,890

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
- **Tokens:** Input: 1,520 | Output: 380

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
- **Tokens:** Input: 1,980 | Output: 540

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
- **Tokens:** Input: 2,150 | Output: 610

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
- **Tokens:** Input: 1,450 | Output: 310
