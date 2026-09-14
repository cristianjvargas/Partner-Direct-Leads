---
name: merchant-qualify
description: "Qualify a merchant-services prospect on the dimensions that actually predict a boarded account - estimated card volume, average ticket, card-present vs CNP mix, MCC and underwriting risk, switching cost, and decision authority. Use for 'is this merchant worth working', 'qualify this lead', or triaging a merchant list. Produces MERCHANT-QUALIFICATION.md."
---

# Merchant Qualification

Generic BANT does not fit merchant services. "Budget" is meaningless when every merchant already
pays for processing — the question is not whether they will spend, it is how much volume flows
through them and whether your underwriting will approve them.

Use this instead of `sales-qualify` for card-processing prospects. Output:
`MERCHANT-QUALIFICATION.md`.

---

## The five real qualifiers

### 1. Volume (40%) — the only thing residuals scale with

Estimate monthly card volume, average ticket and transaction count. Method and honesty rules are in
`merchant-source` Phase 4. Band it:

| Band | Monthly volume | Meaning |
|---|---|---|
| A | $100k+ | Full workup, in-person, senior rep |
| B | $30k-100k | Core target for most agents |
| C | $10k-30k | Inside sales / volume motion |
| D | < $10k | Rarely worth individual rep time |

Average ticket matters independently: a merchant doing $50k on 10,000 transactions (avg $5) has a
completely different cost structure than $50k on 400 transactions (avg $125), because per-item fees
dominate the former and percentage rate dominates the latter. Low-ticket merchants are extremely
sensitive to per-transaction pricing and are often badly served by flat-rate providers — a real
opening.

### 2. Channel mix (15%)

Card-present, keyed, or e-commerce. This drives interchange, hardware needs, fraud exposure and
which competitor you are displacing. Card-present retail on flat-rate is typically the most winnable
profile in the industry. Pure e-commerce on Stripe is typically the least, because the integration
is the product.

### 3. Underwriting fit (20%) — the qualifier most reps skip

A merchant you cannot board is not a lead, no matter how good the volume. Check before investing:

- **MCC / vertical** — is it on your sponsor bank's approved list?
- **Restricted and high-risk categories** — CBD, firearms, nutraceuticals, adult, travel,
  subscription/continuity, debt relief, crypto, gambling, MLM, ticket brokers, tech support. These
  are not automatically disqualifying, but they need a high-risk sponsor and different pricing.
  Routing a high-risk merchant to a low-risk sponsor wastes weeks and burns the relationship.
- **Chargeback exposure** — future delivery, subscriptions, high refund verticals. Ask for chargeback
  ratio; over ~0.9% is a monitoring-program problem.
- **Business age and stability** — under a year trades higher scrutiny and often a reserve.
- **MATCH / TMF list** — a previously terminated merchant is effectively unboardable through normal
  channels. Find out before proposing, not during underwriting.
- **Credit and financials** — personal guarantee, prior bankruptcies, existing reserve requirements.

Mark this **Approved / Conditional / Declined** and say which sponsor assumption you used.

### 4. Switching cost (15%)

From `merchant-payment-stack`. The three things that actually block deals:

- **Equipment lease** — non-cancellable, survives the switch, frequently 48 months. The most common
  deal-killer and the most commonly discovered too late. **Ask on the first call.**
- **Contract term and ETF** — how long left, how much to exit.
- **Integration depth** — POS, online ordering, inventory, payroll, loyalty. A merchant whose
  reservation system, kitchen display and payments are one product is not switching over 30bps.

### 5. Decision authority (10%)

In SMB merchant services the decision maker is usually the owner, and reaching them is most of the
battle. Establish:

- Is this owner-operated, or is there a corporate/franchise structure?
- Does a franchise agreement mandate the processor? (If yes — disqualify, immediately.)
- Is there a bookkeeper, CFO or spouse who actually reviews the statements?
- Who physically has the statement you need?

A gatekeeper who will not pass you to the owner is the single most common point of failure. Plan
for it.

---

## Scoring

Weight and total to 100. Then apply hard gates — these override the score entirely:

**Automatic disqualifiers:**
- Franchisor-mandated processor
- Vertical your sponsor will not board
- Confirmed MATCH listing
- Permanently closed
- Existing customer, or another rep's account in CRM

**Automatic downgrades:**
- Mid-contract with a meaningful ETF
- Equipment lease with 12+ months remaining
- Deeply integrated POS where payments cannot be separated
- Volume band D with no growth trajectory

| Score | Grade | Action |
|---|---|---|
| 80-100 | A | Work now. In person if local. Ask for the statement on the first call |
| 60-79 | B | Work this week. Phone-first |
| 40-59 | C | Nurture. Revisit on a trigger event |
| < 40 | D | Do not work individually |

---

## The discovery questions that matter

Most merchant discovery is wasted on questions the rep could have answered from research. Spend the
call on what only the merchant knows:

1. "Roughly what do you run through cards in a month?" — the whole deal hinges on it
2. "Do you have a copy of last month's statement handy?" — the actual objective of the call
3. "Are you leasing your terminal or do you own it?" — finds the biggest blocker early
4. "How long have you been with them, and do you remember signing a term?" — ETF exposure
5. "What's your average sale?" — drives per-item vs rate strategy
6. "Anything about the current setup that annoys you?" — often more actionable than price
7. "Who else weighs in on something like this?" — surfaces the bookkeeper or partner

Question 3 saves more wasted pipeline than any other question in this industry.

---

## Output

`MERCHANT-QUALIFICATION.md`:

```markdown
# Merchant Qualification — {Name}
{address} · {vertical} · MCC {code, if known} · Analyzed {date}

## Score: {n}/100 — Grade {A-D}
| Dimension | Weight | Score | Basis |
(one row per dimension, and "basis" must cite evidence, not vibes)

## Volume Estimate
{est} /mo · avg ticket {est} · {n} txns
**Basis:** (state the inputs and that it is an estimate)
**Confidence:** high / medium / low

## Underwriting: Approved | Conditional | Declined
Sponsor assumption, MCC, risk notes, reserve likelihood

## Switching Cost: {score}/100
Lease / contract / integration — confirmed vs suspected

## Decision Path
Who decides, who gatekeeps, who holds the statement

## Verdict
Work now / this week / nurture / drop — and the single next action

## Open Questions
The facts that would most change this assessment
```

---

## Rules

1. **Never present an estimated volume as a known figure.** Estimates prioritize your day; they are
   not claims to make to the merchant.
2. **Check underwriting before investing rep hours.** A beautifully qualified merchant your sponsor
   declines is a wasted week and an embarrassed rep.
3. **Ask about the lease on the first call**, every time.
4. **Disqualify decisively.** In a business with this many prospects, a fast no is worth more than a
   slow maybe. Write the disqualification reason down so nobody re-works it in six months.

## Related
- `merchant-payment-stack` · `merchant-statement-analysis` · `merchant-source` · `merchant-compliance`
