#!/usr/bin/env python3
"""Fixture tests for detect_processor fingerprinting. Run: python3 test_detect_processor.py"""
import importlib.util, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("d", os.path.join(HERE, "detect_processor.py"))
d = importlib.util.module_from_spec(spec)
spec.loader.exec_module(d)

FIXTURES = {
    "square": '<script src="https://web.squarecdn.com/v1/square.js"></script><p>$10 card minimum</p>',
    "shopify": '<script src="https://cdn.shopify.com/s/files/x.js"></script><link href="https://shop.app/pay">',
    "authnet": '<script src="https://js.authorize.net/v1/Accept.js"></script>',
    "woo": '<link href="/wp-content/plugins/woocommerce-gateway-stripe/assets/x.css">',
    "toast": '<a href="https://order.toasttab.com/online/joes">Order</a>',
    "clover": '<script src="https://checkout.clover.com/sdk.js"></script>'
              '<p>A service fee of 3.5% applies to card payments.</p>',
    "cash_only": '<p>Sorry, CASH ONLY. No cards accepted.</p>',
    "brochure": '<html><body><h1>Joe Plumbing</h1><p>Call us</p></body></html>',
}

CHECKS = [
    ("square processor",   lambda: "Square" in d.scan(FIXTURES["square"])),
    ("square tell",        lambda: "card minimum" in d.pricing_tells(FIXTURES["square"])),
    ("shopify payments",   lambda: "Shopify Payments" in d.scan(FIXTURES["shopify"])),
    ("authnet is gateway", lambda: d.scan(FIXTURES["authnet"])["Authorize.net"]["layer"] == "gateway"),
    ("woo plugin slug",    lambda: any("WooCommerce gateway" in k for k in d.scan(FIXTURES["woo"]))),
    ("toast processor",    lambda: "Toast" in d.scan(FIXTURES["toast"])),
    ("clover + surcharge", lambda: "Clover" in d.scan(FIXTURES["clover"])
                                   and "card surcharge" in d.pricing_tells(FIXTURES["clover"])),
    ("cash only tell",     lambda: "cash only" in d.pricing_tells(FIXTURES["cash_only"])),
    ("no false positives", lambda: d.scan(FIXTURES["brochure"]) == {}
                                   and d.pricing_tells(FIXTURES["brochure"]) == []),
]

failed = 0
for name, check in CHECKS:
    try:
        ok = check()
    except Exception as e:
        ok, name = False, f"{name} (raised {e!r})"
    print(f"  {'PASS' if ok else 'FAIL'}  {name}")
    failed += not ok

print(f"\n{len(CHECKS) - failed}/{len(CHECKS)} passed")
sys.exit(1 if failed else 0)
