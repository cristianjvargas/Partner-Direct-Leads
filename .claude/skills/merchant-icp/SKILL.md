---
name: merchant-icp
description: "Build an Ideal Merchant Profile for a card-processing / merchant-services business - target verticals, volume bands, MCC and underwriting fit, trigger events, disqualifiers and vertical-specific angles. Use before building any merchant lead list, entering a new vertical or territory, or when asked 'who should we target'. Produces IDEAL-MERCHANT-PROFILE.md."
---

# Ideal Merchant Profile

Use this instead of `sales-icp` for a card-processing business. Generic B2B ICP frameworks optimize
for firmographics like headcount and funding, which barely predict anything in merchant services.
What predicts a good merchant account is **volume, ticket size, channel mix, underwriting fit, and
how easily they can leave their current provider**.

Output: `IDEAL-MERCHANT-PROFILE.md`.

---

## Phase 1: Start from the book you already have

If the user has existing merchants, that data beats any market theory. Ask for, and analyze:

- Volume distribution across the portfolio — where does residual income actually concentrate?
- **Attrition by vertical** — which merchants leave, and how fast? A vertical that closes easily and
  churns in nine months is a bad vertical, not a good one.
- Approval rate by vertical — where does underwriting decline you?
- Sales cycle length and close rate by vertical and by lead source
- Which lead sources produced the merchants still processing after 24 months

The last one is the real ICP question. Most merchant-services teams optimize for close rate and
discover two years later that half the book is gone. **Residual longevity is the metric.**

If there is no existing book, build from market structure and say clearly that the profile is
hypothesis-driven and needs validation after the first 50 merchants.

---

## Phase 2: Define the profile dimensions

### Volume and ticket

Set a target band and state why it is yours. The economics:

- Below ~$10k/mo, individual rep acquisition cost rarely justifies the residual
- $30k-100k/mo is the sweet spot for most independent agents and ISOs — enough volume to matter,
  small enough that the owner decides alone and quickly
- Above ~$250k/mo the merchant likely has an existing agent relationship, may already be on
  competitive interchange-plus, and expects a different level of service

**Average ticket** is a separate axis and drives the pitch entirely:
- **Low ticket** (< $15): per-item fees dominate. Flat-rate providers overcharge them badly. Strong
  target, strong story.
- **Mid ticket** ($15-100): percentage rate dominates. Standard interchange-plus pitch.
- **High ticket** ($100+): rate sensitivity is high in absolute dollars; also higher fraud and
  chargeback exposure.

### Channel mix

Card-present, keyed/MOTO, e-commerce, or hybrid. Each implies different hardware, interchange,
fraud tooling and competitors. Be explicit — "we serve everyone" produces a lead list nobody works.

### Vertical fit

Score candidate verticals against: volume per location, ticket size, underwriting friction,
churn/closure rate, switching cost, density (can a rep walk a corridor?), and referral dynamics.

Common patterns worth testing against your own data:

| Vertical | Why it can work | What to watch |
|---|---|---|
| Quick-service & casual restaurants | High volume, high density, heavy flat-rate penetration | High business-closure rate; Toast lock-in |
| Salons, spas, barbers | Low ticket, fee-sensitive, high card share | Often deep in Square/Vagaro/Boulevard |
| Auto repair & tire | High ticket, stable, owner-operated | Frequently on legacy terminals — good for you |
| Independent retail & specialty | Predictable, walkable density | Seasonal swings |
| Professional services & B2B | **Level 2/3 interchange optimization is real money** | Lower transaction counts |
| Medical, dental, veterinary | High ticket, stable, low churn | Longer cycles, HIPAA-adjacent handling |
| Trades: HVAC, plumbing, electrical | Growing mobile acceptance, high ticket | Often no card acceptance at all — a bigger sale |
| E-commerce SMB | Volume scales fast | Stripe/Shopify lock-in; higher chargebacks |

**B2B professional services is the most consistently under-pitched segment**, because Level 2/3
interchange optimization produces large, verifiable savings and almost no competing rep raises it.

### Trigger events

The highest-converting profile attribute. Rank them:

1. **Ownership change** — new owner re-decides every vendor, owes the incumbent agent nothing
2. **New business opening** — no incumbent at all
3. **Documented payment pain** — reviews citing card minimums, outages, surcharges
4. **Outgrowing flat-rate** — a Square/Stripe merchant whose volume has crossed the point where
   interchange-plus wins
5. **Expansion** — second location, new online channel
6. **Incumbent disruption** — processor price increase, service failure, agent departure

### Disqualifiers

Be as specific here as in the positive profile. Rep time saved is rep time earned:

- Franchisor-mandated processor
- Verticals your sponsor bank will not board
- Confirmed MATCH/TMF listing
- Mid-contract with a large ETF and no offsetting value
- 12+ months remaining on an equipment lease
- POS-fused stacks where payments cannot be separated
- National chains with centralized procurement
- Volume band D with no growth signal

---

## Phase 3: Scoring model

Produce weights the team can apply mechanically in `merchant-source`. A defensible default, to be
tuned against the user's own attrition data:

| Dimension | Weight |
|---|---|
| Estimated volume band | 30% |
| Trigger event present | 25% |
| Switching cost (inverted) | 20% |
| Contactability | 15% |
| Underwriting fit | 10% |

State the pass threshold and what each band means operationally.

---

## Phase 4: Where these merchants are found

An ICP that does not say where to find the merchants is an essay. For each target vertical name the
concrete sources — licence registries, association directories, open-data portals, the specific
review signals — and hand them to `merchant-source`.

---

## Output

`IDEAL-MERCHANT-PROFILE.md`:

```markdown
# Ideal Merchant Profile — {Company}

## Summary
The one-paragraph description of the merchant you want, specific enough that a rep could
recognize one walking down a commercial strip.

## Target Profile
Volume band · average ticket · channel mix · geography · business age

## Target Verticals (ranked)
| Vertical | Why | Typical stack | Angle | Watch-outs |

## Trigger Events (ranked)
| Trigger | Signal source | Why it converts |

## Disqualifiers
Hard stops and automatic downgrades

## Scoring Model
Dimensions, weights, thresholds

## Where to Find Them
Per vertical: named sources and access method

## Positioning by Vertical
The specific opener for each — rate, hardware, Level 2/3, uptime, acceptance

## Validation Plan
What to measure over the first 50 merchants, and which assumptions to revisit
```

---

## Rules

1. **Ground it in the existing book where one exists.** Portfolio data beats market theory.
2. **Optimize for residual longevity, not close rate.** A vertical that closes fast and churns in
   nine months is a trap that takes two years to become visible.
3. **Be specific enough to exclude.** An ICP that disqualifies nothing has no operational value.
4. **Confirm underwriting appetite before naming a target vertical.** Pointing a team at merchants
   the sponsor declines is worse than having no ICP at all.
5. **Say which parts are hypothesis.** Then name the metric that will confirm or kill each.

## Related
- `merchant-source` — apply the profile to build the list
- `merchant-qualify` — apply it to individual merchants
- `sales-icp` — generic B2B version, for non-merchant offerings
