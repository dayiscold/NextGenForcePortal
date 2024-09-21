from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBasic
from sqlalchemy.orm import Session
from application.crud import SpecialityForStudentModel, EnterpriseModel, RequirementsModel
from application.database import SessionLocal, SpecialityForStudent, Enterprise, Requirements
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
security = HTTPBasic()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Метод для запроса информации о предпочтениях в части специальностей и наименовании предприятия


@app.get("/preferences")
def get_preferences(db: Session = Depends(get_db)):
    preferences = db.query(SpecialityForStudent, Enterprise).all()
    return preferences

# Метод для автоматического отбора специальностей, предприятий, адресов расположения предприятий и условий трудоустройства
@app.get("/automatic_selection")
def automatic_selection(db: Session = Depends(get_db)):
    selection = db.query(SpecialityForStudent, Enterprise, Requirements).select_from(SpecialityForStudent).join(Enterprise).join(Requirements).all()
    return selection


# Метод для создания запроса на практику
@app.post("/specialities")
async def create_speciality(speciality: SpecialityForStudentModel, db: Session = Depends(get_db)):
    new_speciality = SpecialityForStudent(**speciality.dict())
    db.add(new_speciality)
    db.commit()
    db.refresh(new_speciality)
    return new_speciality


@app.delete("/specialities/{speciality_id}")
def delete_speciality(speciality_id: int, db: Session = Depends(get_db)):
    speciality = db.query(SpecialityForStudent).filter(SpecialityForStudent.id == speciality_id).first()
    if speciality:
        db.delete(speciality)
        db.commit()
        return {"message": "Speciality deleted successfully"}
    return {"message": "Speciality not found"}


@app.put("/specialities/{speciality_id}")
def update_speciality(speciality_id: int, speciality: SpecialityForStudentModel, db: Session = Depends(get_db)):
    existing_speciality = db.query(SpecialityForStudent).filter(SpecialityForStudent.id == speciality_id).first()
    if existing_speciality:
        existing_speciality.name_speciality = speciality.name_speciality
        db.commit()
        db.refresh(existing_speciality)
        return existing_speciality
    return {"message": "Speciality not found"}
