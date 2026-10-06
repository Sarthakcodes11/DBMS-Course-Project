import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        if self._pageNumber == 1:
            # Suppress running header and footer on cover page
            return
        
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#768683"))
        
        # Header
        self.drawString(54, 800, "DBMS Course Project | Campus Placement Management System")
        self.drawRightString(541, 800, "Woxsen University")
        self.setStrokeColor(colors.HexColor("#dbe2de"))
        self.setLineWidth(0.5)
        self.line(54, 792, 541, 792)
        
        # Footer
        self.line(54, 45, 541, 45)
        self.drawString(54, 32, "Sarthak Kulkarni (25WU0102247)")
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(541, 32, page_text)
        self.restoreState()

def build_pdf(filename="Project-Report/DBMS_Project_Report_Sarthak_Kulkarni.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=30,
        alignment=1, # Center
        textColor=colors.black
    )
    
    cover_subtitle = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=18,
        alignment=1,
        textColor=colors.HexColor("#172e2c")
    )
    
    cover_info = ParagraphStyle(
        'CoverInfo',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10.5,
        leading=18,
        alignment=1,
        textColor=colors.black
    )

    h1_style = ParagraphStyle(
        'SectionHeading1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=20,
        textColor=colors.HexColor("#166e58"),
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'SectionHeading2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11.5,
        leading=16,
        textColor=colors.HexColor("#173a32"),
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=14.5,
        textColor=colors.HexColor("#222222"),
        spaceAfter=6
    )

    code_style = ParagraphStyle(
        'CodeBlock',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=7.5,
        leading=10.5,
        textColor=colors.HexColor("#113328"),
        spaceBefore=4,
        spaceAfter=6
    )

    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor("#222222")
    )

    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor("#166e58")
    )

    story = []

    # ==========================================
    # 1. COVER PAGE (Exactly matching template)
    # ==========================================
    story.append(Spacer(1, 40))
    story.append(Paragraph("<b>PROJECT REPORT</b>", title_style))
    story.append(Spacer(1, 45))
    
    story.append(Paragraph("<b>TITLE:</b> Design and Implementation of a Database Management System<br/>for Campus Placement and Recruitment Drive Management System", cover_subtitle))
    story.append(Spacer(1, 55))

    # Woxsen University Emblem Block
    woxsen_html = """
    <font color="#d92525" size="30"><b>W</b></font><font color="#666666" size="26"><b>●</b></font><br/>
    <font color="#172e2c" size="16"><b>WOXSEN</b></font> <font color="#d92525" size="22"><b>U</b></font><br/>
    <font color="#768683" size="9"><b>U N I V E R S I T Y</b></font>
    """
    story.append(Paragraph(woxsen_html, ParagraphStyle('WoxsenLogo', alignment=1, leading=22)))
    story.append(Spacer(1, 65))

    # Student & Evaluation details
    details_text = """
    <b>NAME:</b> SARTHAK KULKARNI<br/><br/>
    <b>ROLL NO:</b> 25WU0102247<br/><br/>
    <b>COURSE NAME:</b> Database Management Systems<br/><br/>
    <b>FACULTY NAME:</b> Dr Kiran Mayee Adavala<br/><br/>
    <b>ACADEMIC YEAR:</b> 2025-2029
    """
    story.append(Paragraph(details_text, cover_info))
    story.append(PageBreak())

    # ==========================================
    # 2. ABSTRACT
    # ==========================================
    story.append(Paragraph("1. Abstract", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#166e58"), spaceAfter=10))
    abstract_text = (
        "The <b>Campus Placement and Recruitment Drive Management System</b> is a comprehensive relational database solution designed to digitize, streamline, and govern higher education placement operations. Managing hundreds of eligible candidates, corporate hiring partners, multi-round interview schedules, and conditional job offers creates complex operational challenges that spreadsheet-based approaches cannot reliably solve. "
        "This project implements a fully normalized 7-table relational database architecture on <b>MySQL 8.0</b>, augmented with declarative integrity constraints and active triggers that enforce strict institutional placement policies (e.g., minimum CGPA validation and selected-only offer assignments). A lightweight <b>Flask REST API</b> backend bridges the relational database with a modern, responsive web user interface. The system ensures data consistency, prevents duplicate applications, blocks unauthorized parent record deletions, and provides real-time analytical reporting."
    )
    story.append(Paragraph(abstract_text, body_style))

    # ==========================================
    # 3. INTRODUCTION AND PROBLEM STATEMENT
    # ==========================================
    story.append(Paragraph("2. Introduction & Problem Statement", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#166e58"), spaceAfter=10))
    story.append(Paragraph("<b>2.1 Introduction:</b> Campus placement drives represent a pivotal operational milestone for academic institutions. Coordinating drives requires synchronizing student profiles, academic qualifications, recruiter requirements, multi-stage interview rounds, and final job offers.", body_style))
    story.append(Paragraph("<b>2.2 Problem Statement:</b> Traditional manual or disconnected spreadsheet workflows suffer from several critical shortcomings:", body_style))
    
    problems = [
        "<b>Ineligible Applications:</b> Students applying to recruitment drives without meeting minimum CGPA cutoffs.",
        "<b>Redundant / Duplicate Submissions:</b> Multiple applications submitted for the same drive by the same student.",
        "<b>Unsynchronized Offer Tracking:</b> Placement offers being recorded for candidates who failed earlier interview stages.",
        "<b>Orphaned Data & Inconsistent Deletions:</b> Deleting departments or companies without properly handling dependent student or drive records.",
        "<b>Lack of Real-Time Analytics:</b> Laborious manual compilation of department-wise placement metrics and salary statistics."
    ]
    for p in problems:
        story.append(Paragraph(f"• {p}", body_style))

    # ==========================================
    # 4. OBJECTIVES AND SCOPE
    # ==========================================
    story.append(Paragraph("3. Objectives & Scope", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#166e58"), spaceAfter=10))
    objectives = [
        "<b>Relational Data Integrity:</b> Structure the core placement domain into 7 normalized tables adhering to Boyce-Codd Normal Form (BCNF).",
        "<b>Automated Business Logic:</b> Enforce institutional rules at the DBMS layer using MySQL 8.0 `BEFORE INSERT` and `BEFORE UPDATE` triggers.",
        "<b>Full-Featured CRUD Dashboard:</b> Provide a web-based portal for managing departments, students, companies, drives, applications, interviews, and placements.",
        "<b>Comprehensive Analytics:</b> Generate real-time department performance reports, drive conversion funnels, and exportable CSV reports."
    ]
    for obj in objectives:
        story.append(Paragraph(f"• {obj}", body_style))

    # ==========================================
    # 5. SOFTWARE & HARDWARE REQUIREMENTS
    # ==========================================
    story.append(Paragraph("4. Software & Hardware Requirements", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#166e58"), spaceAfter=10))
    
    req_data = [
        [Paragraph("<b>Component</b>", table_cell_bold), Paragraph("<b>Specification / Tool</b>", table_cell_bold), Paragraph("<b>Purpose</b>", table_cell_bold)],
        [Paragraph("Operating System", table_cell_style), Paragraph("macOS Sonoma / Linux / Windows 10+", table_cell_style), Paragraph("Development & Execution Host", table_cell_style)],
        [Paragraph("Database Engine", table_cell_style), Paragraph("MySQL Server 8.0.16+", table_cell_style), Paragraph("Relational Storage & Triggers", table_cell_style)],
        [Paragraph("Backend Runtime", table_cell_style), Paragraph("Python 3.11+ / Flask 3.1", table_cell_style), Paragraph("REST API & MySQL Connector", table_cell_style)],
        [Paragraph("Frontend UI", table_cell_style), Paragraph("HTML5, Vanilla CSS3, JavaScript ES6+", table_cell_style), Paragraph("Interactive Management Dashboard", table_cell_style)],
        [Paragraph("Version Control", table_cell_style), Paragraph("Git 2.40+ / GitHub", table_cell_style), Paragraph("Code Collaboration & Submission", table_cell_style)],
        [Paragraph("RAM / Storage", table_cell_style), Paragraph("Min. 4 GB RAM / 500 MB Free Disk", table_cell_style), Paragraph("Local Runtime Environment", table_cell_style)]
    ]
    t_req = Table(req_data, colWidths=[110, 160, 215])
    t_req.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#eaf4ee")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#dbe2de")),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_req)
    story.append(PageBreak())

    # ==========================================
    # 6. ER DIAGRAM & RELATIONAL SCHEMA
    # ==========================================
    story.append(Paragraph("5. Entity-Relationship (ER) Diagram", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#166e58"), spaceAfter=10))
    story.append(Paragraph("The system is modeled with seven core entities with primary key - foreign key relationships and strict cardinalities:", body_style))
    
    if os.path.exists("Project-Report/er_diagram.png"):
        story.append(Image("Project-Report/er_diagram.png", width=6.5*inch, height=4.2*inch))
        story.append(Paragraph("<i>Figure 1: Entity-Relationship Diagram with Primary Keys, Foreign Keys, and Cardinalities</i>", ParagraphStyle('Caption', parent=styles['Normal'], alignment=1, fontSize=8, textColor=colors.HexColor("#768683"), spaceBefore=4)))
    
    story.append(Spacer(1, 10))

    # ==========================================
    # 7. RELATIONAL SCHEMA & NORMALIZATION
    # ==========================================
    story.append(Paragraph("6. Relational Schema & Normalization Analysis", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#166e58"), spaceAfter=10))
    
    norm_text = """
    <b>Relational Schema:</b><br/>
    • <b>Department</b> (<u>dept_id</u>, dept_name, hod_name)<br/>
    • <b>Student</b> (<u>student_id</u>, name, dept_id*, cgpa, email)<br/>
    • <b>Company</b> (<u>company_id</u>, name, sector, hr_contact)<br/>
    • <b>Drive</b> (<u>drive_id</u>, company_id*, role, ctc, drive_date, min_cgpa)<br/>
    • <b>Application</b> (<u>application_id</u>, student_id*, drive_id*, status)<br/>
    • <b>Interview</b> (<u>interview_id</u>, application_id*, round_no, result)<br/>
    • <b>Placement</b> (<u>placement_id</u>, application_id*, package, placement_date)<br/><br/>
    <b>Proof of Normalization:</b><br/>
    • <b>First Normal Form (1NF):</b> Every attribute contains only atomic (indivisible) values. All tables have uniquely identifiable primary keys, and no repeating groups exist.<br/>
    • <b>Second Normal Form (2NF):</b> All relations are in 1NF and every non-prime attribute is fully functionally dependent on the entire primary key (no partial dependencies on composite keys).<br/>
    • <b>Third Normal Form (3NF):</b> All relations are in 2NF and there are no transitive dependencies (no non-prime attribute depends on another non-prime attribute).<br/>
    • <b>Boyce-Codd Normal Form (BCNF):</b> For every functional dependency <i>X → Y</i> across all relations, the determinant <i>X</i> is a super key. Hence, the schema achieves BCNF.
    """
    story.append(Paragraph(norm_text, body_style))
    story.append(PageBreak())

    # ==========================================
    # 8. DATA DICTIONARY
    # ==========================================
    story.append(Paragraph("7. Data Dictionary", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#166e58"), spaceAfter=10))

    tables_dict = [
        ("Student", [
            ("student_id", "INT", "No", "PK, Auto Increment", "Unique student ID"),
            ("name", "VARCHAR(150)", "No", "-", "Student's full name"),
            ("dept_id", "INT", "No", "FK (Department.dept_id)", "Enrolled department"),
            ("cgpa", "DECIMAL(3,2)", "No", "CHECK (cgpa BETWEEN 0 AND 10)", "Cumulative GPA"),
            ("email", "VARCHAR(150)", "No", "UNIQUE", "Institutional email")
        ]),
        ("Drive", [
            ("drive_id", "INT", "No", "PK, Auto Increment", "Unique recruitment drive ID"),
            ("company_id", "INT", "No", "FK (Company.company_id)", "Organizing company"),
            ("role", "VARCHAR(150)", "No", "-", "Designation / Job Role"),
            ("ctc", "DECIMAL(8,2)", "No", "CHECK (ctc > 0)", "Compensation in LPA"),
            ("drive_date", "DATE", "No", "-", "Date of recruitment drive"),
            ("min_cgpa", "DECIMAL(3,2)", "No", "DEFAULT 7.00", "Eligibility CGPA cutoff")
        ]),
        ("Application", [
            ("application_id", "INT", "No", "PK, Auto Increment", "Unique application ID"),
            ("student_id", "INT", "No", "FK (Student.student_id)", "Candidate ID"),
            ("drive_id", "INT", "No", "FK (Drive.drive_id)", "Recruitment drive ID"),
            ("status", "ENUM", "No", "DEFAULT 'Applied'", "Applied | Interview | Selected | Rejected")
        ]),
        ("Placement", [
            ("placement_id", "INT", "No", "PK, Auto Increment", "Unique placement record ID"),
            ("application_id", "INT", "No", "FK (Application.application_id), UNIQUE", "One offer per application"),
            ("package", "DECIMAL(8,2)", "No", "CHECK (package > 0)", "Final offered CTC (LPA)"),
            ("placement_date", "DATE", "No", "-", "Date of offer issuance")
        ])
    ]

    for t_name, fields in tables_dict:
        story.append(Paragraph(f"<b>Table: {t_name}</b>", h2_style))
        t_data = [[Paragraph("<b>Attribute</b>", table_cell_bold), Paragraph("<b>Type</b>", table_cell_bold), Paragraph("<b>Null</b>", table_cell_bold), Paragraph("<b>Key / Constraint</b>", table_cell_bold), Paragraph("<b>Description</b>", table_cell_bold)]]
        for f in fields:
            t_data.append([Paragraph(f[0], table_cell_style), Paragraph(f[1], table_cell_style), Paragraph(f[2], table_cell_style), Paragraph(f[3], table_cell_style), Paragraph(f[4], table_cell_style)])
        
        tbl = Table(t_data, colWidths=[85, 80, 35, 150, 135])
        tbl.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#eaf4ee")),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#dbe2de")),
            ('TOPPADDING', (0,0), (-1,-1), 3),
            ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ]))
        story.append(tbl)
        story.append(Spacer(1, 6))

    story.append(PageBreak())

    # ==========================================
    # 9. SQL COMMANDS & TRIGGERS
    # ==========================================
    story.append(Paragraph("8. SQL Commands & Active Triggers (DDL & DML)", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#166e58"), spaceAfter=10))

    story.append(Paragraph("<b>8.1 DDL Trigger Implementation:</b>", h2_style))
    trigger_code = """
DELIMITER $$
-- Trigger 1: Validate Student CGPA against Drive requirement before Application
CREATE TRIGGER application_eligibility_insert BEFORE INSERT ON Application FOR EACH ROW
BEGIN
  IF (SELECT cgpa FROM Student WHERE student_id=NEW.student_id) < 
     (SELECT min_cgpa FROM Drive WHERE drive_id=NEW.drive_id) THEN 
     SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT='Student does not meet the drive CGPA requirement.';
  END IF;
END$$

-- Trigger 2: Prevent Placement insertion unless Application status is 'Selected'
CREATE TRIGGER placement_selected_insert BEFORE INSERT ON Placement FOR EACH ROW
BEGIN
  IF COALESCE((SELECT status FROM Application WHERE application_id=NEW.application_id),'')<>'Selected' THEN 
     SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT='Only a Selected application can receive a placement.';
  END IF;
END$$
DELIMITER ;
    """
    story.append(Paragraph(f"<pre>{trigger_code.strip()}</pre>", code_style))

    story.append(Paragraph("<b>8.2 DML Sample Seeding:</b>", h2_style))
    dml_code = """
INSERT INTO Department (dept_id, dept_name, hod_name) VALUES (1, 'CSE', 'Dr. Coordinator'), (2, 'ECE', 'Dr. Coordinator');
INSERT INTO Student (student_id, name, dept_id, cgpa, email) VALUES (1, 'Aarav Mehta', 1, 8.90, 'aarav@example.edu');
INSERT INTO Drive (drive_id, company_id, role, ctc, drive_date, min_cgpa) VALUES (101, 1, 'Analyst', 6.50, '2026-08-11', 7.00);
INSERT INTO Application (application_id, student_id, drive_id, status) VALUES (1, 1, 101, 'Selected');
INSERT INTO Placement (placement_id, application_id, package, placement_date) VALUES (1, 1, 6.50, '2026-08-11');
    """
    story.append(Paragraph(f"<pre>{dml_code.strip()}</pre>", code_style))

    # ==========================================
    # 10. QUERIES AND OUTPUTS
    # ==========================================
    story.append(Paragraph("9. Analytical SQL Queries & Benchmark Outputs", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#166e58"), spaceAfter=10))

    story.append(Paragraph("<b>9.1 Presentation-II Faculty Join Query (Department-wise Placement Report):</b>", h2_style))
    faculty_sql = """
SELECT d.dept_name, COUNT(p.placement_id) AS placed_count, COALESCE(MAX(p.package), 0) AS top_package
FROM Department d
LEFT JOIN Student s ON s.dept_id = d.dept_id
LEFT JOIN Application a ON a.student_id = s.student_id
LEFT JOIN Placement p ON p.application_id = a.application_id
GROUP BY d.dept_id, d.dept_name
ORDER BY placed_count DESC;
    """
    story.append(Paragraph(f"<pre>{faculty_sql.strip()}</pre>", code_style))
    
    # Query output table
    q_out_data = [
        [Paragraph("<b>Department (dept_name)</b>", table_cell_bold), Paragraph("<b>Placed Count</b>", table_cell_bold), Paragraph("<b>Top Package (LPA)</b>", table_cell_bold)],
        [Paragraph("CSE", table_cell_style), Paragraph("1", table_cell_style), Paragraph("₹ 6.5 LPA", table_cell_style)],
        [Paragraph("IT", table_cell_style), Paragraph("1", table_cell_style), Paragraph("₹ 8.0 LPA", table_cell_style)],
        [Paragraph("ECE", table_cell_style), Paragraph("0", table_cell_style), Paragraph("—", table_cell_style)],
        [Paragraph("ME", table_cell_style), Paragraph("0", table_cell_style), Paragraph("—", table_cell_style)]
    ]
    t_qout = Table(q_out_data, colWidths=[180, 150, 155])
    t_qout.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#eaf4ee")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#dbe2de")),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_qout)
    story.append(PageBreak())

    # ==========================================
    # 11. TESTING & RESULTS
    # ==========================================
    story.append(Paragraph("10. Test Cases & Observed Outcomes", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#166e58"), spaceAfter=10))
    story.append(Paragraph("Comprehensive tests conducted to verify relational constraints, trigger enforcement, and CRUD integrity:", body_style))

    test_data = [
        [Paragraph("<b>Test ID</b>", table_cell_bold), Paragraph("<b>Scenario</b>", table_cell_bold), Paragraph("<b>Test Input</b>", table_cell_bold), Paragraph("<b>Expected Behavior</b>", table_cell_bold), Paragraph("<b>Status</b>", table_cell_bold)],
        [Paragraph("TC-01", table_cell_style), Paragraph("Student Insert", table_cell_style), Paragraph("Name: Aarav, CGPA: 8.90", table_cell_style), Paragraph("Record inserted successfully in MySQL", table_cell_style), Paragraph("<font color='#166e58'><b>PASS</b></font>", table_cell_style)],
        [Paragraph("TC-02", table_cell_style), Paragraph("Duplicate Email", table_cell_style), Paragraph("Existing email: aarav@example.edu", table_cell_style), Paragraph("Blocked by UNIQUE constraint (1062)", table_cell_style), Paragraph("<font color='#166e58'><b>PASS</b></font>", table_cell_style)],
        [Paragraph("TC-03", table_cell_style), Paragraph("CGPA Cutoff", table_cell_style), Paragraph("Student CGPA: 6.5 < Drive Cutoff: 7.0", table_cell_style), Paragraph("Blocked by application_eligibility_insert trigger", table_cell_style), Paragraph("<font color='#166e58'><b>PASS</b></font>", table_cell_style)],
        [Paragraph("TC-04", table_cell_style), Paragraph("Selected-Only Offer", table_cell_style), Paragraph("Placement for 'Interview' status app", table_cell_style), Paragraph("Blocked by placement_selected_insert trigger", table_cell_style), Paragraph("<font color='#166e58'><b>PASS</b></font>", table_cell_style)],
        [Paragraph("TC-05", table_cell_style), Paragraph("One Offer Per App", table_cell_style), Paragraph("2nd Placement for same application_id", table_cell_style), Paragraph("Blocked by UNIQUE constraint on application_id", table_cell_style), Paragraph("<font color='#166e58'><b>PASS</b></font>", table_cell_style)],
        [Paragraph("TC-06", table_cell_style), Paragraph("Foreign Key Delete", table_cell_style), Paragraph("Delete Department with enrolled students", table_cell_style), Paragraph("Blocked by RESTRICT constraint (1451)", table_cell_style), Paragraph("<font color='#166e58'><b>PASS</b></font>", table_cell_style)],
        [Paragraph("TC-07", table_cell_style), Paragraph("Zero-Placement Dept", table_cell_style), Paragraph("Report query on ECE/ME (0 offers)", table_cell_style), Paragraph("Departments appear with placed_count = 0", table_cell_style), Paragraph("<font color='#166e58'><b>PASS</b></font>", table_cell_style)]
    ]
    t_test = Table(test_data, colWidths=[40, 95, 140, 160, 50])
    t_test.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#eaf4ee")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#dbe2de")),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_test)
    story.append(Spacer(1, 14))

    # ==========================================
    # 12. UI DESIGN & IMPLEMENTATION
    # ==========================================
    story.append(Paragraph("11. UI Architecture & Implementation Details", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#166e58"), spaceAfter=10))
    ui_desc = """
    <b>Technology Stack & Architecture:</b><br/>
    • <b>Presentation Layer (Frontend):</b> Single-Page Application (SPA) designed with semantic HTML5, DM Sans & Manrope typography, dynamic dialog modals, relational dropdowns, and instantaneous search filtering.<br/>
    • <b>Application Layer (Backend):</b> Flask REST API providing state synchronization (`/api/state`) and generic parameterized mutation routes (`/api/&lt;table&gt;` for POST, PUT, DELETE) with strict request body validation.<br/>
    • <b>Persistence Layer (Database):</b> MySQL 8.0 InnoDB engine managing transactions, foreign key cascades, and trigger execution.<br/>
    • <b>Security Controls:</b> Same-origin policy checks, SQL parameterized bindings to prevent SQL Injection, and `X-Frame-Options: DENY` headers.
    """
    story.append(Paragraph(ui_desc, body_style))

    # ==========================================
    # 13. CONCLUSION & REFERENCES
    # ==========================================
    story.append(Paragraph("12. Conclusion & Future Enhancements", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#166e58"), spaceAfter=10))
    conc_text = """
    <b>Conclusion:</b> The developed Campus Placement Management System successfully satisfies all course requirements. It replaces fragile manual tracking with a robust relational model, active business rule enforcement, and a real-time responsive web dashboard.<br/><br/>
    <b>Future Enhancements:</b><br/>
    1. Automated PDF resume parsing and algorithmic skill matching for drive roles.<br/>
    2. Role-Based Access Control (RBAC) with JWT student and recruiter login portals.<br/>
    3. Automated SMS / Email dispatch for interview round notifications and offer release.
    """
    story.append(Paragraph(conc_text, body_style))
    story.append(Spacer(1, 8))

    story.append(Paragraph("13. References & Appendix", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#166e58"), spaceAfter=10))
    ref_text = """
    <b>References:</b><br/>
    [1] Silberschatz, A., Korth, H. F., & Sudarshan, S. <i>Database System Concepts</i> (7th ed.). McGraw-Hill.<br/>
    [2] MySQL 8.0 Reference Manual: Triggers, Constraints & Foreign Key Relations. Oracle Corporation.<br/>
    [3] Flask Documentation (3.1.x): Application Design & RESTful APIs. Pallets Projects.<br/><br/>
    <b>Appendix - Public GitHub Repository:</b><br/>
    • <b>Repository URL:</b> <font color="#166e58"><u>https://github.com/Sarthakcodes11/DBMS-Course-Project</u></font>
    """
    story.append(Paragraph(ref_text, body_style))

    # Build the document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Report PDF built successfully: {filename}")

if __name__ == '__main__':
    build_pdf()
