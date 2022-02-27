from datetime import date
from sqlmodel import Field, Session, SQLModel, create_engine, select
from app.model.sql_model import Users
import pandas as pd
from app.crud import doctor_crud
#
# def get_user(db: Session, user_id: int):
#     return db.query(models.User).filter(models.User.userid == user_id).first()
#
#
# def get_user_by_email(db: Session, email: str):
#     return db.query(models.User).filter(models.User.email == email).first()
#
def get_user_by_username(db: Session, username: str):
    #return db.query(models.User).filter(models.User.username == username).first()
    statement = select(Users).where(Users.username == username)
    return db.exec(statement).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    #return db.query(models.User).order_by(models.User.userid).offset(skip).limit(limit).all()
    statement = select(Users) #.where(Users.username == "Spider-Boy")
    return db.exec(statement).all()

def authenticate_user(db: Session, username: str, password: str):
    #return db.query(models.User).filter(models.User.username == username).first()
    statement = select(Users).where(Users.username == username, Users.password == password)
    return db.exec(statement).first()

def create_user(db: Session, user: Users):
    #fake_hashed_password = user.password + "notreallyhashed"
    db_user = Users.from_orm(user)
    db_user.created_date = pd.to_datetime("today")
    db_user.update_date = pd.to_datetime("today")
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user_by_username(db: Session, update_user: Users):
    statement = select(Users).where(Users.username == update_user.username)
    user = db.exec(statement).one()
    user.password = update_user.password
    user.address = update_user.address
    user.phone = update_user.phone
    user.birthdate = update_user.birthdate
    user.Description_Detail = update_user.Description_Detail
    user.is_active = update_user.is_active
    user.fullname = update_user.fullname
    user.CCCD = update_user.CCCD
    user.Nation = update_user.Nation
    user.Job = update_user.Job
    user.Ethnic = update_user.Ethnic
    user.city = update_user.city
    user.district = update_user.district
    user.wards = update_user.wards
    user.userrole = update_user.userrole
    user.gender = update_user.gender
    user.update_date = pd.to_datetime("today")

    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def delete_user_by_username(db: Session, username: str):
    statement = select(Users).where(Users.username == username)
    user = db.exec(statement).one()
    if user is None:
        return False
    db.delete(user)
    if user.userrole == "BS":
        doctor_crud.delete_doctor_by_username(db, username=username)
    db.commit()
    return True
