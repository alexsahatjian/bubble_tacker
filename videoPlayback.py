# -*- coding: utf-8 -*-
"""
This program plays the video used in BubbleTracker.m but puts green circles around the tracked paths. Hey
"""
#import random
import cv2
#import numpy as np
def videoPlayRun(AorBFlag,X0,Y0,P2CM,inputPath):
    '''Read in data from Pathfinder.py'''
    if(AorBFlag=="B")
        vidPath=intputPath+"B_paths.txt"
    else:
        vidPath=inputPath+"A_paths.txt"
    file=open(vidPath)
    data=file.read()
    data=data.replace(", \"end\"",'')
    data=data.split('\n')
    for index in range(0,len(data)):
        data[index]=data[index].split('], [')
        for index1 in range(0,len(data[index])):
            data[index][index1]=data[index][index1].replace("[[",'')
            data[index][index1]=data[index][index1].replace("]]",'')
            data[index][index1]=data[index][index1].split(',')
            for index2 in range(0,len(data[index][index1])):
                try:
                    data[index][index1][index2]=float(data[index][index1][index2])
                except:
                    data.pop(index)

    '''Create a list of bubble positions at each frame where index of framePoints is the frame number'''
    framePoints=[[] for i in range(0,7079)]
    for thing in data:
        startFrame=int(thing[0][-1])
        lenPath=len(thing)
        for index in range(0,lenPath):
            if framePoints[startFrame+index]==0:
                framePoints[startFrame+index]=[[thing[index][0],thing[index][1]]]
            else:
                framePoints[startFrame+index].append([thing[index][0],thing[index][1]])

    originX,originY=X0,Y0
    pixleToCM=P2CM

    '''Create video play back device'''
    video=cv2.VideoCapture(r'C:\Users\JD\Documents\Bubble Research\Videos\2-3-20_vid1\side_trim.mp4')
    i=0
    #video.set(3,1920)
    #video.set(4,1080)
    while(video.isOpened()):
        ret,frame=video.read()
        cv2.namedWindow("frame",0)
        #cv2.resizeWindow("frame",1920,1080)
        if i>len(framePoints):
            break
        if ret==True:
        '''Draw a green circle at each tracked position for each frame'''
            for index in range(0,len(framePoints[i])):
                cv2.circle(frame,(int(pixleToCM*framePoints[i][index][0])+originX,int(pixleToCM*framePoints[i][index][1])+originY),50,(0,255,0))
            cv2.imshow('Frame',frame)
            '''cv2.waitKey determines the speed of video if you want a slower video increase this value'''
            if cv2.waitKey(100) & 0xFF == ord('q'):
                break
        else:
            break
        i+=1
    #cv2.namedWindow("frame",0)
    #cv2.resizeWindow("frame",1920,1080)
    video.release()
    cv2.destroyAllWindows
       

        

