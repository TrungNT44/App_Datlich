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

# def update_user_by_username(db: Session, update_user: Users):
#     statement = select(Doctors).where(Doctors.username == update_user.username)
#     user = db.exec(statement).one()
#     user.password = update_user.password
#     user.address = update_user.address
#
#     db.add(user)
#     db.commit()
#     db.refresh(user)
#     return user
#
def delete_doctor_by_username(db: Session, username: str):
    statement = select(Doctors).where(Doctors.username == username)
    doctor = db.exec(statement).one()
    if doctor is None:
        return False
    db.delete(doctor)
    db.commit()
    return True
