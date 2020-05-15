# -*- coding: utf-8 -*-
"""
Created on Mon Feb  3 16:01:15 2020

@author: JD
"""
import numpy as np
import cv2

file=open("DefPath.txt")
data=file.read()
data=data.split(']]]\n')
for path in range(0,len(data)):
    data[path]=data[path].split('], ')
    for element in range(0,len(data[path])):
        data[path][element]=data[path][element].split(', ')
        for thing in range(0,len(data[path][element])):
            data[path][element][thing]=data[path][element][thing].replace('[','')
            data[path][element][thing]=data[path][element][thing].replace('|','')
            data[path][element][thing]=data[path][element][thing].replace('"','')
            try:
                data[path][element][thing]=float(data[path][element][thing])
            except:
                data[path][element][thing]=data[path][element][thing]

for entry in data:
    if entry==[['']]:
        data.remove(entry)

pathDict={}
for entry in range(0,len(data)):
    pathNum=data[entry][0][0]
    data[entry][0].remove(pathNum)
    pathDict[pathNum]=data[entry]

for key,value in pathDict.items():
    x='key: ' + str(key) + ' len: ' +str(len(value))
    print(x)
    
names=[r'C:\Users\JD\Documents\Bubble Research\Videos\2-3-20_vid1\front_trim.mp4',r'C:\Users\JD\Documents\Bubble Research\Videos\2-3-20_vid1\side_trim_1.mp4']
window_titles=['front','side']

cap = [cv2.VideoCapture(i) for i in names]
z=0
frames = [None] * len(names);
gray = [None] * len(names);
ret = [None] * len(names);

pixlesToCM1=140
pixlesToCM2=170.6
xOrigin,yOrigin=278,100
xOrigin2,yOrigin2=168,37

while True:

    for i,c in enumerate(cap):
        if c is not None:
            ret[i], frames[i] = c.read();


    for i,f in enumerate(frames):
        if ret[i] is True:
            for pathNum,path in pathDict.items():
                if int(path[0][-1])<=z and int(path[0][-1])+len(path)>z:
                    frameOffset=z-int(path[0][-1])
                    if i==0:
                        cv2.circle(frames[i],(int(path[frameOffset][0]*pixlesToCM1)+xOrigin,int(path[frameOffset][2]*pixlesToCM1)+yOrigin),int((path[frameOffset][4]+path[frameOffset][3])*pixlesToCM1/4),((47*pathNum)%255,(77*pathNum)%255,(37*pathNum)%255))
                    else:
                        cv2.circle(frames[i],(int(path[frameOffset][1]*pixlesToCM2)+xOrigin2,int(path[frameOffset][2]*pixlesToCM2)+yOrigin2),int((path[frameOffset][4]+path[frameOffset][3])*pixlesToCM2/4),((47*pathNum)%255,(77*pathNum)%255,(37*pathNum)%255))
            #gray[i] = cv2.cvtColor(f, cv2.COLOR_BGR)
            cv2.imshow(window_titles[i], frames[i]);

    if cv2.waitKey(100) & 0xFF == ord('q'):
        break
    
    z+=1

for c in cap:
    if c is not None:
        c.release();

cv2.destroyAllWindows()




            
