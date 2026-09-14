---
name: merchant-payment-stack
description: "Identify what payment processor, gateway, POS and card-acceptance setup a merchant is currently running, by fingerprinting their website, checkout flow and public footprint. Use before any merchant-services outreach - 'what are they processing on', 'who is their processor', 'can we save them money', or when qualifying a card-processing prospect. Produces PAYMENT-STACK.md."
---

# Merchant Payment Stack Detection

You identify a merchant's **current card-acceptance setup** before anyone pitches them. In merchant
services this is the single highest-value qualifying fact: you cannot credibly talk about rates,
savings, or a hardware swap until you know what they are on today, who owns the relationship, and
how painful switching would be.

Output: `PAYMENT-STACK.md` in the working directory.

---

## Why this comes first

A rep who opens with "I can save you money on processing" is one of forty calls that merchant got
this month. A rep who opens with "you're on Square's flat 2.6% + 10¢ and you're doing enough volume
now that interchange-plus would save you real money" is having a different conversation. The
difference is this skill.

Detection also tells you what you **cannot** win. A merchant deep inside Toast or Shopify Payments
has switching costs that dwarf a rate saving. Knowing that early saves the rep a week.

---

## Phase 1: Surface fingerprinting

Run the bundled detector first — it is deterministic, fast, and covers the common cases:

```bash
python3 scripts/detect_processor.py --url <merchant-url> --output json
```

Then use `WebFetch` on these pages, because the detector only sees what the server returns without
JavaScript:

| Page | What to look for |
|------|------------------|
| Homepage | Payment badges in the footer, "Powered by" text, script tags |
| Checkout / cart | The real tell — gateway iframes, card field domains, tokenization scripts |
| `/book`, `/order`, `/reserve`, `/donate` | Restaurants, salons and nonprofits often use a separate processor here |
| Pricing / menu | Cash-discount or dual-pricing language (see Phase 3) |
| Contact / locations | Card-present vs card-not-present mix, number of locations |
| Careers / about | Headcount signals feeding volume estimates |

### What the fingerprints mean

| Signal in page source | Likely stack | What it implies for you |
|---|---|---|
| `js.stripe.com`, `stripe.com/v3` | Stripe | CNP-heavy, developer-run, flat 2.9%+30¢. Rate-sensitive at scale, sticky at low volume |
| `squareup.com`, `square.site`, `web.squarecdn.com` | Square | Flat-rate, often micro/SMB, card-present retail or food. **Best target** once volume > ~$15-25k/mo |
| `clover.com`, `connect.clover.com` | Clover | Fiserv-backed, bank or ISO referral. Hardware is leased or owned — ask which |
| `toasttab.com` | Toast | Restaurant, heavily integrated. Rate pitch alone rarely wins |
| `shopify.com/payments`, `shop.app`, `cdn.shopify.com` + Shop Pay | Shopify Payments (Stripe-backed) | Switching means losing Shopify's native flow; usually a hard no unless volume is large |
| `js.authorize.net`, `accept.authorize.net` | Authorize.net gateway | Gateway ≠ processor. The merchant account behind it is the real target — and it's winnable |
| `paypal.com/sdk`, `paypalobjects.com`, Braintree `js.braintreegateway.com` | PayPal / Braintree | Often a secondary rail alongside a main processor. Look for both |
| `nmi.com`, `secure.networkmerchants.com` | NMI gateway | Almost always sold through an ISO — there is an incumbent agent relationship |
| `heartland`, `globalpay`, `cardconnect`, `bolt.cardconnect` | Heartland / Global / CardConnect | Traditional ISO or bank relationship. Contract and early-termination fees likely |
| `helcim.com`, `paymentcloud`, `stax`, `paysafe` | Mid-market ISO | Already on interchange-plus or subscription pricing. Rate pitch is harder |
| `adyen.com`, `checkout.com`, `braintree` at scale | Enterprise | Out of scope for most ISO/agent books |
| WooCommerce + `woocommerce-gateway-*` | Plugin reveals the gateway | Read the plugin slug — it names the processor exactly |
| No detectable online payment | Card-present only | Often the **highest-value target**: no website checkout means the POS/terminal relationship is everything |

Record confidence honestly: `confirmed` (script or domain present in source), `likely` (badge, logo
or copy reference only), or `unknown`. Never upgrade a guess to a fact — a rep who opens with the
wrong processor loses the call in ten seconds.

---

## Phase 2: Card-present signals

Most merchant-services money is in card-present. The website often will not tell you, so read the
physical footprint:

- **Google/Yelp/Apple Maps photos** — terminals and POS screens are visible in interior and counter
  photos. A Clover Station, Square Register, Toast handheld or Verifone/Ingenico terminal is
  identifiable on sight. Note what you see and what you inferred.
- **Review text** — customers mention "they only take cash", "card minimum $10", "the card machine
  was down", "they added a card fee". Each is a concrete opener.
- **Photos of the counter** — a "we now accept Apple Pay" sign, a tip-screen style, a receipt in a
  review photo. Receipt footers frequently print the processor name.
- **Business type → expected setup**: quick-service restaurant (Toast/Square/Clover), full-service
  (Toast/Aloha/Micros), salon/spa (Square/Vagaro/Boulevard), auto repair (Clover/traditional
  terminal), retail (Square/Clover/Lightspeed), professional services (invoice-based CNP).

---

## Phase 3: Pricing-model tells

How the merchant currently prices tells you which pitch lands:

- **"Cash discount" / "dual pricing" / "3.5% card surcharge" on menus or signage** → they are
  already on a surcharge program, usually sold by an ISO. Pitch compliance risk and customer
  friction, not rate. Note: surcharging is capped and is prohibited or restricted in several
  states — flag jurisdiction before a rep uses this angle.
- **Card minimums ("$10 minimum on cards")** → fee-sensitive, low average ticket, likely flat-rate.
  Strong signal for an interchange-plus conversation.
- **"We accept all major cards" with no Amex** → Amex OptBlue opportunity.
- **No online payment at all for a business that clearly should have one** → gateway/virtual
  terminal upsell, not just a rate play.
- **Invoice-based B2B** → Level 2/Level 3 interchange optimization. Large, credible savings for
  B2B merchants that almost no one pitches them on.

---

## Phase 4: Switching-cost assessment

Score how winnable this is, 0-100 (higher = easier to switch):

| Factor | Weight | Easy (high score) | Hard (low score) |
|---|---|---|---|
| Stack depth | 30% | Standalone terminal, generic gateway | POS + payments fused (Toast, Shopify Payments) |
| Contract exposure | 25% | Month-to-month (Square, Stripe) | Multi-year ISO contract, leased hardware, ETF |
| Integration surface | 20% | Payments only | Payroll, inventory, online ordering, loyalty all tied in |
| Relationship | 15% | No agent contact, bank default | Incumbent agent actively servicing them |
| Tech dependency | 10% | Non-technical owner | Developer-built custom Stripe integration |

A merchant on month-to-month Square with a standalone setup and rising volume is the archetype of a
high-quality lead. A three-location Toast restaurant mid-contract is not — mark it and move on.

**Leased hardware is the most commonly missed disqualifier.** A 48-month non-cancellable terminal
lease means the merchant keeps paying regardless of who processes. Always ask, and flag it in the
output.

---

## Output format

Write `PAYMENT-STACK.md`:

```markdown
# Payment Stack — {Merchant Name}

**URL:** {url} · **Analyzed:** {date} · **Business type:** {type}

## Current Stack
| Layer | Detected | Confidence | Evidence |
|---|---|---|---|
| Processor | | confirmed/likely/unknown | |
| Gateway | | | |
| POS / terminal | | | |
| Online checkout | | | |
| Secondary rails | | | |

## Pricing Model
- Model: flat-rate / interchange-plus / tiered / surcharge / unknown
- Evidence:
- Estimated effective rate: {x.xx}% (basis for estimate: ...)

## Card-Present vs CNP
- Estimated split and why

## Switching Cost: {score}/100 — {Easy | Moderate | Hard}
| Factor | Score | Note |
(one row each)

**Blockers:** leased hardware / contract term / integration depth / incumbent agent — state which
are confirmed vs suspected.

## Savings Hypothesis
State the specific angle with the number attached, or state plainly that there isn't one.
Example: "Flat 2.6%+10¢ on ~$40k/mo card-present retail, avg ticket ~$32. Interchange-plus at
IC+35bps saves roughly $380-520/mo. Verify with a statement."

## Opener
One or two sentences a rep can actually say, built only on **confirmed** facts.

## What to verify on the call
- The three things that would change this assessment
```

---

## Honesty rules

These are not style preferences — violating them costs deals:

1. **Never state a processor as fact from a logo or a badge alone.** Badges go stale; merchants
   switch and forget to update the footer.
2. **Never fabricate a savings number.** Every dollar figure needs its basis stated. If you have no
   volume estimate, say "cannot estimate without a statement" — that is a legitimate finding and
   sets up the statement ask, which is the real goal of the first call anyway.
3. **Distinguish gateway from processor.** Authorize.net or NMI tells you the gateway, not who holds
   the merchant account. Saying "you're with Authorize.net" to a merchant whose account is with
   Elavon marks the rep as uninformed.
4. **Flag when you found nothing.** "No online payment footprint; card-present only, stack unknown
   until the call" is a useful, honest result. Padding it with guesses is not.

## Related

- `merchant-qualify` — turn this into a volume and savings estimate
- `merchant-statement-analysis` — the real numbers, once they send a statement
- `merchant-compliance` — before any call or email goes out
