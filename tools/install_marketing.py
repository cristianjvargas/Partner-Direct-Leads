#!/usr/bin/env python3
"""
Vendor ai-marketing-claude into .claude/, adding the YAML frontmatter that
upstream omits. Without it Claude Code never loads these files.

Descriptions are written to NOT collide with the sales-* suite already
installed - market-competitors is about a competitor's marketing, while
sales-competitors is about displacing an incumbent at a prospect.
"""
import pathlib

SRC = pathlib.Path("/tmp/claude-0/-home-user-Partner-Direct-Leads/"
                   "fabba477-e5b5-5672-8497-55c63776f422/scratchpad/ai-marketing-claude")
DST = pathlib.Path("/home/user/Partner-Direct-Leads/.claude")

SKILLS = {
 "market": ("market/SKILL.md",
   "Router for the AI Marketing suite. Use when the user types /market <subcommand> or asks for "
   "marketing work without naming a specific skill - it dispatches to audit, landing, seo, social, "
   "copy, emails, funnel, brand, ads, competitors, launch, proposal or report."),
 "market-audit": ("skills/market-audit/SKILL.md",
   "Run a full marketing audit of a website using five parallel agents (strategy, content, "
   "conversion, technical, competitive) and produce a scored MARKETING-AUDIT.md. Use for 'audit my "
   "site', 'why isn't my site converting', or a complete marketing workup."),
 "market-landing": ("skills/market-landing/SKILL.md",
   "Analyze a landing page for conversion rate optimization - headline, offer clarity, call to "
   "action, friction, social proof, mobile experience - producing LANDING-PAGE-ANALYSIS.md. Use for "
   "'review my landing page', 'why is nobody converting', or before publishing a new page."),
 "market-seo": ("skills/market-seo/SKILL.md",
   "Audit a site's SEO and content - keywords, titles, meta, headings, internal linking, gaps "
   "against competitors - producing SEO-AUDIT.md. Use for 'help me get found on Google', 'SEO "
   "audit', or 'why doesn't my site rank'."),
 "market-social": ("skills/market-social/SKILL.md",
   "Build a social media content calendar and the posts to fill it, by platform, producing "
   "SOCIAL-CALENDAR.md. Use for 'what should I post', 'build me a content calendar', or planning "
   "Instagram, LinkedIn or TikTok content."),
 "market-copy": ("skills/market-copy/SKILL.md",
   "Analyze and rewrite marketing copy - headlines, value propositions, page and ad copy - against "
   "clarity, specificity and voice, producing COPY-ANALYSIS.md. Use for 'improve this copy', "
   "'rewrite my headline', or 'this doesn't sound like me'."),
 "market-emails": ("skills/market-emails/SKILL.md",
   "Generate an email sequence - welcome, nurture, launch or re-engagement - with subject lines and "
   "send timing, producing EMAIL-SEQUENCE.md. Use for 'write my welcome emails', 'build a nurture "
   "sequence', or email marketing campaigns."),
 "market-funnel": ("skills/market-funnel/SKILL.md",
   "Map and analyze a marketing funnel end to end - traffic source, landing, capture, nurture, "
   "conversion - find where prospects leak out, producing FUNNEL-ANALYSIS.md. Use for 'build me a "
   "funnel', 'where am I losing people', or designing a lead capture flow."),
 "market-brand": ("skills/market-brand/SKILL.md",
   "Define brand voice and messaging guidelines from existing material or a description - tone, "
   "vocabulary, positioning, what to never say - producing BRAND-GUIDELINES.md. Use for 'define my "
   "brand voice', 'how should I sound', or keeping messaging consistent across channels."),
 "market-ads": ("skills/market-ads/SKILL.md",
   "Generate ad creative and copy variants for paid channels with targeting and testing notes, "
   "producing AD-CREATIVE.md. Use for 'write me Facebook ads', 'Google Ads copy', or planning a paid "
   "campaign."),
 "market-competitors": ("skills/market-competitors/SKILL.md",
   "Analyze how competitors market themselves - positioning, messaging, content, channels, offers - "
   "and find the gaps, producing COMPETITIVE-ANALYSIS.md. Use for 'what are competitors doing', "
   "'how do they position', or differentiating your own marketing. For displacing an incumbent at a "
   "specific sales prospect, use sales-competitors instead."),
 "market-launch": ("skills/market-launch/SKILL.md",
   "Build a launch playbook for a product, service or brand - timeline, channels, assets, sequence "
   "and checklist - producing LAUNCH-PLAYBOOK.md. Use for 'I'm launching X', 'plan my launch', or "
   "go-to-market planning."),
 "market-proposal": ("skills/market-proposal/SKILL.md",
   "Generate a proposal for marketing services with scope, deliverables, pricing and timeline, "
   "producing MARKETING-PROPOSAL.md. Use when pitching marketing work to a client. For a general "
   "sales proposal, use sales-proposal instead."),
 "market-report": ("skills/market-report/SKILL.md",
   "Produce a Markdown marketing report from analyses in the working directory - findings, scores "
   "and prioritized actions - producing MARKETING-REPORT.md. Use for 'summarize the marketing "
   "findings' or reporting results to a client."),
 "market-report-pdf": ("skills/market-report-pdf/SKILL.md",
   "Produce a designed multi-page PDF marketing report via scripts/generate_pdf_report.py. Use for "
   "'give me a PDF marketing report' or when findings need to be shared outside the terminal. "
   "Requires reportlab."),
}

AGENTS = {
 "market-strategy": "Evaluates marketing strategy and positioning for a site. Launched by market-audit as one of five parallel subagents.",
 "market-content": "Evaluates content quality, depth and coverage for a site. Launched by market-audit as one of five parallel subagents.",
 "market-conversion": "Evaluates conversion paths, calls to action and friction for a site. Launched by market-audit as one of five parallel subagents.",
 "market-technical": "Evaluates technical marketing health - speed, mobile, metadata, tracking. Launched by market-audit as one of five parallel subagents.",
 "market-competitive": "Evaluates competitive positioning and messaging gaps. Launched by market-audit as one of five parallel subagents.",
}
AGENT_TOOLS = "WebFetch, WebSearch, Read, Write"


def esc(s):
    return s.replace('"', "'")


n = a = 0
for name, (rel, desc) in SKILLS.items():
    body = (SRC / rel).read_text()
    assert not body.startswith("---"), f"{rel} unexpectedly has frontmatter"
    out = DST / "skills" / name / "SKILL.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(f'---\nname: {name}\ndescription: "{esc(desc)}"\n---\n\n{body}')
    n += 1

for name, desc in AGENTS.items():
    body = (SRC / "agents" / f"{name}.md").read_text()
    assert not body.startswith("---")
    (DST / "agents" / f"{name}.md").write_text(
        f'---\nname: {name}\ndescription: "{esc(desc)}"\ntools: {AGENT_TOOLS}\n---\n\n{body}')
    a += 1

# shared scripts and templates live under the orchestrator, as upstream expects
import shutil
for sub in ("scripts", "templates"):
    tgt = DST / "skills" / "market" / sub
    tgt.mkdir(parents=True, exist_ok=True)
    for f in sorted((SRC / sub).iterdir()):
        if f.is_file():
            shutil.copy2(f, tgt / f.name)
shutil.copy2(SRC / "LICENSE", DST / "skills" / "market" / "UPSTREAM-LICENSE")

print(f"installed {n} skills, {a} agents")
