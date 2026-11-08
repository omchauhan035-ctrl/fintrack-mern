import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

doc = docx.Document()

# Page Setup: Standard A4, 0.75 in margins for compact reading
for sec in doc.sections:
    sec.page_width = Inches(8.27)
    sec.page_height = Inches(11.69)
    sec.top_margin = Inches(0.75)
    sec.bottom_margin = Inches(0.75)
    sec.left_margin = Inches(0.75)
    sec.right_margin = Inches(0.75)

# Color Palette
C_NAVY   = RGBColor(0x0F, 0x17, 0x2A) # Slate 900
C_BLUE   = RGBColor(0x1D, 0x4E, 0xD8) # Blue 700
C_DARK   = RGBColor(0x1E, 0x29, 0x3B) # Slate 800
C_GREEN  = RGBColor(0x04, 0x78, 0x57) # Emerald 700
C_MUTED  = RGBColor(0x64, 0x74, 0x8B) # Slate 500
C_ALERT  = RGBColor(0xB9, 0x1C, 0x1C) # Red 700

def style_run(run, font_name="Segoe UI", size_pt=10.5, bold=False, italic=False, color=C_DARK):
    run.font.name = font_name
    run.font.size = Pt(size_pt)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = color

def add_p(text="", align=WD_ALIGN_PARAGRAPH.LEFT, space_before=0, space_after=4, line_spacing=1.15):
    p = doc.add_paragraph()
    p.alignment = align
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = line_spacing
    if text:
        r = p.add_run(text)
        style_run(r, size_pt=10.5, color=C_DARK)
    return p

def add_h1(title):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(title)
    style_run(r, font_name="Segoe UI Semibold", size_pt=18, bold=True, color=C_BLUE)
    return p

def add_h2(subtitle):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(subtitle)
    style_run(r, font_name="Segoe UI Semibold", size_pt=13, bold=True, color=C_NAVY)
    return p

def add_h3(subtitle):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(subtitle)
    style_run(r, font_name="Segoe UI Semibold", size_pt=11.5, bold=True, color=C_DARK)
    return p

def add_bullet(text, prefix="• ", bold_prefix="", space_after=3):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.2)
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.15
    
    r_sym = p.add_run(prefix)
    style_run(r_sym, size_pt=10.5, bold=True, color=C_BLUE)
    
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        style_run(r_pre, size_pt=10.5, bold=True, color=C_DARK)
        
    r_txt = p.add_run(text)
    style_run(r_txt, size_pt=10.5, color=C_DARK)
    return p

def add_qa(q_num, question, answer, key_tip=""):
    p_q = doc.add_paragraph()
    p_q.paragraph_format.space_before = Pt(8)
    p_q.paragraph_format.space_after = Pt(2)
    p_q.paragraph_format.keep_with_next = True
    
    r_num = p_q.add_run(f"Q{q_num}: ")
    style_run(r_num, font_name="Segoe UI Semibold", size_pt=11, bold=True, color=C_BLUE)
    
    r_q = p_q.add_run(question)
    style_run(r_q, font_name="Segoe UI Semibold", size_pt=11, bold=True, color=C_NAVY)
    
    p_a = doc.add_paragraph()
    p_a.paragraph_format.left_indent = Inches(0.2)
    p_a.paragraph_format.space_before = Pt(0)
    p_a.paragraph_format.space_after = Pt(key_tip and 2 or 6)
    p_a.paragraph_format.line_spacing = 1.15
    
    r_ans_lbl = p_a.add_run("Answer: ")
    style_run(r_ans_lbl, size_pt=10, bold=True, color=C_GREEN)
    
    r_ans = p_a.add_run(answer)
    style_run(r_ans, size_pt=10, color=C_DARK)
    
    if key_tip:
        p_tip = doc.add_paragraph()
        p_tip.paragraph_format.left_indent = Inches(0.2)
        p_tip.paragraph_format.space_before = Pt(0)
        p_tip.paragraph_format.space_after = Pt(6)
        
        r_tip_lbl = p_tip.add_run("💡 Examiner Winning Tip: ")
        style_run(r_tip_lbl, size_pt=9.5, bold=True, color=C_ALERT)
        
        r_tip = p_tip.add_run(key_tip)
        style_run(r_tip, size_pt=9.5, italic=True, color=C_DARK)

def add_callout(title, text, color=C_BLUE, bg_hex="EFF6FF"):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    c = tbl.rows[0].cells[0]
    c.width = Inches(6.7)
    
    tcPr = c._tc.get_or_add_tcPr()
    tcPr.append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="{bg_hex}"/>'))
    
    # Left border only
    borders_xml = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'  <w:left w:val="single" w:sz="24" w:space="0" w:color="{color.rgb if hasattr(color, "rgb") else "2563EB"}"/>'
        f'  <w:top w:val="none"/>'
        f'  <w:bottom w:val="none"/>'
        f'  <w:right w:val="none"/>'
        f'</w:tcBorders>'
    )
    tcPr.append(borders_xml)
    
    p = c.paragraphs[0]
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.left_indent = Inches(0.1)
    r1 = p.add_run(title + "\n")
    style_run(r1, font_name="Segoe UI Semibold", size_pt=10.5, bold=True, color=color)
    
    r2 = p.add_run(text)
    style_run(r2, size_pt=10, color=C_DARK)
    
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

def set_table_styling(tbl):
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tblPr = tbl._tbl.tblPr
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

def set_cell_shd(cell, fill_hex="F1F5F9"):
    tcPr = cell._tc.get_or_add_tcPr()
    tcPr.append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>'))

# Setup Header and Footer
def setup_header_footer():
    sec = doc.sections[0]
    hdr = sec.header
    p_hdr = hdr.paragraphs[0]
    p_hdr.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r_hdr = p_hdr.add_run("FinTrack: 2-Hour Viva Cram Guide & Project Startup Manual")
    style_run(r_hdr, size_pt=9, italic=True, color=C_MUTED)
    
    ftr = sec.footer
    p_ftr = ftr.paragraphs[0]
    p_ftr.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r_f1 = p_ftr.add_run("Student: Chauhan Om S. (Roll No. 35)   |   Page ")
    style_run(r_f1, size_pt=9.5, color=C_MUTED)
    
    fld1 = OxmlElement('w:fldSimple')
    fld1.set(qn('w:instr'), 'PAGE')
    p_ftr._p.append(fld1)
    
    r_f2 = p_ftr.add_run(" of ")
    style_run(r_f2, size_pt=9.5, color=C_MUTED)
    
    fld2 = OxmlElement('w:fldSimple')
    fld2.set(qn('w:instr'), 'NUMPAGES')
    p_ftr._p.append(fld2)

setup_header_footer()

# ==============================================================================
# TITLE BANNER
# ==============================================================================
p_title = add_p("🎓 FINTRACK: COMPLETE VIVA & STARTUP CRASH GUIDE", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=6, space_after=2)
p_title.runs[0].font.size = Pt(20)
p_title.runs[0].font.name = "Segoe UI Semibold"
p_title.runs[0].font.bold = True
p_title.runs[0].font.color.rgb = C_BLUE

p_sub = add_p("Prepare Entire Project Viva in 2 Hours + 1-Click Startup Guide for Both Projects", align=WD_ALIGN_PARAGRAPH.CENTER, space_after=10)
p_sub.runs[0].font.size = Pt(11.5)
p_sub.runs[0].font.color.rgb = C_MUTED

add_callout(
    "📌 Quick Metadata for Your Viva",
    "• Student Name: Chauhan Om S.  |  Roll No.: 35  |  Course: BCA (Semester 6 / Final Year)\n"
    "• College: Naran Lala College of Professional & Applied Sciences, Navsari\n"
    "• Guide: Ms. Ayushi Mistry  |  Principal: Dr. Sunil Naik  |  Subject: Advanced Web Designing\n"
    "• Project Title: FinTrack - Personal Finance & Expense Tracker (Available in MERN & PHP Stacks)",
    color=C_BLUE, bg_hex="EFF6FF"
)

# ==============================================================================
# SECTION 1: HOW TO START BOTH PROJECTS
# ==============================================================================
add_h1("1. How to Start Both Projects (Step-by-Step)")

add_p(
    "You have two versions of the FinTrack application on your computer. Both feature the exact same React 19 frontend "
    "and user interface, but utilize different backend architectures:"
)

# Comparison table
start_tbl = doc.add_table(rows=7, cols=3)
set_table_styling(start_tbl)

headers = ["Feature / Step", "Project 1: MERN Stack (Folder: Project)", "Project 2: PHP Stack (Folder: project(2))"]
for i, h in enumerate(headers):
    c = start_tbl.rows[0].cells[i]
    set_cell_shd(c, "F1F5F9")
    p = c.paragraphs[0]
    p.paragraph_format.space_before = Pt(3)
    p.paragraph_format.space_after = Pt(3)
    r = p.add_run(h)
    style_run(r, font_name="Segoe UI Semibold", size_pt=9.5, bold=True, color=C_NAVY)

table_rows = [
    ("Backend Architecture", "Node.js (v18+) + Express.js 5 REST API", "Pure PHP 8.x + Apache / Built-in server"),
    ("Database Engine", "MongoDB (NoSQL) with Mongoose 9 ODM", "MySQL / MariaDB via XAMPP with PDO"),
    ("Database Location", "mongodb://localhost:27017/finance-tracker", "localhost:3306 (database: finance_tracker)"),
    ("1-Click Launch Method", "Double-click: start-project.bat in Project", "Double-click: start-project.bat in project(2)"),
    ("Manual Terminal Commands", "Backend: cd server && npm run dev\nFrontend: cd client && npm run dev", "Backend: cd server && php -S localhost:5000 index.php\nFrontend: cd client && npm run dev"),
    ("Default URLs", "Frontend: http://localhost:5173\nBackend: http://localhost:5000", "Frontend: http://localhost:5173\nBackend: http://localhost:5000")
]

for r_idx, (col0, col1, col2) in enumerate(table_rows):
    row = start_tbl.rows[r_idx + 1]
    for c_idx, val in enumerate([col0, col1, col2]):
        c = row.cells[c_idx]
        p = c.paragraphs[0]
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(2)
        r = p.add_run(val)
        style_run(r, size_pt=9, bold=(c_idx==0), color=C_DARK)

start_tbl.rows[0].cells[0].width = Inches(1.8)
start_tbl.rows[0].cells[1].width = Inches(2.4)
start_tbl.rows[0].cells[2].width = Inches(2.5)

add_p("", space_before=2, space_after=4)

add_h2("A. Starting Project 1 (MERN Stack: Folder 'Project')")
add_bullet("Make sure MongoDB is running (MongoDB Compass or local service `mongod`).", "1. Prerequisite: ")
add_bullet("Open folder `c:\\Users\\Asus\\Desktop\\Project` and double-click `start-project.bat`. This automatically opens two terminal windows (Node backend on 5000 + React frontend on 5173) and opens your browser!", "2. One-Click Launch: ")
add_bullet("Login using your account: Email `om40@gmail.com` and password, or click 'Create account' to register a new user.", "3. Login: ")

add_h2("B. Starting Project 2 (PHP + MySQL Stack: Folder 'project(2)')")
add_bullet("Open XAMPP Control Panel and click 'Start' on MySQL (and Apache).", "1. Prerequisite: ")
add_bullet("Open folder `c:\\Users\\Asus\\Desktop\\project(2)` and double-click `start-project.bat`. This launches the PHP backend server on port 5000, Vite React on port 5173, and launches the browser!", "2. One-Click Launch: ")
add_bullet("The PHP backend auto-creates the MySQL tables and seeds default categories on first run! No manual SQL import required.", "3. Database Auto-Setup: ")

doc.add_page_break()

# ==============================================================================
# SECTION 2: 30-SECOND ELEVATOR PITCH & 4 GOLDEN CONCEPTS
# ==============================================================================
add_h1("2. The 30-Second Elevator Pitch & 4 Golden Concepts")

add_callout(
    "🎯 Memorize This Opening Script (What to Say When the Examiner Says 'Tell Me About Your Project'):",
    "\"Good morning respected examiners. My project is FinTrack, a full-stack personal finance and budget management "
    "platform built with modern Single Page Application architecture.\n\n"
    "It empowers individuals to take complete control of their money through automated expense tracking across multiple "
    "payment channels (UPI, Cards, Net Banking, and Cash), proactive budget threshold warnings (at 80% and 100%), milestone "
    "savings goal ledgers, and interactive visual analytics.\n\n"
    "I engineered it with enterprise-grade security including HTTP-only cookie-based JWT authentication, integer-based "
    "minor currency precision (paise) to eliminate floating-point calculation errors, and an adaptive dark/light responsive design.\"",
    color=C_GREEN, bg_hex="ECFDF5"
)

add_h2("The 4 'Golden Concepts' Examiners Look For (High Marks Topics):")

add_bullet(
    "Why? In programming, floating point math has precision glitches (e.g., in JavaScript `0.1 + 0.2 = 0.30000000000000004`). "
    "In banking and financial software, this causes rounding errors. FinTrack stores ₹250.50 as integer `25050` paise, guaranteeing 100% exact math.",
    bold_prefix="1. Minor-Unit Currency Math (Paise Storage): "
)
add_bullet(
    "Why? Most novice developers store JWTs in browser `localStorage`. However, any malicious third-party script or XSS vulnerability "
    "can read `localStorage` and steal the user's token. By setting `httpOnly: true` and `sameSite: 'lax'`, browser JavaScript CANNOT read the cookie, "
    "completely immunizing the system against XSS session hijacking.",
    bold_prefix="2. HTTP-Only Cookie-Based JWT Authentication: "
)
add_bullet(
    "Why? Traditional spreadsheets don't proactively alert users before they run out of money. FinTrack dynamically computes category expenses "
    "against set limits and applies visual color cues: 🟢 Normal (<80%), 🟡 Warning (80%–99%), 🔴 Exceeded (100%+).",
    bold_prefix="3. Dynamic Real-Time Budget Threshold Alerts: "
)
add_bullet(
    "Why? In MERN, all heavy calculations (monthly totals, category percentage shares) execute inside MongoDB's aggregation pipeline "
    "(`$match`, `$group`, `$sum`), returning lightweight results to React without overloading client RAM.",
    bold_prefix="4. Server-Side Aggregation & High-Performance SVG Charts: "
)

# ==============================================================================
# SECTION 3: 5-MINUTE LIVE DEMO SCRIPT
# ==============================================================================
add_h1("3. Step-by-Step 5-Minute Live Demo Script")
add_p("When the examiner says: 'Show me your project running', follow this exact sequence to look calm and professional:")

add_bullet("Open `http://localhost:5173`. Click the Sun/Moon toggle on the top right to show the zero-flicker Dark/Light theme.", bold_prefix="Step 1 (Theme & Guard): ")
add_bullet("Enter email `om40@gmail.com` and password. Click 'Sign in'. Highlight that unauthenticated users are automatically blocked from dashboard pages.", bold_prefix="Step 2 (Login): ")
add_bullet("Show the 4 KPI cards: Total Balance, Total Income, Total Expenses, Savings Rate. Hover over the Area Chart and Donut Chart to show interactive tooltips.", bold_prefix="Step 3 (Dashboard): ")
add_bullet("Change the dropdown from 'This Month' to 'This Year' or 'All Time'. Show that all calculations update dynamically.", bold_prefix="Step 4 (Timeframe Filter): ")
add_bullet("Click 'Add Transaction'. Add an Expense: Title 'College Viva Lunch', Amount ₹300, Category 'Food & Dining', Method 'UPI'. Submit and show the instant toast alert and updated balance.", bold_prefix="Step 5 (Live Transaction): ")
add_bullet("Go to 'Budgets'. Show the 'Food & Dining' bar. Explain the Green (<80%), Amber (80-99%), and Red (100%+) thresholds.", bold_prefix="Step 6 (Budgets): ")
add_bullet("Go to 'Savings Goals'. Show a goal (e.g., 'Laptop Fund'). Click 'Add Money', deposit ₹2,000, and show the progress bar animate forward.", bold_prefix="Step 7 (Goals): ")
add_bullet("Alt-Tab to MongoDB Compass (or phpMyAdmin for PHP stack) and show the record committed in the database in minor units (e.g. `30000` paise). This gets you an immediate A+!", bold_prefix="Step 8 (The Examiner Clincher): ")

doc.add_page_break()

# ==============================================================================
# SECTION 4: TOP 25 VIVA QUESTIONS & SHORT PUNCHY ANSWERS
# ==============================================================================
add_h1("4. Top 25 Viva Questions & Short Punchy Answers")
add_p("Read these questions and answers twice. They cover 95% of questions asked in university BCA/MCA vivas.")

add_h2("Group A: Architecture & Full-Stack Fundamentals")

add_qa(
    1, "What is FinTrack and what is its main objective?",
    "FinTrack is an automated personal financial management web application. Its objective is to help individuals record daily income and expenses, set category-based monthly budgets with real-time threshold warnings, track savings goals, and visualize cash flow trends.",
    "Mention that it replaces manual paper diaries and unstructured Excel sheets."
)

add_qa(
    2, "What is the difference between your MERN project and PHP project?",
    "The client interface is identical (React 19 + Tailwind CSS). In the MERN project (`Project`), the backend is Node.js/Express 5 with MongoDB (NoSQL) and Mongoose ODM. In the PHP project (`project(2)`), the backend is pure PHP 8.x with MySQL (Relational) via PDO. Both provide RESTful JSON APIs.",
    "Examiners love to see that you understand both NoSQL (MongoDB) and SQL (MySQL) paradigms!"
)

add_qa(
    3, "What is a Single Page Application (SPA)? Why React 19?",
    "An SPA loads a single HTML file and dynamically rewrites the page in the browser as the user interacts, without reloading the full page from the server. React 19 provides Virtual DOM for fast rendering, component modularity, and smooth user experience.",
    "Contrast SPA with traditional multi-page websites where every click triggers a full white-screen page reload."
)

add_qa(
    4, "What is a REST API and what HTTP methods do you use?",
    "REST (Representational State Transfer) is a stateless client-server architecture using standard HTTP verbs: GET (fetch transactions/budgets), POST (create transaction/user), PATCH/PUT (update transaction/goal), and DELETE (remove transaction). All responses are in structured JSON.",
    ""
)

add_h2("Group B: Security & Authentication")

add_qa(
    5, "How does authentication work in your application?",
    "Stateless JWT (JSON Web Token) authentication. When a user logs in with valid email and password, the server generates an HMAC-SHA256 signed JWT token containing the `userId`. This token is sent back inside an HTTP-only cookie. On subsequent requests, the server's auth middleware verifies this cookie.",
    ""
)

add_qa(
    6, "Why did you store the JWT in an HTTP-only cookie instead of localStorage?",
    "Storing tokens in `localStorage` makes them accessible to JavaScript, leaving them vulnerable to theft via Cross-Site Scripting (XSS). An HTTP-only cookie cannot be read or stolen by browser JavaScript (`document.cookie`), ensuring maximum session security.",
    "This is one of the most frequent viva questions in web security!"
)

add_qa(
    7, "How do you store passwords securely in the database?",
    "Passwords are never stored in plain text. They are hashed using `bcrypt` (with 12 salt rounds in MERN / `PASSWORD_BCRYPT` cost 10 in PHP). Bcrypt includes a unique random salt for every user, protecting against rainbow table and brute-force attacks.",
    "Mention that bcrypt is a one-way mathematical function; it cannot be decrypted, only compared."
)

add_qa(
    8, "What is CORS and why did you configure it?",
    "CORS stands for Cross-Origin Resource Sharing. Because the frontend runs on port 5173 and backend on port 5000, the browser blocks cross-origin requests by default. We configure CORS on the server with `origin: 'http://localhost:5173'` and `credentials: true` to allow secure cookie transmission.",
    ""
)

add_qa(
    9, "How do you prevent SQL Injection and NoSQL Injection?",
    "In the PHP/MySQL backend, we use PDO prepared statements with parameter binding, which separates SQL code from data. In MERN, Mongoose schema casting and validation automatically sanitize query objects, preventing malicious operator injection.",
    ""
)

doc.add_page_break()

add_h2("Group C: Database Design & Mathematical Precision")

add_qa(
    10, "Why store currency amounts in minor units (paise) instead of decimal floats?",
    "Floating-point representation in computers (IEEE-754 standard) causes rounding imprecisions (e.g. `0.1 + 0.2 = 0.30000000000000004`). In financial apps, this causes accounts to be off by paise. By storing amounts as integers in minor units (₹1 = 100 paise), all additions and subtractions are 100% mathematically exact.",
    "State: 'Real banking systems like Stripe and PayPal always use minor currency units!'"
)

add_qa(
    11, "What are the core database collections / tables?",
    "1. `users` (user credentials and preferences), 2. `categories` (income/expense categories with icons/colors), 3. `transactions` (financial ledger records), 4. `budgets` (category monthly caps), 5. `savingsgoals` (target funds), 6. `goalcontributions` (deposit/withdrawal history).",
    ""
)

add_qa(
    12, "What is database indexing and what indexes did you create?",
    "An index is a data structure (B-Tree) that speeds up search queries without scanning the entire table. In `transactions`, we created compound indexes: `{ userId: 1, date: -1 }` for reverse-chronological transaction feeds and `{ userId: 1, type: 1, date: -1 }` for cash flow reports.",
    "Explain: 'Without an index, the database does a slow full-collection scan. With an index, lookup is O(log N).'"
)

add_qa(
    13, "What happens if a user tries to create overlapping budgets for the same category?",
    "The system enforces a compound index / uniqueness constraint on `{ userId, category, startDate, endDate }`. If a duplicate is submitted, the server rejects it with an HTTP 409 Conflict error, preventing duplicate budget caps.",
    ""
)

add_qa(
    14, "What is the two-tier ledger architecture in Savings Goals?",
    "`SavingsGoal` holds the high-level target and current progress, while `GoalContribution` stores every timestamped deposit and withdrawal with notes. This guarantees an audit trail so the user can verify every transaction that contributed to their savings.",
    ""
)

add_h2("Group D: Frontend UI, UX & React 19")

add_qa(
    15, "How does the Dark / Light theme switcher work?",
    "We use `ThemeContext` in React and Tailwind CSS custom variants (`@custom-variant dark`). The chosen theme is saved in `localStorage`. When toggled, React updates the `dark` class on the root `<html>` element, which immediately updates all Tailwind color variables without refreshing the page.",
    ""
)

add_qa(
    16, "How do Protected Routes work in React Router v7?",
    "We created a `ProtectedRoute` wrapper component that inspects `isAuthenticated` from `AuthContext`. If the user is authenticated, it renders the requested dashboard view (`<Outlet />`); if not authenticated, it automatically redirects them to `/login`.",
    ""
)

add_qa(
    17, "Why did you choose Recharts for data visualization?",
    "Recharts is a declarative charting library built specifically for React using SVG and D3 under the hood. It is lightweight, supports smooth CSS animations, provides responsive auto-resizing containers, and has built-in interactive tooltip support.",
    ""
)

add_qa(
    18, "How do you handle form validation on the client side?",
    "We use React Hook Form for performant, uncontrolled input management with schema validation (required fields, email regex format, positive number limits for amount). This prevents invalid API requests from reaching the server.",
    ""
)

doc.add_page_break()

add_h2("Group E: Budgets, Goals, Testing & Future Enhancements")

add_qa(
    19, "How are budget thresholds calculated and displayed?",
    "Budget utilization is calculated as `(Total Spent / Budget Limit) * 100`. The UI applies three dynamic states: 🟢 Normal (Spent < 80%), 🟡 Warning (80% <= Spent < 100%), and 🔴 Exceeded (Spent >= 100%), giving users proactive warnings before they overspend.",
    ""
)

add_qa(
    20, "What safety check prevents users from over-withdrawing savings goals?",
    "Before processing a withdrawal, the controller checks `if (withdrawalAmount > goal.currentAmount)`. If true, the server aborts the transaction with an HTTP 400 'Withdrawal amount exceeds current saved funds' error.",
    ""
)

add_qa(
    21, "What are Helmet and Express Rate Limit used for?",
    "`helmet` automatically sets security-focused HTTP response headers (`X-Frame-Options` to prevent clickjacking, `X-Content-Type-Options` to prevent MIME-sniffing). `express-rate-limit` restricts clients to 100 requests per 15-minute window, stopping automated brute-force attacks.",
    ""
)

add_qa(
    22, "What types of testing did you perform?",
    "1. Unit Testing: Tested API endpoints and password hashing using Jest and Supertest. 2. Integration Testing: Verified Axios client communication with the backend. 3. Manual Functional Testing: Executed 12 structured test cases (TC-01 to TC-12) covering registration, invalid logins, and budget calculations.",
    ""
)

add_qa(
    23, "What software development lifecycle (SDLC) model was used?",
    "Agile Iterative Prototyping across 4 sprints: Sprint 1 (Requirements & Schema Design), Sprint 2 (Backend REST APIs & Auth Middleware), Sprint 3 (React Frontend, Tailwind CSS & Recharts), and Sprint 4 (Testing, Data Seeding & Optimization).",
    ""
)

add_qa(
    24, "What are the future enhancements for this project?",
    "1. Optical Character Recognition (OCR) to scan paper grocery and dining receipts. 2. Bank statement CSV/PDF auto-import. 3. AI predictive budgeting to forecast deficits. 4. React Native mobile app for Android and iOS.",
    ""
)

add_qa(
    25, "What did you personally learn the most while building this project?",
    "I learned how to architect a decoupled full-stack application, handle monetary values using integer minor units to prevent rounding errors, enforce cookie-based stateless JWT authentication, and optimize MongoDB queries using compound indexing.",
    "Delivering this answer with enthusiasm shows genuine engineering maturity."
)

# ==============================================================================
# SECTION 5: VIVA CONFIDENCE & BODY LANGUAGE RULES
# ==============================================================================
add_h1("5. Golden Rules for Scoring Maximum Marks in Your Viva")

add_bullet("Speak with moderate pace and a friendly smile. Greet the examiners politely when you enter.", bold_prefix="1. First Impressions Count: ")
add_bullet("Do not rush. If an examiner asks a question, pause for 2 seconds, organize your thoughts, and answer clearly.", bold_prefix="2. Listen Fully Before Answering: ")
add_bullet("Never say 'I don't know'. Instead say: 'Sir/Ma'am, in our current architecture we implemented X, but in a future production release we can explore Y.' This shows proactive problem-solving.", bold_prefix="3. If You Don't Know an Answer: ")
add_bullet("Use terms like 'Decoupled Architecture', 'Stateless JWT', 'Minor Currency Units', 'Compound Indexing', 'Mongoose Aggregation', and 'Virtual DOM'. These signal strong technical foundation.", bold_prefix="4. Use Technical Vocabulary: ")
add_bullet("Be proud of your project. You built a complete, enterprise-grade personal finance system with two working backend stacks!", bold_prefix="5. Confidence: ")

# Save DOCX
out_docx = r"c:\Users\Asus\Desktop\Project\documentation\VIVA_AND_PROJECT_STARTUP_GUIDE.docx"
doc.save(out_docx)
print("Saved Guide DOCX to:", out_docx)
