"""
Medical Report Service - MongoDB Collection Operations for Clinical Diagnoses & Reports.
"""

from typing import List, Dict, Any, Optional
from config import get_collection, COLL_MEDICAL_REPORTS, COLL_PATIENTS, COLL_DOCTORS


class MedicalReportService:
    @staticmethod
    def get_coll():
        return get_collection(COLL_MEDICAL_REPORTS)

    @classmethod
    def create(
        cls,
        report_id: str,
        appointment_id: str,
        patient_id: str,
        doctor_id: str,
        diagnosis: str,
        symptoms: List[str],
        prescriptions: List[Dict[str, str]],
        lab_tests: List[Dict[str, str]],
        follow_up_date: Optional[str] = None
    ) -> str:
        """[C] Issue a new medical examination report."""
        doc = {
            "report_id": report_id,
            "appointment_id": appointment_id.strip(),
            "patient_id": patient_id.strip(),
            "doctor_id": doctor_id.strip(),
            "diagnosis": diagnosis.strip(),
            "symptoms": symptoms,
            "prescriptions": prescriptions,
            "lab_tests": lab_tests,
            "follow_up_date": follow_up_date
        }
        res = cls.get_coll().insert_one(doc)
        return str(res.inserted_id)

    @classmethod
    def get_all(cls) -> List[Dict[str, Any]]:
        """[R] Read all medical reports."""
        return list(cls.get_coll().find({}, {"_id": 0}))

    @classmethod
    def get_by_id(cls, report_id: str) -> Optional[Dict[str, Any]]:
        """[R] Read single medical report by ID."""
        return cls.get_coll().find_one({"report_id": report_id}, {"_id": 0})

    @classmethod
    def get_patient_history(cls, patient_id: str) -> List[Dict[str, Any]]:
        """
        [R] Relational Query: Retrieves all medical reports for a given patient
        with resolved Doctor details via $lookup.
        """
        pipeline = [
            {"$match": {"patient_id": patient_id}},
            {
                "$lookup": {
                    "from": COLL_DOCTORS,
                    "localField": "doctor_id",
                    "foreignField": "doctor_id",
                    "as": "doctor"
                }
            },
            {"$unwind": {"path": "$doctor", "preserveNullAndEmptyArrays": True}},
            {
                "$project": {
                    "_id": 0,
                    "report_id": 1,
                    "appointment_id": 1,
                    "diagnosis": 1,
                    "symptoms": 1,
                    "prescriptions": 1,
                    "lab_tests": 1,
                    "follow_up_date": 1,
                    "doctor_name": "$doctor.name",
                    "doctor_specialization": "$doctor.specialization"
                }
            }
        ]
        return list(cls.get_coll().aggregate(pipeline))

    @classmethod
    def update(cls, report_id: str, **kwargs) -> int:
        """[U] Modify medical report."""
        res = cls.get_coll().update_one({"report_id": report_id}, {"$set": kwargs})
        return res.modified_count

    @classmethod
    def delete(cls, report_id: str) -> int:
        """[D] Remove medical report."""
        res = cls.get_coll().delete_one({"report_id": report_id})
        return res.deleted_count
