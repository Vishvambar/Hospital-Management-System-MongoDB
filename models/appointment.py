"""
Appointment Service - MongoDB Collection Operations with $lookup Relational Joins.
"""

from typing import List, Dict, Any, Optional
from config import get_collection, COLL_APPOINTMENTS, COLL_DOCTORS, COLL_PATIENTS


class AppointmentService:
    @staticmethod
    def get_coll():
        return get_collection(COLL_APPOINTMENTS)

    @classmethod
    def create(
        cls,
        appointment_id: str,
        patient_id: str,
        doctor_id: str,
        date_str: str,
        time_slot: str,
        reason: str,
        fee: float,
        status: str = "Scheduled"
    ) -> str:
        """[C] Book a new appointment."""
        doc = {
            "appointment_id": appointment_id,
            "patient_id": patient_id.strip(),
            "doctor_id": doctor_id.strip(),
            "date": date_str.strip(),
            "time_slot": time_slot.strip(),
            "reason": reason.strip(),
            "fee": float(fee),
            "status": status.strip()  # "Scheduled", "Completed", "Cancelled"
        }
        res = cls.get_coll().insert_one(doc)
        return str(res.inserted_id)

    @classmethod
    def get_all(cls) -> List[Dict[str, Any]]:
        """[R] Read all appointments."""
        return list(cls.get_coll().find({}, {"_id": 0}))

    @classmethod
    def get_by_id(cls, appointment_id: str) -> Optional[Dict[str, Any]]:
        """[R] Read single appointment by ID."""
        return cls.get_coll().find_one({"appointment_id": appointment_id}, {"_id": 0})

    @classmethod
    def get_detailed_appointments(cls) -> List[Dict[str, Any]]:
        """
        [R] Relational Query: Performs $lookup joins across appointments,
        patients, and doctors to produce a unified view.
        """
        pipeline = [
            {
                "$lookup": {
                    "from": COLL_PATIENTS,
                    "localField": "patient_id",
                    "foreignField": "patient_id",
                    "as": "patient"
                }
            },
            {"$unwind": {"path": "$patient", "preserveNullAndEmptyArrays": True}},
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
                    "appointment_id": 1,
                    "date": 1,
                    "time_slot": 1,
                    "status": 1,
                    "fee": 1,
                    "reason": 1,
                    "patient_id": 1,
                    "patient_name": {"$ifNull": ["$patient.name", "Unknown Patient"]},
                    "patient_contact": "$patient.contact",
                    "doctor_id": 1,
                    "doctor_name": {"$ifNull": ["$doctor.name", "Unknown Doctor"]},
                    "specialization": "$doctor.specialization",
                    "dept_id": "$doctor.dept_id"
                }
            },
            {"$sort": {"date": -1, "time_slot": 1}}
        ]
        return list(cls.get_coll().aggregate(pipeline))

    @classmethod
    def update_status(cls, appointment_id: str, status: str) -> int:
        """[U] Update appointment status (e.g. Completed, Cancelled)."""
        res = cls.get_coll().update_one(
            {"appointment_id": appointment_id},
            {"$set": {"status": status}}
        )
        return res.modified_count

    @classmethod
    def delete(cls, appointment_id: str) -> int:
        """[D] Cancel and remove appointment record."""
        res = cls.get_coll().delete_one({"appointment_id": appointment_id})
        return res.deleted_count
