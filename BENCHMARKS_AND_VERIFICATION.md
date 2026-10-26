# Production Verification & Healthcare System Audit
### Hospital Clinical Management System (NoSQL Architecture)
**Project:** Hospital Management System (MongoDB Backend)  
**Core Purpose:** Comprehensive verification of cross-collection operations, CRUD workflows, `$lookup` joins across 5 clinical entities, and multi-stage aggregation analytics.  
**Tech Stack:** Python 3.12+ | MongoDB 9.0 / PyMongo | `pandas`, `tabulate`, `seaborn`, `matplotlib`

---

## 1. Relational-Like Document Architecture in MongoDB

```text
 [ departments ] (dept_id, name, block_floor, head_doctor, total_beds)
        ▲
        │ 1:N
   [ doctors ] (doctor_id, name, specialization, dept_id, fee, available_days)
        ▲
        │ 1:N ($lookup Join)
 [ appointments ] (appointment_id, patient_id, doctor_id, date, slot, fee, status)
        │
        │ N:1 ($lookup Join)
        ▼
   [ patients ] (patient_id, name, age, gender, contact, blood_group, status)
        │
        │ 1:N
 [ medical_reports ] (report_id, appointment_id, patient_id, doctor_id, diagnosis, symptoms, prescriptions)
```

---

## 2. CRUD Execution Across All 5 Healthcare Entities

Output of automated test suite `python3 test_all_operations.py`:

```text
================================================================================
>>> 1. DEPARTMENTS CRUD
================================================================================
[✓] [C] Create : Inserted 'Emergency & Trauma Care' (ID: DEP-EMER, Beds: 30)
[✓] [R] Read   : Fetched DEP-EMER | Location: Block E, Ground Floor
[✓] [U] Update : Modified total_beds to 35 (Modified: 1)
[✓] [D] Delete : Removed test department (Deleted: 1)

================================================================================
>>> 2. DOCTORS CRUD
================================================================================
[✓] [C] Create : Registered Dr. Alok Verma (Gastroenterology, Fee: ₹1,100)
[✓] [R] Read   : Query by department 'DEP-CARD' returned 2 active doctors
[✓] [U] Update : Revised consultation fee to ₹1,250.00
[✓] [D] Delete : Removed test doctor record

================================================================================
>>> 3. PATIENTS CRUD & SEARCH
================================================================================
[✓] [C] Create : Registered patient Ritu Singhania (PAT-213, Age: 31, B+)
[✓] [R] Search : Regex query 'Singhania' matched 1 patient record
[✓] [U] Update : Updated status to 'Admitted'
[✓] [D] Delete : Removed test patient record

================================================================================
>>> 4. APPOINTMENTS CRUD & $LOOKUP RELATIONAL JOINS
================================================================================
[✓] [C] Create : Booked appointment APT-316 (Patient PAT-202 -> Doctor DOC-101)
[✓] [R] $lookup: Reconstructed relational join linking patient & doctor names:
                 Patient: Pooja Hegde | Doctor: Dr. Rajesh Sharma | Fee: ₹1,200
[✓] [U] Update : Marked appointment as 'Completed'
[✓] [D] Delete : Cancelled and removed test appointment

================================================================================
>>> 5. MEDICAL REPORTS CRUD & NESTED CLINICAL RECORDS
================================================================================
[✓] [C] Create : Issued clinical report REP-506 with nested prescriptions array
[✓] [R] History: Fetched patient PAT-201 history with resolved doctor details:
                 Diagnosis: Hypertension & Angina Pectoris | Meds: Amlodipine, Sorbitrate
[✓] [D] Delete : Removed test medical report
```

---

## 3. Cross-Collection Revenue Analytics (`$lookup` + `$group`)

Result of pipeline joining `appointments` $\rightarrow$ `doctors` $\rightarrow$ `departments`:

```text
╒══════════════╤════════════════╤═══════════════╤═══════════════╕
│ Department   │   Appointments │   Revenue (₹) │   Avg Fee (₹) │
╞══════════════╪════════════════╪═══════════════╪═══════════════╡
│ Orthopedics  │              4 │      4,200.00 │      1,050.00 │
│ Cardiology   │              4 │      4,200.00 │      1,050.00 │
│ Oncology     │              2 │      3,600.00 │      1,800.00 │
│ Neurology    │              2 │      3,000.00 │      1,500.00 │
│ Pediatrics   │              3 │      2,900.00 │        966.67 │
╘══════════════╧════════════════╧═══════════════╧═══════════════╛
```

---

## 4. Core Technical Decisions & Architecture FAQs

- **Q1: How do you model relationships like Foreign Keys in MongoDB?**  
  *Answer:* Through **Document Referencing**. A document stores the identifier of another document (e.g. `appointments.doctor_id = "DOC-101"`). At query time, the `$lookup` aggregation stage joins the collections similar to an SQL `LEFT JOIN`.
- **Q2: Why is MongoDB well-suited for clinical Medical Reports?**  
  *Answer:* Clinical data has nested, polymorphic structures. MongoDB stores nested arrays of prescriptions (medication, dosage, duration) and lab test objects directly inside the document without requiring multiple relational join tables.
- **Q3: How does the system compute departmental revenue without a relational schema?**  
  *Answer:* Using a 4-stage pipeline: `$lookup` from doctors $\rightarrow$ `$lookup` from departments $\rightarrow$ `$group` by department name calculating `$sum: "$fee"` $\rightarrow$ `$sort` by revenue descending.
- **Q4: How does this project integrate with Data Visualisation?**  
  *Answer:* Aggregated MongoDB healthcare collections are transformed into Pandas DataFrames and visualized using Matplotlib and Seaborn (department revenue charts, patient age histograms by gender, and executive dashboards).

---
**Verification Status:** Operational | MongoDB Connected | 100% Tests Passing
