#we'll generate all encoing we need of faces
import cv2
import face_recognition
import pickle
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

cred = credentials.Certificate("/home/aishanya/Desktop/Facial_attendance/facialattendance-19c89-firebase-adminsdk-9e5lh-1b16a2ae14.json")
firebase_admin.initialize_app(cred,{
    'databaseURL' : "https://facialattendance-19c89-default-rtdb.firebaseio.com",
    'storageBucket' : "facialattendance-19c89.appspot.com"

})


#importing the student images
folderPath = '/home/aishanya/Desktop/Facial_attendance/Images'
path_list = os.listdir(folderPath)
print(path_list)
imgList = []
studentIDs = []     #importing IDs
for path in path_list:
    imgList.append(cv2.imread(os.path.join(folderPath , path)))
    
    studentIDs.append(os.path.splitext((path)[0] ))
# print(studentIDs)
    fileName = os.path.join(folderPath , path)
    bucket = storage.bucket()
    blob = bucket.blob(fileName)
    blob.upload_from_filename(fileName)

#we'll send a list to this fucntion and this fucntion will generate all encodings and split out list with all the encodings
def findEcodings(ImagesList):
    encodeList = []
    for img in ImagesList:
        #changing colour : step1 
        img = cv2.cvtColor(img , cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]#finding encodings of the colour converted image : step2
        encodeList.append(encode)
    return encodeList

print("encoding started")
EncodeListKnown = findEcodings(imgList)
EncodeListKnownwithIDs = [EncodeListKnown,studentIDs]
print("encoding complete")
print(EncodeListKnown)

#saving into pickle
file = open("EncodeFile.p" , 'wb')
pickle.dump(EncodeListKnownwithIDs , file)
file.close()
print("file saved")