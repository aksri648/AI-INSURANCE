from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch, mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable
)
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
from reportlab.platypus.flowables import Flowable
from datetime import datetime, timedelta
import random

OUTPUT = "/home/akshat/Projects/AI_INSURANCE_COPILOT/scripts/Sample_Car_Insurance_Policy.pdf"

WIDTH, HEIGHT = A4
MARGIN = 0.75 * inch

start_date = datetime(2025, 6, 1)
end_date = start_date + timedelta(days=365)
today = datetime.now()

policy_data = {
    "policy_no": "MCI-2025-47A9B2",
    "insured_name": "Rahul Sharma",
    "insured_addr": "42, Green Valley Apartments, Andheri East, Mumbai - 400093",
    "insured_dob": "15 August 1990",
    "insured_phone": "+91 98765 43210",
    "insured_email": "rahul.sharma@email.com",
    "vehicle_reg": "MH-01-XY-1234",
    "vehicle_make": "Maruti Suzuki",
    "vehicle_model": "Dzire ZXi+",
    "vehicle_year": 2024,
    "vehicle_chassis": "MA3EZKF1S004A1234",
    "vehicle_engine": "K14B-8765432",
    "vehicle_color": "Pearl Arctic White",
    "vehicle_fuel": "Petrol",
    "vehicle_cc": 1197,
    "vehicle_seating": 5,
    "coverage_type": "Comprehensive",
    "idv": 725000,
    "premium_base": 18450,
    "premium_od": 9230,
    "premium_tp": 5210,
    "premium_pa": 1050,
    "premium_zero_dep": 2950,
    "premium_windshield": 650,
    "premium_ncb": -3690,
    "premium_cess": 1476,
    "premium_gst": 3720,
    "premium_final": 27046,
    "deductible_compulsory": 1000,
    "deductible_voluntary": 2500,
    "ncb_pct": 20,
    "start_date": start_date,
    "end_date": end_date,
}
policy_data["premium_total_before_tax"] = (
    policy_data["premium_base"] + policy_data["premium_od"] + policy_data["premium_tp"]
    + policy_data["premium_pa"] + policy_data["premium_zero_dep"]
    + policy_data["premium_windshield"] + policy_data["premium_ncb"]
)
policy_data["premium_final"] = policy_data["premium_total_before_tax"] + policy_data["premium_cess"] + policy_data["premium_gst"]


styles = getSampleStyleSheet()

styles.add(ParagraphStyle(
    "TitleLarge", parent=styles["Title"], fontSize=20, spaceAfter=4, textColor=colors.HexColor("#1a237e")
))
styles.add(ParagraphStyle(
    "SubTitle", parent=styles["Normal"], fontSize=11, textColor=colors.HexColor("#555555"),
    alignment=TA_CENTER, spaceAfter=6
))
styles.add(ParagraphStyle(
    "SectionHead", parent=styles["Heading2"], fontSize=13, textColor=colors.HexColor("#1a237e"),
    spaceBefore=16, spaceAfter=6, borderPadding=(0, 0, 2, 0)
))
styles.add(ParagraphStyle(
    "CellStyle", parent=styles["Normal"], fontSize=9, leading=13
))
styles.add(ParagraphStyle(
    "CellStyleBold", parent=styles["Normal"], fontSize=9, leading=13,
    fontName="Helvetica-Bold"
))
styles.add(ParagraphStyle(
    "SmallNote", parent=styles["Normal"], fontSize=8, leading=10,
    textColor=colors.HexColor("#888888")
))
styles.add(ParagraphStyle(
    "FooterStyle", parent=styles["Normal"], fontSize=7, leading=9,
    textColor=colors.HexColor("#999999"), alignment=TA_CENTER
))


def hr():
    return HRFlowable(width="100%", thickness=1, color=colors.HexColor("#cccccc"),
                      spaceBefore=4, spaceAfter=4)


def cell(text, bold=False):
    style = "CellStyleBold" if bold else "CellStyle"
    return Paragraph(text, styles[style])


def header_row(text, cols=2):
    if cols == 2:
        return [cell(text, bold=True), cell("")]
    return [cell(text, bold=True)]


def kv_row(k, v):
    return [cell(k, bold=True), cell(v)]


def make_table(data, col_widths=None, header_rows=0):
    if col_widths is None:
        col_widths = [WIDTH - 2 * MARGIN]
    t = Table(data, colWidths=col_widths, repeatRows=header_rows)
    style_cmds = [
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cccccc")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]
    for i in range(header_rows):
        style_cmds.append(("BACKGROUND", (0, i), (-1, i), colors.HexColor("#1a237e")))
        style_cmds.append(("TEXTCOLOR", (0, i), (-1, i), colors.white))
        style_cmds.append(("FONTNAME", (0, i), (-1, i), "Helvetica-Bold"))
        style_cmds.append(("FONTSIZE", (0, i), (-1, i), 9))
    t.setStyle(TableStyle(style_cmds))
    return t


doc = SimpleDocTemplate(
    OUTPUT, pagesize=A4,
    leftMargin=MARGIN, rightMargin=MARGIN,
    topMargin=0.6 * inch, bottomMargin=0.6 * inch
)

story = []

# ── HEADER ──
story.append(Paragraph("MOTOR INSURANCE POLICY", styles["TitleLarge"]))
story.append(Paragraph("COMPREHENSIVE CAR INSURANCE - PRIVATE CAR PACKAGE POLICY", styles["SubTitle"]))
story.append(hr())
story.append(Spacer(1, 4))

story.append(Paragraph(
    f"<b>Policy Number:</b> {policy_data['policy_no']} &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
    f"<b>Issue Date:</b> {today.strftime('%d %B %Y')} &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
    f"<b>Status:</b> In Force",
    ParagraphStyle("PolicyNo", parent=styles["Normal"], fontSize=10, spaceAfter=6)
))
story.append(Spacer(1, 6))

# ── INSURED & VEHICLE DETAILS ──
cw = [WIDTH - 2 * MARGIN]
col2 = [cw[0] * 0.35, cw[0] * 0.65]

t_insured = make_table([
    [cell("<b>INSURED DETAILS</b>", bold=True), cell("")],
    kv_row("Name", policy_data["insured_name"]),
    kv_row("Address", policy_data["insured_addr"]),
    kv_row("Date of Birth", policy_data["insured_dob"]),
    kv_row("Phone", policy_data["insured_phone"]),
    kv_row("Email", policy_data["insured_email"]),
], col_widths=col2, header_rows=1)

story.append(t_insured)
story.append(Spacer(1, 8))

col3 = [cw[0] * 0.30, cw[0] * 0.40, cw[0] * 0.30]
t_vehicle = make_table([
    [cell("<b>VEHICLE DETAILS</b>", bold=True), cell(""), cell("")],
    [cell("Registration No.", bold=True), cell(policy_data["vehicle_reg"]), cell("")],
    [cell("Make / Model", bold=True), cell(f"{policy_data['vehicle_make']} {policy_data['vehicle_model']}"), cell("")],
    [cell("Year of Manufacture", bold=True), cell(str(policy_data["vehicle_year"])), cell("")],
    [cell("Chassis No.", bold=True), cell(policy_data["vehicle_chassis"]), cell("")],
    [cell("Engine No.", bold=True), cell(policy_data["vehicle_engine"]), cell("")],
    [cell("Color", bold=True), cell(policy_data["vehicle_color"]), cell("")],
    [cell("Fuel Type", bold=True), cell(policy_data["vehicle_fuel"]), cell("")],
    [cell("Engine Capacity", bold=True), cell(f"{policy_data['vehicle_cc']} cc"), cell("")],
    [cell("Seating Capacity", bold=True), cell(f"{policy_data['vehicle_seating']} Persons"), cell("")],
], col_widths=col3, header_rows=1)

story.append(t_vehicle)
story.append(Spacer(1, 8))

# ── POLICY PERIOD ──
t_period = make_table([
    [cell("<b>POLICY PERIOD</b>", bold=True), cell(""), cell("")],
    [cell("Coverage Start", bold=True), cell(start_date.strftime("%d %B %Y"), bold=False), cell("12:00 AM")],
    [cell("Coverage Expiry", bold=True), cell(end_date.strftime("%d %B %Y"), bold=False), cell("11:59 PM")],
    [cell("Policy Term", bold=True), cell("1 Year"), cell("")],
], col_widths=col3, header_rows=1)

story.append(t_period)
story.append(Spacer(1, 8))

# ── COVERAGE SCHEDULE ──
t_cov_hdr = [
    [cell("<b>Coverage</b>", bold=True), cell("<b>Limit / Sum Insured</b>", bold=True),
     cell("<b>Deductible</b>", bold=True)]
]
t_cov_data = [
    t_cov_hdr[0],
    [cell("Own Damage (OD)"), cell(f"Rs. {policy_data['idv']:,} (IDV)"), cell(f"Rs. {policy_data['deductible_compulsory']:,} Compulsory")],
    [cell("Third Party Liability"), cell("Rs. 7,50,000 per accident"), cell("As per IRDAI")],
    [cell("Personal Accident Cover"), cell(f"Rs. 1,05,000 per person"), cell("N/A")],
    [cell("Zero Depreciation Cover"), cell("Up to Rs. 7,25,000"), cell(f"Rs. {policy_data['deductible_voluntary']:,} Voluntary")],
    [cell("Windshield & Glass Cover"), cell("Up to Rs. 10,000"), cell("N/A")],
    [cell("No Claim Bonus (NCB)"), cell(f"{policy_data['ncb_pct']}% Protection"), cell("N/A")],
]
t_cov = make_table(t_cov_data, col_widths=[cw[0]*0.30, cw[0]*0.40, cw[0]*0.30], header_rows=1)
story.append(t_cov)
story.append(Spacer(1, 8))

# ── PREMIUM BREAKDOWN ──
t_prem_hdr = [["<b>Component</b>", "<b>Amount (Rs.)</b>"]]
t_prem_data = [
    t_prem_hdr[0],
    ["Base Premium (Own Damage)", f"{policy_data['premium_base']:,}"],
    ["Own Damage Cover", f"{policy_data['premium_od']:,}"],
    ["Third Party Premium", f"{policy_data['premium_tp']:,}"],
    ["Personal Accident Cover", f"{policy_data['premium_pa']:,}"],
    ["Zero Depreciation Add-on", f"{policy_data['premium_zero_dep']:,}"],
    ["Windshield & Glass Cover", f"{policy_data['premium_windshield']:,}"],
    [Paragraph("No Claim Bonus (NCB)", styles["CellStyleBold"]),
     Paragraph(f"-{abs(policy_data['premium_ncb']):,}", styles["CellStyle"])],
    [Paragraph("Subtotal (before tax)", styles["CellStyleBold"]),
     Paragraph(f"{policy_data['premium_total_before_tax']:,}", styles["CellStyle"])],
    ["Cess @ 4%", f"{policy_data['premium_cess']:,}"],
    ["GST @ 10%", f"{policy_data['premium_gst']:,}"],
    [Paragraph("<b>Total Premium</b>", styles["CellStyleBold"]),
     Paragraph(f"<b>Rs. {policy_data['premium_final']:,}</b>", styles["CellStyleBold"])],
]
t_prem = make_table(t_prem_data, col_widths=[cw[0]*0.65, cw[0]*0.35], header_rows=1)
table_style_extra = [
    ("BACKGROUND", (0, len(t_prem_data)-1), (-1, len(t_prem_data)-1), colors.HexColor("#e8eaf6")),
    ("LINEABOVE", (0, len(t_prem_data)-1), (-1, len(t_prem_data)-1), 1.5, colors.HexColor("#1a237e")),
    ("LINEBELOW", (0, len(t_prem_data)-1), (-1, len(t_prem_data)-1), 1.5, colors.HexColor("#1a237e")),
    ("LINEABOVE", (0, len(t_prem_data)-3), (-1, len(t_prem_data)-3), 0.75, colors.HexColor("#999999")),
]
t_prem.setStyle(TableStyle(table_style_extra))
story.append(t_prem)
story.append(Spacer(1, 6))

story.append(Paragraph(
    f"<i>Premium is payable in full at inception. GST and Cess are as applicable.</i>",
    styles["SmallNote"]
))
story.append(PageBreak())

# ── PAGE 2: TERMS & CONDITIONS ──
story.append(Paragraph("TERMS, CONDITIONS & EXCLUSIONS", styles["TitleLarge"]))
story.append(hr())
story.append(Spacer(1, 4))

sections = [
    ("1. GENERAL CONDITIONS", [
        "This Policy is a legal contract between the Insured and the Insurer. It is governed by the provisions of the Insurance Act, 1938, the Motor Vehicles Act, 1988, and IRDAI regulations.",
        "The Insured must disclose all material facts accurately. Non-disclosure or misrepresentation will render this Policy void ab initio.",
        "Any change in risk profile (e.g., change of vehicle use, modification of engine, transfer of ownership) must be communicated to the Insurer within 14 days.",
        "The Insured shall take all reasonable steps to maintain the Vehicle in good condition and comply with all legal requirements including valid Registration Certificate, Pollution Under Control certificate, and Driving License.",
        "The Insurer reserves the right to inspect the Vehicle at any time during the policy period.",
        "Premium once paid is non-refundable except in cases of policy cancellation within the free-look period of 15 days.",
    ]),
    ("2. COVERAGE - OWN DAMAGE (SECTION I)", [
        "The Insurer agrees to indemnify the Insured against loss or damage to the Vehicle caused by or arising out of:",
        "a) Fire, explosion, self-ignition or lightning;",
        "b) Burglary, housebreaking or theft;",
        "c) Riot and strike;",
        "d) Earthquake (fire and shock damage);",
        "e) Flood, inundation, storm, typhoon, hurricane, tornado, cyclone or other atmospheric disturbances;",
        "f) Accident by external means (collision, overturning, impact with falling objects);",
        "g) Malicious acts;",
        "h) Terrorism damage (as per reinsurance terms);",
        "i) While in transit by road, rail, inland waterway, lift, elevator or air.",
        "The liability of the Insurer shall not exceed the Insured's Declared Value (IDV) as specified in the Schedule.",
    ]),
    ("3. COVERAGE - THIRD PARTY LIABILITY (SECTION II)", [
        "The Insurer indemnifies the Insured against all sums which the Insured shall become legally liable to pay in respect of:",
        "a) Death of or bodily injury to any person (including occupants carried in the Vehicle);",
        "b) Damage to property of third parties.",
        "The maximum limit of liability for third party property damage is Rs. 7,50,000 per accident. Third party bodily injury is unlimited as per the Motor Vehicles Act.",
    ]),
    ("4. PERSONAL ACCIDENT COVER", [
        "The Insurer provides personal accident cover for the owner-driver (as named in the policy schedule):",
        "a) Death: Rs. 1,05,000;",
        "b) Permanent Total Disablement: Rs. 1,05,000;",
        "c) Loss of two limbs or sight of both eyes: 100% of sum insured;",
        "d) Loss of one limb or sight of one eye: 50% of sum insured.",
    ]),
    ("5. ADD-ON COVERS", [
        "a) <b>Zero Depreciation Cover:</b> The Insurer shall not apply depreciation on plastic, rubber, fiberglass, or metal parts while assessing claims. This cover is subject to a maximum of Rs. 50,000 per claim and voluntary deductible of Rs. 2,500.",
        "b) <b>Windshield and Glass Cover:</b> Covers replacement and repair of windscreen, window glass, sunroof glass without affecting the NCB. Limit: Rs. 10,000 per policy period.",
        "c) <b>NCB Protection:</b> The No Claim Bonus accrued is protected even if a claim is made. One claim per policy period is permitted without affecting the NCB.",
    ]),
    ("6. EXCLUSIONS", [
        "The Insurer shall not be liable for:",
        "a) Any consequential loss, depreciation, wear and tear, mechanical or electrical breakdown, failures or breakages;",
        "b) Damage to tires and tubes unless the Vehicle is damaged at the same time;",
        "c) Loss or damage arising from the Vehicle being used beyond its geographical limits;",
        "d) Loss or damage arising while the Vehicle is being used otherwise than in accordance with the limitations as to use;",
        "e) Any claim arising whilst the Insured or any person driving with the Insured's knowledge is under the influence of intoxicating liquor or drugs;",
        "f) Any claim arising whilst the Vehicle is being driven by a person not holding a valid driving license;",
        "g) Nuclear perils, war, invasion, act of foreign enemy, hostilities, civil war, rebellion, revolution, insurrection, military or usurped power;",
        "h) Loss or damage due to the Vehicle being overloaded or used for any purpose other than private use;",
        "i) Any claim where the Insured has violated any terms and conditions of the policy.",
    ]),
]

for section_title, bullets in sections:
    story.append(Paragraph(section_title, styles["SectionHead"]))
    for b in bullets:
        story.append(Paragraph(f"&bull; {b}", ParagraphStyle(
            "Bullet", parent=styles["Normal"], fontSize=9, leading=13,
            leftIndent=14, spaceAfter=3
        )))
    story.append(Spacer(1, 4))

story.append(PageBreak())

# ── PAGE 3: CLAIMS & MORE ──
story.append(Paragraph("CLAIMS PROCEDURE & ADDITIONAL INFORMATION", styles["TitleLarge"]))
story.append(hr())
story.append(Spacer(1, 4))

story.append(Paragraph("7. CLAIMS PROCEDURE", styles["SectionHead"]))
claim_steps = [
    "Immediate Notification: The Insured must notify the Insurer within 24 hours of any loss/damage via the 24x7 claims hotline or the mobile app.",
    "FIR Registration: In case of theft or third-party injury/death, register an FIR at the nearest police station within 24 hours.",
    "Survey & Inspection: An authorized surveyor will inspect the Vehicle within 48 hours of intimation. Do not repair the Vehicle before inspection.",
    "Documentation: Submit the following documents: Duly filled claim form, Copy of RC & Driving License, FIR (if applicable), Original repair bills & estimate, Photographs of the damage, Policy document copy.",
    "Cashless Repairs: Get repairs done at any of the 5,000+ network garages for cashless settlement. For non-network garages, submit bills for reimbursement.",
    "Claim Settlement Timeline: Survey report within 7 days, cashless approval within 24 hours of survey, reimbursement within 30 days of receipt of all documents.",
]
for i, step in enumerate(claim_steps, 1):
    story.append(Paragraph(
        f"<b>{i}.</b> {step}",
        ParagraphStyle("Step", parent=styles["Normal"], fontSize=9, leading=13,
                       leftIndent=14, spaceAfter=3)
    ))

story.append(Spacer(1, 8))
story.append(Paragraph("8. CLAIMS SETTLEMENT RATIO (PREVIOUS FINANCIAL YEAR)", styles["SectionHead"]))

claims_table_data = [
    [cell("<b>Metric</b>", bold=True), cell("<b>Value</b>", bold=True)],
    [cell("Total Claims Reported"), cell("1,24,873")],
    [cell("Claims Settled"), cell("1,18,629")],
    [cell("Claims Repudiated"), cell("4,102")],
    [cell("Claims Pending"), cell("2,142")],
    [cell("Claim Settlement Ratio"), cell("<b>95.0%</b>")],
    [cell("Average Settlement Time"), cell("12.4 days")],
    [cell("Cashless Claims %"), cell("78.3%")],
    [cell("Network Garages"), cell("5,247")],
]
t_claims = make_table(claims_table_data, col_widths=[cw[0]*0.50, cw[0]*0.50], header_rows=1)
story.append(t_claims)
story.append(Spacer(1, 8))

story.append(Paragraph("9. PREMIUM COMPARISON FOR RENEWAL", styles["SectionHead"]))
renewal_data = [
    [cell("<b>Year</b>", bold=True), cell("<b>NCB</b>", bold=True), cell("<b>Base Premium</b>", bold=True),
     cell("<b>Estimated Total</b>", bold=True)],
    [cell("Year 1 (Current)"), cell("0%"), cell("Rs. 18,450"), cell("Rs. 27,046")],
    [cell("Year 2 (Renewal)"), cell("20%"), cell("Rs. 14,760"), cell("Rs. 22,760")],
    [cell("Year 3"), cell("25%"), cell("Rs. 13,838"), cell("Rs. 21,450")],
    [cell("Year 4"), cell("35%"), cell("Rs. 11,993"), cell("Rs. 18,990")],
    [cell("Year 5"), cell("50%"), cell("Rs. 9,225"), cell("Rs. 15,520")],
]
t_renewal = make_table(renewal_data, col_widths=[cw[0]*0.18, cw[0]*0.14, cw[0]*0.32, cw[0]*0.36], header_rows=1)
story.append(t_renewal)
story.append(Spacer(1, 8))

story.append(Paragraph("10. IMPORTANT NOTES", styles["SectionHead"]))
notes = [
    "The IDV (Insured's Declared Value) is calculated based on the manufacturer's listed selling price less depreciation as per IRDAI tariff.",
    "Geographical limits: The policy covers the vehicle within the boundaries of India (excluding the State of Jammu & Kashmir for certain perils).",
    "The policy can be cancelled by the Insured at any time, and a refund of premium on short-period scale will be given.",
    "The Insurer may cancel the policy by sending 7 days notice by recorded delivery to the Insured's last known address, in which case a refund on the pro-rata basis will be given.",
    "Any dispute arising under this policy shall be subject to the jurisdiction of Indian courts only.",
    "In case of any grievance, contact the Grievance Redressal Officer at grievance@insurer.com or call 1800-XXX-XXXX. You may also approach the Insurance Ombudsman as per IRDAI guidelines.",
]
for note in notes:
    story.append(Paragraph(f"&bull; {note}", ParagraphStyle(
        "Note", parent=styles["Normal"], fontSize=9, leading=13,
        leftIndent=14, spaceAfter=3
    )))

story.append(Spacer(1, 16))
story.append(hr())
story.append(Spacer(1, 6))

# ── SIGNATURE SECTION ──
sig_data = [
    [Paragraph("<b>Authorized Signatory</b>", styles["CellStyleBold"]),
     Paragraph("<b>Policy Holder</b>", styles["CellStyleBold"])],
    [Spacer(1, 30), Spacer(1, 30)],
    [Paragraph("_________________________", styles["CellStyle"]),
     Paragraph("_________________________", styles["CellStyle"])],
    [Paragraph("Name: S. Mehta", styles["CellStyle"]),
     Paragraph(f"Name: {policy_data['insured_name']}", styles["CellStyle"])],
    [Paragraph("Designation: Manager - Underwriting", styles["CellStyle"]),
     Paragraph(f"Date: {today.strftime('%d %B %Y')}", styles["CellStyle"])],
]
t_sig = Table(sig_data, colWidths=[cw[0]*0.5, cw[0]*0.5])
t_sig.setStyle(TableStyle([
    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
    ("VALIGN", (0, 0), (-1, -1), "BOTTOM"),
    ("FONTSIZE", (0, 0), (-1, -1), 9),
    ("TOPPADDING", (0, 0), (-1, -1), 2),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
]))
story.append(t_sig)

story.append(Spacer(1, 10))
story.append(Paragraph(
    "This is a computer-generated sample policy document for demonstration purposes only. "
    "It is not a valid insurance contract and does not confer any coverage or benefits.",
    ParagraphStyle("Disclaimer", parent=styles["Normal"], fontSize=8, leading=10,
                   textColor=colors.HexColor("#ff0000"), alignment=TA_CENTER,
                   spaceBefore=8)
))

doc.build(story)
print(f"PDF generated: {OUTPUT}")
