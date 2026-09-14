---
name: merchant-compliance
description: "Check merchant-services prospecting and outreach against the rules that actually generate liability - TCPA and DNC for cold calls and texts, CAN-SPAM for email, state telemarketing law, card-brand rules on rate claims and surcharging, and data-collection terms when building lead lists. Use before launching any outbound campaign, buying a list, or sending a savings claim. Produces COMPLIANCE-CHECK.md."
---

# Merchant Services Outreach Compliance

Merchant services is one of the most aggressively prospected industries in the country, and one of
the most litigated. TCPA suits are a genuine business line for plaintiff firms, statutory damages run
$500-1,500 **per call or text**, and class actions against ISOs and their agents are routine. A
sourcing or outreach decision made carelessly on Monday is a six-figure exposure by Friday.

Run this **before** a campaign goes out, not after. Output: `COMPLIANCE-CHECK.md`.

> **This is operational guidance, not legal advice.** Rules change, differ by state, and turn on
> facts specific to a business. Anything that looks close to a line goes to the company's counsel or
> compliance officer before it ships. Where this skill and counsel disagree, counsel wins.

---

## 1. Phone — the largest exposure

**Autodialers and prerecorded messages (TCPA).** Using an autodialer or a prerecorded/artificial
voice to call a cell phone without the right consent is the classic exposure. Merchant cell numbers
are constantly mistaken for business landlines — a huge share of small-business "business lines" are
the owner's mobile. Assume a small-business number may be a cell unless verified otherwise.

**Do-Not-Call.** The National DNC Registry primarily protects residential subscribers, and
business-to-business calls are treated differently — but sole proprietors and home-based businesses
routinely blur that line, and many states regulate more broadly than the federal rules. Practically:

- Scrub against the **National DNC Registry** where applicable
- Maintain and honour an **internal do-not-call list** — this obligation is not optional and applies
  regardless of the B2B question
- Record every opt-out immediately and permanently, across every channel
- Respect calling-hours restrictions
- Register where a state requires telemarketer registration — several do, with real penalties

**Texting.** SMS to a mobile without prior express written consent is high-risk. Cold-texting merchant
numbers pulled from a directory is the single riskiest thing an outbound merchant-services team can
do. Do not do it on scraped numbers.

**Recording calls.** Several states require all-party consent. Know which rule applies to both ends
of the call before recording.

---

## 2. Email — CAN-SPAM

Lower risk than phone, but the requirements are simple and there is no excuse for missing them:

- Accurate, non-deceptive **From**, **Reply-To** and routing information
- A subject line that does not misrepresent the message
- Identification as an advertisement
- A **valid physical postal address**
- A **working, obvious unsubscribe** honoured promptly — and permanently
- No harvesting addresses from websites, and no dictionary attacks (both are explicit aggravating
  factors that increase penalties)

Note that `merchant-source`'s guidance to never fabricate contacts is a compliance control, not just
a data-quality one: guessed addresses drive bounce rates, damage domain reputation, and edge toward
harvesting behaviour.

---

## 3. Data collection — how the list was built

The lawfulness of the list is upstream of the lawfulness of the outreach:

- **Honour `robots.txt` and site terms of service.** Many directories explicitly prohibit automated
  collection. Prefer official APIs — Google Places, Yelp Fusion — and use them within their terms,
  including their restrictions on storage and redistribution.
- **Public record ≠ unrestricted use.** State business filings, licence registries and inspection
  lists are public, but some carry explicit restrictions on commercial solicitation use. Check the
  terms attached to each dataset. Some states specifically prohibit using filing data for marketing.
- **Purchased lists** — verify provenance and consent representations in writing before use. "The
  vendor said it was opt-in" is not a defence anyone has enjoyed making.
- **Rate-limit politely** and identify your agent honestly. Do not evade bot protection to collect
  data — beyond the terms question, circumvention changes the legal character of the activity.
- **Personal data.** Owner names, personal mobiles and home addresses attached to sole proprietors
  are personal data under several state privacy laws (CCPA/CPRA and successors), with access and
  deletion obligations. Know what you are storing and be able to delete it on request.

---

## 4. Rate and savings claims

This is where merchant services earns its reputation, and where a rep's own credibility is at stake:

- **Never claim to beat interchange.** It is fixed by the card networks. Competing on it is not a
  claim you can support.
- **Every savings number needs a stated basis**, and the switching costs — ETF, remaining equipment
  lease — belong in the same table as the savings, not a footnote. See `merchant-statement-analysis`.
- **No teaser rates that omit qualifying conditions.** A "0.29%" headline that is the qualified tier
  of a three-tier structure is the practice that generated this industry's reputation.
- **Disclose the term, the ETF and the equipment arrangement** before signature. Equipment leases
  through a separate leasing entity must be identified as such — merchants routinely believe the
  lease cancels with the processing agreement. It does not.
- **Do not misrepresent affiliation.** Implying you are from the merchant's current processor, their
  bank, or a card network in order to get past a gatekeeper is deceptive practice. It is also common
  in this industry, which is exactly why it draws regulatory attention.

---

## 5. Surcharging and cash discount

If you sell surcharge or dual-pricing programs, the rules are specific and the exposure sits with
the merchant, which means it sits with you:

- Surcharging is **prohibited or restricted in several states**, and the landscape changes through
  litigation — verify the current rule for the merchant's jurisdiction, every time
- Card-brand rules cap surcharge amounts and require advance notification to the networks
- Required signage at entry and point of sale, and disclosure on the receipt
- **Debit cards cannot be surcharged**
- "Cash discount" and "surcharge" are legally distinct structures — programs that call themselves
  cash discount while functioning as a surcharge are the ones that draw enforcement

Selling a merchant into a non-compliant surcharge program exposes them to fines and card-brand
action. Verify the state rule before the pitch, not after the install.

---

## 6. Pre-campaign checklist

Run this before any outbound campaign. Every line gets an explicit yes:

```
LIST
[ ] Source terms reviewed; collection method permitted
[ ] Public-record datasets checked for commercial-use restrictions
[ ] Scrubbed against National DNC (where applicable)
[ ] Scrubbed against internal DNC
[ ] Scrubbed against existing CRM (customers and other reps' accounts)
[ ] Mobile vs landline identified where phone outreach is planned
[ ] No fabricated or pattern-guessed contacts presented as verified

PHONE
[ ] No autodialer/prerecorded to mobiles without required consent
[ ] Calling hours respected for each recipient's time zone
[ ] State telemarketer registration in place where required
[ ] Opt-out captured immediately and permanently
[ ] Call recording consent rule confirmed for both states

EMAIL
[ ] Accurate headers and non-deceptive subject
[ ] Physical postal address present
[ ] Working unsubscribe, honoured promptly
[ ] No harvested addresses

SMS
[ ] Prior express written consent on file — or the channel is not used

CLAIMS
[ ] No "beat interchange" claim
[ ] Every savings figure carries its basis
[ ] ETF and equipment lease disclosed alongside savings
[ ] No implied affiliation with processor, bank or card network
[ ] Surcharge program verified against current state rule

RECORDS
[ ] Consent, opt-out and source provenance retained and auditable
```

---

## Output

`COMPLIANCE-CHECK.md` recording: campaign description, channels, list provenance and terms,
scrubs performed with dates, claims review, unresolved items, and what was escalated to counsel.
Keep it — the record that you checked is itself part of the defence.

---

## Standing rules

1. **Phone and SMS carry the real exposure.** Email mistakes cost reputation; TCPA mistakes cost
   statutory damages per contact, multiplied by the list size.
2. **When a rule is unclear, escalate rather than infer.** The cost of asking counsel is an hour.
3. **Honour opt-outs instantly, everywhere, forever** — across channels and across campaigns.
4. **Never help evade a compliance control**, whether it is bot protection on a directory, a DNC
   scrub, or a disclosure a merchant is entitled to.
5. **Document.** Provenance, scrubs and consent records are what turn a defensible program into a
   provably defensible one.

## Related
- `merchant-source` — list building is where scrubbing must happen
- `merchant-statement-analysis` — the claim-integrity rules
