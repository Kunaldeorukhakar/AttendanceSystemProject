import cv2
import face_recognition
import numpy as np
import os
from datetime import datetime
import json 
from tkinter import *
import csv

# Opening json file and reading data inside it.
with open("Studentinfo.json","r+") as f:
    data = json.load(f)
# Putting the data of json in lists and reading the images present inside the images folder.
path = "images"
images = []
classnames=[]
classrollno=[]
newattendance=[]
with open("Studentinfo.json","r+") as f:
    data = json.load(f)
    for p in data['studentinfo']:
        classnames.append(p['name'])
        classrollno.append(p['rollno'])
print(classnames)
print(classrollno)
mydir = os.listdir(path)
print(mydir)
for cl in mydir:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
# Creating function for finding the encodings of the images inside the images folder.
def findencodings(images):
    encodelist = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodelist.append(encode)
    return encodelist

encodelistknown = findencodings(images)
print('Encoding Complete')
# Creating function for adding the data of recognized image inside csv(Excel file).
def markattendance(name,rollno):
    with open("Attendance.csv","r+") as f:
        myDataList = f.readlines()
        Datelist = []
        namelist = []
        for line in myDataList:
            entry = line.split(',')
            Datelist.append(entry[3])
            namelist.append(entry[1])
        now = datetime.now()
        dtstring = now.strftime('%m/%d/%Y')
        tstring = now.strftime('%H:%M:%S')
        if dtstring not in Datelist or name not in namelist:
            f.writelines(f'\n{rollno},{name},{tstring},{dtstring}')
        else:
            print("Your Attendance has already been marked!")
# Creating function to recognize the face when the camera is on.
def face_recognize():
    cap = cv2.VideoCapture(0)
    while True:
        success, img = cap.read()
        imgS = cv2.resize(img,(0,0),None,0.25,0.25)
        imgS = cv2.cvtColor(imgS,cv2.COLOR_BGR2RGB)
        
        facesCurFrame = face_recognition.face_locations(imgS)
        encodeCurFrame = face_recognition.face_encodings(imgS,facesCurFrame)
        
        for encodeFace,faceLoc in zip(encodeCurFrame,facesCurFrame):
            matches = face_recognition.compare_faces(encodelistknown,encodeFace)
            faceDis = face_recognition.face_distance(encodelistknown,encodeFace)
            # print(faceDis)
            matchIndex = np.argmin(faceDis)
            if matches[matchIndex]:
                name = classnames[matchIndex].upper()
                rollno = classrollno[matchIndex]
                print(name)
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1*4 ,x2*4 ,y2*4 ,x1*4   
                cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
                cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
                cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
                markattendance(name,rollno)
        cv2.imshow('Webcam',img)
        k =cv2.waitKey(1)
        if k == 27:
            break
    cv2.destroyAllWindows()
# Creating a funtion to add a new user with images and other data.
def saveimage():
    imgroll = rollnovar.get()
    imgname = namevar.get()
    print(imgroll)
    print(imgname)
    cam = cv2.VideoCapture(0)
    
    cv2.namedWindow("Newuser")
    # img_counter = 0

    while True:
        ret, frame = cam.read()
        if not ret:
            print("failed to grab frame")
            break
        cv2.putText(frame,"Press SPACE to save & Esc to close",(20,20),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(255,0,0),1)
        cv2.imshow("Newuser", frame)
        k = cv2.waitKey(1)
        if k%256 == 27:
            # ESC pressed
            print("Escape hit, closing...")
            break
        elif k%256 == 32:
            # SPACE pressed
            img_name = "D:\Kunal projects\Attendance system using face recognition project\images\{}_{}.png".format(imgroll,imgname)
            cv2.imwrite(img_name, frame)
            print("{} written!".format(img_name))

            with open('Studentinfo.json') as json_file: 
                data = json.load(json_file) 
                temp = data['studentinfo']
                # python object to be appended 
                y = {"name":imgname, 
                    "rollno": imgroll
                    } 
                # appending data to studentinfo  
                temp.append(y)
            with open("Studentinfo.json",'w') as f:
                json.dump(data,f,indent=4) 
            # img_counter += 1
    # cam.release()
    cv2.destroyAllWindows()
# Designing of the gui start from here.
root = Tk()
root.geometry("1080x789")
root.title("Attendance System Using Face Recognition")
root['bg']='#524421'
# Heading
heading = Frame(root,bg='#524421')
heading.pack(fill=X,pady=15)
l1 = Label(heading,text="Face Recognition Based Attendance System",font="comicsansms 20 bold",bg="#524421",fg="white")
l1.pack()

# Left frame
lf = Frame(root,bg="skyblue")
lf.pack(side=LEFT,anchor="nw",fill=BOTH,padx=(40,10),pady=(20,80),expand=True) 
# Left frame heading
lft=Frame(lf,bg="green")
lft.pack(side=TOP,fill=X,pady=(0,20))
lb=Label(lft,text="Attendance Details",font="comicsansms 16 bold",bg="green")
lb.pack()
Label(lf,text="Attendance",bg='skyblue',font="comicsansms 16 bold").pack(pady=(15,0))
lbx = Listbox(lf,width=85,height=20)
with open('Attendance.csv', newline='') as csvfile:
    attendancereader = csv.reader(csvfile)
    for row in attendancereader:
        lbx.insert(END,row)
lbx.pack(padx=20)
Button(lf,text="Mark Attendance",bg="yellow",command=face_recognize,padx=160,font='comicsansms 16 bold').pack(pady=20)
Button(lf,text="Quit",bg="red",command=quit,padx=230,font='comicsansms 16 bold').pack(pady=20)

# Right Frame
rf = Frame(root,bg="skyblue")
rf.pack(side=RIGHT,anchor="ne",fill=BOTH,padx=(0,40),pady=(20,80),expand=True)
rollnovar=IntVar()
namevar=StringVar()
# Right frame heading
rft=Frame(rf,bg="green")
rft.pack(side=TOP,fill=X)
lb2=Label(rft,text="Add New Student",font="comicsansms 16 bold",bg="green",padx=40)
lb2.pack()

rollnolb=Label(rf,text="Enter Roll No.: ",pady=5,font="comicsansms 16 bold",bg='skyblue',padx=5)
rollnolb.pack(padx=120,pady=(60,0))
rollnoentry =Entry(rf,textvariable=rollnovar,width=60)
rollnoentry.pack(padx=10)

namelb=Label(rf,text="Enter Student Name: ",pady=5,font="comicsansms 16 bold",bg='skyblue')
namelb.pack(padx=110,pady=(50,0))
nameentry =Entry(rf,textvariable=namevar,width=60)
nameentry.pack(padx=10)
Button(rf,text="Take Photo",command=saveimage,padx=120,font='comicsansms 16 bold',bg='blue').pack(pady=(90,25))
# Button(rf,text="Save Profile",padx=120,font='comicsansms 16 bold',bg='blue').pack()

root.mainloop()









