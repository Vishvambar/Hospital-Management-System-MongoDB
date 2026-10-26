"""
Patient Service - MongoDB Collection Operations for Hospital Patients.
"""

from typing import List, Dict, Any, Optional
from config import get_collection, COLL_PATIENTS


class PatientService:
    @staticmethod
    def get_coll():
        return get_collection(COLL_PATIENTS)

    @classmethod
    def create(
        cls,
        patient_id: str,
        name: str,
        age: int,
        gender: str,
        contact: str,
        blood_group: str,
        emergency_contact: str,
        status: str = "Outpatient"
    ) -> str:
        """[C] Create Patient document."""
        doc = {
            "patient_id": patient_id,
            "name": name.strip(),
            "age": int(age),
            "gender": gender.strip(),
            "contact": contact.strip(),
            "blood_group": blood_group.strip().upper(),
            "emergency_contact": emergency_contact.strip(),
            "status": status.strip()  # "Outpatient", "Admitted", "Discharged"
        }
        res = cls.get_coll().insert_one(doc)
        return str(res.inserted_id)

    @classmethod
    def get_all(cls) -> List[Dict[str, Any]]:
        """[R] Read all patients."""
        return list(cls.get_coll().find({}, {"_id": 0}))

    @classmethod
    def get_by_id(cls, patient_id: str) -> Optional[Dict[str, Any]]:
        """[R] Read patient by patient_id."""
        return cls.get_coll().find_one({"patient_id": patient_id}, {"_id": 0})

    @classmethod
    def search(cls, keyword: str) -> List[Dict[str, Any]]:
        """[R] Search patients by name or contact."""
        query = {
            "$or": [
                {"name": {"$regex": keyword, "$options": "i"}},
                {"contact": {"$regex": keyword, "$options": "i"}},
                {"blood_group": {"$regex": keyword, "$options": "i"}}
            ]
        }
        return list(cls.get_coll().find(query, {"_id": 0}))

    @classmethod
    def update(cls, patient_id: str, **kwargs) -> int:
        """[U] Update patient details."""
        res = cls.get_coll().update_one({"patient_id": patient_id}, {"$set": kwargs})
        return res.modified_count

    @classmethod
    def delete(cls, patient_id: str) -> int:
        """[D] Remove patient."""
        res = cls.get_coll().delete_one({"patient_id": patient_id})
        return res.deleted_count
