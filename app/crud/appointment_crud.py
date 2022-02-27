from sqlmodel import Field, Session, select, or_, asc, desc, text
from app.model.sql_model import Appointments, Doctors
from datetime import date, timedelta
import pandas as pd


def get_appointments(db: Session):
    statement = select(Appointments)
    return db.exec(statement).all()


def get_appointment_by_patient_username(db: Session, patient_username: str, skip: int = 0, limit: int = 30):
    # statement = select(Appointments).where(Appointments.patient_username == patient_username).order_by(
    #     Appointments.booking_date).offset(skip).limit(
    #     limit)
    # return db.exec(statement).all()
    stmt = text("""SELECT a.id, a.booking_date, a.patient_username, a.doctor_username, d.fullname doctor_fullname, 
        a.specialist, a.place, a.fromHour, a.toHour, a.status, a.is_BHYT,
        d.price FROM dbo.Appointments a
        left join dbo.Doctors d
        on a.doctor_username = d.username
        where a.patient_username = :du
        order by a.booking_date""")
    stmt = stmt.bindparams(du=patient_username)
    return db.exec(stmt).all()


# loc cuoc hen theo user dang nhap app (chi la bac si hoac chi la benh nhan)
def get_appointment_by_doctor_username(db: Session, username: str, skip: int = 0, limit: int = 200):
    # statement = select(Appointments).where(
    #     or_(Appointments.doctor_username == username, Appointments.patient_username == username)).order_by(
    #     Appointments.booking_date).offset(skip).limit(
    #     limit)
    # return db.exec(statement).all()
    stmt = text("""SELECT a.id, a.booking_date, a.patient_username, a.doctor_username, d.fullname doctor_fullname, 
            a.specialist, a.place, a.fromHour, a.toHour, a.status, a.is_BHYT,
            d.price FROM dbo.Appointments a
            left join dbo.Doctors d
            on a.doctor_username = d.username
            where a.doctor_username = :du
            order by a.booking_date""")
    stmt = stmt.bindparams(du=username)
    return db.exec(stmt).all()

# loc ngày xa nhất có lịch hẹn đã generate
def get_furthest_appointment_date_by_doctor_username(db: Session, username: str, skip: int = 0, limit: int = 10):
    statement = select(Appointments).where(Appointments.doctor_username == username).order_by(
        desc(Appointments.booking_date))
    result = db.exec(statement).first()
    if result is not None:
        return result.booking_date
    else:
        return pd.to_datetime("today")


def get_appointment_by_username(db: Session, doctor_username: str):
    statement = select(Appointments).where(Appointments.doctor_username == doctor_username)
    return db.exec(statement).first()


def create_appointment(db: Session, appointment: Appointments):
    db_appointment = Appointments.from_orm(appointment)
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    return db_appointment

# code backup
# def generate_appointment_of_doctor(db: Session, doctor: Doctors):
#     furthest_booking_date = get_furthest_appointment_date_by_doctor_username(db, doctor.username)
#     today = pd.to_datetime("today")
#     if furthest_booking_date is not None and furthest_booking_date > today + timedelta(days=31):
#         return True
#     List_Appointments = []
#     fromHour_range = []
#     if doctor.examination_schedule == 'S3':
#         booking_freq = 'W-TUE'
#         booking_dates = pd.date_range(today, today + timedelta(days=60), freq=booking_freq)
#     for each_date in booking_dates:
#         if doctor.examination_schedule[0:1] == 'S':  # lich kham buoi sang
#             fromHour_range = [8, 9, 10, 11, 12]
#         elif doctor.examination_schedule[0:1] == 'C':  # buoi chieu
#             fromHour_range = [13, 14, 15, 16, 17]
#         for fromHour in fromHour_range:
#             newAppointment = Appointments(doctor_username=doctor.username, booking_date=each_date,
#                                           fromHour=fromHour, toHour=fromHour + 1, status="AVAILABLE")
#             List_Appointments.append(newAppointment)
#
#     db.add_all(List_Appointments)
#     # db.add(Appointments[0])
#     db.commit()
#     # db.refresh(List_Appointments)
#     return True

# hàm generate lịch khám của bác sỹ dựa vào thông tin đăng ký khám trên DB
def generate_appointment_of_doctor(db: Session, doctor: Doctors):
    furthest_booking_date = get_furthest_appointment_date_by_doctor_username(db, doctor.username)
    today = pd.to_datetime("today")
    start_day = today
    # nếu đã generate lịch làm việc trong 1 tháng từ hiện tại rồi, thì return luôn
    if furthest_booking_date is not None and furthest_booking_date > today + timedelta(days=31):
        return True
    # thực hiện generate lịch làm việc trong vòng 2 tháng kể từ ngày xa nhất có lịch
    if furthest_booking_date is not None and furthest_booking_date > today:
        start_day = furthest_booking_date

    List_Appointments = []
    fromHour_range = []
    weekly_schedule_dictionary = {
        "S2": "W-MON",
        "S3": "W-TUE",
        "S4": "W-WED",
        "S5": "W-THU",
        "S6": "W-FRI",
        "S7": "W-SAT",
        "S8": "W-SUN",
        "C2": "W-MON",
        "C3": "W-TUE",
        "C4": "W-WED",
        "C5": "W-THU",
        "C6": "W-FRI",
        "C7": "W-SAT",
        "C8": "W-SUN"
    }

    # convert lịch làm việc bs từ string sang list (phân cách bởi dấu , như "S3,S4,C8")
    list_schedules = list(doctor.examination_schedule.replace(" ", "").split(","))
    for each_schedule in list_schedules:
        booking_freq = weekly_schedule_dictionary.get(each_schedule)
        booking_dates = pd.date_range(start_day, start_day + timedelta(days=60), freq=booking_freq)
        for each_date in booking_dates:
            if each_schedule[0:1] == 'S':  # lich kham buoi sang
                fromHour_range = [8, 9, 10, 11, 12]
            elif each_schedule[0:1] == 'C':  # buoi chieu
                fromHour_range = [13, 14, 15, 16, 17]
            for fromHour in fromHour_range:
                newAppointment = Appointments(doctor_username=doctor.username, booking_date=each_date,
                                              fromHour=fromHour, toHour=fromHour + 1, status="AVAILABLE")
                List_Appointments.append(newAppointment)

    db.add_all(List_Appointments)
    # db.add(Appointments[0])
    db.commit()
    # db.refresh(List_Appointments)
    return True


def update_appointment_by_id(db: Session, appointment: Appointments):
    statement = select(Appointments).where(Appointments.id == appointment.id)
    result = db.exec(statement).one()
    # result.booking_date = appointment.booking_date
    result.patient_username = appointment.patient_username
    result.doctor_username = appointment.doctor_username
    result.specialist = appointment.specialist
    result.place = appointment.place
    # result.fromHour = appointment.fromHour
    # result.toHour = appointment.toHour
    result.status = appointment.status
    result.is_BHYT = appointment.is_BHYT
    db.add(result)
    db.commit()
    db.refresh(result)
    return result


def delete_appointment_by_username(db: Session, username: str):
    statement = select(Appointments).where(Appointments.username == username)
    appointment = db.exec(statement).one()
    if appointment is None:
        return False
    db.delete(appointment)
    db.commit()
    return True


def test_sql(db: Session, doctor_username: str):
    stmt = text("""SELECT a.booking_date, a.patient_username, a.doctor_username, d.fullname doctor_fullname, 
        a.specialist, a.place, a.fromHour, a.toHour, a.status, a.is_BHYT,
        d.price FROM dbo.Appointments a
        left join dbo.Doctors d
        on a.doctor_username = d.username
        where a.doctor_username = :du""")
    stmt = stmt.bindparams(du=doctor_username)
    return db.exec(stmt).all()
