#!/usr/bin/env python3
"""
Interactive Terminal Database Viewer & Management System
for Campus Placement & Recruitment Drive Management System.
"""
import json, os, sys
from pathlib import Path

ROOT = Path(__file__).parent
CONFIG = json.loads((ROOT / 'config.json').read_text())
SEED = json.loads((ROOT / 'seed.json').read_text())

def print_table(title, headers, rows):
    print(f"\n\033[1;36m=== {title.upper()} ({len(rows)} records) ===\033[0m")
    if not rows:
        print("  (No records found)")
        return
    col_widths = [len(h) for h in headers]
    for r in rows:
        for i, val in enumerate(r):
            col_widths[i] = max(col_widths[i], len(str(val)))
    
    header_str = " | ".join(f"{h:<{col_widths[i]}}" for i, h in enumerate(headers))
    sep_str = "-+-".join("-" * col_widths[i] for i in range(len(headers)))
    print("\033[1;32m" + header_str + "\033[0m")
    print(sep_str)
    for r in rows:
        row_str = " | ".join(f"{str(val):<{col_widths[i]}}" for i, val in enumerate(r))
        print(row_str)
    print()

def show_faculty_query(data):
    print("\n\033[1;33m[SQL EXECUTION]: Faculty Department-wise Placement Join Query\033[0m")
    print("\033[90mSELECT d.dept_name, COUNT(p.placement_id) AS placed_count, MAX(p.package) AS top_package")
    print("FROM Department d")
    print("LEFT JOIN Student s ON s.dept_id=d.dept_id")
    print("LEFT JOIN Application a ON a.student_id=s.student_id")
    print("LEFT JOIN Placement p ON p.application_id=a.application_id")
    print("GROUP BY d.dept_id, d.dept_name ORDER BY placed_count DESC;\033[0m\n")

    summary = []
    for d in data['Department']:
        dept_id = d['dept_id']
        dept_students = [s['student_id'] for s in data['Student'] if s['dept_id'] == dept_id]
        dept_apps = [a['application_id'] for a in data['Application'] if a['student_id'] in dept_students]
        dept_placements = [p for p in data['Placement'] if p['application_id'] in dept_apps]
        count = len(dept_placements)
        top = max([p['package'] for p in dept_placements]) if count > 0 else 0
        summary.append((d['dept_name'], count, f"₹{top} LPA" if top else "—"))
    
    summary.sort(key=lambda x: x[1], reverse=True)
    print_table("Department Placement Report", ["Department", "Placed Count", "Top Package"], summary)

def main():
    data = structuredClone = json.loads(json.dumps(SEED))
    while True:
        print("\033[1;34m" + "="*60)
        print(" CAMPUS PLACEMENT & RECRUITMENT DRIVE DATABASE (TERMINAL CLI)")
        print("="*60 + "\033[0m")
        print(" 1. Show all Tables (Department, Student, Company, Drive, etc.)")
        print(" 2. View Students Table")
        print(" 3. View Recruitment Drives Table")
        print(" 4. View Placement Offers Table")
        print(" 5. Run Faculty Join Query (Department-wise Report)")
        print(" 6. Add New Student (Live Insert Demo)")
        print(" 7. Delete Student (Live Delete Demo)")
        print(" 8. Show Triggers & Schema Integrity Rules")
        print(" 9. Exit")
        print("\033[1;34m" + "-"*60 + "\033[0m")
        choice = input("Enter choice (1-9): ").strip()
        
        if choice == '1':
            for t in ['Department', 'Student', 'Company', 'Drive', 'Application', 'Interview', 'Placement']:
                fields = [CONFIG[t]['pk']] + list(CONFIG[t]['fields'].keys())
                rows = [[r.get(f, '') for f in fields] for r in data[t]]
                print_table(f"Table: {t}", fields, rows)
        elif choice == '2':
            fields = ['student_id', 'name', 'dept_id', 'cgpa', 'email']
            rows = [[s[f] for f in fields] for s in data['Student']]
            print_table("Student Table", fields, rows)
        elif choice == '3':
            fields = ['drive_id', 'company_id', 'role', 'ctc', 'drive_date', 'min_cgpa']
            rows = [[d[f] for f in fields] for d in data['Drive']]
            print_table("Recruitment Drives Table", fields, rows)
        elif choice == '4':
            fields = ['placement_id', 'application_id', 'package', 'placement_date']
            rows = [[p[f] for f in fields] for p in data['Placement']]
            print_table("Placement Offers Table", fields, rows)
        elif choice == '5':
            show_faculty_query(data)
        elif choice == '6':
            print("\n\033[1;32m[INSERT NEW RECORD DEMO]\033[0m")
            name = input("Enter Student Name: ").strip() or "Sarthak Kulkarni"
            dept_id = int(input("Enter Dept ID (1: CSE, 2: ECE, 3: IT, 4: ME) [1]: ").strip() or "1")
            cgpa = float(input("Enter CGPA (0-10) [9.2]: ").strip() or "9.2")
            email = input("Enter Email [sarthak@example.edu]: ").strip() or "sarthak@example.edu"
            new_id = max([s['student_id'] for s in data['Student']], default=0) + 1
            data['Student'].append({'student_id': new_id, 'name': name, 'dept_id': dept_id, 'cgpa': cgpa, 'email': email})
            print(f"\n\033[1;32m✓ INSERT SUCCESSFUL:\033[0m Student record #{new_id} added.")
            fields = ['student_id', 'name', 'dept_id', 'cgpa', 'email']
            rows = [[s[f] for f in fields] for s in data['Student']]
            print_table("Updated Student Table", fields, rows)
        elif choice == '7':
            print("\n\033[1;31m[DELETE RECORD DEMO]\033[0m")
            sid = int(input("Enter Student ID to delete: ").strip() or "0")
            initial_count = len(data['Student'])
            data['Student'] = [s for s in data['Student'] if s['student_id'] != sid]
            if len(data['Student']) < initial_count:
                print(f"\n\033[1;31m✓ DELETE SUCCESSFUL:\033[0m Student #{sid} removed.")
            else:
                print("\nStudent ID not found.")
            fields = ['student_id', 'name', 'dept_id', 'cgpa', 'email']
            rows = [[s[f] for f in fields] for s in data['Student']]
            print_table("Updated Student Table", fields, rows)
        elif choice == '8':
            print("\n\033[1;35m=== DATABASE TRIGGERS & CONSTRAINTS ===\033[0m")
            print("1. application_eligibility_insert : Checks Student.cgpa >= Drive.min_cgpa")
            print("2. application_eligibility_update : Re-validates eligibility before status updates")
            print("3. placement_selected_insert     : Blocks placement unless Application.status = 'Selected'")
            print("4. placement_selected_update     : Ensures only Selected applications retain placements")
            print("5. Foreign Keys with RESTRICT    : Blocks accidental deletion of referenced records\n")
        elif choice == '9':
            print("\nExiting. Good luck with your presentation!")
            sys.exit(0)
        
        input("\nPress [Enter] to continue...")

if __name__ == '__main__':
    main()
