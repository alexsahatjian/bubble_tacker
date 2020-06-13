from tkinter import *
from tkinter.messagebox import showinfo
import 3Dmatch.py
import Pathfinder.py
import videoPlayback.py
import 3Dplayback.py
import BubbleDetect.py

master = Tk()

similarFramesValue = StringVar()
outputEntryValue = StringVar()
maxDistanceValue = StringVar()
minBlobAreaValue = StringVar()
maxHeightDiffValue = StringVar()


#///readFile=open("somepath")
#data=file.read()
#data=data.split("\n")
#similarFramesValue.set(data[])
#outputEntryValue.set(data[])
#maxDistanceValue.set(data[])
#minBlobArea.set(data[])
#maxHeightDiffValue.set(data[])
similarFramesValue.set("3")
outputEntryValue.set("C:\\")
maxDistanceValue.set(".3")
minBlobAreaValue.set("51")
maxHeightDiffValue.set(".1")


def fileExist(path, i=0):
    if(os.path.isfile(path + str(i) + ".mp4")):
        i +=  1
        return fileExist(path, i)
    else:
        return(str(path) + str(i))
def isValidVideo(path):
    extension = mimetypes.guess_type(path)
    if(os.path.isfile(path) and not os.path.isdir(path)):
        if(extension[0] == 'video/mp4' or extension[0]== 'video/avi' or extension[0]=='video/mov'):
            return True
        else:
            raise Error("Path is Invalid")
    else:
        raise Error("Path is Invalid")

def isValidOutput(path):
    if(os.path.isdir(path)):
        return True
    else:
        raise Error("Path is Invalid")

def videoOut():
    print("Hey")

def changeMe():
    run.grid_forget()
    settings.grid_forget()
    runVideo.grid_forget()
    outputLabel.grid()
    outputEntry.grid()
    similarFramesLabel.grid()
    similarFrames.grid()
    distanceLabel.grid()
    maxDistance.grid()
    minBlobAreaLabel.grid()
    minBlobArea.grid()
    maxHeightDiffLabel.grid()
    maxHeightDiff.grid()
    saveMeButt.grid()


def saveMe():
    try:
        int(similarFrames.get())
        try:
            float(maxDistance.get())
            try:
                isValidOutput(outputEntry.get())
                try:
                    float(maxHeightDiff.get())
                    try:
                        float(minBlobArea.get())
                        if(similarFrames.get() != ""):
                            similarFramesValue.set(similarFrames.get())
                        if(maxDistance.get() != ""):
                            maxDistanceValue.set(maxDistance.get())
                        if(minBlobArea.get() != ""):
                            minBlobAreaValue.set(minBlobArea.get())
                        if(maxHeightDiff.get() != ""):
                            maxHeightDiffValue.set(maxHeightDiff.get())
                        if(outputEntry.get() != ""):
                            outputEntryValue.set(outputEntry.get())
                        saveMeButt.grid_forget()
                        outputEntry.grid_forget()
                        similarFrames.grid_forget()
                        maxDistance.grid_forget()
                        distanceLabel.grid_forget()
                        minBlobArea.grid_forget()
                        minBlobAreaLabel.grid_forget()
                        saveMeButt.grid_forget()
                        run.grid()
                        settings.grid()
                        runVideo.grid()
                    except:
                        showinfo("Error","Enter Valid Double for Minimum Blob Area")
                except:
                    showinfo("Error","Enter Valid Double for Maximum Hieght Difference For 2 Bubbles To Be Considered a Match")
            except:
                showinfo("Error", "Enter Valid Path for Output Path")
        except:
            showinfo("Error","Enter Valid Double for Max Distance")
    except:
        showinfo('Error', "Enter Valid Integer for Number of Frames and Bubbles that Share a Common Height")

def match3D():


def trackMe():
    run.grid_forget()
    settings.grid_forget()
    runVideo.grid_forget()
    Video1Label.grid()
    Video1.grid()
    Video2Label.grid()
    Video2.grid()
    OriginXLabel.grid()
    OriginX.grid()
    OriginYLabel.grid()
    OriginY.grid()
    TiltLabel.grid()
    Tilt.grid()
    PixleToCMLabel.grid()
    PixleToCM.grid()
    OriginXLabel2.grid()
    OriginX2.grid()
    OriginYLabel2.grid()
    OriginY2.grid()
    TiltLabel2.grid()
    Tilt2.grid()
    PixleToCMLabel2.grid()
    PixleToCM2.grid()
    proccessMe.grid()

def validOrgin(path, x, y):  # change to your own video path
    vid = cv2.VideoCapture(path)
    height = vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
    width = vid.get(cv2.CAP_PROP_FRAME_WIDTH)
    if(x > width or y > height):
        raise Error("Invalid Origin")
    else:
        return True

def parameterValid():
    try:
        isValidVideo(Video1.get())
        try:
            isValidVideo(Video2.get())
            try:
                int(OriginX.get())
                try:
                    int(OriginY.get())
                    try:
                        float(Tilt.get())
                        if Tilt.get()>180 or Tilt.get()<-180:
                            raise Error("Tilt must be between -180 and 180")
                        try:
                            float(PixleToCM.get())
                            try:
                                int(OriginX2.get())
                                try:
                                    int(OriginY2.get())
                                    try:
                                        float(Tilt2.get())
                                        if Tilt2.get()>180 or Tilt2.get()<-180:
                                            raise Error("Tilt must be between -180 and 180")
                                        try:
                                            float(PixleToCM2.get())
                                        except:
                                            showinfo("Error","Enter Valid Double for Video 2 Pixle To CM")
                                    except:
                                        showinfo("Error","Enter Valid Double for Video 2 Tilt")
                                except:
                                    showinfo("Error","Enter Valid Integer for Video 2 Origin Y")
                            except:
                                showinfo("Error","Enter Valid Integer for Video 2 Origin X")
                        except:
                            showinfor("Error","Enter Valid Double for Video 1 Pixle To CM")
                    except:
                        showinfo("Error","Enter Valid Double for Video 1 Tilt")
                except:
                    showinfo("Error","Enter Valid Integer for Video 1 Origin X")
            except:
                showinfo("Error","Enter Valid Integer for Video 1 Origin X")
        except:
            showinfo("Error","Enter Valid Video Path for Video 2")
    except:
        showinfo("Error","Enter Valid Video Path for Video 1")
    try:
        validOrigin(Video1.get(),OriginX.get(),OriginY.get())
    except:
        showinfo("Error", "Origin outside of frame for Video 1")
    try:
        validOrigin(Video2.get(),OriginX2.get(),OriginY2.get())
    except:
        showinfo("Error","Origin outside of frame for Video 2")

    BubbleDetect.bubbleDetect(Video1.get(), outputEntry.get(), minBlobArea.get(), 'A')
    BubbleDetect.bubbleDetect(Video2.get(), outputEntry.get(), minBlobArea.get(), 'B')
    Pathfinder.pathFinder(maxDistance.get(),outputEntry.get())                                      #Start Here



run = Button(master, text='Run', command=trackMe)
runVideo = Button(master, text='Run Video Output', command=videoOut)
settings = Button(master, text='Settings', command=changeMe)

#Global Settings
outputLabel = Label(master, text="Enter Output Path")
similarFramesLabel = Label(master, text="Enter Number of Frames and Bubbles that Share a Common Height")
distanceLabel = Label(master, text="Enter Max Distance")
minBlobAreaLabel = Label(master, text="Enter Minimum Blob Area")
maxHeightDiffLabel = Label(master, text="Max Height Difference")

outputEntry = Entry(master,textvariable=outputEntryValue) #Check for path
maxDistance = Entry(master, textvariable=maxDistanceValue) #Check for double#
minBlobArea = Entry(master, textvariable=minBlobAreaValue) #Check for numeric#
maxHeightDiff = Entry(master, textvariable=maxHeightDiffValue)#check for double
similarFrames = Entry(master, textvariable=similarFramesValue)

saveMeButt = Button(master, text='Save', command=saveMe)

Video1Label= Label(master,text = "Video 1 Name")
Video2Label = Label(master, text = "Video 2 Name")
OriginXLabel = Label(master, text ="X Origin Value")
OriginYLabel = Label(master, text ="Y Origin Value" )
TiltLabel = Label(master, text = "Tilt" )
PixleToCMLabel = Label(master, text = "Pixle to CM" )
OriginXLabel2 = Label(master, text = "X Origin Value")
OriginYLabel2 = Label(master, text = "Y Origin Value")
TiltLabel2 = Label(master, text = "Tilt")
PixleToCMLabel2 = Label(master, text = "Pixle to CM")

Video1 = Entry(master)
Video2 = Entry(master)
OriginX = Entry(master)
OriginY = Entry(master)
Tilt = Entry(master)
PixleToCM = Entry(master)
OriginX2 = Entry(master)
OriginY2 = Entry(master)
Tilt2 = Entry(master)
PixleToCM2 = Entry(master)

proccessMe= Button(master, text="Next", command=parameterValid)

run.grid()
settings.grid()
runVideo.grid()
#minBlobArea.grid_forget()
#minBlobAreaLabel.grid_forget()
#distanceLabel.grid_forget()
#maxDistance.grid_forget()
#outputLabel.grid_forget()
#outputEntry.grid_forget()
mainloop()
