"""
Doctor Service - MongoDB Collection Operations for Hospital Doctors.
"""

from typing import List, Dict, Any, Optional
from config import get_collection, COLL_DOCTORS


class DoctorService:
    @staticmethod
    def get_coll():
        return get_collection(COLL_DOCTORS)

    @classmethod
    def create(
        cls,
        doctor_id: str,
        name: str,
        specialization: str,
        dept_id: str,
        email: str,
        phone: str,
        consultation_fee: float,
        available_days: List[str]
    ) -> str:
        """[C] Create Doctor document."""
        doc = {
            "doctor_id": doctor_id,
            "name": name.strip(),
            "specialization": specialization.strip(),
            "dept_id": dept_id.strip(),
            "email": email.strip().lower(),
            "phone": phone.strip(),
            "consultation_fee": float(consultation_fee),
            "available_days": available_days
        }
        res = cls.get_coll().insert_one(doc)
        return str(res.inserted_id)

    @classmethod
    def get_all(cls) -> List[Dict[str, Any]]:
        """[R] Read all doctors."""
        return list(cls.get_coll().find({}, {"_id": 0}))

    @classmethod
    def get_by_id(cls, doctor_id: str) -> Optional[Dict[str, Any]]:
        """[R] Read single doctor by doctor_id."""
        return cls.get_coll().find_one({"doctor_id": doctor_id}, {"_id": 0})

    @classmethod
    def get_by_dept(cls, dept_id: str) -> List[Dict[str, Any]]:
        """[R] Read doctors by department."""
        return list(cls.get_coll().find({"dept_id": dept_id}, {"_id": 0}))

    @classmethod
    def update(cls, doctor_id: str, **kwargs) -> int:
        """[U] Update doctor details."""
        res = cls.get_coll().update_one({"doctor_id": doctor_id}, {"$set": kwargs})
        return res.modified_count

    @classmethod
    def delete(cls, doctor_id: str) -> int:
        """[D] Remove doctor."""
        res = cls.get_coll().delete_one({"doctor_id": doctor_id})
        return res.deleted_count
