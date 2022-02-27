from sqlmodel import Field, Session, SQLModel, create_engine, select
from app.model.sql_model import Doctors

def get_doctors(db: Session):
    statement = select(Doctors) #.where(Users.username == "Spider-Boy")
    return db.exec(statement).all()


def get_doctor_by_username(db: Session, username: str):
    statement = select(Doctors).where(Doctors.username == username)
    return db.exec(statement).first()


def create_doctor(db: Session, doctor: Doctors):
    db_doctor = Doctors.from_orm(doctor)
    db.add(db_doctor)
    db.commit()
    db.refresh(db_doctor)
    return db_doctor

def update_doctor_by_username(db: Session, doctor: Doctors):
    statement = select(Doctors).where(Doctors.username == doctor.username)
    update_doctor = db.exec(statement).one()
    update_doctor.specialist = doctor.specialist
    update_doctor.examination_schedule = doctor.examination_schedule
    update_doctor.note = doctor.note
    update_doctor.price = doctor.price

    db.add(update_doctor)
    db.commit()
    db.refresh(update_doctor)
    return update_doctor

def delete_doctor_by_username(db: Session, username: str):
    statement = select(Doctors).where(Doctors.username == username)
    doctor = db.exec(statement).one()
    if doctor is None:
        return False
    db.delete(doctor)
    db.commit()
    return True
