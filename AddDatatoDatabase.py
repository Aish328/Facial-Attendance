import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
cred = credentials.Certificate("/home/aishanya/Desktop/Facial_attendance/facialattendance-19c89-firebase-adminsdk-9e5lh-1b16a2ae14.json")
firebase_admin.initialize_app(cred,{
    'databaseURL' : "https://facialattendance-19c89-default-rtdb.firebaseio.com"

})
ref = db.reference('students')      #creating a database reference to make directory named students where data is stored
data = {
    "1" : 
    {
        "name" : "Obama" , 
        "major" : "politics",
        "starting_year" : 2013,
        "total_attendance" : 23,
        "standing" : "G",
        "year" : 3,
        "last_attendance_time" : "2022-02-11 00:54:34"
    },
    "3" : 
    {
        "name" : "Elon" , 
        "major" : "politics",
        "starting_year" : 2015,
        "total_attendance" : 12,
        "standing" : "G",
        "year" : 4,
        "last_attendance_time" : "2022-02-11 00:54:34"
    },
    "2" : 
    {
        "name" : "Modi" , 
        "major" : "politics",
        "starting_year" : 2020,
        "total_attendance" : 42,
        "standing" : "G",
        "year" : 2,
        "last_attendance_time" : "2022-02-11 00:54:34"
    },
    "4" : 
    {
        "name" : "Aishanya" , 
        "major" : "Engineering",
        "starting_year" : 2021,
        "total_attendance" : 30,
        "standing" : "G",
        "year" : 4,
        "last_attendance_time" : "2022-02-11 00:54:34"
    }
}

for key, value in data.items():
    ref.child(key).set(value)                 #when we send data to specific directory, we use child