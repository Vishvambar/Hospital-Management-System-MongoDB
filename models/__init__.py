"""
Hospital Management System Models Package.
Exports CRUD managers for Departments, Doctors, Patients, Appointments, and Medical Reports.
"""

from .department import DepartmentService
from .doctor import DoctorService
from .patient import PatientService
from .appointment import AppointmentService
from .medical_report import MedicalReportService

__all__ = [
    "DepartmentService",
    "DoctorService",
    "PatientService",
    "AppointmentService",
    "MedicalReportService"
]
