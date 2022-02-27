from typing import Optional
from sqlmodel import Field, SQLModel
from datetime import date, datetime


class Users(SQLModel, table=True):
    userid: Optional[int] = Field(default=None, primary_key=True)
    username: str
    email: str
    password: str
    phone: str
    address: str
    birthdate: date
    Description_Detail: Optional[str]
    created_date: Optional[datetime]
    update_date: Optional[datetime]
    is_active: Optional[bool]
    fullname: str
    CCCD: Optional[str]
    Nation: Optional[str]
    Job: Optional[str]
    Ethnic: Optional[str]
    city: Optional[str]
    district: Optional[str]
    wards: Optional[str]
    userrole: str
    gender: str


class UserResponse():
    username: str
    password: str
    userrole: str

    def __init__(self, username, password, userrole):
        self.username = username
        self.password = password
        self.userrole = userrole


class Doctors(SQLModel, table=True):
    username: Optional[str] = Field(default=None, primary_key=True)
    fullname: str
    gender: str
    specialist: str  # chuyên khoa
    note: str
    examination_schedule: str  # lịch khám bệnh đăng ký (như sáng t4, chiều t7,...)
    price: float


class Appointments(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    booking_date: date
    patient_username: str
    doctor_username: str
    specialist: str  # chuyên khoa
    place: str  # dia diem
    fromHour: int
    toHour: int
    status: str  # trang thai
    is_BHYT: Optional[str]
