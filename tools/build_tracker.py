#!/usr/bin/env python3
"""
Build the Partner Direct tracker workbook.

Every tab, column and target here comes from Cristian's own documents:
  - Partner Direct Launch Kit (30-day plan, tiers, templates, weekly rhythm)
  - Six Rules for Getting to $10K (rules 02, 03, 05)
  - Partner Direct Meeting Notes (section 6 targeting, section 9 next steps)

Usage: python3 tools/build_tracker.py [output.xlsx]
"""

import sys
from datetime import date
from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

OUT = sys.argv[1] if len(sys.argv) > 1 else "tracker/Partner-Direct-Tracker-TEMPLATE.xlsx"

FONT = "Arial"
INK = "1A1A1A"
MUTED = "6B6B6B"
ACCENT = "1F4E79"          # header bands
ACCENT_FILL = "1F4E79"
INPUT_FILL = "FFF2CC"      # yellow = you fill this
CALC_FILL = "EDF3F8"       # computed
EXAMPLE_FILL = "F2F2F2"

thin = Side(style="thin", color="D0D0D0")
BORDER = Border(left=thin, right=thin, top=thin, bottom=thin)

# Tier and segment vocabularies — keep in sync with the dropdowns below.
TIERS = ["1 - Would pick up at 10pm",
         "2 - Warm, business unknown",
         "3 - Confirmed business, cooler",
         "4 - Harvested referral"]
SEGMENTS = ["Authorize.net", "E-commerce", "B2B", "Retail",
            "Restaurant/Bar/Lounge", "Vendor", "Unknown"]
STATUSES = ["Not contacted", "Contacted - no answer", "Conversation had",
            "Referred to Jeremy", "Closed won", "No"]
OUTCOMES = ["Conversation", "No answer", "Left voicemail",
            "Not interested", "Wrong timing"]
JEREMY = ["Sent", "Jeremy contacted", "In progress",
          "Closed won", "Closed lost", "No response"]
SOURCES = ["Warm list", "Tier 4 referral", "Referral partner",
           "Inbound - page", "Inbound - social", "Event"]
PARTNER_TYPES = ["Business broker", "POS installer", "Bookkeeper / CPA",
                 "Liquor / food rep", "Consultant", "Commercial broker / landlord",
                 "Route vendor (linen, uniform, waste, pest)", "Other"]
PARTNER_STATUS = ["Not contacted", "Contacted", "Agreed to refer",
                  "Active - has sent one", "Cold"]
YN = ["Y", "N"]


def style_header(ws, row, headers, widths):
    for i, (h, w) in enumerate(zip(headers, widths), start=1):
        c = ws.cell(row=row, column=i, value=h)
        c.font = Font(name=FONT, size=10, bold=True, color="FFFFFF")
        c.fill = PatternFill("solid", fgColor=ACCENT_FILL)
        c.alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
        c.border = BORDER
        ws.column_dimensions[get_column_letter(i)].width = w
    ws.row_dimensions[row].height = 30
    ws.freeze_panes = ws.cell(row=row + 1, column=1)


def note(ws, cell, text, size=9, italic=True, color=MUTED, bold=False):
    c = ws[cell]
    c.value = text
    c.font = Font(name=FONT, size=size, italic=italic, bold=bold, color=color)
    c.alignment = Alignment(vertical="top", wrap_text=True)
    return c


def add_dv(ws, formula_list, col, first=3, last=400):
    dv = DataValidation(type="list", formula1='"' + ",".join(formula_list) + '"',
                        allow_blank=True, showDropDown=False)
    ws.add_data_validation(dv)
    dv.add(f"{col}{first}:{col}{last}")


def example_row(ws, row, values):
    for i, v in enumerate(values, start=1):
        c = ws.cell(row=row, column=i, value=v)
        c.font = Font(name=FONT, size=9, italic=True, color=MUTED)
        c.fill = PatternFill("solid", fgColor=EXAMPLE_FILL)
        c.border = BORDER
        c.alignment = Alignment(vertical="top", wrap_text=True)


wb = Workbook()

# ---------------------------------------------------------------- Start Here
ws = wb.active
ws.title = "Start Here"
ws.sheet_view.showGridLines = False
ws.column_dimensions["A"].width = 3
ws.column_dimensions["B"].width = 96

r = 2
t = ws.cell(row=r, column=2, value="Partner Direct — Tracker")
t.font = Font(name=FONT, size=20, bold=True, color=ACCENT)
r += 1
note(ws, f"B{r}", "The log is the job. Everything else follows from it.", size=11)
r += 2

SECTIONS = [
    ("How this workbook is used", [
        "Reconnect Sprint — every person you know who owns or runs something that takes cards.",
        "    Rule 02 says you are probably sitting on 150-300 names. Fill it in one sitting, before you call anyone.",
        "Call Log — every conversation, logged the same day. Week one has no exceptions; the habit is the point.",
        "Referral Log — every handoff to Jeremy, including the ones that die. Rule 05: track your no's like they're wins.",
        "Objections — what you actually hear. Review with Jeremy weekly and find the two you keep hitting.",
        "Referral Partners — people who already walk into businesses you cannot reach. Give before you ask.",
        "Dashboard — targets vs. actual, pulled automatically from the logs. Set your Week 1 start date there.",
    ]),
    ("Colour key", [
        "Yellow cells are yours to fill in.",
        "Blue-grey cells are calculated — don't type over them.",
        "Grey italic rows are examples showing the expected format. Delete them once you start.",
    ]),
    ("The line", [
        '"I have a guy who was a client at LIV, he\'s in payment processing. There\'s a new program called',
        'Partner Direct — they partner customers directly with the processor, cutting out the middleman',
        'cost, and rates start at three cents."',
        "",
        "Then stop talking.",
        "",
        "Technical question comes back? \"I don't know that. Let me introduce you to Jeremy Schauffer.\"",
    ]),
    ("The question that compounds — ask it every time, including the no's", [
        '"Who else do you know that takes cards?"',
        "",
        "Log the answer in the Call Log 'Names harvested' column. If Tier 4 stays empty, you aren't asking it.",
    ]),
    ("The handoff — same day, every time", [
        "To Jeremy:   Referral: [Name], [Business], [phone]. [One line on how you know them and what they're running.]",
        "",
        "To the merchant:   [Name] — sent your info to Jeremy, he'll reach out in the next day or two.",
        "                   He's the one who actually knows this stuff. Any issues, tell me.",
        "",
        "The second text is the part most people skip. It's what makes the introduction land.",
    ]),
    ("Priority order (Meeting Notes §6, Rule 03)", [
        "Slam dunk   Authorize.net users — APS is one of only 11 processors directly integrated.",
        "Strong      E-commerce, and B2B (level 2/3 interchange optimization is a real edge).",
        "Good        Retail. Square and Clover users are worth asking.",
        "Hardest     Restaurants, bars, lounges. Great if landed; resistance is about the solution, not the rate.",
        "",
        "Do not filter. Anyone who processes cards goes to Jeremy. The no's are the training.",
    ]),
    ("Don't", [
        "Don't research gateways and interchange to prepare. Rule 01: knowing too much too fast is the failure mode.",
        "Don't post rate numbers or the processor's name before Clay and Jeremy approve.",
        "Don't screenshot residual income. Ever.",
        "Don't chase. One follow-up — \"Did Jeremy ever get you?\" — then let it go.",
    ]),
]

for title, lines in SECTIONS:
    c = ws.cell(row=r, column=2, value=title)
    c.font = Font(name=FONT, size=12, bold=True, color=ACCENT)
    r += 1
    for line in lines:
        c = ws.cell(row=r, column=2, value=line)
        c.font = Font(name=FONT, size=10, color=INK)
        c.alignment = Alignment(vertical="top", wrap_text=False)
        r += 1
    r += 1

# ---------------------------------------------------- Reconnect Sprint
ws = wb.create_sheet("Reconnect Sprint")
note(ws, "A1", "Every person you know who owns or runs something that takes cards. "
               "Rule 02: 150-300 names, built before you make a single call. "
               "Column F fills itself from the Segment you pick.", size=10, bold=True, color=ACCENT)
ws.merge_cells("A1:O1")
ws.row_dimensions[1].height = 28

hdrs = ["Name", "Business", "Their role", "Tier", "Segment", "Priority",
        "How I know them", "Phone", "IG / LinkedIn", "Website",
        "What they run (ask, don't research)", "Status", "Last contact",
        "Next action", "Notes"]
widths = [20, 24, 16, 24, 20, 16, 26, 15, 20, 24, 26, 20, 13, 24, 32]
style_header(ws, 2, hdrs, widths)

example_row(ws, 3, ["Marco Ruiz", "Ruiz Hospitality Group", "Owner",
                    TIERS[0], "Restaurant/Bar/Lounge", "", "LIV regular, 4 years",
                    "305-555-0142", "@marcoruiz", "ruizhg.com", "",
                    "Not contacted", "", "Call week 1", "Two venues in Wynwood"])

for row in range(3, 401):
    ws[f"F{row}"] = (
        f'=IF(E{row}="","",'
        f'IF(E{row}="Authorize.net","1 - Slam dunk",'
        f'IF(OR(E{row}="E-commerce",E{row}="B2B",E{row}="Vendor"),"2 - Strong",'
        f'IF(E{row}="Retail","3 - Good",'
        f'IF(E{row}="Restaurant/Bar/Lounge","4 - Hardest","5 - Unknown")))))'
    )
    ws[f"F{row}"].fill = PatternFill("solid", fgColor=CALC_FILL)
    ws[f"F{row}"].font = Font(name=FONT, size=10, color=INK)
    for col in "ABCDEGHIJKLMNO":
        c = ws[f"{col}{row}"]
        c.font = Font(name=FONT, size=10, color=INK)
        if row > 3:
            c.fill = PatternFill("solid", fgColor=INPUT_FILL)
    ws[f"M{row}"].number_format = "mm/dd/yyyy"

add_dv(ws, TIERS, "D")
add_dv(ws, SEGMENTS, "E")
add_dv(ws, STATUSES, "L")

# ------------------------------------------------------------- Call Log
ws = wb.create_sheet("Call Log")
note(ws, "A1", "Every conversation, logged the same day. Week one has no exceptions — the habit is the whole point.",
     size=10, bold=True, color=ACCENT)
ws.merge_cells("A1:I1")

hdrs = ["Date", "Name", "Tier", "Channel", "Outcome",
        "Asked the referral question?", "Names harvested",
        "Referred to Jeremy?", "Notes"]
widths = [12, 22, 24, 14, 18, 22, 16, 18, 44]
style_header(ws, 2, hdrs, widths)
example_row(ws, 3, [date(2026, 9, 15), "Marco Ruiz", TIERS[0], "Call", "Conversation",
                    "Y", 2, "Y", "On Toast, annoyed about the exit clause. Gave me two names."])

for row in range(3, 601):
    for col in "ABCDEFGHI":
        c = ws[f"{col}{row}"]
        c.font = Font(name=FONT, size=10, color=INK)
        if row > 3:
            c.fill = PatternFill("solid", fgColor=INPUT_FILL)
    ws[f"A{row}"].number_format = "mm/dd/yyyy"

add_dv(ws, TIERS, "C", last=600)
add_dv(ws, ["Call", "Text", "DM", "In person", "Event"], "D", last=600)
add_dv(ws, OUTCOMES, "E", last=600)
add_dv(ws, YN, "F", last=600)
add_dv(ws, YN, "H", last=600)

# --------------------------------------------------------- Referral Log
ws = wb.create_sheet("Referral Log")
note(ws, "A1", "Every handoff to Jeremy, including the ones that die. Rule 05: track your no's like they're wins. "
               "Bring this to the Friday call.", size=10, bold=True, color=ACCENT)
ws.merge_cells("A1:J1")

hdrs = ["Date sent", "Source", "Sourced by", "Name", "Business", "Phone",
        "What they're running", "Sent merchant the heads-up text?", "Jeremy status",
        "Why it didn't work", "Date closed", "Notes"]
widths = [12, 18, 20, 20, 24, 15, 24, 26, 18, 32, 12, 28]
style_header(ws, 2, hdrs, widths)
example_row(ws, 3, [date(2026, 9, 15), "Referral partner", "Dani (Breakthru liquor rep)",
                    "Marco Ruiz", "Ruiz Hospitality Group", "305-555-0142",
                    "Toast", "Y", "Jeremy contacted", "", "",
                    "Wants to wait for contract end in March"])

for row in range(3, 401):
    for col in "ABCDEFGHIJKL":
        c = ws[f"{col}{row}"]
        c.font = Font(name=FONT, size=10, color=INK)
        if row > 3:
            c.fill = PatternFill("solid", fgColor=INPUT_FILL)
    ws[f"A{row}"].number_format = "mm/dd/yyyy"
    ws[f"K{row}"].number_format = "mm/dd/yyyy"

add_dv(ws, SOURCES, "B")
add_dv(ws, YN, "H")
add_dv(ws, JEREMY, "I")

# ----------------------------------------------------------- Objections
ws = wb.create_sheet("Objections")
note(ws, "A1", "What you actually hear. Review with Jeremy weekly and find the two you keep hitting. "
               "Column F counts how many times the same objection text appears.",
     size=10, bold=True, color=ACCENT)
ws.merge_cells("A1:F1")

hdrs = ["Date", "Business", "Segment", "Objection heard", "Jeremy's answer", "Times heard"]
widths = [12, 24, 22, 44, 48, 13]
style_header(ws, 2, hdrs, widths)
example_row(ws, 3, [date(2026, 9, 16), "Ruiz Hospitality Group", "Restaurant/Bar/Lounge",
                    "Locked into Toast, switching is too disruptive",
                    "Ask what the exit clause looks like and revisit 60 days out", ""])

for row in range(3, 301):
    ws[f"F{row}"] = f'=IF(D{row}="","",COUNTIF($D$3:$D$300,D{row}))'
    ws[f"F{row}"].fill = PatternFill("solid", fgColor=CALC_FILL)
    ws[f"F{row}"].font = Font(name=FONT, size=10, color=INK)
    for col in "ABCDE":
        c = ws[f"{col}{row}"]
        c.font = Font(name=FONT, size=10, color=INK)
        if row > 3:
            c.fill = PatternFill("solid", fgColor=INPUT_FILL)
    ws[f"A{row}"].number_format = "mm/dd/yyyy"

add_dv(ws, SEGMENTS, "C", last=300)

# --------------------------------------------------- Referral Partners
ws = wb.create_sheet("Referral Partners")
note(ws, "A1", "People who already walk into the businesses you cannot reach. One liquor rep touches "
               "15 accounts a week. Give before you ask - column K is the discipline, not a nicety. "
               "Priority fills itself from Type.",
     size=10, bold=True, color=ACCENT)
ws.merge_cells("A1:N1")
ws.row_dimensions[1].height = 28

hdrs = ["Partner name", "Type", "Priority", "Company", "How I know them",
        "Phone", "Email", "Accounts they touch", "Status", "Last contact",
        "Last thing I gave them", "Date I gave it", "Referrals received", "Notes"]
widths = [20, 26, 14, 22, 24, 15, 22, 16, 20, 13, 28, 13, 15, 28]
style_header(ws, 2, hdrs, widths)

example_row(ws, 3, ["Dani Restrepo", "Liquor / food rep", "", "Breakthru Beverage",
                    "Comped her table at LIV for years", "305-555-0178",
                    "dani@example.com", "15/wk", "Agreed to refer", "",
                    "Sent her Marco's number for a tasting", "", "",
                    "Asked her to flag any spot changing hands"])

for row in range(3, 201):
    # Priority ranks by how close the partner sits to a moment a merchant re-decides.
    ws["C%d" % row] = (
        '=IF(B{r}="","",'
        'IF(B{r}="Business broker","1 - Highest",'
        'IF(OR(B{r}="POS installer",B{r}="Bookkeeper / CPA"),"2 - High",'
        'IF(OR(B{r}="Liquor / food rep",B{r}="Consultant"),"3 - Strong",'
        'IF(B{r}="Other","5 - Other","4 - Good")))))'
    ).format(r=row)
    ws["M%d" % row] = (
        '=IF(A{r}="","",COUNTIF(\'Referral Log\'!$C$4:$C$400,A{r}))'
    ).format(r=row)
    for col in ("C", "M"):
        ws["%s%d" % (col, row)].fill = PatternFill("solid", fgColor=CALC_FILL)
        ws["%s%d" % (col, row)].font = Font(name=FONT, size=10, color=INK)
    for col in "ABDEFGHIJKLN":
        c = ws["%s%d" % (col, row)]
        c.font = Font(name=FONT, size=10, color=INK)
        if row > 3:
            c.fill = PatternFill("solid", fgColor=INPUT_FILL)
    ws["J%d" % row].number_format = "mm/dd/yyyy"
    ws["L%d" % row].number_format = "mm/dd/yyyy"

add_dv(ws, PARTNER_TYPES, "B", last=200)
add_dv(ws, PARTNER_STATUS, "I", last=200)

# ------------------------------------------------------------ Dashboard
ws = wb.create_sheet("Dashboard")
ws.sheet_view.showGridLines = False
for col, w in zip("ABCDEFGHIJ", [3, 20, 12, 12, 14, 12, 12, 12, 14, 12]):
    ws.column_dimensions[col].width = w

c = ws["B2"]; c.value = "Dashboard"
c.font = Font(name=FONT, size=18, bold=True, color=ACCENT)

note(ws, "B4", "Week 1 start (Monday):", size=10, italic=False, bold=True, color=INK)
ws["D4"] = None
ws["D4"].fill = PatternFill("solid", fgColor=INPUT_FILL)
ws["D4"].number_format = "mm/dd/yyyy"
ws["D4"].border = BORDER
ws["D4"].font = Font(name=FONT, size=10, bold=True, color="0000FF")
note(ws, "E4", "← set this first; every week below is calculated from it", size=9)

hdrs = ["", "Week", "Start", "End", "Convos tgt", "Convos", "Refs tgt", "Refs",
        "Names tgt", "Names"]
style_header(ws, 6, hdrs, [3, 20, 12, 12, 14, 12, 12, 12, 14, 12])

# Targets straight from the Launch Kit. Week 3 and 4 state no names target.
TARGETS = [("Week 1 — Build", 12, 3, 5),
           ("Week 2 — Widen", 20, 5, 10),
           ("Week 3 — Vendors", 20, 5, None),
           ("Week 4 — Compound", 20, 7, None)]

for i, (label, ct, rt, nt) in enumerate(TARGETS):
    row = 7 + i
    ws[f"B{row}"] = label
    ws[f"C{row}"] = f"=IF($D$4=\"\",\"\",$D$4+{i * 7})"
    ws[f"D{row}"] = f"=IF($D$4=\"\",\"\",$D$4+{i * 7 + 6})"
    ws[f"E{row}"] = ct
    ws[f"F{row}"] = (f"=IF($D$4=\"\",\"\",COUNTIFS('Call Log'!$A$4:$A$600,\">=\"&$C{row},"
                     f"'Call Log'!$A$4:$A$600,\"<=\"&$D{row},"
                     f"'Call Log'!$E$4:$E$600,\"Conversation\"))")
    ws[f"G{row}"] = rt
    ws[f"H{row}"] = (f"=IF($D$4=\"\",\"\",COUNTIFS('Referral Log'!$A$4:$A$400,\">=\"&$C{row},"
                     f"'Referral Log'!$A$4:$A$400,\"<=\"&$D{row}))")
    ws[f"I{row}"] = nt if nt is not None else "—"
    ws[f"J{row}"] = (f"=IF($D$4=\"\",\"\",SUMIFS('Call Log'!$G$4:$G$600,"
                     f"'Call Log'!$A$4:$A$600,\">=\"&$C{row},"
                     f"'Call Log'!$A$4:$A$600,\"<=\"&$D{row}))")
    for col in "BCDEFGHIJ":
        cell = ws[f"{col}{row}"]
        cell.font = Font(name=FONT, size=10, color=INK)
        cell.border = BORDER
        if col in "CDFHJ":
            cell.fill = PatternFill("solid", fgColor=CALC_FILL)
    ws[f"C{row}"].number_format = "mm/dd/yyyy"
    ws[f"D{row}"].number_format = "mm/dd/yyyy"

# Month 1 summary
r = 13
c = ws[f"B{r}"]; c.value = "Month 1"
c.font = Font(name=FONT, size=13, bold=True, color=ACCENT)
r += 1
SUMMARY = [
    ("Conversations", "=SUM(F7:F10)", "60-70 is a good month"),
    ("Referrals sent", "=SUM(H7:H10)", "18-20"),
    ("Accounts closed", "=COUNTIF('Referral Log'!$I$4:$I$400,\"Closed won\")", "2-4"),
    ("Names harvested", "=SUM(J7:J10)", "feeds Tier 4"),
    ("Tier 4 names on list", "=COUNTIF('Reconnect Sprint'!$D$4:$D$400,\"4 - Harvested referral\")",
     "if this stays 0, you aren't asking the referral question"),
    ("Referral question asked", "=IF(COUNTIF('Call Log'!$F$4:$F$600,\"Y\")+COUNTIF('Call Log'!$F$4:$F$600,\"N\")=0,"
                                "\"\",COUNTIF('Call Log'!$F$4:$F$600,\"Y\")/"
                                "(COUNTIF('Call Log'!$F$4:$F$600,\"Y\")+COUNTIF('Call Log'!$F$4:$F$600,\"N\")))",
     "aim for 100%"),
    ("Active referral partners",
     "=COUNTIF('Referral Partners'!$I$4:$I$200,\"Active - has sent one\")",
     "people who have actually sent you someone"),
    ("From outside the warm list",
     "=IF(COUNTA('Referral Log'!$B$4:$B$400)=0,\"\","
     "COUNTIFS('Referral Log'!$B$4:$B$400,\"<>Warm list\","
     "'Referral Log'!$B$4:$B$400,\"<>\")/COUNTA('Referral Log'!$B$4:$B$400))",
     "zero in month one is fine; still zero at month four means nothing replaced the list"),
]
for label, formula, hint in SUMMARY:
    ws[f"B{r}"] = label
    ws[f"B{r}"].font = Font(name=FONT, size=10, color=INK)
    cell = ws[f"D{r}"]
    cell.value = formula
    cell.font = Font(name=FONT, size=10, bold=True, color=INK)
    cell.fill = PatternFill("solid", fgColor=CALC_FILL)
    cell.border = BORDER
    cell.alignment = Alignment(horizontal="center")
    if label in ("Referral question asked", "From outside the warm list"):
        cell.number_format = "0%"
    note(ws, f"E{r}", hint, size=9)
    r += 1

r += 1
note(ws, f"B{r}", "Judge month one against the range above, not against $10k. "
                  "Clay's first residual was $32.62; Jeremy's was $100.", size=10)

wb.save(OUT)
print(f"wrote {OUT}")
