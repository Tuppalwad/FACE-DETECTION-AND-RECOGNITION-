import cv2
# from flask import Flask
import face_recognition
import os 
import numpy as np

class video:
    def __init__(self,path) :
        self.image=[]
        self.path=path
        self.className=[]
        self.mylist=os.listdir(path)
        self.cam = cv2.VideoCapture(0)
        self.name=''
    
    def Find_encodings(self,imgs):
        encodelist=[]
        for img in imgs:
            img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
            encode=face_recognition.face_encodings(img)[0]
            encodelist.append(encode)
        return encodelist 
    def __del__(self):
        return self.cam.release()
    def get_person_name(self):
        self.get_name()
    def get_name(self):
                
        for i in self.mylist:
            curimg=cv2.imread(f'{self.path}/{i}')
            self.image.append(curimg)
            self.className.append(os.path.splitext(i)[0])

        encodelistknown=self.Find_encodings(self.image)


        cv2.namedWindow("Take Image")
        faceDetector=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        img_counter = 0

        while True:
            SUCCESS, frame = self.cam.read()
            resizeimg=cv2.resize(frame,(0,0),None,0.25,0.25) 
            resizeimg=cv2.cvtColor(resizeimg,cv2.COLOR_BGR2RGB)
            face=faceDetector.detectMultiScale(frame,1.3,5)
            facecurframe=face_recognition.face_locations(resizeimg)
            encodecurframe=face_recognition.face_encodings(resizeimg,facecurframe)

            for encodeFace,faceloc in zip(encodecurframe,facecurframe):
                maches=face_recognition.compare_faces(encodelistknown,encodeFace)
                facedistance=face_recognition.face_distance(encodelistknown,encodeFace)
                machindex=np.argmin(facedistance) 
                if maches[machindex]:
                    self.name=self.className[machindex].upper()
            
            
            if not SUCCESS:
                print("failed to grab frame")
                break
            for x,y,w,h in face:
                x1,y1=x+w,y+h 
                # cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,255),2)
                #top part
                cv2.line(frame,(x,y),(x+30,y),(255,0,255),12)
                cv2.line(frame,(x,y),(x,y+30),(255,0,255),12)

                cv2.line(frame,(x1,y),(x1-30,y),(255,0,255),12)
                cv2.line(frame,(x1,y),(x1,y+30),(255,0,255),12)
                #bottom part
                cv2.line(frame,(x,y1),(x+30,y1),(255,0,255),12)
                cv2.line(frame,(x,y1),(x,y1-30),(255,0,255),12)

                cv2.line(frame,(x1,y1),(x1-30,y1),(255,0,255),12)
                cv2.line(frame,(x1,y1),(x1,y1-30),(255,0,255),12)
            cv2.imshow("test", frame)

            k = cv2.waitKey(1)
            if k%256 == 27:
                # ESC pressed
                print("Escape hit, closing...")
                break
            elif k%256 == 32:
                # SPACE pressed
                img_name = "opencv_frame_{}.png".format(img_counter)
                cv2.imwrite(img_name, frame)
                print("{} written!".format(img_name))
                img_counter += 1
    
        self.cam.release()
        cv2.destroyAllWindows()
        return self.name if self.name!="" else '' 
path='Images'
v=video(path)
print(v.get_name())