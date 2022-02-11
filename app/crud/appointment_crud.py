from sqlmodel import Field, Session, select, or_
from app.model.sql_model import Appointments


def get_appointments(db: Session):
    statement = select(Appointments)
    return db.exec(statement).all()


def get_appointment_by_patient_username(db: Session, patient_username: str):
    statement = select(Appointments).where(Appointments.patient_username == patient_username)
    return db.exec(statement).first()


# loc cuoc hen theo user dang nhap app (chi la bac si hoac chi la benh nhan)
def get_appointment_by_doctor_username(db: Session, username: str, skip: int = 0, limit: int = 10):
    statement = select(Appointments).where(
        or_(Appointments.doctor_username == username, Appointments.patient_username == username)).offset(int).limit(
        limit)
    return db.exec(statement).all()


def get_appointment_by_username(db: Session, doctor_username: str):
    statement = select(Appointments).where(Appointments.doctor_username == doctor_username)
    return db.exec(statement).first()


def create_appointment(db: Session, appointment: Appointments):
    db_appointment = Appointments.from_orm(appointment)
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    return db_appointment


# def update_user_by_username(db: Session, update_user: Users):
#     statement = select(appointments).where(appointments.username == update_user.username)
#     user = db.exec(statement).one()
#     user.password = update_user.password
#     user.address = update_user.address
#
#     db.add(user)
#     db.commit()
#     db.refresh(user)
#     return user
#
def delete_appointment_by_username(db: Session, username: str):
    statement = select(Appointments).where(Appointments.username == username)
    appointment = db.exec(statement).one()
    if appointment is None:
        return False
    db.delete(appointment)
    db.commit()
    return True
