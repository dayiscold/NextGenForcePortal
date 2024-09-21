from fastapi import Depends
from database import SessionLocal
from typing import List, Optional
from pydantic import BaseModel


def get_db_session():
    """Receives Session Database"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class SpecialityForStudentModel(BaseModel):
    name_speciality: str


class EnterpriseModel(BaseModel):
    name_enterprise: str
    address_enterprise: str


class RequirementsModel(BaseModel):
    company_id: int
    price_work: Optional[int]
    work_time: int
    employement_time: Optional[int]
