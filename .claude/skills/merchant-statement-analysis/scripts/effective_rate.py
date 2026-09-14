#!/usr/bin/env python3
"""
Effective Rate Calculator — merchant services.

Computes a merchant's true effective rate from statement totals, separates
winnable processor markup from pass-through interchange, and models a proposed
interchange-plus offer including payback against switching costs.

Stdlib only. No network. Nothing leaves the machine.

Usage:
    python3 effective_rate.py --volume 84500 --transactions 2640 --fees 2871
    python3 effective_rate.py --volume 84500 --transactions 2640 --fees 2871 \
        --interchange 41000 --assessments 1100 \
        --proposed-markup-bps 30 --proposed-per-item 0.08 --proposed-monthly-fees 25 \
        --etf 495 --lease-monthly 89 --lease-months 22 --output json
"""

import argparse
import json
import sys

BPS = 10_000.0


def money(x):
    return f"${x:,.2f}"


def pct(x):
    return f"{x:.3f}%"


def analyze(a):
    if a.volume <= 0:
        raise SystemExit("error: --volume must be greater than zero")
    if a.transactions <= 0:
        raise SystemExit("error: --transactions must be greater than zero")

    cur = {
        "volume": a.volume,
        "transactions": a.transactions,
        "total_fees": a.fees,
        "effective_rate_pct": a.fees / a.volume * 100,
        "avg_ticket": a.volume / a.transactions,
        "cost_per_transaction": a.fees / a.transactions,
    }

    # Cost layers. Interchange + assessments are pass-through; the remainder is markup.
    passthrough = None
    if a.interchange is not None:
        passthrough = a.interchange + (a.assessments or 0.0)
        markup = a.fees - passthrough
        cur.update({
            "interchange": a.interchange,
            "assessments": a.assessments or 0.0,
            "passthrough_total": passthrough,
            "passthrough_pct_of_volume": passthrough / a.volume * 100,
            "processor_markup": markup,
            "markup_pct_of_volume": markup / a.volume * 100,
            "markup_bps": markup / a.volume * BPS,
            "markup_share_of_fees_pct": (markup / a.fees * 100) if a.fees else 0.0,
        })

    out = {"current": cur, "notes": []}

    if passthrough is None:
        out["notes"].append(
            "No --interchange supplied, so pass-through and winnable markup could not be "
            "separated. Effective rate alone does not tell you how much is actually winnable."
        )

    # Proposed offer
    if a.proposed_markup_bps is not None:
        if passthrough is None:
            out["notes"].append(
                "Proposed offer modelled, but without --interchange the savings figure assumes "
                "interchange is unchanged and is therefore NOT a defensible savings claim."
            )
            base = None
        else:
            base = passthrough

        prop_markup = a.volume * (a.proposed_markup_bps / BPS)
        prop_items = a.transactions * a.proposed_per_item
        prop_fixed = a.proposed_monthly_fees
        prop_total = (base or 0.0) + prop_markup + prop_items + prop_fixed

        prop = {
            "markup_bps": a.proposed_markup_bps,
            "markup_cost": prop_markup,
            "per_item_cost": prop_items,
            "monthly_fees": prop_fixed,
            "passthrough_assumed": base,
            "total_fees": prop_total,
        }
        if base is not None:
            prop["effective_rate_pct"] = prop_total / a.volume * 100
            prop["cost_per_transaction"] = prop_total / a.transactions

            saving = a.fees - prop_total
            prop["monthly_saving"] = saving
            prop["annual_saving"] = saving * 12
            prop["saving_pct_of_current_fees"] = (saving / a.fees * 100) if a.fees else 0.0

            # Honest range: inputs are estimates, so present a band.
            lo, hi = sorted((saving * 0.85, saving * 1.15))
            prop["monthly_saving_range"] = [lo, hi]

            # Switching cost and payback
            lease_remaining = a.lease_monthly * a.lease_months
            switch_cost = a.etf + lease_remaining
            prop["switching_cost"] = {
                "etf": a.etf,
                "lease_monthly": a.lease_monthly,
                "lease_months_remaining": a.lease_months,
                "lease_remaining_total": lease_remaining,
                "total": switch_cost,
            }
            if saving > 0:
                prop["payback_months"] = switch_cost / saving
                prop["first_year_net"] = saving * 12 - switch_cost
            else:
                out["notes"].append(
                    "Proposed pricing is NOT cheaper than current. This merchant already has a "
                    "competitive deal — say so. Manufacturing a saving here destroys credibility."
                )
            if lease_remaining > 0:
                out["notes"].append(
                    f"Equipment lease of {money(a.lease_monthly)}/mo for {a.lease_months} more "
                    f"months ({money(lease_remaining)}) typically SURVIVES a processor switch. "
                    "Do not present lease relief as savings unless termination is confirmed in writing."
                )
        out["proposed"] = prop

    out["notes"].append(
        "Interchange and assessment schedules are set by the card networks and change roughly "
        "twice a year. Verify against the current published tables and state the effective date."
    )
    out["notes"].append(
        "One statement month is a sample. Seasonal merchants vary widely — request three months "
        "before committing to an annual savings figure."
    )
    return out


def render(r):
    c = r["current"]
    print("\n" + "=" * 62)
    print("  CURRENT STATE")
    print("=" * 62)
    print(f"  Volume                {money(c['volume'])}")
    print(f"  Transactions          {c['transactions']:,}")
    print(f"  Average ticket        {money(c['avg_ticket'])}")
    print(f"  Total fees            {money(c['total_fees'])}")
    print(f"  EFFECTIVE RATE        {pct(c['effective_rate_pct'])}")
    print(f"  Cost per transaction  {money(c['cost_per_transaction'])}")

    if "processor_markup" in c:
        print("\n  Cost layers")
        print(f"    Interchange         {money(c['interchange']):>14}   (not winnable)")
        print(f"    Assessments         {money(c['assessments']):>14}   (not winnable)")
        print(f"    Processor markup    {money(c['processor_markup']):>14}   "
              f"({c['markup_bps']:.1f} bps — this is the target)")
        print(f"    Markup = {c['markup_share_of_fees_pct']:.1f}% of what they pay")

    p = r.get("proposed")
    if p:
        print("\n" + "=" * 62)
        print("  PROPOSED")
        print("=" * 62)
        print(f"  Markup                {p['markup_bps']:.0f} bps  ({money(p['markup_cost'])})")
        print(f"  Per-item              {money(p['per_item_cost'])}")
        print(f"  Monthly fees          {money(p['monthly_fees'])}")
        print(f"  Total fees            {money(p['total_fees'])}")
        if "effective_rate_pct" in p:
            print(f"  EFFECTIVE RATE        {pct(p['effective_rate_pct'])}")
            lo, hi = p["monthly_saving_range"]
            print(f"\n  MONTHLY SAVING        {money(p['monthly_saving'])}  "
                  f"(range {money(lo)}–{money(hi)})")
            print(f"  ANNUAL SAVING         {money(p['annual_saving'])}")
            sc = p["switching_cost"]
            if sc["total"] > 0:
                print(f"\n  Switching cost        {money(sc['total'])}  "
                      f"(ETF {money(sc['etf'])} + lease {money(sc['lease_remaining_total'])})")
                if "payback_months" in p:
                    print(f"  Payback               {p['payback_months']:.1f} months")
                    print(f"  First-year net        {money(p['first_year_net'])}")

    if r["notes"]:
        print("\n" + "-" * 62)
        for n in r["notes"]:
            print(f"  ! {n}")
    print()


def main():
    ap = argparse.ArgumentParser(
        description="Compute a merchant's effective rate and model a proposed offer.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    ap.add_argument("--volume", type=float, required=True, help="Total monthly card volume")
    ap.add_argument("--transactions", type=int, required=True, help="Total monthly transaction count")
    ap.add_argument("--fees", type=float, required=True,
                    help="ALL fees for the month (discount, per-item, monthly, PCI, batch, lease...)")
    ap.add_argument("--interchange", type=float, default=None,
                    help="Interchange for the month, if the statement breaks it out")
    ap.add_argument("--assessments", type=float, default=None, help="Card network assessments")
    ap.add_argument("--proposed-markup-bps", type=float, default=None,
                    help="Proposed markup over interchange, in basis points")
    ap.add_argument("--proposed-per-item", type=float, default=0.0, help="Proposed per-transaction fee")
    ap.add_argument("--proposed-monthly-fees", type=float, default=0.0, help="Proposed fixed monthly fees")
    ap.add_argument("--etf", type=float, default=0.0, help="Incumbent early termination fee")
    ap.add_argument("--lease-monthly", type=float, default=0.0, help="Equipment lease payment per month")
    ap.add_argument("--lease-months", type=int, default=0, help="Lease months remaining")
    ap.add_argument("--output", choices=["text", "json"], default="text")
    args = ap.parse_args()

    result = analyze(args)
    if args.output == "json":
        print(json.dumps(result, indent=2))
    else:
        render(result)


if __name__ == "__main__":
    sys.exit(main())
