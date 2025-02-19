#GRAPHICS

import cv2
import os
import pickle
import face_recognition
import numpy as np
import cvzone
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
from datetime import datetime
cred = credentials.Certificate("/home/aishanya/Desktop/Facial_attendance/facialattendance-19c89-firebase-adminsdk-9e5lh-1b16a2ae14.json")

firebase_admin.initialize_app(cred,{
    'databaseURL' : "https://facialattendance-19c89-default-rtdb.firebaseio.com/",
    'storageBucket' : "facialattendance-19c89.appspot.com"

})
bucket = storage.bucket()
cap = cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)

img_background = cv2.imread('/home/aishanya/Desktop/Facial_attendance/Resources/background.png')
#importing mode images into a list
folderModePath = '/home/aishanya/Desktop/Facial_attendance/Resources/Modes'
mode_path_list = os.listdir(folderModePath)
imgModeList = []
for path in mode_path_list:
    imgModeList.append(cv2.imread(os.path.join(folderModePath , path)))
# print(len(imgModeList))

#load the encoding files
print("loading encode file")
file = open('EncodeFile.p' , 'rb')
EncodeListKnownwithIDs = pickle.load(file)
file.close()
EncodeListKnown,studentIDs = EncodeListKnownwithIDs
print("studentzzIdZZ" ,studentIDs)
print("encode file loaded")
modeType = 0
counter = 0
id = -1
imgStudent = []
while True:
    success , img = cap.read()

    #scaling down the image
    imgSmall = cv2.resize(img , (0,0) , None ,0.25 , 0.25   )
    imgSmall  = cv2.cvtColor(imgSmall , cv2.COLOR_BGR2RGB)
    #faces in the current frame :
    faceCurFrame = face_recognition.face_locations(imgSmall)
    #encoding in current frame
    encodeCurFrame = face_recognition.face_encodings(imgSmall,faceCurFrame)

    img_background[162:162+480 , 55:55+640] = img       #overlapping webcam on img_background
    img_background[44:44+633 , 808:808+414] = imgModeList[modeType]       #overlapping webcam on img modes in imgModeList
    if faceCurFrame:
        for encodeFace , faceLoc in zip(encodeCurFrame,faceCurFrame):
            matches = face_recognition.compare_faces(EncodeListKnown, encodeFace)
            face_dist = face_recognition.face_distance(EncodeListKnown, encodeFace)
            # print("matches" , matches)
            print("face_dist : " , face_dist)
            matchIndex = np.argmin(face_dist)
            print("match index : " , face_dist[matchIndex])
            
            if matches[matchIndex]:
                print("matches : ", matches[matchIndex])
                print("known face detected")
                print("studentId" , studentIDs[matchIndex])
                
                y1,x1,y2,x2 =faceLoc
                y1,x1,y2,x2 = y1*4,x2*4,y2*4,x2*4
                bbox = 55 + x1 , 162 + y1 , x2-x1 , y2-y1
                imgbackground = cvzone.cornerRect(img_background, bbox,rt = 0)
                
                id = studentIDs[matchIndex]
                print("ids" , id[0])
                id = id[0]
                if counter ==0:
                    counter = 1
                    modeType  = 1
        if counter != 0:

            if counter== 1:
                #print(f"Attempting to retrieve data for student ID: {id}")
                #get the data
                path = f'students/{id}'
                
                print(f"Querying path: {path}")
                studentInfo = db.reference(path).get()
                print("studentsInfo:", studentInfo)
                #get image from storage
                blob = bucket.get_blob(f'/home/aishanya/Desktop/Facial_attendance/Images/{id}.jpeg')
                # print(f"Blob path: {blob.name}")
                # print(f"Blob exists: {blob.exists()}")
                array = np.frombuffer(blob.download_as_string(),np.uint8)
                imgStudent = cv2.imdecode(array,cv2.COLOR_BGRA2BGR)
                
                #update data of attendance
                datetimeObject = datetime.strptime(studentInfo['last_attendance_time'], "%Y-%m-%d %H:%M:%S")
                seconds_elapse = (datetime.now()-datetimeObject).total_seconds()
                print("seconds_elapses" , seconds_elapse)
                if seconds_elapse > 30:
                    
                    ref = db.reference(path)
                    studentInfo['total_attendance'] += 1
                    ref.child('total_attendance').set(studentInfo['total_attendance'])
                    ref.child('total_attendance_time').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                else:
                    modeType = 3
                    counter = 0 
                    img_background[44:44+633 , 808:808+414] = imgModeList[modeType]       #overlapping webcam on img modes in imgModeList
            if modeType  != 3:
                                
                if 10<counter < 20:
                    modeType = 1
                img_background[44:44+633 , 808:808+414] = imgModeList[modeType]       #overlapping webcam on img modes in imgModeList
                        
                        
                if counter <= 10:
                    cv2.putText(imgbackground , str(studentInfo['total_attendance']) , (861,125) , cv2.FONT_HERSHEY_COMPLEX , 1,(255,255,255) , 1)
                    (w , h ) , _ = cv2.getTextSize(studentInfo['name'],cv2.FONT_HERSHEY_COMPLEX,1,1)

                    offset = (414-w)//2
                    
                    cv2.putText(imgbackground , str(studentInfo['name']) , (808+offset,445) , cv2.FONT_HERSHEY_COMPLEX , 1,(255,255,255) , 1)
                    cv2.putText(imgbackground , str(studentInfo['major']) , (808 + offset,580) , cv2.FONT_HERSHEY_COMPLEX , 1,(255,255,255) , 1)
                    # cv2.putText(imgbackground , str(studentInfo['id']) , (1006,493) , cv2.FONT_HERSHEY_COMPLEX , 1,(255,255,255) , 1)
                    cv2.putText(imgbackground , str(studentInfo['standing']) , (910,625) , cv2.FONT_HERSHEY_COMPLEX , 1,(255,255,255) , 1)
                    cv2.putText(imgbackground , str(studentInfo['year']) , (1025,625) , cv2.FONT_HERSHEY_COMPLEX , 1,(255,255,255) , 1)
                    cv2.putText(imgbackground , str(studentInfo['starting_year']) , (1125,625) , cv2.FONT_HERSHEY_COMPLEX , 1,(255,255,255) , 1)
                    imgStudent_resized = cv2.resize(imgStudent, (216, 226))
                    img_background[175:175+226, 909:909+216] = imgStudent_resized
                counter+= 1
                if counter >= 20:
                    counter = 0 
                    modeType = 3
                    studentInfo = []
                    imgStudent = []
                    img_background[44:44+633 , 808:808+414] = imgModeList[modeType]       #overlapping webcam on img modes in imgModeList
    else : 
        modeType = 0
        counter = 0
         


    # cv2.imshow("Fweb cam" , img)
    cv2.imshow("Face Attendance" , img_background)
    cv2.waitKey(1)