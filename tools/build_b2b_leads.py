#!/usr/bin/env python3
"""
Build the B2B/wholesale starter list in Reconnect Sprint column order.

Sourced from web search, September 2026. Owner names and phone numbers are
deliberately blank: search surfaced the businesses, not verified contacts, and
an invented phone number is worse than an empty cell.

"What they run" is blank by design - per Rule 01 that is a question for the
merchant, not research to do beforehand.
"""

import csv

HEADERS = ["Name", "Business", "Their role", "Tier", "Segment", "Priority",
           "How I know them", "Phone", "IG / LinkedIn", "Website",
           "What they run (ask, don't research)", "Status", "Last contact",
           "Next action", "Notes"]

TIER = "3 - Confirmed business cooler"
SRC = "Web search Sep 2026 - unverified"
NEXT = "Sunbiz for officer name, then call"

# (business, website, note)  — note carries category, address and any flag.
LEADS = [
    # ---- General wholesale / import-export ----
    ("PJ Distributors", "pjdistributorsusa.com",
     "IMPORT-EXPORT. Est 1999. Supplies supermarkets/wholesalers across US, LatAm, Caribbean."),
    ("TANO Wholesale Inc", "tanowholesale.com",
     "IMPORT-EXPORT. Doral. Mobile phones, data storage, energy backup. B2B resellers."),
    ("Donec Distributors LLC", "donecdistributors.com",
     "IMPORT-EXPORT. 6356 NW 99th Ave, Doral 33178. Designer fragrances + consumer electronics."),
    ("Miami Trading Zone LLC", "miamitradingzone.com",
     "IMPORT-EXPORT. Brand-name perfume wholesale to retailers and wholesalers."),
    ("Miami Lots", "miamilots.com",
     "IMPORT-EXPORT. Bulk fragrances, cosmetics, electronics for resellers. Has online ordering - ask about the gateway."),
    ("Florida European Import Export", "",
     "IMPORT-EXPORT. Est 1973. Premium specialty produce. 50+ years = likely a legacy processor nobody has reviewed."),
    ("Tocumen Produce", "tocumenproduceusa.com",
     "IMPORT-EXPORT. Family-owned citrus import/export. Family-owned means the owner decides alone."),
    ("J.H. Wholesale", "",
     "IMPORT-EXPORT. Est 1993. Name-brand closeout merchandise."),
    ("AJ Globals", "aj-globals.com",
     "IMPORT-EXPORT. General wholesale distribution, Miami."),

    # ---- Food / Latin grocery ----
    ("Los Nicas Distributors", "losnicasdistributors.com",
     "FOOD. Hialeah. Family-owned, Nicaraguan and Latin American products."),
    ("La Autentica Foods LLC", "",
     "FOOD. 989 SE 11 Place, Hialeah 33010."),
    ("A.M.L.L. Corp", "",
     "FOOD. 124 West 24 Street, Hialeah 33010."),
    ("Fedenico Inc", "",
     "FOOD. Latin American food distributor - restaurants, supermarkets, institutions."),
    ("Central American Products Corp", "",
     "FOOD. Imports and wholesales Central American products to FL, SC, IL."),
    ("Cubanita Frozen Food", "cubanitafrozenfood.com",
     "FOOD. Frozen food wholesale distribution."),
    ("Goya Foods (Miami operations)", "",
     "FOOD. FLAG: national company, procurement is almost certainly centralized. Low priority."),

    # ---- Auto parts ----
    ("Auto Parts Distributor (APD)", "",
     "AUTO. North Miami. European, American and Japanese parts. Retail + wholesale + import/export."),
    ("GJ Parts", "gjparts.com",
     "AUTO. Radiator distribution in Hialeah and Medley. Japanese, Korean, American parts. Serves LatAm/Caribbean."),
    ("IMEX Service", "",
     "AUTO. Aftermarket spare parts, Japanese and Korean vehicles."),
    ("IG Tuning Miami", "igtuningmiami.com",
     "AUTO. 30 years. Car accessories wholesale, network across Americas and Caribbean."),
    ("Mighty Auto Parts - North Miami", "",
     "AUTO. 2300 NE 151st St, North Miami. FLAG: franchise - check whether the franchisor mandates processing before working it."),

    # ---- Apparel / textile ----
    ("Magnolia Fashion Wholesale", "",
     "APPAREL. Miami Fashion and Arts District. Women's fashion wholesale."),
    ("Wings2Fashion", "wings2fashion.com",
     "APPAREL. Boutique clothing supplier and manufacturer, Miami."),
    ("Miami Style", "",
     "APPAREL. Lifestyle apparel, high-end brands, wholesale distribution."),
    ("Hemisphere Inc", "",
     "APPAREL. Toddler, infant and newborn apparel, full range."),
    ("Bonita Fashion / Giti Wholesale", "",
     "APPAREL. Global wholesale clothing seller."),
    ("Hannah Bella Collection", "",
     "APPAREL. Downtown Miami fashion district. Designer items at wholesale."),
    ("Samuel Kunstler Textiles Inc", "",
     "APPAREL. Textiles, Miami."),
    ("Sunbrand", "",
     "APPAREL. Apparel and textile services, Miami."),

    # ---- Building materials / construction supply ----
    ("Allsteel Building Material International", "",
     "BUILDING. Medley. Steel and building materials."),
    ("Nachon Lumber and Hardware", "nachonlumberandhardware.com",
     "BUILDING. Hialeah and Miami. 43 years in business - long-tenured, likely legacy processor."),
    ("Olympia Building Supplies", "",
     "BUILDING. Construction materials, Miami and Hialeah."),
    ("Above Interior Distributors", "",
     "BUILDING. Interior construction materials, Miami area."),
    ("Wholesale Building Products", "wholesalebuildingproducts.com",
     "BUILDING. Building materials and wood products, statewide Florida."),
    ("John Abell Corp", "johnabellcorp.com",
     "BUILDING. Concrete supplies and materials, Miami."),
    ("Shell Lumber & Hardware", "",
     "BUILDING. Long-established Miami lumber and hardware."),
    ("FPG Wholesale", "",
     "BUILDING. Building supplies wholesale, Miami."),
    ("American Fasteners", "",
     "BUILDING. Fasteners and hardware wholesale, Miami."),
    ("International Plywood", "",
     "BUILDING. Plywood and wood products, Miami."),
    ("Everglades Lumber & Building Supply", "",
     "BUILDING. Lumber and building supply, Miami."),
    ("Cemex - Medley", "",
     "BUILDING. FLAG: multinational. Centralized procurement, out of scope for an agent. Listed only so it is not re-researched."),
]

OUT = "/home/user/Partner-Direct-Leads/tracker/starter-leads-b2b-wholesale.csv"

with open(OUT, "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(HEADERS)
    for business, site, note in LEADS:
        w.writerow(["", business, "", TIER, "B2B", "", SRC, "", "", site, "",
                    "Not contacted", "", NEXT, note])

print(f"wrote {len(LEADS)} leads to {OUT}")

# sanity checks
flagged = [b for b, _, n in LEADS if "FLAG:" in n]
cats = {}
for _, _, n in LEADS:
    cats[n.split(".")[0]] = cats.get(n.split(".")[0], 0) + 1
print("by category:", cats)
print("flagged (do not work / check first):", flagged)
assert len({b for b, _, _ in LEADS}) == len(LEADS), "duplicate business name"
print("no duplicates")
