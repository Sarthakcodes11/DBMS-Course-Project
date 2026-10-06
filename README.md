# Campus Placement & Recruitment Drive Management System
A relational DBMS application covering students, departments, companies, drives, applications, interviews and placement offers.

Student name: **fill in your name**  
Roll number: **fill in your roll number**  
Course / faculty: **fill in your details**

The supplied placement slides name Sarthak Kulkarni (25WU0102247). This project leaves author details blank rather than assuming that is your identity.

## Windows setup (MySQL demo)
1. Install Python 3.11+ and MySQL Server / Workbench 8.0.16+.
2. Open MySQL Workbench and connect to your local server.
3. Run `Presentation-II/schema.sql`, then `Presentation-II/seed.sql` once in an empty database.
4. In a terminal opened in this folder: `python -m pip install -r requirements.txt`.
5. Copy `.env.example` to `.env`. Set MYSQL_PASSWORD to your real MySQL password.
6. Run `python app.py` and open http://127.0.0.1:5000.
7. Confirm the banner says **MySQL connected**. If it instead says preview, fix your database settings and refresh; preview data is not acceptable proof of MySQL connectivity.

## Demo sequence
- Students → Add student → enter a new name, department, CGPA and unique email.
- Show the inserted student in the table and run `SELECT * FROM Student;` in Workbench.
- Delete that unreferenced student, show the UI and rerun the query.
- Show the selected-only placement rule and department report.
- Screenshot every screen and before/after states using your real running app.

## Features
Seven-table CRUD, search, CSV export, responsive layout, relational dropdowns, CGPA eligibility, selected-only placements, restrictive foreign-key deletion, unique applications / email / interview rounds / offers, reporting.
Amounts are in lakhs per annum (LPA). Preview uses the PDF's five students and two placements. The provided PDF's CSE count of 3 conflicts with its dataset (actual CSE 1, IT 1); reports use correct joins with zero-placement departments included.

## Submission
Create your own public GitHub repository `DBMS-Course-Project`, retain the four folders, fill in author details, add your own original Presentation-I / II / III slides, actual screenshots, assigned query solution and final report PDF. Hard report deadline in supplied instructions: 10 October 2026. Do not claim scaffold files or the checklist are your finished report. Explain and adapt the code yourself for the original-work requirement.

The live hosted site is an interactive browser-local preview. The Flask app is the real MySQL version. It binds to localhost and is intended for an academic demonstration, not an internet-facing multiuser deployment. No user authentication is implemented.

Validation: frontend script syntax and behavioral checks plus Python compilation. MySQL integration must be run on your machine; no MySQL service was available in the build environment.
