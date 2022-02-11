from typing import Optional

from sqlmodel import Field, SQLModel
from datetime import date, datetime

#
# class Hero(SQLModel, table=True):
#     id: Optional[int] = Field(default=None, primary_key=True)
#     name: str
#     secret_name: str
#     age: Optional[int] = None


class Users(SQLModel, table=True):
    userid: Optional[int] = Field(default=None, primary_key=True)
    username: str
    email: str
    password: str
    phone: int
    address: str
    birthdate: date
    Description_Detail: str
    created_date: datetime
    update_date: datetime
    is_active: bool


class Doctors(SQLModel, table=True):
    username: Optional[str] = Field(default=None, primary_key=True)
    fullname: str
    gender: str
    specialist: str #chuyên khoa
    note: str
    examination_schedule: str #lịch khám bệnh đăng ký (như sáng t4, chiều t7,...)



class Appointments(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    booking_date: date
    patient_username: str
    doctor_username: str
    specialist: str #chuyên khoa
    place: str  #dia diem
    fromHour: int
    toHour: int
    status: str  #trang thai