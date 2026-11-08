import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

doc = docx.Document()

# 1. Page Setup - A4 with 1-inch margins
sec = doc.sections[0]
sec.page_width = Inches(8.27)
sec.page_height = Inches(11.69)
sec.top_margin = Inches(1.0)
sec.bottom_margin = Inches(1.0)
sec.left_margin = Inches(1.0)
sec.right_margin = Inches(1.0)

# Colors
C_NAVY = RGBColor(0x1A, 0x36, 0x8A)      # College Header (#1A368A)
C_DARK = RGBColor(0x1E, 0x29, 0x3B)      # Primary Dark Text (#1E293B)
C_MUTED = RGBColor(0x64, 0x74, 0x8B)     # Muted Slate (#64748B)
C_CAPTION = RGBColor(0x47, 0x55, 0x69)   # Captions (#475569)

# Helper styling functions
def style_run(run, font_name="Cambria", size_pt=11.5, bold=False, italic=False, color=C_DARK):
    run.font.name = font_name
    run.font.size = Pt(size_pt)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = color

def add_p(text="", align=WD_ALIGN_PARAGRAPH.LEFT, space_before=0, space_after=6, line_spacing=1.15):
    p = doc.add_paragraph()
    p.alignment = align
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = line_spacing
    if text:
        r = p.add_run(text)
        style_run(r, size_pt=11.5, color=C_DARK)
    return p

def add_heading_1(title):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(8)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(title)
    style_run(r, size_pt=24, bold=True, color=C_DARK)
    return p

def add_heading_2(subtitle):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(subtitle)
    style_run(r, size_pt=15, bold=True, color=C_DARK)
    return p

def add_heading_3(subtitle):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(subtitle)
    style_run(r, size_pt=12.5, bold=True, color=C_DARK)
    return p

def add_bullet(text, bold_prefix="", space_after=4):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.25)
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.15
    
    r_sym = p.add_run("• ")
    style_run(r_sym, size_pt=11.5, bold=True, color=C_NAVY)
    
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        style_run(r_pre, size_pt=11.5, bold=True, color=C_DARK)
    
    r_txt = p.add_run(text)
    style_run(r_txt, size_pt=11.5, color=C_DARK)
    return p

def add_figure(img_path, caption, width_in=5.5):
    if os.path.exists(img_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(8)
        p_img.paragraph_format.space_after = Pt(4)
        r_img = p_img.add_run()
        r_img.add_picture(img_path, width=Inches(width_in))
        
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_before = Pt(2)
        p_cap.paragraph_format.space_after = Pt(10)
        r_cap = p_cap.add_run(caption)
        style_run(r_cap, size_pt=10.5, bold=True, italic=True, color=C_CAPTION)
    else:
        print("Warning: image not found:", img_path)

def set_table_borders(table):
    tblPr = table._tbl.tblPr
    borders_xml = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'  <w:top w:val="single" w:sz="6" w:space="0" w:color="CBD5E1"/>'
        f'  <w:bottom w:val="single" w:sz="8" w:space="0" w:color="94A3B8"/>'
        f'  <w:insideH w:val="single" w:sz="4" w:space="0" w:color="E2E8F0"/>'
        f'  <w:insideV w:val="none"/>'
        f'  <w:left w:val="none"/>'
        f'  <w:right w:val="none"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders_xml)

def set_cell_shading(cell, fill_hex="F1F5F9"):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def add_page_break():
    doc.add_page_break()

# Setup Header and Footer
def setup_header_footer():
    # Header
    hdr = sec.header
    p_hdr = hdr.paragraphs[0]
    p_hdr.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_hdr.paragraph_format.space_after = Pt(0)
    r_hdr = p_hdr.add_run("Personal Finance & Expense Tracker (FinTrack) - MERN Stack")
    style_run(r_hdr, size_pt=9.5, italic=True, color=C_MUTED)
    
    # Footer
    ftr = sec.footer
    p_ftr = ftr.paragraphs[0]
    p_ftr.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_ftr.paragraph_format.space_after = Pt(0)
    
    r_f1 = p_ftr.add_run("Enrollment No: 35   |   Page ")
    style_run(r_f1, size_pt=10, color=C_MUTED)
    
    # Page Field
    fld1 = OxmlElement('w:fldSimple')
    fld1.set(qn('w:instr'), 'PAGE')
    p_ftr._p.append(fld1)
    
    r_f2 = p_ftr.add_run(" of ")
    style_run(r_f2, size_pt=10, color=C_MUTED)
    
    # NumPages Field
    fld2 = OxmlElement('w:fldSimple')
    fld2.set(qn('w:instr'), 'NUMPAGES')
    p_ftr._p.append(fld2)

setup_header_footer()

sc_dir = r"c:\Users\Asus\Desktop\Project\documentation\screenshots"
logo_path = os.path.join(sc_dir, "naran_lala_logo.png")

print("Building Document Content...")

# ==============================================================================
# 1. TITLE / COVER PAGE
# ==============================================================================
p = add_p("NARAN LALA COLLEGE", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=12, space_after=2)
p.runs[0].font.size = Pt(22)
p.runs[0].font.bold = True
p.runs[0].font.color.rgb = C_NAVY

p = add_p("OF PROFESSIONAL & APPLIED SCIENCES", align=WD_ALIGN_PARAGRAPH.CENTER, space_after=2)
p.runs[0].font.size = Pt(17)
p.runs[0].font.bold = True
p.runs[0].font.color.rgb = C_NAVY

p = add_p("NAVSARI", align=WD_ALIGN_PARAGRAPH.CENTER, space_after=14)
p.runs[0].font.size = Pt(16)
p.runs[0].font.bold = True
p.runs[0].font.color.rgb = C_NAVY

# Logo
if os.path.exists(logo_path):
    p_logo = doc.add_paragraph()
    p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_logo.paragraph_format.space_before = Pt(4)
    p_logo.paragraph_format.space_after = Pt(14)
    r_logo = p_logo.add_run()
    r_logo.add_picture(logo_path, width=Inches(1.75))

p = add_p("Course: Bachelor of Computer Applications (BCA)", align=WD_ALIGN_PARAGRAPH.CENTER, space_after=6)
p.runs[0].font.size = Pt(13.5)
p.runs[0].font.bold = True

p = add_p("MINOR PROJECT REPORT", align=WD_ALIGN_PARAGRAPH.CENTER, space_after=8)
p.runs[0].font.size = Pt(15)
p.runs[0].font.bold = True
p.runs[0].font.color.rgb = C_NAVY

p = add_p("PROJECT TITLE: PERSONAL FINANCE & EXPENSE TRACKER (FINTRACK)", align=WD_ALIGN_PARAGRAPH.CENTER, space_after=6)
p.runs[0].font.size = Pt(13)
p.runs[0].font.bold = True

p = add_p("SUBJECT NAME: ADVANCED WEB DESIGNING", align=WD_ALIGN_PARAGRAPH.CENTER, space_after=20)
p.runs[0].font.size = Pt(12)
p.runs[0].font.bold = True

# Student, Guide, Principal info
p = add_p("Submitted By:", align=WD_ALIGN_PARAGRAPH.CENTER, space_after=2)
p.runs[0].font.size = Pt(11.5)
p.runs[0].font.bold = True

p = add_p("Chauhan Om S.\nRoll No.: 35", align=WD_ALIGN_PARAGRAPH.CENTER, space_after=14)
p.runs[0].font.size = Pt(11.5)

p = add_p("Project Guide:", align=WD_ALIGN_PARAGRAPH.CENTER, space_after=2)
p.runs[0].font.size = Pt(11.5)
p.runs[0].font.bold = True

p = add_p("Ms. Ayushi Mistry", align=WD_ALIGN_PARAGRAPH.CENTER, space_after=14)
p.runs[0].font.size = Pt(11.5)

p = add_p("Principal:", align=WD_ALIGN_PARAGRAPH.CENTER, space_after=2)
p.runs[0].font.size = Pt(11.5)
p.runs[0].font.bold = True

p = add_p("Dr. Sunil Naik", align=WD_ALIGN_PARAGRAPH.CENTER, space_after=10)
p.runs[0].font.size = Pt(11.5)

p = add_p("Academic Year: 2025 - 2026", align=WD_ALIGN_PARAGRAPH.CENTER, space_after=0)
p.runs[0].font.size = Pt(11)
p.runs[0].font.italic = True
p.runs[0].font.color.rgb = C_MUTED

add_page_break()

# ==============================================================================
# 2. DECLARATION & ACKNOWLEDGEMENT
# ==============================================================================
p_dec_title = add_p("➢ DECLARATION:", space_before=6, space_after=8)
p_dec_title.runs[0].font.size = Pt(14)
p_dec_title.runs[0].font.bold = True

add_p(
    "I/We hereby declare that the Minor Project titled “Personal Finance & Expense Tracker (FinTrack)” "
    "submitted in partial fulfillment of the requirements for the Bachelor of Computer Applications (BCA) "
    "is an original work carried out by me/us under the guidance and supervision of Ms. Ayushi Mistry. "
    "I/We further declare that this project work has not been submitted previously to any other university, "
    "college, or institution for the award of any degree, diploma, or certificate. "
    "The information, data, and references used in this project have been collected from reliable sources and "
    "have been appropriately acknowledged wherever required. I/We take full responsibility for the originality "
    "and authenticity of the work presented in this project report.",
    space_after=12
)

add_p("Date: __________________", space_after=4).runs[0].font.bold = True
add_p("Student Exam No. & Name:", space_after=2).runs[0].font.bold = True
add_p("1. Roll No. 35 — Chauhan Om S.", space_after=8)
add_p("Signature:", space_after=4).runs[0].font.bold = True
add_p("1. __________________________________________________", space_after=18)

p_ack_title = add_p("➢ ACKNOWLEDGEMENT:", space_before=12, space_after=8)
p_ack_title.runs[0].font.size = Pt(14)
p_ack_title.runs[0].font.bold = True

add_p(
    "We would like to express our sincere gratitude to everyone who has supported and guided us in successfully "
    "completing our BCA Minor Project titled “Personal Finance & Expense Tracker (FinTrack)”. "
    "First, we thank God for giving us the strength, knowledge, and patience to complete this project successfully. "
    "We are also thankful to the Principal, Dr. Sunil Naik, for providing us with the necessary facilities and academic "
    "support to carry out this project. We would like to express our heartfelt gratitude to our Project Guide, "
    "Ms. Ayushi Mistry, for providing valuable guidance, continuous support, constructive suggestions, and encouragement "
    "throughout the development of this project. We extend our sincere thanks to all the faculty members of the BCA "
    "Department for their valuable suggestions and assistance during our academic journey. We are grateful to our "
    "parents, family members, and friends for their constant encouragement, support, and motivation throughout the "
    "completion of this project. Finally, we thank everyone who directly or indirectly contributed to the successful "
    "completion of this project.",
    space_after=10
)

p_ty = add_p("Thank You.", space_after=0)
p_ty.runs[0].font.bold = True
p_ty.runs[0].font.size = Pt(12)

add_page_break()

# ==============================================================================
# 3. PROJECT CERTIFICATION FORM & ABSTRACT
# ==============================================================================
p_cert = add_p("PROJECT CERTIFICATION FORM", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=6, space_after=12)
p_cert.runs[0].font.size = Pt(17)
p_cert.runs[0].font.bold = True
p_cert.runs[0].font.color.rgb = C_DARK

add_p(
    "This is to certify that the project entitled \"Personal Finance & Expense Tracker (FinTrack)\" is a bona fide work "
    "carried out by the student of Bachelor of Computer Applications (BCA) in partial fulfillment of the requirements "
    "for the academic year 2025-2026.",
    space_after=10
)

add_p("Student Name: Chauhan Om S.", space_after=4).runs[0].font.bold = True
add_p("Enrollment Number: Roll No. 35", space_after=8).runs[0].font.bold = True

add_p(
    "The project report has been examined and evaluated by the internal project guide and program coordinator, and meets "
    "the requisite academic standards prescribed by the institute.",
    space_after=18
)

# Table for signatures
sig_table = doc.add_table(rows=1, cols=2)
sig_table.alignment = WD_TABLE_ALIGNMENT.CENTER
for c in sig_table.rows[0].cells:
    c.width = Inches(3.1)

c0 = sig_table.rows[0].cells[0]
p0 = c0.paragraphs[0]
p0.paragraph_format.line_spacing = 1.2
r = p0.add_run("______________________________\nSignature of Project Guide\n(Ms. Ayushi Mistry)\nDate: _______________")
style_run(r, size_pt=10.5, bold=True, color=C_DARK)

c1 = sig_table.rows[0].cells[1]
p1 = c1.paragraphs[0]
p1.alignment = WD_ALIGN_PARAGRAPH.RIGHT
p1.paragraph_format.line_spacing = 1.2
r = p1.add_run("______________________________\nSignature of Principal / HOD\n(Dr. Sunil Naik)\nDate: _______________")
style_run(r, size_pt=10.5, bold=True, color=C_DARK)

add_p("", space_before=14, space_after=4)

# Abstract
p_abs = add_p("EXECUTIVE SUMMARY / ABSTRACT", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=12, space_after=10)
p_abs.runs[0].font.size = Pt(16)
p_abs.runs[0].font.bold = True
p_abs.runs[0].font.color.rgb = C_DARK

add_p(
    "The Personal Finance & Expense Tracker (FinTrack) is an automated web-based financial management system engineered "
    "to provide individuals with real-time clarity over income, expenditure, category-wise budgets, and milestone savings. "
    "Built on an asynchronous Single Page Application (SPA) architecture, the solution features a high-performance MERN "
    "stack backend utilizing Node.js 18+ and Express 5 REST API communicating via Mongoose 9 ODM with a MongoDB database, "
    "coupled with a responsive, modern React 19 frontend utilizing Tailwind CSS v4 and Recharts.\n\n"
    "FinTrack resolves critical pain points in contemporary personal finance, including fragmented cash flow across UPI, "
    "credit cards, bank transfers, and cash, lack of proactive budget threshold warnings, floating-point calculation inaccuracies, "
    "and session vulnerabilities. Storing all monetary values internally in integer-based minor currency units (paise) ensures "
    "100% mathematical precision without rounding errors. Robust defense against script injection is achieved by utilizing "
    "HMAC-SHA256 signed JSON Web Tokens (JWT) stored exclusively in HTTP-only, SameSite cookies. The result is an intuitive, "
    "fast, and enterprise-grade financial management platform tailored for modern personal wealth discipline.",
    space_after=0
)

add_page_break()

# ==============================================================================
# 4. TABLE OF CONTENTS
# ==============================================================================
p_toc = add_p("TABLE OF CONTENTS", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=6, space_after=14)
p_toc.runs[0].font.size = Pt(18)
p_toc.runs[0].font.bold = True
p_toc.runs[0].font.color.rgb = C_DARK

toc_data = [
    ("Title Page", "1"),
    ("Declaration & Acknowledgement", "2"),
    ("Project Certification Form & Abstract", "3"),
    ("Table of Contents", "4"),
    ("1. Introduction", "5"),
    ("    1.1 Purpose", "5"),
    ("    1.2 Scope", "5"),
    ("    1.3 Definition", "6"),
    ("    1.4 Technologies to be Used", "6"),
    ("2. System Analysis", "8"),
    ("    2.1 Identification of Need", "8"),
    ("    2.2 Functionalities (Usual and Distinct)", "8"),
    ("    2.3 User Characteristics", "9"),
    ("    2.4 Software Development Process", "10"),
    ("3. Conceptual Diagrams", "11"),
    ("    3.1 Use Case Diagram", "11"),
    ("    3.2 Activity Diagram", "12"),
    ("    3.3 System Architecture Diagram", "13"),
    ("4. System Design", "14"),
    ("    4.1 Data Dictionary (MongoDB Schemas)", "14"),
    ("    4.2 User Interface Design", "17"),
    ("    4.3 Reports and Analytical Outputs", "22"),
    ("5. Testing", "24"),
    ("    5.1 Test Cases", "24"),
    ("    5.2 Testing Reports & Evaluation", "26"),
    ("6. Future Scope and Further Enhancement", "27"),
    ("7. Learning During Project Work", "28"),
    ("References", "29")
]

toc_table = doc.add_table(rows=len(toc_data), cols=2)
toc_table.alignment = WD_TABLE_ALIGNMENT.CENTER
set_table_borders(toc_table)

for r_idx, (title_str, page_str) in enumerate(toc_data):
    row = toc_table.rows[r_idx]
    c0 = row.cells[0]
    c1 = row.cells[1]
    c0.width = Inches(5.2)
    c1.width = Inches(1.0)
    
    p0 = c0.paragraphs[0]
    p0.paragraph_format.space_before = Pt(2)
    p0.paragraph_format.space_after = Pt(2)
    is_main = not title_str.startswith("    ")
    r0 = p0.add_run(title_str)
    style_run(r0, size_pt=10.5, bold=is_main, color=C_DARK)
    
    p1 = c1.paragraphs[0]
    p1.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p1.paragraph_format.space_before = Pt(2)
    p1.paragraph_format.space_after = Pt(2)
    r1 = p1.add_run(page_str)
    style_run(r1, size_pt=10.5, bold=is_main, color=C_DARK)

add_page_break()

# ==============================================================================
# 5. CHAPTER 1: INTRODUCTION
# ==============================================================================
add_heading_1("1. Introduction")

add_heading_2("1.1. Purpose")
add_p(
    "The primary objective of the Personal Finance & Expense Tracker (FinTrack) project is to deliver a reliable, "
    "automated, and secure digital platform that enables users to record, categorize, analyze, and optimize their daily "
    "financial transactions. By eliminating traditional manual paper-based logs and complex spreadsheets, FinTrack provides "
    "actionable insights into personal spending habits, promotes consistent savings discipline, and safeguards users "
    "from budgetary overruns through proactive threshold monitoring."
)

add_heading_2("1.2. Scope")
add_p(
    "The scope of FinTrack spans the full spectrum of personal cash-flow management for individual users, students, and "
    "families. The functional boundaries are defined as follows:"
)

add_p("In-Scope Capabilities:", space_before=4, space_after=4).runs[0].font.bold = True
add_bullet("User account creation, profile preference management, and JWT-authenticated session security via HTTP-only cookies.")
add_bullet("Double-entry styled cash flow recording (Income vs. Expense) with granular categorization, tags, payment method tracking (UPI, Card, Net Banking, Cash), and transaction notes.")
add_bullet("Flexible category management allowing custom color codes and Lucide icon representations.")
add_bullet("Time-bound monthly budget allocations per expense category with dynamic percentage consumption indicators (Green <80%, Amber >=80%, Red >=100%).")
add_bullet("Target-oriented savings goals tracking milestone deposits and withdrawals with comprehensive ledger records.")
add_bullet("Interactive visual dashboard and analytics including 6-month trends and categorical spending distributions via Recharts.")
add_bullet("Persistent zero-flicker Dark/Light theme switching powered by Tailwind CSS 4.")

add_p("Out-of-Scope (for Current Release):", space_before=6, space_after=4).runs[0].font.bold = True
add_bullet("Direct bank account open-banking synchronization via proprietary banking APIs.")
add_bullet("Multi-party joint commercial accounting, corporate payroll, and GST tax invoice generation.")
add_bullet("Stock market ticker integration and automated algorithmic trading.")

add_heading_2("1.3. Definition")
add_p("To ensure clarity throughout this documentation, key technical and domain terms are defined below:")
add_bullet("MERN Stack: An end-to-end JavaScript/TypeScript engineering architecture comprising MongoDB, Express.js, React 19, and Node.js for high-speed full-stack web applications.")
add_bullet("MongoDB & Mongoose: A high-performance document database storing JSON-like BSON documents, paired with Mongoose 9 ODM for schema enforcement, pre-save hooks, and compound indexing.")
add_bullet("JWT (JSON Web Token): A compact, URL-safe means of representing claims securely between client and server, utilized here within HTTP-only SameSite cookies for stateless authentication.")
add_bullet("REST (Representational State Transfer): An architectural style utilizing standard HTTP verbs (GET, POST, PATCH, DELETE) to manipulate resources via structured JSON payloads.")
add_bullet("SPA (Single Page Application): A web application that dynamically rewrites the current browser page with data from the server rather than loading entire new pages from the server.")
add_bullet("Minor Units (Paise): Storing currency amounts as integers multiplied by 100 (e.g. ₹250.00 = 25000 paise) to eliminate floating-point arithmetic rounding errors in monetary calculations.")

add_heading_2("1.4. Technologies to be Used")
add_p("Hardware Requirements (Development & Deployment):", space_before=4, space_after=4).runs[0].font.bold = True
add_bullet("Processor: Dual Core Intel Core i3 / AMD Ryzen 3 or higher (2.0 GHz+).")
add_bullet("Memory (RAM): Minimum 4 GB RAM (8 GB recommended for development).")
add_bullet("Storage: 500 MB free disk space for application files, dependencies, and database storage.")
add_bullet("Display: 1366 x 768 minimum display resolution (Optimized for 1920 x 1080 Full HD).")

add_p("Software Requirements:", space_before=6, space_after=4).runs[0].font.bold = True
add_bullet("Operating System: Microsoft Windows 10 / 11, Linux (Ubuntu 20.04+), or macOS.")
add_bullet("Backend Runtime: Node.js (v18.x or v20.x LTS) with NPM package manager.")
add_bullet("Backend Web Framework: Express.js 5.x with Helmet 8, Express-Rate-Limit 8, and Cookie-Parser 1.4.")
add_bullet("Database Engine: MongoDB Community Server v6.0+ (Local) or MongoDB Atlas Cloud Cluster.")
add_bullet("Object Data Modeling (ODM): Mongoose 9.x with compound index optimization.")
add_bullet("Frontend Stack: React 19, Vite 8 build tool, Tailwind CSS v4, Recharts 3.x, Axios 1.x, Lucide React icons.")
add_bullet("Client Web Browser: Modern Chromium-based browser (Google Chrome, Microsoft Edge, Brave) or Mozilla Firefox.")

add_page_break()

# ==============================================================================
# 6. CHAPTER 2: SYSTEM ANALYSIS
# ==============================================================================
add_heading_1("2. System Analysis")

add_heading_2("2.1. Identification of Need")
add_p(
    "In the modern economic environment, individuals encounter multiple payment channels including UPI, debit/credit cards, "
    "net banking, and physical cash. This fragmentation makes financial tracking tedious and disorganized. Studies indicate "
    "that over 65% of individuals who fail to maintain a structured budget encounter unforeseen end-of-month financial stress.\n\n"
    "Existing commercial alternatives often charge heavy monthly subscription fees, display intrusive advertising, or harvest "
    "user banking data for third-party monetization. Furthermore, many web applications store sensitive tokens in browser "
    "`localStorage`, leaving sessions exposed to Cross-Site Scripting (XSS) attacks. There is an unmistakable need for a "
    "lightweight, transparent, highly secure, and intuitive web application that allows users to regain complete mastery "
    "over their financial life without compromising personal privacy or data security."
)

add_heading_2("2.2. Functionalities")
add_p("Usual Functionalities:", space_before=4, space_after=4).runs[0].font.bold = True
add_bullet("User Registration, Secure Login, Logout, Profile update, and Password change.")
add_bullet("Full CRUD operations (Create, Read, Update, Delete) for income and expense transactions.")
add_bullet("Filtering transactions by date range, transaction type, category, and payment method.")
add_bullet("Pre-configured default categories (Salary, Food & Dining, Utilities, Entertainment, Housing, Transportation, etc.).")
add_bullet("Pagination and real-time search capabilities for reviewing extensive transaction records.")

add_p("Distinct Functionalities:", space_before=6, space_after=4).runs[0].font.bold = True
add_bullet("High-Precision Financial Computation: Financial amounts are stored internally in minor units (integer paise) to guarantee zero floating-point calculation errors.")
add_bullet("Real-Time Budget Utilization Gauges: Dynamic status tags ('Normal' <80%, 'Warning' >=80%, 'Exceeded' >=100%) computed on-the-fly against live transaction aggregations.")
add_bullet("Milestone-Driven Goal Tracker: Visual progress meters with dedicated contribution and withdrawal transaction histories for targeted savings.")
add_bullet("Full-Stack MERN Architecture: Pure JavaScript/Node.js stack utilizing Express 5 REST API and Mongoose 9 ODM without legacy framework bloat.")
add_bullet("Interactive Data Visualizations: High-performance SVG responsive charts rendering monthly income-vs-expense comparisons and categorical expense distributions.")
add_bullet("Adaptive Dark/Light Theme: Seamless, persistent theme switcher using Tailwind CSS 4 custom variants and local storage sync.")

add_heading_2("2.3. User Characteristics")
add_bullet("Regular User / Working Professional: Needs rapid expense recording, salary logging, and monthly budget notifications to curb overspending.")
add_bullet("Student / Freelancer: Manages irregular income streams, requires tracking of project-based milestone fees, and monitors living expenditures.")
add_bullet("System Administrator: Manages database integrity, inspects server health endpoints, oversees compound query indexes, and maintains backup/restore procedures.")

add_heading_2("2.4. Software Development Process")
add_p(
    "The Agile Iterative Prototyping methodology was adopted for this project. Development proceeded across four structured sprints:"
)
add_bullet("Sprint 1 (Requirements & Database Architecture): Defined REST contracts, constructed Mongoose schemas (`User.js`, `Transaction.js`, `Budget.js`, `SavingsGoal.js`, `GoalContribution.js`, `Category.js`), and designed compound indexes.", "• Sprint 1: ")
add_bullet("Sprint 2 (Backend Core Services): Implemented Express 5 REST controllers, JWT cookie authentication middleware, Helmet security headers, and Express rate limiting.", "• Sprint 2: ")
add_bullet("Sprint 3 (Frontend & Visual Components): Developed responsive React 19 views with Tailwind CSS 4, Recharts analytics, Lucide icons, and Axios API services.", "• Sprint 3: ")
add_bullet("Sprint 4 (Testing, Data Seeding & Optimization): Populated database with comprehensive realistic test data (`seed.js`), executed automated Jest test suites, and polished UI micro-interactions.", "• Sprint 4: ")

add_page_break()

# ==============================================================================
# 7. CHAPTER 3: CONCEPTUAL DIAGRAMS
# ==============================================================================
add_heading_1("3. Conceptual Diagrams")

add_heading_2("3.1. Use Case Diagram")
add_p(
    "The Use Case Diagram defines the interactions between the external actor (Registered User) and the core sub-systems "
    "of the Personal Finance Tracker application."
)

use_case_img = os.path.join(sc_dir, "3_1_use_case_diagram.png")
add_figure(use_case_img, "Figure 3.1: UML Use Case Diagram for FinTrack System", width_in=5.8)

add_p(
    "As illustrated in Figure 3.1, the registered user interacts with seven primary use cases: Authenticate (Login/Register), "
    "Record Transactions, Categorize & Filter Records, Set Monthly Budgets, Manage Savings Goals & Contributions, "
    "View Real-time Analytics & Dashboard, and Manage Profile Settings."
)

add_heading_2("3.2. Activity Diagram")
add_p(
    "The Activity Diagram models the dynamic operational workflow of recording an expense, validating user inputs, updating "
    "database state, and recalculating dashboard metrics."
)

activity_img = os.path.join(sc_dir, "3_2_activity_diagram.png")
add_figure(activity_img, "Figure 3.2: UML Activity Diagram for Financial Transaction Lifecycle", width_in=5.2)

add_p(
    "Figure 3.2 demonstrates the end-to-end decision flow from authentication, through transaction capture and validation, "
    "to atomic database commit in MongoDB and real-time visualization update in React."
)

add_heading_2("3.3. System Architecture Diagram")
add_p(
    "The System Architecture Diagram visualizes the 3-tier decoupled MERN architecture connecting the React 19 Single Page "
    "Application, Express 5 REST API server, and MongoDB document database."
)

arch_img = os.path.join(sc_dir, "3_3_system_architecture.png")
add_figure(arch_img, "Figure 3.3: MERN Stack 3-Tier System Architecture Diagram", width_in=5.8)

add_p(
    "Figure 3.3 illustrates the physical separation of concerns: Presentation Tier (React 19 + Tailwind CSS + Recharts), "
    "Application & Business Logic Tier (Node.js + Express 5 REST API + JWT Cookie Security Middleware), and Data Storage "
    "Tier (MongoDB + Mongoose 9 ODM with compound indexing and minor-unit currency storage)."
)

add_page_break()

# ==============================================================================
# 8. CHAPTER 4: SYSTEM DESIGN
# ==============================================================================
add_heading_1("4. System Design")

add_heading_2("4.1. Data Dictionary")
add_p(
    "The Data Dictionary provides an exhaustive specification of the database collections, fields, BSON data types, "
    "indexes, and validation constraints configured in the MongoDB database via Mongoose 9 schemas."
)

# Helper function to generate Data Dictionary Table
def create_schema_table(caption_title, headers, rows_data):
    add_heading_3(caption_title)
    tbl = doc.add_table(rows=len(rows_data) + 1, cols=len(headers))
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl)
    
    # Header row
    hdr_row = tbl.rows[0]
    for c_idx, h_text in enumerate(headers):
        cell = hdr_row.cells[c_idx]
        set_cell_shading(cell, "F1F5F9")
        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(3)
        p.paragraph_format.space_after = Pt(3)
        r = p.add_run(h_text)
        style_run(r, size_pt=9.5, bold=True, color=C_DARK)
    
    # Data rows
    for r_idx, r_data in enumerate(rows_data):
        row = tbl.rows[r_idx + 1]
        for c_idx, val in enumerate(r_data):
            cell = row.cells[c_idx]
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(2)
            r = p.add_run(val)
            style_run(r, size_pt=9.0, color=C_DARK)
    
    # Set standard column widths
    for row in tbl.rows:
        row.cells[0].width = Inches(1.5)
        row.cells[1].width = Inches(1.1)
        row.cells[2].width = Inches(1.6)
        row.cells[3].width = Inches(2.0)
    
    add_p("", space_before=2, space_after=6)

# Table 4.1: users
create_schema_table(
    "Table 4.1: users Collection Schema",
    ["Field Name", "BSON Type", "Constraints / Indexes", "Description"],
    [
        ("_id", "ObjectId", "PRIMARY KEY (Auto)", "Unique MongoDB document identifier"),
        ("name", "String", "required, trim, max: 100", "Full name of the registered user"),
        ("email", "String", "required, unique, lowercase", "User email address for authentication"),
        ("passwordHash", "String", "required, min: 6, select: false", "Bcrypt hashed password (12 salt rounds)"),
        ("preferredCurrency", "String", "enum: ['INR','USD','EUR'...], def: 'INR'", "User selected currency formatting preference"),
        ("theme", "String", "enum: ['light', 'dark'], def: 'light'", "UI display theme preference"),
        ("createdAt / updatedAt", "Date", "timestamps: true", "Document creation and modification timestamps")
    ]
)

# Table 4.2: categories
create_schema_table(
    "Table 4.2: categories Collection Schema",
    ["Field Name", "BSON Type", "Constraints / Indexes", "Description"],
    [
        ("_id", "ObjectId", "PRIMARY KEY (Auto)", "Unique category document identifier"),
        ("userId", "ObjectId", "ref: 'User', index: true, nullable", "Associated user reference (null for system defaults)"),
        ("name", "String", "required, trim, max: 50", "Display name of the category"),
        ("type", "String", "enum: ['income','expense','both']", "Cash flow category classification"),
        ("color", "String", "match: hex regex, def: '#6366f1'", "Hex color code used in UI charts"),
        ("icon", "String", "def: 'tag'", "Lucide icon identifier name"),
        ("isDefault", "Boolean", "def: false", "Flag preventing deletion of system default categories"),
        ("Index", "Compound", "{ userId: 1, name: 1 }, unique: true", "Enforces unique category names per user")
    ]
)

# Table 4.3: transactions
create_schema_table(
    "Table 4.3: transactions Collection Schema",
    ["Field Name", "BSON Type", "Constraints / Indexes", "Description"],
    [
        ("_id", "ObjectId", "PRIMARY KEY (Auto)", "Unique transaction document identifier"),
        ("userId", "ObjectId", "ref: 'User', required, index: true", "Associated user owner reference"),
        ("title", "String", "required, trim, max: 200", "Transaction description or payee"),
        ("amountMinor", "Number", "required, min: 1 (Integer)", "Amount in minor currency units (paise: ₹100 = 10000)"),
        ("type", "String", "required, enum: ['income', 'expense']", "Cash flow direction classification"),
        ("category", "String", "required, trim", "Category name string"),
        ("date", "Date", "required, index: true", "Date and time of transaction"),
        ("paymentMethod", "String", "enum: ['cash','upi','credit_card'...]", "Payment channel used for transaction"),
        ("notes", "String", "trim, max: 500, nullable", "Optional notes or transaction remarks"),
        ("tags", "Array[String]", "trim, nullable", "Array of search tags"),
        ("Compound Indexes", "Indexes", "{userId:1, date:-1}, {userId:1, type:1, date:-1}", "High-speed indexed reverse chronological queries")
    ]
)

# Table 4.4: budgets
create_schema_table(
    "Table 4.4: budgets Collection Schema",
    ["Field Name", "BSON Type", "Constraints / Indexes", "Description"],
    [
        ("_id", "ObjectId", "PRIMARY KEY (Auto)", "Unique budget document identifier"),
        ("userId", "ObjectId", "ref: 'User', required, index: true", "User reference"),
        ("category", "String", "required, trim", "Target expense category"),
        ("amountMinor", "Number", "required, min: 1 (Integer)", "Spending cap limit in minor currency units"),
        ("period", "String", "enum: ['monthly','weekly','yearly']", "Budget allocation frequency (default monthly)"),
        ("startDate", "Date", "required", "Start of budget validity interval"),
        ("endDate", "Date", "required", "End of budget validity interval"),
        ("Index", "Compound", "{userId:1, category:1, startDate:1, endDate:1}", "Prevents overlapping budgets for same category")
    ]
)

# Table 4.5: savingsgoals
create_schema_table(
    "Table 4.5: savingsgoals Collection Schema",
    ["Field Name", "BSON Type", "Constraints / Indexes", "Description"],
    [
        ("_id", "ObjectId", "PRIMARY KEY (Auto)", "Unique goal document identifier"),
        ("userId", "ObjectId", "ref: 'User', required, index: true", "Owner user reference"),
        ("title", "String", "required, trim, max: 100", "Goal target name (e.g. Emergency Fund)"),
        ("targetAmountMinor", "Number", "required, min: 1 (Integer)", "Target savings amount in minor currency units"),
        ("currentAmountMinor", "Number", "min: 0, def: 0 (Integer)", "Accumulated savings balance in minor units"),
        ("targetDate", "Date", "nullable, def: null", "Target milestone completion deadline"),
        ("status", "String", "enum: ['active','completed','archived']", "Current milestone status flag"),
        ("color / icon", "String", "def: '#6366f1' / 'target'", "Custom card theme palette and Lucide icon")
    ]
)

# Table 4.6: goalcontributions
create_schema_table(
    "Table 4.6: goalcontributions Collection Schema",
    ["Field Name", "BSON Type", "Constraints / Indexes", "Description"],
    [
        ("_id", "ObjectId", "PRIMARY KEY (Auto)", "Unique contribution ledger ID"),
        ("userId", "ObjectId", "ref: 'User', required, index: true", "User reference"),
        ("goalId", "ObjectId", "ref: 'SavingsGoal', required, index", "Associated savings goal reference"),
        ("amountMinor", "Number", "required, min: 1 (Integer)", "Deposit or withdrawal amount in paise"),
        ("type", "String", "required, enum: ['contribution','withdrawal']", "Type of balance alteration"),
        ("notes", "String", "trim, max: 200, nullable", "Deposit memo or reason"),
        ("date", "Date", "def: Date.now, index: -1", "Timestamp of ledger record")
    ]
)

add_heading_2("4.2. User Interface Design")
add_p(
    "The following section presents live application snapshots captured from the working FinTrack MERN system, "
    "highlighting key operational interfaces, input fields, and real-time validations:"
)

# UI Screen 1: Login
add_heading_3("1. Authentication & Login Screen")
add_figure(os.path.join(sc_dir, "01_login_page.png"), "Figure 4.1: User Login Screen with Input Validation", width_in=5.8)
add_bullet("Validation: Email format validation regex (`^\\S+@\\S+\\.\\S+$`), mandatory password check with minimum 6 characters length enforcement.")
add_bullet("Security: Upon verification, the Express backend issues an HTTP-only SameSite cookie containing a signed HMAC-SHA256 JWT token.")

# UI Screen 2: Dashboard Overview
add_heading_3("2. Executive Financial Dashboard")
add_figure(os.path.join(sc_dir, "02_dashboard_overview.png"), "Figure 4.2: Real-time Financial Dashboard with Summary Metrics", width_in=5.8)
add_bullet("Real-Time Metrics: Total Income, Total Expenses, Net Balance, and Calculated Savings Rate dynamically computed.")
add_bullet("Quick Action Triggers: One-click modal launching to register immediate transactions with instant dashboard refresh.")

# UI Screen 3: Dashboard Charts
add_heading_3("3. Dashboard Visual Charts & Category Breakdown")
add_figure(os.path.join(sc_dir, "03_dashboard_charts.png"), "Figure 4.3: 6-Month Income vs Expense Bar Chart and Top Expense Distribution", width_in=5.8)
add_bullet("6-Month Cash Flow: Dual-bar graph comparing monthly income and expenditure patterns rendered via Recharts.")
add_bullet("Top Expense Categories: Aggregated ranking displaying category spending totals, counts, and percentage distribution.")

# UI Screen 4: Transactions List
add_heading_3("4. Transaction Management & Multi-Filter Registry")
add_figure(os.path.join(sc_dir, "04_transactions_list.png"), "Figure 4.4: Paginated Transaction Table with Filtering Controls", width_in=5.8)
add_bullet("Multi-parameter Search: Filter records by transaction type (Income/Expense), category dropdown, date intervals, and payment methods.")
add_bullet("Pagination & Sorting: Server-side pagination executing MongoDB `skip()` and `limit()` queries for optimal responsiveness.")

# UI Screen 5: Add Transaction Modal
add_heading_3("5. Transaction Creation & Validation Modal")
add_figure(os.path.join(sc_dir, "05_add_transaction_modal.png"), "Figure 4.5: Add Transaction Modal Dialog with Strict Form Controls", width_in=5.8)
add_bullet("Validation Rules: Title (mandatory, max 200 chars), Amount (must be strictly positive integer/float converted to minor units), Category selection, and Valid Date format.")

# UI Screen 6: Budgets Page
add_heading_3("6. Monthly Budgets & Spending Threshold Tracker")
add_figure(os.path.join(sc_dir, "06_budgets_page.png"), "Figure 4.6: Category Budget Utilization Cards with Warning Badges", width_in=5.8)
add_bullet("Dynamic Color Status: Normal (Green < 80%), Warning (Amber >= 80%), and Exceeded (Red >= 100%).")
add_bullet("Overlap Prevention: Backend compound index rejects overlapping budget intervals for the same category.")

# UI Screen 7: Savings Goals
add_heading_3("7. Savings Goals & Milestone Progress Tracker")
add_figure(os.path.join(sc_dir, "07_savings_goals.png"), "Figure 4.7: Target Savings Goals with Contribution History", width_in=5.8)
add_bullet("Goal Automation: Automatically switches status to 'Completed' when accumulated contributions match or exceed the target.")
add_bullet("Withdrawal Safety: Blocks withdrawals that exceed current accumulated milestone funds.")

# UI Screen 8: Settings & Categories
add_heading_3("8. Category Customization & Profile Preferences")
add_figure(os.path.join(sc_dir, "09_settings_categories.png"), "Figure 4.8: Category Palette Customizer and System Settings", width_in=5.8)
add_bullet("Customization: Add custom category names, hex colors, and Lucide icons.")
add_bullet("Protection: Default system categories are locked against deletion, preserving historical transaction integrity.")

add_heading_2("4.3. Reports and Analytical Outputs")
add_p(
    "FinTrack generates comprehensive visual analytical reports reflecting cash flow distributions and trend trajectories over multi-month intervals:"
)

add_figure(os.path.join(sc_dir, "08_analytics_reports.png"), "Figure 4.9: Analytical Reports showing Cash Flow Trend and Expense Breakdown", width_in=5.8)
add_bullet("Income vs. Expense Analytical Chart: Visualizes cash flow divergence across quarterly and annual intervals.")
add_bullet("Categorical Distribution: Donut / Bar breakdown showing percentage utilization per category.")
add_bullet("Monthly Trend Analysis: Mathematical evaluation of savings rate trajectories to assist long-term wealth planning.")

add_page_break()

# ==============================================================================
# 9. CHAPTER 5: TESTING
# ==============================================================================
add_heading_1("5. Testing")

add_heading_2("5.1. Test Cases")
add_p(
    "Comprehensive manual and automated test suites were executed across the authentication, transaction, budgeting, "
    "and analytical modules. The results are summarized below:"
)

test_cases_data = [
    ("TC-01", "User Registration", "Valid name, email, 8-char password", "User created (201), default categories seeded", "Account created, categories seeded", "Pass"),
    ("TC-02", "Duplicate Registration", "Existing registered email address", "HTTP 409 Conflict, validation error message", "HTTP 409 Conflict returned", "Pass"),
    ("TC-03", "User Authentication", "Correct email & password", "HTTP 200, JWT token set in HTTP-only cookie", "Auth cookie set, user profile returned", "Pass"),
    ("TC-04", "Invalid Login", "Unregistered email or wrong password", "HTTP 401 Unauthorized", "HTTP 401 Unauthorized returned", "Pass"),
    ("TC-05", "Record Transaction", "Positive amount, category, valid date", "Record committed, amount stored in minor units (paise)", "Committed to MongoDB in paise", "Pass"),
    ("TC-06", "Negative Amount Validation", "Amount = -500", "Frontend validation block & HTTP 400 error", "Blocked with validation alert", "Pass"),
    ("TC-07", "Budget Overlap Check", "Duplicate budget for same category/month", "HTTP 409 Overlapping budget conflict", "HTTP 409 Conflict triggered", "Pass"),
    ("TC-08", "Budget Exceeded Flag", "Expenses exceed 100% of budget cap", "Budget status set to 'exceeded', badge red", "Calculated 100%+ and red badge shown", "Pass"),
    ("TC-09", "Goal Contribution", "Deposit amount added to active goal", "Balance updated, record logged in history", "Balance incremented, ledger stored", "Pass"),
    ("TC-10", "Goal Excessive Withdrawal", "Withdrawal amount > current savings", "HTTP 400 'Exceeds current savings'", "HTTP 400 rejected with message", "Pass"),
    ("TC-11", "Protected Route Guard", "Unauthenticated visit to `/dashboard`", "Client redirected immediately to `/login`", "Redirected to `/login` successfully", "Pass"),
    ("TC-12", "Theme Mode Persistence", "Toggle dark mode and reload browser", "Theme preserved in localStorage and DOM class", "Dark theme loaded on reload", "Pass")
]

test_table = doc.add_table(rows=len(test_cases_data) + 1, cols=6)
test_table.alignment = WD_TABLE_ALIGNMENT.CENTER
set_table_borders(test_table)

tc_headers = ["Test ID", "Test Scenario", "Input Parameters", "Expected Result", "Actual Result", "Status"]
for c_idx, h_text in enumerate(tc_headers):
    cell = test_table.rows[0].cells[c_idx]
    set_cell_shading(cell, "F1F5F9")
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(3)
    p.paragraph_format.space_after = Pt(3)
    r = p.add_run(h_text)
    style_run(r, size_pt=9.0, bold=True, color=C_DARK)

for r_idx, r_vals in enumerate(test_cases_data):
    row = test_table.rows[r_idx + 1]
    for c_idx, val in enumerate(r_vals):
        cell = row.cells[c_idx]
        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(2)
        r = p.add_run(val)
        style_run(r, size_pt=8.5, bold=(c_idx==5 or c_idx==0), color=C_DARK)

for row in test_table.rows:
    row.cells[0].width = Inches(0.7)
    row.cells[1].width = Inches(1.3)
    row.cells[2].width = Inches(1.2)
    row.cells[3].width = Inches(1.4)
    row.cells[4].width = Inches(1.2)
    row.cells[5].width = Inches(0.5)

add_heading_2("5.2. Testing Reports & Evaluation")
add_bullet("Unit Testing: Evaluated all Express 5 REST endpoints, authentication middleware, and Mongoose pre-save hooks using Jest and Supertest test suites.")
add_bullet("Integration Testing: Verified end-to-end data flow between React Axios services, Vite proxy, Express controllers, and MongoDB collections.")
add_bullet("Security Testing: Verified resistance against NoSQL injection through Mongoose schema type-casting; confirmed password hashing resistance using Bcrypt (cost factor 12); verified Cross-Site Scripting (XSS) defenses through React sanitized JSX rendering and HTTP-only SameSite cookie storage.")

add_page_break()

# ==============================================================================
# 10. CHAPTER 6: FUTURE SCOPE & ENHANCEMENT
# ==============================================================================
add_heading_1("6. Future Scope and Further Enhancement")
add_p(
    "While the current version of FinTrack provides a robust and complete personal finance management solution, "
    "future iterations can introduce several advanced capabilities:"
)

add_bullet("Integrating computer vision algorithms (e.g. Tesseract.js / Google Cloud Vision API) to allow users to photograph paper receipts and automatically parse date, vendor, tax, and itemized totals.", "1. Optical Character Recognition (OCR) for Receipts: ")
add_bullet("Direct parsing of standard banking statement exports to batch-import transactions with automated categorization.", "2. Automated Bank Statement Import (PDF/CSV): ")
add_bullet("Machine learning algorithms to analyze historical spending patterns and project future cash-flow deficits before they occur.", "3. AI-Powered Predictive Budgeting: ")
add_bullet("Packaging the React frontend with Capacitor or React Native to deliver push notifications for daily budget reminders on Android and iOS devices.", "4. Native Mobile Application: ")
add_bullet("Collaborative financial accounts allowing shared household budgets with customizable permission tiers.", "5. Multi-User Family Wallets: ")

add_page_break()

# ==============================================================================
# 11. CHAPTER 7: LEARNING DURING PROJECT WORK
# ==============================================================================
add_heading_1("7. Learning During Project Work")
add_p(
    "The journey of conceptualizing, designing, and engineering the Personal Finance Tracker provided profound hands-on experience "
    "across the full modern software development lifecycle:"
)

add_bullet("Gained in-depth appreciation for separating business logic into clean REST endpoints, allowing the backend to run on Express 5 while the frontend operates as a decoupled modern React application.", "• Decoupled MERN Architecture: ")
add_bullet("Learned the critical importance of integer-based minor currency representation (`amountMinor`) to avoid floating-point imprecision in financial systems.", "• Defensive Database Design & Currency Precision: ")
add_bullet("Mastered token-based stateless security, implementing HMAC-SHA256 JWTs paired with secure HTTP-only cookies to thwart token theft and XSS vulnerabilities.", "• Robust Authentication Patterns: ")
add_bullet("Leveraged Mongoose aggregation pipelines and compound indexing (`{ userId: 1, date: -1 }`) to deliver instant chart responses without burdening client-side memory.", "• Asynchronous Data Visualization: ")
add_bullet("Learned how to construct zero-runtime-overhead theme systems using Tailwind CSS 4 custom variants and React Context API.", "• Modern Responsive UI & Theming: ")

add_page_break()

# ==============================================================================
# 12. REFERENCES
# ==============================================================================
add_heading_1("References")

refs = [
    "1. Banks, A., & Porcello, E. (2020). Learning React: Modern Patterns for Developing React Apps (2nd ed.). O'Reilly Media.",
    "2. Chodorow, K. (2019). MongoDB: The Definitive Guide - Powerful and Scalable Data Storage (3rd ed.). O'Reilly Media.",
    "3. Brown, E. (2019). Web Development with Node and Express: Leveraging the JavaScript Stack (2nd ed.). O'Reilly Media.",
    "4. React Core Team. (2025). React Documentation & Hooks Reference. Retrieved from https://react.dev",
    "5. MongoDB Documentation Team. (2025). MongoDB Manual & Mongoose 9 ODM Reference. Retrieved from https://www.mongodb.com/docs/",
    "6. Express.js Community. (2025). Express 5 API Documentation. Retrieved from https://expressjs.com",
    "7. Mozilla Developer Network (MDN). (2024). HTTP Cookies, SameSite Policies, and Web Security Standards. Retrieved from https://developer.mozilla.org/en-US/docs/Web/HTTP/Cookies",
    "8. Tailwind Labs. (2025). Tailwind CSS v4 Documentation and Variant Architecture. Retrieved from https://tailwindcss.com"
]

for ref in refs:
    add_p(ref, space_after=8)

# Save DOCX
out_docx = r"c:\Users\Asus\Desktop\Project\documentation\Project_Documentation_Report.docx"
doc.save(out_docx)
print("Saved DOCX successfully to:", out_docx)
