"""
Configuration Module for Hospital Management System (MongoDB Backend).
Handles MongoDB client connectivity, database selection, and collections access.
"""

import os
import sys
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection
import mongomock

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
DB_NAME = os.getenv("HOSPITAL_DB", "hospital_management_db")

# Collection names
COLL_DEPARTMENTS = "departments"
COLL_DOCTORS = "doctors"
COLL_PATIENTS = "patients"
COLL_APPOINTMENTS = "appointments"
COLL_MEDICAL_REPORTS = "medical_reports"


def get_client() -> MongoClient:
    """
    Returns a PyMongo MongoClient instance.
    Connects to live MongoDB server; if unreachable, falls back to mongomock.
    """
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=2000)
        client.admin.command('ping')
        return client
    except Exception as e:
        print(f"[!] Live MongoDB not accessible ({e}). Activating in-memory mongomock.", file=sys.stderr)
        return mongomock.MongoClient()


def get_db() -> Database:
    """Returns the hospital database object."""
    return get_client()[DB_NAME]


def get_collection(collection_name: str) -> Collection:
    """Returns a specific collection from hospital database."""
    return get_db()[collection_name]
