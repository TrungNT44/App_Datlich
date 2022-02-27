from datetime import datetime, timedelta
from typing import Optional
import app.app_config as config

from fastapi import Depends, FastAPI, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.db import SessionLocal, engine
from app.crud import user_crud, doctor_crud, appointment_crud
from app.model import sql_model
from sqlmodel import Session, SQLModel

SECRET_KEY = config.SECRET_KEY #"903b23dc56d0790bf74b31b004b662f711073c22b63e923e4af3bd732804eb02"
ALGORITHM = config.ALGORITHM #"HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = config.ACCESS_TOKEN_EXPIRE_MINUTES #60

app = FastAPI()

def get_session():
    with Session(engine) as session:
        try:
            yield session
        finally:
            session.close()

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# @app.on_event("startup")
# def on_startup():
#     #create_db_and_tables()



class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")




def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)



def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def verify_token(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    return token_data.username

# router = APIRouter(
#     prefix="/users",
#     tags=["users"],
#     dependencies=[Depends(verify_token)],
#     responses={404: {"description": "Not found"}},
# )

router = APIRouter()
#app.include_router(router)
#app.include_router(router,prefix="/posts",tags=["posts"])

@router.get("/")
async def posts():
    return {"posts": 'test'}

@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_session)):
    #user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    user = user_crud.authenticate_user(db, username=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}



#@app.get("/users/all", response_model=List[sql_model.Users], dependencies=[Depends(verify_token)])
@app.get("/users/all", dependencies=[Depends(verify_token)])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_session)):
    users = user_crud.get_users(db, skip=skip, limit=limit)
    return {
        "data": users,
        "status": 200,
        "detail": "OK"
    }


# lay thong tin 1 user
@app.get("/users/{username}", dependencies=[Depends(verify_token)])
#@router.get("/{username}", response_model=sql_model.Users)
def read_user(username: str, db: Session = Depends(get_session)):
    users = user_crud.get_user_by_username(db, username=username)
    if users is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        "data": users,
        "status": 200,
        "detail": "OK"
    }


# tao user moi
@app.post("/users/create_user")
def create_user(user: sql_model.Users, db: Session = Depends(get_session)):
    db_user = user_crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    new_user = user_crud.create_user(db=db, user=user)
    data = sql_model.UserResponse(username=new_user.username,password=new_user.password,userrole=new_user.userrole)
    return {
        "data": data,
        "status": 200,
        "detail": "OK"
    }


# update user
@app.post("/users/update_user", response_model=sql_model.Users, dependencies=[Depends(verify_token)])
def update_user(user: sql_model.Users, db: Session = Depends(get_session)):
    db_user = user_crud.update_user_by_username(db, user)
    return db_user
    return {
            "data": db_user,
            "status": 200,
            "detail": "OK"
        }


# xoa user
@app.post("/users/delete_user", dependencies=[Depends(verify_token)])
def delete_user(username: str, db: Session = Depends(get_session)):
    result = user_crud.delete_user_by_username(db, username=username)
    if not result:
        raise HTTPException(status_code=400, detail="User does not exist")
    return {
            "data": result,
            "status": 200,
            "detail": "OK"
        }


# Cum API Bac sy
@app.get("/doctors/all", dependencies=[Depends(verify_token)])
def read_doctors(skip: int = 0, limit: int = 100, db: Session = Depends(get_session)):
    doctors = doctor_crud.get_doctors(db)
    return {
        "data": doctors,
        "status": 200,
        "detail": "OK"
    }


# lay thong tin 1 bac sy
@app.get("/doctors/{username}", dependencies=[Depends(verify_token)])
def read_doctor(username: str, db: Session = Depends(get_session)):
    doctors = doctor_crud.get_doctor_by_username(db, username=username)
    if doctors is None:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return {
        "data": doctors,
        "status": 200,
        "detail": "OK"
    }


# tao BS moi
@app.post("/doctors/create_doctor")
def create_doctor(doctor: sql_model.Doctors, db: Session = Depends(get_session)):
    db_doctor = doctor_crud.get_doctor_by_username(db, username=doctor.username)
    if db_doctor:
        raise HTTPException(status_code=400, detail="Username already registered")
    new_doctor = doctor_crud.create_doctor(db=db, doctor=doctor)
    return {
        "data": new_doctor,
        "status": 200,
        "detail": "OK"
    }

# update doctor
@app.post("/doctors/update_doctor", response_model=sql_model.Doctors, dependencies=[Depends(verify_token)])
def update_doctor(doctor: sql_model.Doctors, db: Session = Depends(get_session)):
    doctors = doctor_crud.get_doctor_by_username(db, username=doctor.username)
    if doctors is None:
        raise HTTPException(status_code=404, detail="Doctor not found")
    updated_doctor = doctor_crud.update_doctor_by_username(db, doctor)
    return {
            "data": updated_doctor,
            "status": 200,
            "detail": "OK"
        }

# xoa BS
@app.post("/doctors/delete_doctor", dependencies=[Depends(verify_token)])
def delete_doctor(username: str, db: Session = Depends(get_session)):
    result = doctor_crud.delete_doctor_by_username(db, username=username)
    if not result:
        raise HTTPException(status_code=400, detail="Doctor does not exist")
    return {
            "data": result,
            "status": 200,
            "detail": "OK"
        }



# Cum API lich hen kham
@app.get("/appointments/all", dependencies=[Depends(verify_token)])
def read_appointments(skip: int = 0, limit: int = 100, db: Session = Depends(get_session)):
    appointments = appointment_crud.get_appointments(db)
    return {
        "data": appointments,
        "status": 200,
        "detail": "OK"
    }

# lay thong tin buoi lich kham theo username
@app.get("/appointments/{username}", dependencies=[Depends(verify_token)])
def read_doctor(username: str, db: Session = Depends(get_session), skip: int = 0, limit: int = 200):
    user = user_crud.get_user_by_username(db, username=username)
    appointment = None
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if user.userrole == 'BN': #benh nhan
        appointment = appointment_crud.get_appointment_by_patient_username(db, username, skip, limit)
    elif user.userrole == 'BS': #bac sy
        doctor = doctor_crud.get_doctor_by_username(db, username=username)
        appointment_crud.generate_appointment_of_doctor(db, doctor)
        appointment = appointment_crud.get_appointment_by_doctor_username(db, username, skip, limit)
    return {
        "data": appointment,
        "status": 200,
        "detail": "OK"
    }


# update lich hen
@app.post("/appointments/update_appointment", dependencies=[Depends(verify_token)])
def update_user(requestAppointment: sql_model.Appointments, db: Session = Depends(get_session)):
    appointment = appointment_crud.update_appointment_by_id(db, requestAppointment)
    return {
            "data": appointment,
            "status": 200,
            "detail": "OK"
        }
