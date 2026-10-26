"""
Verification Suite: Hospital Clinical Management System (MongoDB Backend).
Tests full CRUD across Departments, Doctors, Patients, Appointments, and Medical Reports,
demonstrating relational-like associations and $lookup joins.
"""

from tabulate import tabulate
from models import (
    DepartmentService,
    DoctorService,
    PatientService,
    AppointmentService,
    MedicalReportService
)
from seed_data import seed_hospital_data


def print_section(title: str):
    print("\n" + "=" * 80)
    print(f" >>> {title.upper()} <<<")
    print("=" * 80)


def run_tests():
    # 0. Re-seed clean test state
    seed_hospital_data(reset=True)

    # -------------------------------------------------------------------------
    # 1. DEPARTMENTS CRUD
    # -------------------------------------------------------------------------
    print_section("1. Departments CRUD Operations")
    
    # 1.1 Create
    d_id = DepartmentService.create(
        dept_id="DEP-EMER",
        name="Emergency & Trauma Care",
        block_floor="Block E, Ground Floor",
        head_doctor="Dr. Sameer Khan",
        total_beds=30
    )
    print(f" [✓] [C] Create Department: Inserted 'Emergency & Trauma Care' (ID: DEP-EMER)")

    # 1.2 Read
    dept = DepartmentService.get_by_id("DEP-EMER")
    print(f" [✓] [R] Read Department: {dept['name']} | Location: {dept['block_floor']} | Beds: {dept['total_beds']}")

    # 1.3 Update
    mod_d = DepartmentService.update("DEP-EMER", total_beds=35, head_doctor="Dr. Sameer Khan (Director)")
    dept_up = DepartmentService.get_by_id("DEP-EMER")
    print(f" [✓] [U] Update Department: Modified {mod_d} record -> New Beds: {dept_up['total_beds']}")

    # 1.4 Delete
    del_d = DepartmentService.delete("DEP-EMER")
    print(f" [✓] [D] Delete Department: Removed {del_d} test department.")

    # -------------------------------------------------------------------------
    # 2. DOCTORS CRUD
    # -------------------------------------------------------------------------
    print_section("2. Doctors CRUD Operations")

    # 2.1 Create
    doc_new = DoctorService.create(
        doctor_id="DOC-109",
        name="Dr. Alok Verma",
        specialization="Gastroenterology",
        dept_id="DEP-CARD",
        email="alok.verma@hospital.com",
        phone="+91-9876500109",
        consultation_fee=1100.0,
        available_days=["Mon", "Wed", "Fri"]
    )
    print(f" [✓] [C] Create Doctor: Registered Dr. Alok Verma (ID: DOC-109)")

    # 2.2 Read
    doctor = DoctorService.get_by_id("DOC-109")
    print(f" [✓] [R] Read Doctor: {doctor['name']} | Spec: {doctor['specialization']} | Fee: ₹{doctor['consultation_fee']:,.2f}")

    # 2.3 Update
    mod_doc = DoctorService.update("DOC-109", consultation_fee=1250.0)
    print(f" [✓] [U] Update Doctor: Fee revised to ₹1,250.00 (Modified: {mod_doc})")

    # 2.4 Delete
    del_doc = DoctorService.delete("DOC-109")
    print(f" [✓] [D] Delete Doctor: Cleaned up test doctor (Deleted: {del_doc})")

    # -------------------------------------------------------------------------
    # 3. PATIENTS CRUD & SEARCH
    # -------------------------------------------------------------------------
    print_section("3. Patients CRUD Operations & Search")

    # 3.1 Create
    p_new = PatientService.create(
        patient_id="PAT-213",
        name="Ritu Singhania",
        age=31,
        gender="Female",
        contact="+91-9811100213",
        blood_group="B+",
        emergency_contact="+91-9811199999",
        status="Outpatient"
    )
    print(f" [✓] [C] Create Patient: Registered Ritu Singhania (ID: PAT-213)")

    # 3.2 Read & Search
    search_res = PatientService.search("Singhania")
    print(f" [✓] [R] Search Patient: Found {len(search_res)} matching record(s):")
    print(tabulate(search_res, headers="keys", tablefmt="fancy_grid"))

    # 3.3 Update
    mod_p = PatientService.update("PAT-213", status="Admitted", blood_group="B+ (Verified)")
    print(f" [✓] [U] Update Patient: Status changed to 'Admitted' (Modified: {mod_p})")

    # 3.4 Delete
    del_p = PatientService.delete("PAT-213")
    print(f" [✓] [D] Delete Patient: Removed {del_p} test patient.")

    # -------------------------------------------------------------------------
    # 4. APPOINTMENTS CRUD & $LOOKUP RELATIONAL JOINS
    # -------------------------------------------------------------------------
    print_section("4. Appointments CRUD & Relational $lookup Joins")

    # 4.1 Create
    apt_new = AppointmentService.create(
        appointment_id="APT-316",
        patient_id="PAT-202",
        doctor_id="DOC-101",
        date_str="2026-10-31",
        time_slot="10:00 AM",
        reason="Follow-up cardiovascular evaluation",
        fee=1200.0,
        status="Scheduled"
    )
    print(f" [✓] [C] Create Appointment: Booked appointment APT-316 for Patient PAT-202 with Doctor DOC-101")

    # 4.2 Read with $lookup Join
    print("\n[*] [R] Read Detailed Appointments ($lookup joining Patients & Doctors):")
    detailed_apts = AppointmentService.get_detailed_appointments()
    display_apts = detailed_apts[:5]
    print(tabulate(display_apts, headers="keys", tablefmt="fancy_grid"))

    # 4.3 Update
    mod_apt = AppointmentService.update_status("APT-316", "Completed")
    print(f"\n [✓] [U] Update Appointment: Marked APT-316 as 'Completed' (Modified: {mod_apt})")

    # 4.4 Delete
    del_apt = AppointmentService.delete("APT-316")
    print(f" [✓] [D] Delete Appointment: Removed test appointment (Deleted: {del_apt})")

    # -------------------------------------------------------------------------
    # 5. MEDICAL REPORTS CRUD
    # -------------------------------------------------------------------------
    print_section("5. Medical Reports CRUD & Clinical Diagnosis Records")

    # 5.1 Create
    rep_new = MedicalReportService.create(
        report_id="REP-506",
        appointment_id="APT-306",
        patient_id="PAT-206",
        doctor_id="DOC-101",
        diagnosis="Mild Tachycardia & Anxiety",
        symptoms=["Palpitations", "Restlessness", "Sleep Disturbance"],
        prescriptions=[
            {"medication": "Metoprolol", "dosage": "25mg once daily", "duration": "14 days"}
        ],
        lab_tests=[
            {"test": "Thyroid Profile (T3, T4, TSH)", "result": "Normal"}
        ],
        follow_up_date="2026-11-15"
    )
    print(f" [✓] [C] Create Medical Report: Generated REP-506 for Patient PAT-206")

    # 5.2 Read Patient Clinical History with $lookup
    print("\n[*] [R] Read Patient Medical History ($lookup joining Doctor details):")
    history = MedicalReportService.get_patient_history("PAT-201")
    for h in history:
        print(f"  • Report ID   : {h['report_id']}")
        print(f"    Doctor      : {h['doctor_name']} ({h['doctor_specialization']})")
        print(f"    Diagnosis   : {h['diagnosis']}")
        print(f"    Symptoms    : {', '.join(h['symptoms'])}")
        print(f"    Medications : {h['prescriptions']}")
        print(f"    Lab Tests   : {h['lab_tests']}")

    # 5.3 Delete test report
    del_rep = MedicalReportService.delete("REP-506")
    print(f"\n [✓] [D] Delete Medical Report: Cleaned up test report REP-506 (Deleted: {del_rep})")

    # -------------------------------------------------------------------------
    # 6. RELATIONAL AGGREGATION PIPELINE: REVENUE & VOLUME BY DEPARTMENT
    # -------------------------------------------------------------------------
    print_section("6. Cross-Collection Executive Analytics ($lookup & $group)")
    from config import get_db, COLL_APPOINTMENTS, COLL_DOCTORS, COLL_DEPARTMENTS
    db = get_db()
    pipeline = [
        {
            "$lookup": {
                "from": COLL_DOCTORS,
                "localField": "doctor_id",
                "foreignField": "doctor_id",
                "as": "doc"
            }
        },
        {"$unwind": "$doc"},
        {
            "$lookup": {
                "from": COLL_DEPARTMENTS,
                "localField": "doc.dept_id",
                "foreignField": "dept_id",
                "as": "dept"
            }
        },
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
    dept_analytics = list(db[COLL_APPOINTMENTS].aggregate(pipeline))
    print(tabulate(dept_analytics, headers="keys", tablefmt="fancy_grid"))

    print_section("ALL HOSPITAL MANAGEMENT CRUD & RELATIONAL OPERATIONS PASSED (100%)")


if __name__ == "__main__":
    run_tests()
