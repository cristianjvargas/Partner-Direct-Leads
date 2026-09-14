# Partner Direct Leads — Sales & Merchant-Services Skills

Claude skills for lead sourcing, prospecting and deal work at a credit card processing /
merchant services company.

Two layers:

1. **`sales-*`** — a general B2B prospecting suite, vendored from
   [zubair-trabzada/ai-sales-team-claude](https://github.com/zubair-trabzada/ai-sales-team-claude) (MIT).
2. **`merchant-*`** — a merchant-services layer written for this business, covering the things
   generic B2B sales tooling gets wrong about card processing.

---

## Install

### In this repo (already done)

Skills live in `.claude/skills/` and agents in `.claude/agents/`. Any Claude Code session
opened on this repository — terminal, web or IDE — loads them automatically. Nothing to run.

### On your claude.ai account (available everywhere)

Repo-level skills only work in this repo. To use them across Claude apps, Cowork and other
projects, upload them to the account:

```bash
./tools/package_for_claude_ai.sh          # all skills
./tools/package_for_claude_ai.sh merchant # just the merchant-services layer
```

Then in **claude.ai → Settings → Capabilities → Skills → Upload skill**, upload each
`.zip` from `dist/skills/`. (`dist/` is gitignored.)

### On a local machine, for every project

```bash
cp -r .claude/skills/* ~/.claude/skills/
cp -r .claude/agents/* ~/.claude/agents/
```

---

## The merchant-services layer

| Skill | What it does |
|---|---|
| `merchant-icp` | Ideal Merchant Profile — verticals, volume bands, triggers, disqualifiers. **Start here.** |
| `merchant-source` | Build scored lead lists from public sources, licence registries and review signals |
| `merchant-payment-stack` | Fingerprint what processor / gateway / POS a merchant runs today |
| `merchant-qualify` | Qualify on volume, ticket, channel mix, underwriting fit and switching cost |
| `merchant-statement-analysis` | Statement → true effective rate → defensible savings number |
| `merchant-compliance` | TCPA / DNC / CAN-SPAM, data-collection terms, rate-claim and surcharge rules |

### Why these exist alongside `sales-*`

The generic suite assumes a B2B SaaS motion: research a company, find a buying committee, run
BANT. Merchant services does not work that way.

- **BANT is the wrong frame.** Every merchant already pays for processing. The question is volume
  and underwriting approval, not budget.
- **The buying committee is one person** — the owner — and reaching them past a gatekeeper is the
  whole game.
- **The qualifying fact is the incumbent processor**, which no generic tool detects.
- **The deliverable is a statement analysis**, not a proposal deck.
- **Cold outreach here is legally regulated** in ways that SaaS prospecting is not.

Use the `sales-*` skills for partner, ISV and referral-channel work where the B2B motion fits.
Use `merchant-*` for merchants.

### Typical flow

```
merchant-icp                → define the target
  └─ merchant-source        → build and score the list
       └─ merchant-compliance   → scrub before anyone dials
            └─ merchant-payment-stack  → what are they on today?
                 └─ merchant-qualify   → worth a rep's hours?
                      └─ merchant-statement-analysis → the number that closes
```

### Bundled tools

```bash
# Fingerprint a merchant's payment stack
python3 .claude/skills/merchant-payment-stack/scripts/detect_processor.py --url example.com

# Effective rate, winnable markup, savings and payback
python3 .claude/skills/merchant-statement-analysis/scripts/effective_rate.py \
    --volume 84500 --transactions 2640 --fees 2871 \
    --interchange 1520 --assessments 118 \
    --proposed-markup-bps 30 --proposed-per-item 0.08 \
    --etf 495 --lease-monthly 89 --lease-months 22
```

Both are stdlib-only, need no API keys, and the rate calculator makes no network calls.

```bash
# Tests
python3 .claude/skills/merchant-payment-stack/scripts/test_detect_processor.py
```

---

## Principles these skills enforce

Merchant services has a deserved reputation problem. These skills are written to work against it,
because over-promising loses the account, the referral network and eventually the licence:

- **Never claim to beat interchange.** It is fixed by the card networks. Only markup is winnable.
- **Every savings number carries its basis**, and switching costs (ETF, remaining equipment lease)
  sit in the same table as the savings — never a footnote.
- **Never present an estimate as a known figure.** Volume estimates prioritize a rep's day; they
  are not claims to make to a merchant.
- **Never fabricate a contact.** A pattern-guessed email is labelled as a guess.
- **If the merchant already has a good deal, say so.** It costs one deal and earns a referral source.
- **Compliance is checked before the campaign**, not after the complaint.

---

## Notes on the upstream suite

`sales-*` is vendored rather than submoduled so the frontmatter fix travels with it. Upstream
ships every `SKILL.md` and agent file **without YAML frontmatter**, which means Claude Code never
loads them — they are inert as published. The `name:` and `description:` frontmatter here was
added during vendoring; skill and agent bodies are otherwise upstream's, MIT licensed
(`.claude/skills/sales/UPSTREAM-LICENSE`).

Upstream also installs to `~/.claude/` via `install.sh`. That is machine-local and does not
survive a fresh container, so this repo vendors instead.

## Layout

```
.claude/
  skills/
    sales/                        orchestrator + shared scripts/ and templates/
    sales-*/                      13 upstream sub-skills
    merchant-*/                   6 merchant-services skills
  agents/                         5 subagents used by sales-prospect
tools/
  package_for_claude_ai.sh        build .zip bundles for claude.ai upload
```
