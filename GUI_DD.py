import tkinter as tk
from threading import Thread
import pyttsx3
from comtypes.safearray import numpy
from PIL import ImageTk, Image
from scipy.spatial import distance
import PIL
import cv2
import dlib
from imutils import  face_utils
import face_recognition
import os
import csv
import GUI_BAR
import GUI_USERS
from datetime import datetime
import GUI_line
encode_list=[]
name=[]
mylist=os.listdir("re/known/")
def Open_bar():
    GUI_BAR.bar_chart()
file_name=datetime.now().day.__str__()+"-"+datetime.now().month.__str__()+"-"+datetime.now().year.__str__()+".csv"
if  os.path.exists("re/user_files/"+file_name):
    pass
else:
    with open("re/user_files/"+file_name,'w',newline="") as file:
        writer=csv.writer(file)
        writer.writerow(["name","hours"])

#file_name=datetime.now().day.__str__()+"-"+datetime.now().month.__str__()+"-"+datetime.now().year.__str__()+".csv"
if  os.path.exists("re/drowsiness_files/"+file_name):
    pass
else:
    with open("re/drowsiness_files/"+file_name,'w',newline="") as file:
        writer=csv.writer(file)
        writer.writerow(["name","time","EAR"])
for i in mylist:
    img=face_recognition.load_image_file("re/known/"+i)
    img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    encode=face_recognition.face_encodings(img)[0]
    encode_list.append(encode)
    name.append(os.path.splitext(i)[0])
class data_t:
    EAR_tr = 0.3
    EAR_FRAME = 15
    COUNTER = 0
    FLAG_S=False
    FRAME_First=True
    name=""
    FLAG_START=False
    stime = None
    etime = None
    pt = None
    frame_c=0
d=data_t

#Load Detoctor and predictor
det=cv2.CascadeClassifier("haarcascades\haarcascade_frontalface_default.xml")
pre=dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
def Start_frame():
    d.FLAG_START=True
    show_frame()
    start_b["state"] = "disabled"
    view_user_b["state"] = "disabled"
    report_b["state"] = "disabled"
    report_b1["state"] = "disabled"
    end_b["state"] = "active"
def Stop_frame():
    d.FLAG_START = False
    start_b["state"]="active"
    view_user_b["state"]="active"
    report_b["state"] = "active"
    report_b1["state"] = "active"
    end_b["state"] = "disabled"
    d.FLAG_START=False
    d.etime=datetime.now()
    d.pt=d.etime - d.stime
    print(d.stime)
    print(d.etime)
    print(d.pt)
    d.pt=str(d.pt)
    d.pt=datetime.strptime(d.pt,"%H:%M:%S.%f")
    with open("re/user_files/"+file_name, 'a') as file:
        writer=csv.writer(file)
        tot=(d.pt.minute * 0.0166667)+d.pt.hour
        writer.writerow([d.name,tot])

width, height = 800, 600
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
root=tk.Toplevel()
background = "dbms.png"
img=Image.open(background)
img=img.resize((800, 600), Image.ANTIALIAS)
img = ImageTk.PhotoImage(img)
panel = tk.Label(root, image=img)
panel.image = img
panel.pack()
selction=tk.Frame(root)
selction.pack()

#panel.grid(row=1,column=1)
start_b=tk.Button(selction,text="Start",command=Start_frame)
start_b.grid(row=1,column=1)
#start_b.pack()
end_b=tk.Button(selction,text="Stop",command=Stop_frame)
end_b["state"]="disabled"
end_b.grid(row=1,column=2)
view_user_b=tk.Button(selction,text="View Users",command=GUI_USERS.Users)
view_user_b.grid(row=1,column=3)
report_b=tk.Button(selction,text="Bar Chart",command=Open_bar)
report_b.grid(row=1,column=4)
report_b1=tk.Button(selction,text="Line Chart",command=GUI_line.bar_chart)
report_b1.grid(row=1,column=5)
#end_b.pack()
def Speak():
   engine = pyttsx3.init()
   engine.setProperty('volume', 1.0)
   engine.say("Wake Up"+d.name)
   engine.runAndWait()
   d.FLAG_S=False
def eye_aspect_ratio(eye):
   A=distance.euclidean(eye[1],eye[5])
   B=distance.euclidean(eye[2],eye[4])
   C=distance.euclidean(eye[0],eye[3])
   ear=(A+B)/(2.0*C)
   return ear

def find_eye(shape):
   (lstart, lend) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
   (rstart, rend) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]
   lefteye=shape[lstart:lend]
   righteye=shape[rstart:rend]
   leftEAR=eye_aspect_ratio(lefteye)
   right_EAR=eye_aspect_ratio(righteye)
   ear=(leftEAR+right_EAR)/2
   return ear,leftEAR,right_EAR


def show_frame():
    _, frame = cap.read()
    #frame = cv2.flip(frame, 1)
    #Code for Drowsiness
    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    rects=det.detectMultiScale(gray,scaleFactor=1.1,minNeighbors=5,flags=cv2.CASCADE_SCALE_IMAGE)
    if d.FRAME_First:
        loct = face_recognition.face_locations(frame)
        encodet = face_recognition.face_encodings(frame)
        for face, loca in zip(encodet, loct):
            match = face_recognition.compare_faces(encode_list, face, 0.5)
            dist = face_recognition.face_distance(encode_list, face)
            matin = numpy.argmin(dist)
            if match[matin]:
                frame = cv2.rectangle(frame, (loca[3], loca[0]), (loca[1], loca[2]), (0, 255, 0), 2)
                frame = cv2.putText(frame, name[matin], (loca[3], loca[2] + 48), cv2.FONT_HERSHEY_DUPLEX, 2, (0, 255, 0),4)
                d.name=name[matin]
            else:
                h = loca[2] - loca[0]
                w = loca[1] - loca[3]
                crop_img = frame[loca[0]:loca[0] + h, loca[2]:loca[2] + w]
                cv2.imwrite("re/unknown/unknown.png", crop_img)
                d.name=""
                frame = cv2.rectangle(frame, (loca[3], loca[0]), (loca[1], loca[2]), (0, 255, 0), 2)
                frame = cv2.putText(frame, "Unknown", (loca[3], loca[2] + 48), cv2.FONT_HERSHEY_DUPLEX, 2, (0, 255, 0), 4)
            print(match)
            print(dist)
            d.stime=datetime.now()
            d.FRAME_First=False
        #,minSize=(30,30)
    for (x,y,w,h) in rects:
        rect=dlib.rectangle(int(x),int(y),int(x+w),int(y+h))

        shape=pre(gray,rect)
        shape=face_utils.shape_to_np(shape)

        eye=find_eye(shape)
        ear=eye[0]
        leftEAR=eye[1]
        rightEAR=eye[2]
        if d.frame_c > 100:
            with open("re/drowsiness_files/" + file_name, 'a', newline="") as file:
                writer = csv.writer(file)
                date=str(datetime.now().time().hour) + ":" + str(datetime.now().time().minute) + ":" + str(datetime.now().time().second)
                writer.writerow([d.name, date, ear])
            d.frame_c = 0
        d.frame_c=d.frame_c+1
        if ear<d.EAR_tr:
            print(d.COUNTER)
            d.COUNTER = d.COUNTER + 1
            if d.COUNTER>d.EAR_FRAME:
                print("You are sleeping")
                with open("re/drowsiness_files/"+file_name,'a',newline="") as file:
                    writer=csv.writer(file)
                    date=str(datetime.now().time().hour) + ":" + str(datetime.now().time().minute) + ":" + str(datetime.now().time().second)
                    writer.writerow([d.name,date,ear])
                if not d.FLAG_S:
                    d.FLAG_S=True
                    t=Thread(target=Speak())
                    t.daemon=True
                    t.start()
        else:
            d.COUNTER = 0

    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    img = PIL.Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    panel.imgtk = imgtk
    panel.configure(image=imgtk)
    if d.FLAG_START:
        panel.after(10, show_frame)
if d.FLAG_START:
    show_frame()
root.mainloop()



