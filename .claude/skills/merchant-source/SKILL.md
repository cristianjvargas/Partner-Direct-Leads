---
name: merchant-source
description: "Build a targeted list of merchant-services prospects from public sources - local business data, new-business filings, licence registries, review signals and trigger events - filtered for card-processing fit and scored for quality. Use for 'find me leads', 'build a prospect list', 'who should we call this week', or sourcing merchants in a vertical or territory. Produces MERCHANT-LEADS.csv and LEAD-SOURCING.md."
---

# Merchant Lead Sourcing

You build **lists of merchants worth calling** for a card-processing / merchant-services company.
The goal is not volume. A list of 40 merchants with a confirmed trigger event beats 4,000 scraped
names, because a rep's day is finite and their connect rate is what actually constrains revenue.

Outputs: `MERCHANT-LEADS.csv` (the working list) and `LEAD-SOURCING.md` (method, sources, caveats).

---

## Before you start: read `merchant-compliance`

Sourcing decisions determine whether the resulting calls are legal. Cold-calling merchant phone
numbers pulled from a directory is regulated territory (TCPA, state telemarketing law, DNC). Check
`merchant-compliance` *before* building the list, not after — because the list is where the
scrubbing has to happen.

Also: honour `robots.txt` and site terms on every source. Prefer official APIs and official bulk
data over scraping a rendered page. Where a source publishes an API, use it. Where a source forbids
automated collection, use it manually or drop it — an ISO with a scraping lawsuit has bigger
problems than pipeline.

---

## Phase 1: Define the target before collecting anything

Do not collect first and filter later. Establish, from the user:

1. **Territory** — metro, radius, state, or national
2. **Vertical(s)** — restaurant, retail, auto, medical, professional services, e-commerce, high-risk
3. **Size band** — the estimated monthly card volume you actually want (see Phase 4)
4. **Channel** — card-present, card-not-present, or both
5. **Exclusions** — verticals the sponsor bank or underwriting will not approve

If the user has not defined an ICP, run `merchant-icp` first. Sourcing without an ICP produces a
list nobody works.

---

## Phase 2: Sources, ranked by lead quality

### Tier 1 — Trigger-event sources (highest quality)

A trigger event means the merchant is *already* in a decision window. These convert several times
better than cold directory pulls.

| Source | Trigger it reveals | How to access |
|---|---|---|
| Secretary of State new-business filings | Brand-new entity — no processor yet | Most states publish searchable/bulk registries, many free |
| State ABC / liquor licence registries | New bar or restaurant opening | Usually public, often downloadable |
| County/city health-dept restaurant permits | New food service opening | Public inspection and permit lists |
| City business licence issuance | Any new local business | Open-data portals in most mid/large cities |
| BizBuySell, business-for-sale listings | Ownership change — new owner re-decides everything | Public listings |
| Commercial lease / new-location news | Expansion | Local business journals, LoopNet |
| Franchise disclosure + franchisor "now open" pages | New franchisee, needs a stack | Public |
| Job postings for cashiers/servers at a new address | Pre-opening staffing | Indeed, company sites |

**Ownership changes are the single best trigger in this industry.** A new owner inherits a processor
they did not choose, has no loyalty to the incumbent agent, and is actively re-examining every
vendor line on the P&L in their first 90 days.

### Tier 2 — Signal-rich directory sources

| Source | What to extract | Notes |
|---|---|---|
| Google Places / Maps | Name, address, phone, category, rating, review count, hours, photos | Use the official Places API. Photos reveal the POS — see `merchant-payment-stack` |
| Yelp | Category, price tier, review text, "accepts credit cards" attribute | Official Fusion API |
| Apple Maps / Bing Places | Cross-verification | |
| Industry associations | Vetted member lists by vertical | Often the cleanest data available |
| Chamber of commerce directories | Local, engaged businesses | Frequently permits access; check terms |
| Better Business Bureau | Accreditation, complaint history | Complaint history is an underwriting signal |

### Tier 3 — Enrichment layers (not sources on their own)

Apollo, ZoomInfo, Clay, Lusha and similar fill in owner name, email, LinkedIn and firmographics once
you already have the business. They are weak at *finding* small local merchants — a two-location
taqueria is invisible in a B2B SaaS database — but strong at putting a name to one you found.

---

## Phase 3: The review-mining signal (do not skip this)

Customer reviews are the most underused source of merchant-services intent, and they are public
text. Search review corpora for these phrases and flag every hit:

| Phrase pattern | What it means | Opener it earns |
|---|---|---|
| "cash only", "they don't take cards" | No card acceptance at all | Largest possible deal — full acceptance |
| "$10 card minimum", "minimum for cards" | Fee-sensitive, flat-rate, low ticket | Interchange-plus saves them the minimum |
| "card machine was down", "system was down" | Reliability pain with the incumbent | Uptime + backup terminal |
| "they charge 3% for cards", "card fee" | Surcharge program in place | Compliance exposure + customer friction |
| "only takes Visa/MC, no Amex" | No Amex acceptance | Amex OptBlue |
| "no Apple Pay", "chip reader broken" | Aging hardware | Hardware refresh |
| "took forever to run my card" | Slow terminal or connection | Speed → table turns → revenue |
| "they don't do online ordering" | No CNP channel | Gateway / e-comm attach |

A merchant with three reviews complaining about a card minimum is a warm lead who has never been
called about the actual thing bothering their customers.

---

## Phase 4: Volume estimation (the quality filter)

Lead quality in this business is **estimated monthly card volume**, because residual income scales
with it. Estimate before you call; refine on the call.

Reasonable public-signal estimation:

```
est_monthly_volume ≈ avg_ticket × est_daily_transactions × operating_days × card_share
```

Ground each input:

- **avg_ticket** — Yelp/Google price tier ($ ≈ $12-20, $$ ≈ $25-45, $$$ ≈ $60-100+), vertical norms,
  posted menu or price list. A published menu is the best source available without a statement.
- **est_daily_transactions** — review count is a usable proxy for foot traffic within a vertical and
  metro (roughly, reviews accrue at a stable fraction of transactions). Seat count, drive-thru
  presence, hours, and staff count all refine it.
- **operating_days** — from posted hours; watch for seasonal closures.
- **card_share** — 80-95% for most US retail/restaurant today; lower for cash-heavy verticals
  (barbers, some bodegas, food trucks), higher for e-commerce (100%).

**State every estimate as an estimate, with its basis.** An estimate presented as a fact gets a rep
laughed off a call when the merchant knows the real number. The correct use of the estimate is
internal prioritization and the decision of who to call first — not a claim to make out loud.

Band the results:

| Band | Est. monthly card volume | Treatment |
|---|---|---|
| A | $100k+ | Direct rep, in-person, full workup |
| B | $30k-100k | Direct rep, phone-first, worth a statement analysis |
| C | $10k-30k | Volume/inside sales motion |
| D | < $10k | Usually not worth agent time unless it is a portfolio or referral play |

---

## Phase 5: Quality scoring

Score each lead 0-100. Weights reflect what actually predicts a closed merchant account:

| Factor | Weight | Notes |
|---|---|---|
| Estimated volume band | 30% | The residual driver |
| Trigger event present | 25% | New owner / new opening / documented payment pain |
| Switching cost (from `merchant-payment-stack`) | 20% | Inverted: easy to switch scores high |
| Contactability | 15% | Owner name known, direct line, not a chain HQ |
| Underwriting fit | 10% | Vertical approvable, no obvious MATCH/chargeback red flags |

**Hard disqualifiers** — drop, do not score:
- Franchise where the franchisor mandates the processor
- Vertical the sponsor bank will not board
- Chain with centralized national procurement (unless you sell enterprise)
- Business permanently closed (check "permanently closed" flags — stale directory data is rampant)
- On the internal DNC or already in CRM under another rep

---

## Phase 6: Output

`MERCHANT-LEADS.csv` with these columns:

```
business_name,dba,address,city,state,zip,phone,website,vertical,mcc_guess,
est_monthly_volume,volume_band,avg_ticket_est,current_processor,processor_confidence,
switching_cost,trigger_event,trigger_date,signal_notes,owner_name,owner_source,
quality_score,disqualifier,source,collected_date,dnc_checked
```

Two columns carry more weight than the rest and must never be blank:
- `signal_notes` — the specific, quotable reason to call **this** merchant. "Yelp review 3 weeks ago:
  'annoying $15 card minimum'" is a lead. "Restaurant in Dallas" is a row.
- `processor_confidence` — `confirmed` / `likely` / `unknown`. Reps must know what they can say.

Then write `LEAD-SOURCING.md` documenting: sources used and their terms, filters applied, counts at
each funnel stage, volume-estimation assumptions, disqualified counts by reason, and known data
quality gaps.

---

## Quality bar

Before handing a list over, check it yourself:

1. **Spot-check 10 records against reality.** Directory data is stale — businesses close, move and
   change numbers constantly. If more than two of ten are wrong, the list is not ready.
2. **Every row has a reason to be called.** If you cannot state it in one sentence, delete the row.
3. **No fabricated contacts.** Never generate a plausible-looking owner name, email or phone. An
   unverified `firstname@domain` guess must be labelled as a pattern guess, not a verified address.
4. **Deduplicate on phone and address**, not name — DBA spellings vary wildly across sources.
5. **Prefer 50 excellent rows to 5,000 mediocre ones.** The constraint is rep hours, not list size.

## Related

- `merchant-icp` — define the target first
- `merchant-payment-stack` — enrich each lead with its current processor
- `merchant-qualify` — work the list top-down
- `merchant-compliance` — scrub before anyone dials
