---
name: merchant-statement-analysis
description: "Analyze a merchant processing statement to compute the true effective rate, separate pass-through interchange from processor markup, identify junk fees and downgrades, and quantify defensible monthly savings. Use whenever a merchant shares a statement, or for 'what are they really paying', 'build a savings proposal', 'effective rate', or 'cost comparison'. Produces SAVINGS-ANALYSIS.md."
---

# Merchant Statement Analysis

You turn a merchant's processing statement into the one number that closes deals: **what they are
actually paying, and what of that is genuinely winnable.**

Output: `SAVINGS-ANALYSIS.md`.

This is the core deliverable of merchant services. Everything upstream — sourcing, stack detection,
qualification — exists to get a statement in hand. Do this well and the proposal writes itself.

---

## The one equation

```
Effective rate = (total fees for the month) ÷ (total card volume for the month)
```

Total fees means **everything**: discount rate, per-item fees, monthly service fees, PCI fees, batch
fees, gateway fees, statement fees, minimum charges, annual fees amortized, equipment lease. If it
left the merchant's bank account because they accept cards, it counts.

Most merchants quote you their "rate" (say 2.6%) and have no idea their effective rate is 3.4%. The
gap is the conversation.

---

## Phase 1: Read the statement correctly

Statements are deliberately hard to read. Work through them in this order:

### 1.1 Establish the denominators
- **Total sales volume** (gross card volume processed)
- **Total transaction count**
- **Average ticket** = volume ÷ count
- **Volume split by card type** — Visa / MC / Discover / Amex, and debit vs credit
- **Card-present vs keyed vs e-commerce** split

Watch for: statements that report volume net of refunds in one place and gross in another. Use gross
consistently and say which you used.

### 1.2 Identify the pricing model

| Model | How it looks on the statement | Merchant's real exposure |
|---|---|---|
| **Tiered** | "Qualified / Mid-Qualified / Non-Qualified" buckets | The worst. The processor decides what "qualifies". Downgrade abuse lives here |
| **Flat / blended** | One rate for everything (2.6% + 10¢) | Simple, predictable, expensive above ~$25k/mo |
| **Interchange-plus (IC+)** | Interchange listed separately + a stated markup (e.g. IC + 25bps + $0.10) | Transparent. Compare markup only |
| **Subscription / membership** | Monthly fee + interchange + small per-item | Cheapest at high volume, worst at low volume |
| **Surcharge / cash discount** | Fees pushed to cardholder | Merchant cost near zero; compliance and customer-friction risk instead |

Identifying the model correctly is the whole job. A tiered statement and an IC+ statement at the same
headline rate are wildly different deals.

### 1.3 Separate the three cost layers

```
Total cost  =  Interchange  +  Assessments  +  Processor markup
               (not winnable)  (not winnable)   (100% winnable)
```

- **Interchange** — set by Visa/Mastercard/Discover, paid to the card-issuing bank. Identical for
  every processor. **Nobody can beat it.** Any competitor claiming to "beat interchange" is lying or
  quoting a teaser.
- **Assessments / network fees** — the card brands' own cut (Visa APF/acquirer fees, Mastercard NABU,
  etc.). Also fixed.
- **Processor markup** — the ISO/processor's margin. **This is the only thing you are competing on.**

Interchange and assessment schedules are published by the card networks and **change twice a year
(typically April and October)**. Look up the current published tables rather than relying on
remembered figures, and state the effective date of the schedule you used. Quoting a stale
interchange table into a proposal is how a savings number becomes a lie.

---

## Phase 2: Hunt the junk fees

These are pure markup wearing an official-sounding name. Enumerate every one found, with its monthly
cost:

| Fee | Typical reality |
|---|---|
| PCI non-compliance fee | Charged when the merchant never completed an SAQ. Often $20-50/mo, entirely avoidable — helping them complete compliance is free goodwill and kills the fee |
| PCI / regulatory "program" fee | Frequently just margin |
| Statement fee | Paper statement in 2026 |
| Batch / settlement fee | Per-batch charge, daily |
| Monthly minimum | Charged when discount fees fall below a floor — punishes low months |
| Annual fee | Amortize it into the monthly comparison |
| "IRS reporting" / "1099-K" fee | Compliance obligation the processor already has |
| Gateway / virtual terminal fee | Sometimes legitimate, often duplicated with a fee they already pay |
| Wireless / data fee | Per-terminal |
| Non-EMV / non-compliance surcharge | |
| Early termination fee (ETF) | Not a monthly cost, but it sets the switching cost — **find this before proposing** |
| Equipment lease | The killer. Often a 48-month non-cancellable lease at several times hardware value, from a separate leasing entity. **The merchant keeps paying it even after they leave.** Never include lease relief in a savings number unless you have confirmed it can actually be terminated |

---

## Phase 3: Find the downgrades

Downgrades are transactions that failed to qualify for the best interchange category. They are often
the largest recoverable cost, and unlike rate, fixing them is real operational value:

| Cause | Fix |
|---|---|
| Keyed-in (card-not-present) transactions on a card-present account | Card reader usage, or correct account setup |
| Missing AVS / CVV on keyed transactions | Data capture at entry |
| Late batching (settling > 24h) | Auto-batch configuration |
| Corporate / purchasing / business cards without Level 2 data | Enable L2: tax amount, customer code |
| B2B invoicing without Level 3 data | Enable L3: line-item detail. **Can be worth 50-100bps on B2B volume** |
| International cards | Not fixable, but must be excluded from savings claims |

A B2B merchant processing corporate cards without Level 2/3 data is leaving very large money on the
table, and almost nobody pitches them on it. That is a differentiated opener.

---

## Phase 4: Compute

Use the bundled calculator:

```bash
python3 scripts/effective_rate.py --volume 84500 --transactions 2640 --fees 2871 \
    --proposed-markup-bps 30 --proposed-per-item 0.08 --interchange-est 41000
```

Produce:

| Metric | Current | Proposed | Delta |
|---|---|---|---|
| Total volume | | (same) | |
| Total fees | | | |
| Effective rate | | | |
| Cost per transaction | | | |
| Markup over interchange | | | |

Then annualize, and state the payback period against any switching cost (ETF, remaining lease).

---

## Phase 5: Write it honestly

`SAVINGS-ANALYSIS.md` structure:

```markdown
# Processing Cost Analysis — {Merchant}
Statement period: {month} · Analyzed: {date}

## Current State
Volume / transactions / average ticket / pricing model
**Effective rate: {x.xx}%**

## Where the money goes
| Layer | Monthly | % of volume | Winnable? |
| Interchange | | | No — fixed by card networks |
| Assessments | | | No |
| Processor markup | | | Yes |
| Fixed & junk fees | | | Mostly |

## Junk fees identified
(table with monthly cost each, and which are avoidable)

## Downgrades
(what is downgrading, why, estimated cost, whether it is fixable)

## Proposed
Pricing model, markup, per-item, fees eliminated, fees retained

## Savings
- Monthly: $X (range $X-$Y)
- Annual: $X
- **Basis:** exactly which assumptions produce this number
- **Switching cost:** ETF $X + remaining lease $X/mo for N months
- **Payback:** N months

## What could change this
The assumptions that, if wrong, would move the number — and how to verify each.
```

---

## Integrity rules

A savings number is a promise. The merchant will check it against their next statement, and a rep
who over-promised loses the account and the referral network around it. So:

1. **Never present a savings figure without its basis.** Every number traces to a statement line.
2. **Never claim to beat interchange.** Compete on markup and fees only.
3. **One month of statement is a sample, not a trend.** Seasonal businesses vary enormously. Ask for
   three months; if you only have one, say the estimate is based on one month and may not represent
   an annual average.
4. **Never bury the switching cost.** ETF and remaining equipment lease go in the same table as the
   savings, not a footnote. A "saves $400/mo" that omits a $5,800 lease is a misrepresentation.
5. **Give a range, not a false-precision point estimate.** "$380-520/mo" is honest. "$447.83/mo" from
   estimated inputs is not.
6. **If the merchant already has a good deal, say so.** Telling a merchant on a fair IC+30bps deal
   that they are already priced well is the single most credible thing a rep can do. It costs one
   deal and earns a referral source. Manufacturing savings that do not exist costs the relationship.
7. **Redact before sharing.** Statements carry MIDs, bank account and routing numbers. Never write
   full account numbers into output files. Mask to last four.

## Related
- `merchant-payment-stack` — what they run, before the statement arrives
- `merchant-qualify` — whether this merchant is worth the workup
- `merchant-compliance` — how the savings claim may be presented
