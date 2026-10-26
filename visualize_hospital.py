"""
Visualizer Module: Hospital Clinical Management System Analytics.
Generates publication-quality visual charts from MongoDB healthcare collections.
"""

import os
import warnings
warnings.filterwarnings('ignore')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

from config import get_db, COLL_APPOINTMENTS, COLL_DOCTORS, COLL_DEPARTMENTS, COLL_PATIENTS, COLL_MEDICAL_REPORTS
from models import AppointmentService

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "visualizations")


def ensure_output_dir():
    os.makedirs(OUTPUT_DIR, exist_ok=True)


def plot_department_revenue():
    """Dual-axis bar chart comparing appointment volume and revenue per department."""
    ensure_output_dir()
    filepath = os.path.join(OUTPUT_DIR, "1_dept_appointments_revenue.png")

    db = get_db()
    pipeline = [
        {"$lookup": {"from": COLL_DOCTORS, "localField": "doctor_id", "foreignField": "doctor_id", "as": "doc"}},
        {"$unwind": "$doc"},
        {"$lookup": {"from": COLL_DEPARTMENTS, "localField": "doc.dept_id", "foreignField": "dept_id", "as": "dept"}},
        {"$unwind": "$dept"},
        {
            "$group": {
                "_id": "$dept.name",
                "appointments": {"$sum": 1},
                "revenue": {"$sum": "$fee"}
            }
        },
        {"$sort": {"revenue": -1}}
    ]
    data = list(db[COLL_APPOINTMENTS].aggregate(pipeline))
    df = pd.DataFrame(data)

    fig, ax1 = plt.subplots(figsize=(10, 5), dpi=300)
    plt.title("Hospital Department Metrics: Patient Appointments & Revenue", fontsize=13, fontweight='bold', pad=15)

    x = range(len(df))
    width = 0.35
    c_apts = '#0284c7'
    c_rev = '#10b981'

    bars1 = ax1.bar([i - width/2 for i in x], df['appointments'], width=width, label='Appointments', color=c_apts, alpha=0.85)
    ax1.set_xlabel('Clinical Department', fontsize=11, fontweight='semibold', labelpad=10)
    ax1.set_ylabel('Total Appointments', color=c_apts, fontsize=11, fontweight='semibold')
    ax1.set_xticks(x)
    ax1.set_xticklabels(df['_id'], fontsize=10, fontweight='bold')
    ax1.tick_params(axis='y', labelcolor=c_apts)
    ax1.grid(axis='y', linestyle='--', alpha=0.3)

    for bar in bars1:
        h = bar.get_height()
        ax1.annotate(f"{int(h)}", xy=(bar.get_x() + bar.get_width() / 2, h),
                     xytext=(0, 3), textcoords="offset points", ha='center', fontweight='bold')

    # Secondary axis: Revenue
    ax2 = ax1.twinx()
    bars2 = ax2.bar([i + width/2 for i in x], df['revenue'], width=width, label='Revenue (₹)', color=c_rev, alpha=0.85)
    ax2.set_ylabel('Consultation Revenue (₹)', color=c_rev, fontsize=11, fontweight='semibold')
    ax2.tick_params(axis='y', labelcolor=c_rev)

    for bar in bars2:
        h = bar.get_height()
        ax2.annotate(f"₹{h:,.0f}", xy=(bar.get_x() + bar.get_width() / 2, h),
                     xytext=(0, 3), textcoords="offset points", ha='center', fontsize=9, fontweight='bold')

    plt.tight_layout()
    plt.savefig(filepath, bbox_inches='tight')
    plt.close()
    return filepath


def plot_patient_demographics():
    """Generates demographic charts for patients (Age spread & Blood groups)."""
    ensure_output_dir()
    filepath = os.path.join(OUTPUT_DIR, "2_patient_demographics_blood_groups.png")

    db = get_db()
    patients = list(db[COLL_PATIENTS].find({}, {"_id": 0}))
    df = pd.DataFrame(patients)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5), dpi=300)
    fig.suptitle("Patient Demographics & Clinical Profile Analysis", fontsize=14, fontweight='bold', y=0.98)

    # 1. Age distribution by gender
    sns.histplot(data=df, x='age', hue='gender', multiple='stack', ax=ax1, palette='Set1', bins=7)
    ax1.set_title("1. Patient Age Distribution by Gender", fontweight='bold', fontsize=11)
    ax1.set_xlabel("Age (Years)")
    ax1.set_ylabel("Patient Count")

    # 2. Blood group distribution
    bg_counts = df['blood_group'].value_counts()
    sns.barplot(x=bg_counts.index, y=bg_counts.values, ax=ax2, palette='mako')
    ax2.set_title("2. Blood Group Distribution", fontweight='bold', fontsize=11)
    ax2.set_xlabel("Blood Group")
    ax2.set_ylabel("Number of Patients")
    for p in ax2.patches:
        ax2.annotate(f"{int(p.get_height())}", (p.get_x() + p.get_width() / 2., p.get_height()),
                     ha='center', va='baseline', fontsize=10, xytext=(0, 3), textcoords='offset points')

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.savefig(filepath, bbox_inches='tight')
    plt.close()
    return filepath


def plot_executive_dashboard():
    """4-Quadrant Executive Hospital Management Analytics Dashboard."""
    ensure_output_dir()
    filepath = os.path.join(OUTPUT_DIR, "3_hospital_executive_dashboard.png")

    db = get_db()
    detailed_apts = AppointmentService.get_detailed_appointments()
    df_apts = pd.DataFrame(detailed_apts)
    patients = list(db[COLL_PATIENTS].find({}, {"_id": 0}))
    df_patients = pd.DataFrame(patients)
    doctors = list(db[COLL_DOCTORS].find({}, {"_id": 0}))
    df_doctors = pd.DataFrame(doctors)

    fig, axes = plt.subplots(2, 2, figsize=(14, 10), dpi=300)
    fig.suptitle("Hospital Management System - Executive Clinical Dashboard", fontsize=16, fontweight='bold', y=0.98)

    # 1. Appointment Status Breakdown (Donut)
    ax1 = axes[0, 0]
    st_counts = df_apts['status'].value_counts()
    ax1.pie(st_counts, labels=st_counts.index, autopct='%1.1f%%', startangle=140,
            colors=['#10b981', '#3b82f6', '#f43f5e'],
            wedgeprops=dict(width=0.4, edgecolor='white', linewidth=2))
    ax1.set_title("1. Appointment Status Share", fontweight='bold', fontsize=11)

    # 2. Consultation Fees across Specializations (Box Plot)
    ax2 = axes[0, 1]
    sns.boxplot(data=df_apts, x='specialization', y='fee', ax=ax2, palette='Purples')
    ax2.set_title("2. Consultation Fee Spread by Specialization", fontweight='bold', fontsize=11)
    ax2.set_xlabel("")
    ax2.set_ylabel("Fee (₹)")
    ax2.tick_params(axis='x', rotation=25)

    # 3. Patient Admission Status (Bar Chart)
    ax3 = axes[1, 0]
    p_status = df_patients['status'].value_counts()
    sns.barplot(x=p_status.index, y=p_status.values, ax=ax3, palette='crest')
    ax3.set_title("3. Patient Admission Status", fontweight='bold', fontsize=11)
    ax3.set_xlabel("Status")
    ax3.set_ylabel("Patient Count")
    for p in ax3.patches:
        ax3.annotate(f"{int(p.get_height())}", (p.get_x() + p.get_width() / 2., p.get_height()),
                     ha='center', va='baseline', fontsize=10, xytext=(0, 3), textcoords='offset points')

    # 4. Hospital Key Metrics Card
    ax4 = axes[1, 1]
    ax4.axis('off')
    total_rev = df_apts['fee'].sum()
    metrics_text = (
        "HOSPITAL SYSTEM AUDIT METRICS\n"
        "-----------------------------------------\n"
        f"• Active Clinical Departments : 5\n"
        f"• Medical Doctors on Roster   : {len(df_doctors)}\n"
        f"• Registered Patients Count   : {len(df_patients)}\n"
        f"• Total Consultations Booked  : {len(df_apts)}\n"
        f"• Total Outpatient Revenue    : ₹{total_rev:,.2f}\n"
        f"• Average Consultation Fee    : ₹{df_apts['fee'].mean():,.2f}\n"
        "-----------------------------------------\n"
        "Backend Architecture: MongoDB NoSQL Cluster\n"
        "Relational Association: $lookup Joins"
    )
    ax4.text(0.1, 0.5, metrics_text, fontsize=11, family='monospace',
             bbox=dict(boxstyle='round,pad=1', facecolor='#f8fafc', edgecolor='#cbd5e1'))
    ax4.set_title("4. Operational Overview Card", fontweight='bold', fontsize=11)

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.savefig(filepath, bbox_inches='tight')
    plt.close()
    return filepath


def generate_all_visualizations():
    """Generates all 3 clinical visual reports."""
    print("[*] Generating Hospital Management Visualizations from MongoDB...")
    c1 = plot_department_revenue()
    print(f" [✓] Created: {os.path.basename(c1)}")
    c2 = plot_patient_demographics()
    print(f" [✓] Created: {os.path.basename(c2)}")
    c3 = plot_executive_dashboard()
    print(f" [✓] Created: {os.path.basename(c3)}")

    print(f"[✓] Visual charts successfully saved to: {OUTPUT_DIR}")
    return [c1, c2, c3]


if __name__ == "__main__":
    generate_all_visualizations()
