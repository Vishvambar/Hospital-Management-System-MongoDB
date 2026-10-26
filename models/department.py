"""
Department Service - MongoDB Collection Operations for Hospital Departments.
"""

from typing import List, Dict, Any, Optional
from config import get_collection, COLL_DEPARTMENTS


class DepartmentService:
    @staticmethod
    def get_coll():
        return get_collection(COLL_DEPARTMENTS)

    @classmethod
    def create(cls, dept_id: str, name: str, block_floor: str, head_doctor: str, total_beds: int = 20) -> str:
        """[C] Create Department document."""
        doc = {
            "dept_id": dept_id,
            "name": name.strip(),
            "block_floor": block_floor.strip(),
            "head_doctor": head_doctor.strip(),
            "total_beds": total_beds
        }
        res = cls.get_coll().insert_one(doc)
        return str(res.inserted_id)

    @classmethod
    def get_all(cls) -> List[Dict[str, Any]]:
        """[R] Read all departments."""
        return list(cls.get_coll().find({}, {"_id": 0}))

    @classmethod
    def get_by_id(cls, dept_id: str) -> Optional[Dict[str, Any]]:
        """[R] Read single department by dept_id."""
        return cls.get_coll().find_one({"dept_id": dept_id}, {"_id": 0})

    @classmethod
    def update(cls, dept_id: str, **kwargs) -> int:
        """[U] Update department details."""
        res = cls.get_coll().update_one({"dept_id": dept_id}, {"$set": kwargs})
        return res.modified_count

    @classmethod
    def delete(cls, dept_id: str) -> int:
        """[D] Remove department."""
        res = cls.get_coll().delete_one({"dept_id": dept_id})
        return res.deleted_count
