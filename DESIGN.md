# Design

## 1. Use case
- Freelance software developer in Pakistan, business card + business bank account
- At tax time they need spending sorted into deductible categories, income totalled,
  and non-spending (transfers, card payments, refunds) excluded

## 2. Categories and kinds
- Category = what it is for tax; kind = what kind of money movement it is
- Why separate: a refund is money back, not income; a card bill payment is not spending
- Totals only count kinds that matter for tax
- Totals: tax rows count in neither total expenses nor income. They only appear in
  "Tax already paid". Mixing them in would overstate business expenses.
- Refund of withheld tax: keep it as category Tax Withheld, kind tax, with a positive
  amount. Then "Tax already paid" is just the net sum of tax rows, and the sign handles
  it. Don't call it a refund. The refund kind means a merchant gave money back on a purchase.

## 3. Pipeline
- Ingest → Parse → Normalize → Classify → Post-check → Review
- Why separate stages: each one is testable on its own; a wrong category can be
  traced to one stage

## 4. The brain (rule order and why)
1. User rules (what the user already corrected wins)
2. Structural: fees, card payments, savings transfers
   - "FOREIGN TXN FEE AWS" contains AWS → fee must win
   - "PAYMENT THANK YOU" is positive → must not be read as a refund
3. Exact merchants (AWS beats the AMAZON guard; UBER EATS beats UBER)
4. Ambiguous guard (Amazon, Daraz → always review)
5. Keywords ("ACCOUNTANTS" beats generic "IBFT TO <person>")
6. Direction: positive amount from a merchant on a card → refund
7. Nothing confident → Needs Review
- Rules live in YAML, not code

## 5. Confidence and Needs Review
- Threshold: 0.8
- Why: a wrong guess is worse than asking; keyword matches land below it on purpose
- Every decision stores rule_id + reason so the UI can show why

## 6. Messy data handled
- (table: case → how handled → test name), fill in when tests exist

## 7. Learning from corrections
- "Remember for this merchant" → saves a user rule → re-runs the statement

## 8. Trade-offs and limits
- CSV only (no PDF): reliability over coverage in the time available
- Rules only, no ML: explainable, and the brief requires the brain to be my code
- Money as Decimal, raw description never changed

## 9. What I'd build next
- PDF/OFX import, more bank profiles, a rule management screen