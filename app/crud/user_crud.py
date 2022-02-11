#from sqlalchemy.orm import Session

#from app.model import models
#from app.schemas import schemas
from sqlmodel import Field, Session, SQLModel, create_engine, select
from app.model.sql_model import Users

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
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user_by_username(db: Session, update_user: Users):
    statement = select(Users).where(Users.username == update_user.username)
    user = db.exec(statement).one()
    user.password = update_user.password
    user.address = update_user.address

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
    db.commit()
    return True
