from fastapi import FastAPI, Depends
from fastapi.security import HTTPBasic
from sqlalchemy.orm import Session
from application.crud import SpecialityForStudentModel, EnterpriseModel, RequirementsModel
from application.database import SessionLocal, SpecialityForStudent, Enterprise, Requirements

app = FastAPI()
security = HTTPBasic()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Метод для запроса информации о предпочтениях в части специальностей и наименовании предприятия
@app.get("/preferences")
def get_preferences(db: Session = Depends(get_db)):
    preferences = db.query(SpecialityForStudent, Enterprise).join(Enterprise).all()
    return preferences

# Метод для автоматического отбора специальностей, предприятий, адресов расположения предприятий и условий трудоустройства
@app.get("/automatic_selection")
def automatic_selection(db: Session = Depends(get_db)):
    selection = db.query(SpecialityForStudent, Enterprise, Requirements).join(Enterprise).join(Requirements).all()
    return selection



@app.post("/specialities")
async def create_speciality(speciality: SpecialityForStudentModel, db: Session = Depends(get_db)):
    new_speciality = SpecialityForStudent(**speciality.dict())
    db.add(new_speciality)
    db.commit()
    db.refresh(new_speciality)
    return new_speciality
