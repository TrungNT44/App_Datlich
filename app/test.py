from sqlmodel import Field, Session, select, or_, asc, desc, text
from app.model.sql_model import Appointments, Doctors
from datetime import date, timedelta
import pandas as pd

today = pd.to_datetime("today")
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
list_schedules = list("S8 , C2".replace(" ", "").split(","))
for each_schedule in list_schedules:
    # if each_schedule == 'S3':
    #     booking_freq = 'W-TUE'
    #     booking_dates = pd.date_range(today, today + timedelta(days=60), freq=booking_freq)
    booking_freq = weekly_schedule_dictionary.get(each_schedule)
    booking_dates = pd.date_range(today, today + timedelta(days=10), freq=booking_freq)
    for each_date in booking_dates:
        if each_schedule[0:1] == 'S':  # lich kham buoi sang
            fromHour_range = [8, 9, 10, 11, 12]
        elif each_schedule[0:1] == 'C':  # buoi chieu
            fromHour_range = [13, 14, 15, 16, 17]
        for fromHour in fromHour_range:
            newAppointment = Appointments(doctor_username="trung", booking_date=each_date,
                                          fromHour=fromHour, toHour=fromHour + 1, status="AVAILABLE")
            List_Appointments.append(newAppointment)

for x in List_Appointments:
    print(x)
#print(List_Appointments)