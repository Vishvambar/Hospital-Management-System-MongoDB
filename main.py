"""
Interactive CLI for Task 4: Hospital Management System (MongoDB Backend).
Provides comprehensive menus for Departments, Doctors, Patients,
Appointments, Medical Reports, $lookup Analytics, and Visual Dashboards.
"""

import sys
from tabulate import tabulate
from models import (
    DepartmentService,
    DoctorService,
    PatientService,
    AppointmentService,
    MedicalReportService
)
from seed_data import seed_hospital_data
from test_all_operations import run_tests
from visualize_hospital import generate_all_visualizations


def clear_screen():
    print("\n" + "-" * 75)


def get_input(prompt: str, default: str = None) -> str:
    val = input(f"{prompt} " + (f"[{default}]: " if default else ": ")).strip()
    return val if val else (default if default is not None else "")


def print_table(data, headers="keys", title=None):
    if title:
        print(f"\n--- {title} ---")
    if not data:
        print("[!] No records found.")
        return
    print(tabulate(data, headers=headers, tablefmt="fancy_grid"))


# ==============================================================================
# SUBMENUS
# ==============================================================================
def handle_departments():
    while True:
        clear_screen()
        print("                 === DEPARTMENTS MANAGEMENT ===")
        print("  [1] List All Departments")
        print("  [2] Add New Department")
        print("  [3] Update Department (Beds / Head)")
        print("  [4] Delete Department")
        print("  [0] Back to Main Menu")
        choice = get_input("Select option (0-4)")

        if choice == "0":
            break
        elif choice == "1":
            print_table(DepartmentService.get_all(), title="CLINICAL DEPARTMENTS")
            input("\nPress Enter to continue...")
        elif choice == "2":
            d_id = get_input("Department ID (e.g. DEP-ENT)")
            name = get_input("Department Name")
            loc = get_input("Location / Floor", "Block B, Floor 2")
            head = get_input("Head Doctor")
            beds = int(get_input("Total Beds", "20"))
            DepartmentService.create(d_id, name, loc, head, beds)
            print(f"[✓] Department '{name}' created successfully!")
            input("\nPress Enter to continue...")
        elif choice == "3":
            d_id = get_input("Department ID to update")
            beds = get_input("New Bed Count (leave blank to keep)")
            head = get_input("New Head Doctor (leave blank to keep)")
            up = {}
            if beds:
                up["total_beds"] = int(beds)
            if head:
                up["head_doctor"] = head
            if up:
                DepartmentService.update(d_id, **up)
                print("[✓] Department updated successfully!")
            input("\nPress Enter to continue...")
        elif choice == "4":
            d_id = get_input("Department ID to delete")
            del_c = DepartmentService.delete(d_id)
            print(f"[✓] Deleted {del_c} department record(s).")
            input("\nPress Enter to continue...")


def handle_doctors():
    while True:
        clear_screen()
        print("                   === DOCTORS DIRECTORY ===")
        print("  [1] List All Doctors")
        print("  [2] View Doctors by Department")
        print("  [3] Register New Doctor")
        print("  [4] Update Doctor (Fee / Availability)")
        print("  [5] Delete Doctor")
        print("  [0] Back to Main Menu")
        choice = get_input("Select option (0-5)")

        if choice == "0":
            break
        elif choice == "1":
            docs = DoctorService.get_all()
            for d in docs:
                d['available_days'] = ", ".join(d.get('available_days', []))
            print_table(docs, title="MEDICAL DOCTORS ROSTER")
            input("\nPress Enter to continue...")
        elif choice == "2":
            d_id = get_input("Enter Department ID (e.g. DEP-CARD, DEP-NEUR)")
            docs = DoctorService.get_by_dept(d_id)
            for d in docs:
                d['available_days'] = ", ".join(d.get('available_days', []))
            print_table(docs, title=f"DOCTORS IN {d_id}")
            input("\nPress Enter to continue...")
        elif choice == "3":
            doc_id = get_input("Doctor ID (e.g. DOC-110)")
            name = get_input("Doctor Name")
            spec = get_input("Specialization")
            d_id = get_input("Department ID")
            email = get_input("Email")
            phone = get_input("Phone")
            fee = float(get_input("Consultation Fee (₹)", "1000"))
            days_raw = get_input("Available Days (comma-separated)", "Mon, Wed, Fri")
            days = [d.strip() for d in days_raw.split(",")]
            DoctorService.create(doc_id, name, spec, d_id, email, phone, fee, days)
            print(f"[✓] Doctor '{name}' registered successfully!")
            input("\nPress Enter to continue...")
        elif choice == "4":
            doc_id = get_input("Doctor ID to update")
            fee = get_input("New Consultation Fee (leave blank to keep)")
            up = {}
            if fee:
                up["consultation_fee"] = float(fee)
            if up:
                DoctorService.update(doc_id, **up)
                print("[✓] Doctor details updated!")
            input("\nPress Enter to continue...")
        elif choice == "5":
            doc_id = get_input("Doctor ID to delete")
            del_c = DoctorService.delete(doc_id)
            print(f"[✓] Deleted {del_c} doctor record.")
            input("\nPress Enter to continue...")


def handle_patients():
    while True:
        clear_screen()
        print("                  === PATIENTS DIRECTORY ===")
        print("  [1] List All Patients")
        print("  [2] Search Patients (by Name / Contact / Blood Group)")
        print("  [3] Register New Patient")
        print("  [4] Update Patient Admission Status")
        print("  [5] Delete Patient Record")
        print("  [0] Back to Main Menu")
        choice = get_input("Select option (0-5)")

        if choice == "0":
            break
        elif choice == "1":
            print_table(PatientService.get_all(), title="REGISTERED PATIENTS")
            input("\nPress Enter to continue...")
        elif choice == "2":
            kw = get_input("Enter search keyword")
            results = PatientService.search(kw)
            print_table(results, title=f"SEARCH RESULTS FOR '{kw}'")
            input("\nPress Enter to continue...")
        elif choice == "3":
            pid = get_input("Patient ID (e.g. PAT-214)")
            name = get_input("Full Name")
            age = int(get_input("Age"))
            gender = get_input("Gender (Male/Female/Other)", "Male")
            contact = get_input("Contact Phone")
            bg = get_input("Blood Group", "O+")
            econtact = get_input("Emergency Contact")
            status = get_input("Status (Outpatient/Admitted/Discharged)", "Outpatient")
            PatientService.create(pid, name, age, gender, contact, bg, econtact, status)
            print(f"[✓] Patient '{name}' registered successfully!")
            input("\nPress Enter to continue...")
        elif choice == "4":
            pid = get_input("Patient ID to update")
            new_st = get_input("New Status (Outpatient/Admitted/Discharged)")
            PatientService.update(pid, status=new_st)
            print("[✓] Patient status updated successfully!")
            input("\nPress Enter to continue...")
        elif choice == "5":
            pid = get_input("Patient ID to delete")
            del_c = PatientService.delete(pid)
            print(f"[✓] Deleted {del_c} patient record.")
            input("\nPress Enter to continue...")


def handle_appointments():
    while True:
        clear_screen()
        print("                === APPOINTMENTS & SCHEDULING ===")
        print("  [1] View Detailed Appointments ($lookup Joins)")
        print("  [2] Book New Appointment")
        print("  [3] Update Appointment Status (Completed / Cancelled)")
        print("  [4] Delete / Cancel Appointment")
        print("  [0] Back to Main Menu")
        choice = get_input("Select option (0-4)")

        if choice == "0":
            break
        elif choice == "1":
            detailed = AppointmentService.get_detailed_appointments()
            print_table(detailed, title="SCHEDULED & COMPLETED APPOINTMENTS")
            input("\nPress Enter to continue...")
        elif choice == "2":
            apt_id = get_input("Appointment ID (e.g. APT-320)")
            pid = get_input("Patient ID (e.g. PAT-201)")
            doc_id = get_input("Doctor ID (e.g. DOC-101)")
            adate = get_input("Date (YYYY-MM-DD)", "2026-10-31")
            slot = get_input("Time Slot", "11:00 AM")
            reason = get_input("Consultation Reason", "General Checkup")
            fee = float(get_input("Fee (₹)", "1000"))
            AppointmentService.create(apt_id, pid, doc_id, adate, slot, reason, fee, "Scheduled")
            print(f"[✓] Appointment {apt_id} booked successfully!")
            input("\nPress Enter to continue...")
        elif choice == "3":
            apt_id = get_input("Appointment ID to update")
            st = get_input("New Status (Completed/Cancelled/Rescheduled)", "Completed")
            AppointmentService.update_status(apt_id, st)
            print(f"[✓] Appointment {apt_id} marked as '{st}'.")
            input("\nPress Enter to continue...")
        elif choice == "4":
            apt_id = get_input("Appointment ID to remove")
            AppointmentService.delete(apt_id)
            print(f"[✓] Appointment {apt_id} deleted.")
            input("\nPress Enter to continue...")


def handle_medical_reports():
    while True:
        clear_screen()
        print("             === MEDICAL REPORTS & CLINICAL HISTORY ===")
        print("  [1] View All Clinical Examination Reports")
        print("  [2] View Patient Medical History ($lookup Doctor details)")
        print("  [3] Issue New Medical Report")
        print("  [4] Delete Medical Report")
        print("  [0] Back to Main Menu")
        choice = get_input("Select option (0-4)")

        if choice == "0":
            break
        elif choice == "1":
            reports = MedicalReportService.get_all()
            for r in reports:
                r['symptoms'] = ", ".join(r.get('symptoms', []))
            print_table(reports, title="CLINICAL MEDICAL REPORTS")
            input("\nPress Enter to continue...")
        elif choice == "2":
            pid = get_input("Enter Patient ID (e.g. PAT-201, PAT-203, PAT-204)")
            history = MedicalReportService.get_patient_history(pid)
            if not history:
                print(f"[!] No medical history found for patient {pid}.")
            else:
                print(f"\n--- MEDICAL HISTORY FOR PATIENT {pid} ---")
                for h in history:
                    print(f"  • Report: {h['report_id']} | Doctor: {h['doctor_name']} ({h['doctor_specialization']})")
                    print(f"    Diagnosis   : {h['diagnosis']}")
                    print(f"    Symptoms    : {', '.join(h['symptoms'])}")
                    print(f"    Prescription: {h['prescriptions']}")
                    print(f"    Lab Tests   : {h['lab_tests']}")
                    print(f"    Follow-up   : {h['follow_up_date']}\n")
            input("\nPress Enter to continue...")
        elif choice == "3":
            rid = get_input("Report ID (e.g. REP-510)")
            aid = get_input("Appointment ID")
            pid = get_input("Patient ID")
            did = get_input("Doctor ID")
            diag = get_input("Clinical Diagnosis")
            symp = [s.strip() for s in get_input("Symptoms (comma-separated)").split(",")]
            med = get_input("Primary Medication")
            dosage = get_input("Dosage", "Daily")
            pres = [{"medication": med, "dosage": dosage, "duration": "14 days"}]
            lab = [{"test": get_input("Lab Test Name", "Blood Test"), "result": "Normal"}]
            fdate = get_input("Follow-up Date (YYYY-MM-DD)", "2026-11-20")
            MedicalReportService.create(rid, aid, pid, did, diag, symp, pres, lab, fdate)
            print(f"[✓] Medical Report {rid} issued successfully!")
            input("\nPress Enter to continue...")
        elif choice == "4":
            rid = get_input("Report ID to delete")
            MedicalReportService.delete(rid)
            print(f"[✓] Deleted medical report {rid}.")
            input("\nPress Enter to continue...")


def main():
    clear_screen()
    print("=" * 75)
    print("   TASK 4: HOSPITAL MANAGEMENT SYSTEM APPLICATION (MONGODB)")
    print("   Relational-like Documents: Departments, Doctors, Patients, Appointments, Reports")
    print("=" * 75)

    while True:
        clear_screen()
        print("                     === HOSPITAL MAIN DASHBOARD ===")
        print("  [1] Departments Management    (Beds, Locations, Heads)")
        print("  [2] Doctors Directory          (Specializations, Availability, Fees)")
        print("  [3] Patients Directory         (Registration, Medical Profiles, Blood Groups)")
        print("  [4] Appointments & Booking     (Scheduling, Relational $lookup Joins)")
        print("  [5] Clinical Medical Reports   (Diagnoses, Prescriptions, Lab Tests)")
        print("  [6] Executive Analytics        (Cross-collection Department Revenue)")
        print("  [7] Run Automated Test Suite   (100% Verification across all 5 Entities)")
        print("  [8] Generate Visual Dashboards (Matplotlib & Seaborn Analytics)")
        print("  [9] Reset & Seed Hospital DB   (Restore default clinical dataset)")
        print("  [0] Exit")
        print("-" * 75)

        choice = get_input("Select an option (0-9)")
        if choice == "0":
            print("\nExiting Hospital Management System. Goodbye!\n")
            break
        elif choice == "1":
            handle_departments()
        elif choice == "2":
            handle_doctors()
        elif choice == "3":
            handle_patients()
        elif choice == "4":
            handle_appointments()
        elif choice == "5":
            handle_medical_reports()
        elif choice == "6":
            from test_all_operations import run_tests
            from config import get_db, COLL_APPOINTMENTS, COLL_DOCTORS, COLL_DEPARTMENTS
            db = get_db()
            pipeline = [
                {"$lookup": {"from": COLL_DOCTORS, "localField": "doctor_id", "foreignField": "doctor_id", "as": "doc"}},
                {"$unwind": "$doc"},
                {"$lookup": {"from": COLL_DEPARTMENTS, "localField": "doc.dept_id", "foreignField": "dept_id", "as": "dept"}},
                {"$unwind": "$dept"},
                {
                    "$group": {
                        "_id": "$dept.name",
                        "total_appointments": {"$sum": 1},
                        "total_revenue": {"$sum": "$fee"},
                        "avg_consultation_fee": {"$avg": "$fee"}
                    }
                },
                {"$sort": {"total_revenue": -1}},
                {
                    "$project": {
                        "Department": "$_id",
                        "Appointments": "$total_appointments",
                        "Revenue (₹)": {"$round": ["$total_revenue", 2]},
                        "Avg Fee (₹)": {"$round": ["$avg_consultation_fee", 2]},
                        "_id": 0
                    }
                }
            ]
            res = list(db[COLL_APPOINTMENTS].aggregate(pipeline))
            print_table(res, title="DEPARTMENT-WISE APPOINTMENT VOLUME & REVENUE")
            input("\nPress Enter to continue...")
        elif choice == "7":
            run_tests()
            input("\nPress Enter to continue...")
        elif choice == "8":
            charts = generate_all_visualizations()
            print(f"\n[✓] Generated {len(charts)} chart figures in visualizations/ folder.")
            input("\nPress Enter to continue...")
        elif choice == "9":
            seed_hospital_data(reset=True)
            input("\nPress Enter to continue...")
        else:
            print("[!] Invalid option. Please enter 0 to 9.")


if __name__ == "__main__":
    main()
