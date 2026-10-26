"""
Hospital Management System Sample Data Seeder.
Populates realistic hospital data across Departments, Doctors, Patients,
Appointments, and Medical Reports in MongoDB.
"""

from config import get_db, COLL_DEPARTMENTS, COLL_DOCTORS, COLL_PATIENTS, COLL_APPOINTMENTS, COLL_MEDICAL_REPORTS
from models import DepartmentService, DoctorService, PatientService, AppointmentService, MedicalReportService


def seed_hospital_data(reset: bool = True):
    db = get_db()
    if reset:
        print("[*] Resetting hospital management collections...")
        for coll_name in [COLL_DEPARTMENTS, COLL_DOCTORS, COLL_PATIENTS, COLL_APPOINTMENTS, COLL_MEDICAL_REPORTS]:
            db[coll_name].drop()

    print("\n" + "=" * 70)
    print("      SEEDING HOSPITAL MANAGEMENT SYSTEM (MONGODB)")
    print("=" * 70)

    # 1. Departments
    departments = [
        ("DEP-CARD", "Cardiology", "Block A, Floor 3", "Dr. Rajesh Sharma", 40),
        ("DEP-NEUR", "Neurology", "Block B, Floor 4", "Dr. Sneha Pillai", 30),
        ("DEP-ORTH", "Orthopedics", "Block A, Floor 2", "Dr. Anand Joshi", 35),
        ("DEP-PEDI", "Pediatrics", "Block C, Floor 1", "Dr. Shalini Gupta", 25),
        ("DEP-ONCO", "Oncology", "Block D, Floor 5", "Dr. Vikram Seth", 50)
    ]
    print("\n[*] Seeding Departments...")
    for d_id, name, floor, head, beds in departments:
        DepartmentService.create(d_id, name, floor, head, beds)
        print(f"  [+] Department: {name:<18} ({d_id}) | Head: {head}")

    # 2. Doctors
    doctors = [
        ("DOC-101", "Dr. Rajesh Sharma", "Interventional Cardiology", "DEP-CARD", "rajesh.sharma@hospital.com", "+91-9876500101", 1200.0, ["Mon", "Wed", "Fri"]),
        ("DOC-102", "Dr. Priya Bansal", "Clinical Cardiology", "DEP-CARD", "priya.bansal@hospital.com", "+91-9876500102", 900.0, ["Tue", "Thu", "Sat"]),
        ("DOC-103", "Dr. Sneha Pillai", "Neurosurgeon", "DEP-NEUR", "sneha.pillai@hospital.com", "+91-9876500103", 1500.0, ["Mon", "Tue", "Thu"]),
        ("DOC-104", "Dr. Anand Joshi", "Orthopedic Surgeon", "DEP-ORTH", "anand.joshi@hospital.com", "+91-9876500104", 1000.0, ["Mon", "Wed", "Sat"]),
        ("DOC-105", "Dr. Meera Nambiar", "Joint Replacement Specialist", "DEP-ORTH", "meera.n@hospital.com", "+91-9876500105", 1100.0, ["Tue", "Fri"]),
        ("DOC-106", "Dr. Shalini Gupta", "Pediatrician", "DEP-PEDI", "shalini.g@hospital.com", "+91-9876500106", 800.0, ["Mon", "Tue", "Wed", "Thu", "Fri"]),
        ("DOC-107", "Dr. Vikram Seth", "Medical Oncology", "DEP-ONCO", "vikram.seth@hospital.com", "+91-9876500107", 1800.0, ["Tue", "Thu", "Fri"]),
        ("DOC-108", "Dr. Rohan Deshpande", "Pediatric Neurologist", "DEP-PEDI", "rohan.d@hospital.com", "+91-9876500108", 1300.0, ["Wed", "Sat"])
    ]
    print("\n[*] Seeding Doctors...")
    for doc_id, name, spec, d_id, email, phone, fee, days in doctors:
        DoctorService.create(doc_id, name, spec, d_id, email, phone, fee, days)
        print(f"  [+] Doctor: {name:<22} | {spec:<25} | Fee: ₹{fee:,.0f}")

    # 3. Patients
    patients = [
        ("PAT-201", "Aarav Roy", 45, "Male", "+91-9811100201", "O+", "+91-9811199991", "Outpatient"),
        ("PAT-202", "Pooja Hegde", 28, "Female", "+91-9811100202", "B+", "+91-9811199992", "Outpatient"),
        ("PAT-203", "Ramesh Kulkarni", 62, "Male", "+91-9811100203", "A+", "+91-9811199993", "Admitted"),
        ("PAT-204", "Sunita Nair", 53, "Female", "+91-9811100204", "AB+", "+91-9811199994", "Outpatient"),
        ("PAT-205", "Kabir Mehta", 8, "Male", "+91-9811100205", "O+", "+91-9811199995", "Outpatient"),
        ("PAT-206", "Ananya Rao", 34, "Female", "+91-9811100206", "B-", "+91-9811199996", "Outpatient"),
        ("PAT-207", "Devendra Singh", 71, "Male", "+91-9811100207", "A-", "+91-9811199997", "Admitted"),
        ("PAT-208", "Neha Sen", 12, "Female", "+91-9811100208", "O-", "+91-9811199998", "Outpatient"),
        ("PAT-209", "Amitav Ghosh", 58, "Male", "+91-9811100209", "B+", "+91-9811199999", "Outpatient"),
        ("PAT-210", "Tanvi Agarwal", 26, "Female", "+91-9811100210", "A+", "+91-9811199900", "Discharged"),
        ("PAT-211", "Karan Johar", 39, "Male", "+91-9811100211", "O+", "+91-9811199901", "Outpatient"),
        ("PAT-212", "Farida Khan", 65, "Female", "+91-9811100212", "AB-", "+91-9811199902", "Admitted")
    ]
    print("\n[*] Seeding Patients...")
    for p_id, name, age, gender, cont, bg, econt, status in patients:
        PatientService.create(p_id, name, age, gender, cont, bg, econt, status)
        print(f"  [+] Patient: {name:<18} ({p_id}) | Age: {age:<2} | Gender: {gender:<6} | Status: {status}")

    # 4. Appointments
    appointments = [
        ("APT-301", "PAT-201", "DOC-101", "2026-10-25", "10:00 AM", "Chest tightness & breathlessness", 1200.0, "Completed"),
        ("APT-302", "PAT-202", "DOC-106", "2026-10-25", "11:30 AM", "Pediatric consultation for child", 800.0, "Completed"),
        ("APT-303", "PAT-203", "DOC-104", "2026-10-25", "02:00 PM", "Chronic knee pain evaluation", 1000.0, "Completed"),
        ("APT-304", "PAT-204", "DOC-103", "2026-10-26", "09:30 AM", "Severe recurring migraines", 1500.0, "Completed"),
        ("APT-305", "PAT-205", "DOC-106", "2026-10-26", "10:30 AM", "Seasonal flu & cough", 800.0, "Completed"),
        ("APT-306", "PAT-206", "DOC-101", "2026-10-26", "11:00 AM", "Routine cardiovascular checkup", 1200.0, "Completed"),
        ("APT-307", "PAT-207", "DOC-107", "2026-10-26", "01:00 PM", "Follow-up oncology consultation", 1800.0, "Completed"),
        ("APT-308", "PAT-208", "DOC-108", "2026-10-27", "10:00 AM", "Pediatric neurological evaluation", 1300.0, "Scheduled"),
        ("APT-309", "PAT-209", "DOC-104", "2026-10-27", "11:30 AM", "Post-operative orthopedic review", 1000.0, "Scheduled"),
        ("APT-310", "PAT-210", "DOC-102", "2026-10-27", "02:00 PM", "ECG and BP monitoring", 900.0, "Scheduled"),
        ("APT-311", "PAT-211", "DOC-105", "2026-10-28", "10:00 AM", "Hip joint pain consultation", 1100.0, "Scheduled"),
        ("APT-312", "PAT-212", "DOC-107", "2026-10-28", "11:30 AM", "Chemotherapy cycle review", 1800.0, "Scheduled"),
        ("APT-313", "PAT-201", "DOC-102", "2026-10-29", "09:00 AM", "Follow-up lipid & BP checkup", 900.0, "Scheduled"),
        ("APT-314", "PAT-203", "DOC-105", "2026-10-29", "12:00 PM", "Knee MRI scan consultation", 1100.0, "Scheduled"),
        ("APT-315", "PAT-204", "DOC-103", "2026-10-30", "03:00 PM", "Brain EEG follow-up review", 1500.0, "Scheduled")
    ]
    print("\n[*] Seeding Appointments...")
    for apt_id, p_id, d_id, adate, slot, reason, fee, st in appointments:
        AppointmentService.create(apt_id, p_id, d_id, adate, slot, reason, fee, st)
        print(f"  [+] Appointment {apt_id}: Patient {p_id} -> Doctor {d_id} | Date: {adate} | Fee: ₹{fee:,.0f}")

    # 5. Medical Reports
    reports = [
        (
            "REP-501", "APT-301", "PAT-201", "DOC-101",
            "Hypertension & Angina Pectoris",
            ["Chest pain on exertion", "Elevated Blood Pressure 150/95", "Mild fatigue"],
            [{"medication": "Amlodipine", "dosage": "5mg once daily", "duration": "30 days"},
             {"medication": "Sorbitrate", "dosage": "5mg sublingual as needed", "duration": "15 days"}],
            [{"test": "ECG", "result": "Sinus Rhythm with ST-T changes"},
             {"test": "Troponin-T", "result": "Negative (<0.01 ng/mL)"}],
            "2026-11-25"
        ),
        (
            "REP-502", "APT-303", "PAT-203", "DOC-104",
            "Osteoarthritis Grade 3 (Bilateral Knee)",
            ["Severe joint stiffness in morning", "Crepitus on flexion", "Swelling"],
            [{"medication": "Celecoxib", "dosage": "200mg daily", "duration": "14 days"},
             {"medication": "Glucosamine + Chondroitin", "dosage": "1 tablet daily", "duration": "60 days"}],
            [{"test": "X-Ray Both Knees", "result": "Medial joint space narrowing noted"}],
            "2026-11-10"
        ),
        (
            "REP-503", "APT-304", "PAT-204", "DOC-103",
            "Chronic Migraine with Visual Aura",
            ["Throbbing unilateral headache", "Photophobia", "Nausea"],
            [{"medication": "Sumatriptan", "dosage": "50mg at onset", "duration": "PRN"},
             {"medication": "Propranolol", "dosage": "40mg daily (prophylaxis)", "duration": "30 days"}],
            [{"test": "Brain MRI", "result": "Normal intracranial study, no structural lesion"}],
            "2026-11-20"
        ),
        (
            "REP-504", "APT-305", "PAT-205", "DOC-106",
            "Acute Upper Respiratory Tract Infection (Pediatric)",
            ["Fever 101F", "Rhinorrhea", "Cough"],
            [{"medication": "Paracetamol Syrup", "dosage": "5ml every 6 hours", "duration": "3 days"},
             {"medication": "Cetirizine Syrup", "dosage": "2.5ml at night", "duration": "5 days"}],
            [{"test": "Complete Blood Count", "result": "Mild lymphocytosis, normal platelet count"}],
            "2026-11-02"
        ),
        (
            "REP-505", "APT-307", "PAT-207", "DOC-107",
            "Colorectal Carcinoma (Post-Chemotherapy Surveillance)",
            ["Mild neuropathic numbness", "Appetite recovered", "No acute bleeding"],
            [{"medication": "Pregabalin", "dosage": "75mg at bedtime", "duration": "30 days"},
             {"medication": "Vitamin B-Complex", "dosage": "1 capsule daily", "duration": "30 days"}],
            [{"test": "Serum CEA Level", "result": "1.8 ng/mL (Normal < 2.5 ng/mL)"},
             {"test": "Contrast CT Abdomen", "result": "No evidence of recurrence"}],
            "2026-12-01"
        )
    ]
    print("\n[*] Seeding Medical Reports...")
    for r_id, apt_id, p_id, d_id, diag, symp, pres, labs, fdate in reports:
        MedicalReportService.create(r_id, apt_id, p_id, d_id, diag, symp, pres, labs, fdate)
        print(f"  [+] Medical Report {r_id}: Patient {p_id} | Diagnosis: {diag}")

    print("\n" + "=" * 70)
    print("[✓] Hospital Management System Database Seeded Successfully!")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    seed_hospital_data()
