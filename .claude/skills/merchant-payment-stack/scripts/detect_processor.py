#!/usr/bin/env python3
"""
Payment Stack Detector — merchant-services prospecting.

Fetches a merchant's public pages and fingerprints the payment processor,
gateway, POS and e-commerce platform from page source.

Stdlib only. No API keys. Read-only GETs.

Usage:
    python3 detect_processor.py --url https://example.com
    python3 detect_processor.py --url example.com --output json
"""

import argparse
import json
import re
import ssl
import sys
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen

UA = "Mozilla/5.0 (compatible; MerchantStackDetector/1.0)"

# (label, layer, [regex patterns]) — patterns are matched against page source.
SIGNATURES = [
    # --- Processors / full-stack ---
    ("Stripe",            "processor", [r"js\.stripe\.com", r"api\.stripe\.com", r"stripe\.com/v3", r"__stripe_mid"]),
    ("Square",            "processor", [r"squareup\.com", r"web\.squarecdn\.com", r"square\.site", r"squarecdn"]),
    ("Clover",            "processor", [r"\bclover\.com", r"connect\.clover\.com", r"clover\.net"]),
    ("Toast",             "processor", [r"toasttab\.com", r"toastwebstatic"]),
    ("Shopify Payments",  "processor", [r"cdn\.shopify\.com", r"shop\.app", r"shopifycdn", r"shopify_pay"]),
    ("PayPal",            "processor", [r"paypal\.com/sdk", r"paypalobjects\.com", r"paypal\.com/checkout"]),
    ("Braintree",         "processor", [r"js\.braintreegateway\.com", r"braintree-api\.com"]),
    ("Adyen",             "processor", [r"checkoutshopper.*adyen", r"adyen\.com"]),
    ("Checkout.com",      "processor", [r"cdn\.checkout\.com", r"api\.checkout\.com"]),
    ("Heartland",         "processor", [r"heartlandpaymentsystems", r"\bheartland\b.*payment", r"securesubmit"]),
    ("Global Payments",   "processor", [r"globalpay(ments)?\.com", r"gpapi"]),
    ("CardConnect",       "processor", [r"cardconnect\.com", r"bolt\.cardconnect"]),
    ("Elavon",            "processor", [r"elavon\.com", r"converge.*elavon", r"convergepay"]),
    ("Worldpay / FIS",    "processor", [r"worldpay\.com", r"secure\.worldpay"]),
    ("Helcim",            "processor", [r"helcim\.com", r"secure\.helcim"]),
    ("Stax",              "processor", [r"staxpayments\.com", r"fattmerchant"]),
    ("Payment Depot",     "processor", [r"paymentdepot\.com"]),
    ("Paysafe",           "processor", [r"paysafe\.com", r"netbanx"]),

    # --- Gateways (NOT the merchant account) ---
    ("Authorize.net",     "gateway",   [r"js\.authorize\.net", r"accept\.authorize\.net", r"authorize\.net/gateway"]),
    ("NMI",               "gateway",   [r"secure\.networkmerchants\.com", r"\bnmi\.com", r"secure\.nmi\.com"]),
    ("USAePay",           "gateway",   [r"usaepay\.com"]),
    ("Cybersource",       "gateway",   [r"cybersource\.com"]),
    ("2Checkout / Verifone", "gateway", [r"2checkout\.com", r"verifone\.cloud"]),
    ("Payflow",           "gateway",   [r"payflowlink", r"payflowpro"]),

    # --- POS / vertical platforms ---
    ("Lightspeed",        "pos",       [r"lightspeedhq\.com", r"lightspeedpos"]),
    ("Vagaro",            "pos",       [r"vagaro\.com"]),
    ("Boulevard",         "pos",       [r"blvd\.co", r"joinblvd"]),
    ("Mindbody",          "pos",       [r"mindbodyonline\.com"]),
    ("ChowNow",           "pos",       [r"chownow\.com"]),
    ("Olo",               "pos",       [r"\.olo\.com", r"olo\.com/"]),
    ("Revel",             "pos",       [r"revelsystems\.com"]),
    ("SpotOn",            "pos",       [r"spoton\.com"]),
    ("Aloha / NCR",       "pos",       [r"ncr\.com", r"alohaenterprise"]),

    # --- E-commerce platforms (context, not processor) ---
    ("Shopify",           "platform",  [r"cdn\.shopify\.com", r"Shopify\.theme"]),
    ("WooCommerce",       "platform",  [r"woocommerce", r"wp-content/plugins/woocommerce"]),
    ("BigCommerce",       "platform",  [r"bigcommerce\.com"]),
    ("Wix",               "platform",  [r"wix\.com", r"wixstatic"]),
    ("Squarespace",       "platform",  [r"squarespace\.com", r"sqsp\.net"]),
    ("Magento",           "platform",  [r"magento", r"/static/version"]),
    ("Ecwid",             "platform",  [r"ecwid\.com"]),
]

# WooCommerce gateway plugins name the processor outright.
WOO_GATEWAY = re.compile(r"plugins/woocommerce-gateway-([a-z0-9\-]+)", re.I)

# Pricing-model tells worth surfacing to the rep.
PRICING_TELLS = [
    ("cash discount program", r"cash discount"),
    ("dual pricing",          r"dual[- ]pricing"),
    ("card surcharge",        r"(surcharge|service fee) (of |is )?\d"),
    ("card minimum",          r"\$\d+\s*(card |credit card )?minimum"),
    ("no Amex",               r"(we )?(do not|don't) accept (american express|amex)"),
    ("cash only",             r"cash only"),
]

CANDIDATE_PATHS = ["", "/checkout", "/cart", "/shop", "/order", "/book", "/donate",
                   "/pricing", "/contact", "/menu"]


def fetch(url, timeout=12):
    """GET a URL, returning (html, final_url) or (None, err)."""
    ctx = ssl.create_default_context()
    try:
        req = Request(url, headers={"User-Agent": UA, "Accept": "text/html,*/*"})
        resp = urlopen(req, timeout=timeout, context=ctx)
        raw = resp.read(2_000_000)
        charset = resp.headers.get_content_charset() or "utf-8"
        return raw.decode(charset, errors="replace"), resp.geturl()
    except (HTTPError, URLError, ssl.SSLError, OSError, ValueError) as e:
        return None, str(e)


def scan(html):
    """Return {label: {layer, patterns_hit}} for everything fingerprinted."""
    hits = {}
    for label, layer, patterns in SIGNATURES:
        matched = [p for p in patterns if re.search(p, html, re.I)]
        if matched:
            hits[label] = {"layer": layer, "matched": matched}
    for m in WOO_GATEWAY.finditer(html):
        slug = m.group(1)
        hits[f"WooCommerce gateway: {slug}"] = {"layer": "gateway", "matched": [m.group(0)]}
    return hits


def pricing_tells(html):
    text = re.sub(r"<[^>]+>", " ", html)
    return [label for label, pat in PRICING_TELLS if re.search(pat, text, re.I)]


def normalize(url):
    if not urlparse(url).scheme:
        url = "https://" + url
    return url


def main():
    ap = argparse.ArgumentParser(
        description="Fingerprint a merchant's payment processor, gateway and POS.",
        epilog="Example: python3 detect_processor.py --url example.com --output json")
    ap.add_argument("--url", required=True, help="Merchant website URL")
    ap.add_argument("--output", choices=["text", "json"], default="text")
    ap.add_argument("--timeout", type=int, default=12)
    ap.add_argument("--paths", default=",".join(CANDIDATE_PATHS),
                    help="Comma-separated paths to probe")
    args = ap.parse_args()

    base = normalize(args.url)
    results, errors, tells = {}, {}, set()
    pages_fetched = []

    for path in args.paths.split(","):
        target = urljoin(base, path) if path else base
        html, info = fetch(target, args.timeout)
        if html is None:
            errors[target] = info
            continue
        pages_fetched.append(target)
        for label, data in scan(html).items():
            entry = results.setdefault(label, {"layer": data["layer"], "pages": [], "matched": set()})
            entry["pages"].append(target)
            entry["matched"].update(data["matched"])
        tells.update(pricing_tells(html))

    for entry in results.values():
        entry["matched"] = sorted(entry["matched"])

    # Confidence: seen on 2+ pages is stronger evidence than a single stale badge.
    for label, entry in results.items():
        entry["confidence"] = "confirmed" if len(entry["pages"]) >= 2 else "likely"

    by_layer = {}
    for label, entry in results.items():
        by_layer.setdefault(entry["layer"], []).append(label)

    out = {
        "url": base,
        "pages_fetched": pages_fetched,
        "detected": results,
        "by_layer": by_layer,
        "pricing_tells": sorted(tells),
        "errors": errors,
        "note": ("Gateway != processor. A gateway hit tells you how cards are transmitted, "
                 "not who holds the merchant account. Card-present setup is not visible here — "
                 "check maps photos and reviews."),
    }

    if args.output == "json":
        print(json.dumps(out, indent=2))
        return

    print(f"\nPayment stack for {base}")
    print(f"Pages fetched: {len(pages_fetched)}")
    if not results:
        print("\n  No payment fingerprints found.")
        print("  -> Likely card-present only, or checkout is JS-rendered / on a third-party domain.")
        print("  -> This is a finding, not a failure. Card-present-only merchants are often the best targets.")
    for layer in ("processor", "gateway", "pos", "platform"):
        labels = by_layer.get(layer, [])
        if labels:
            print(f"\n  {layer.upper()}")
            for label in sorted(labels):
                e = results[label]
                print(f"    - {label}  [{e['confidence']}, {len(e['pages'])} page(s)]")
    if tells:
        print("\n  PRICING TELLS")
        for t in sorted(tells):
            print(f"    - {t}")
    if errors:
        print(f"\n  {len(errors)} path(s) unreachable (normal — most sites lack all probed paths)")
    print()


if __name__ == "__main__":
    sys.exit(main())
