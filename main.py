import tkinter
from tkinter import filedialog
import cv2
import PIL.Image, PIL.ImageTk
from functools import partial
import threading
import imutils
import time

flag = True

#Browsing Video Clip from File System
def browse_clip():
    """Method used to Browse Video Clip"""
    clip = filedialog.askopenfilename(initialdir="E:\BCA5-MiniProject(DRS)",type=("*.mp4"))
    global stream
    stream = cv2.VideoCapture(clip)

#Creating play function
def play(speed):
    """Method used to control the flow of Video Clip"""
    global flag
    #playing the video clip in reverse/forward mode
    frame1 = stream.get(cv2.CAP_PROP_POS_FRAMES)
    stream.set(cv2.CAP_PROP_POS_FRAMES,frame1 + speed)

    grabbed,frame = stream.read()
    #Exit the window when video ends
    if not grabbed:
        exit()
    frame = imutils.resize(frame,width=SET_WIDTH,height=SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0,0,image = frame,anchor = tkinter.NW)
    if flag:
        #Creating Blinking "Decision Pending" Text
        canvas.create_text(140,29, fill="Red",font = "Times 26 italic bold", text="Decision Pending")
    flag = not flag

#Creating pending function
def pending(decision):
    """Method used to show decision pending image, sponsor image and display out/not out image"""
    #Display decision pending image
    frame = cv2.cvtColor(cv2.imread("pending.png"),cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame,width=SET_WIDTH,height=SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0,0,image=frame,anchor=tkinter.NW)

    #Wait for 1 second
    time.sleep(1)

    #Display sponsor image
    frame = cv2.cvtColor(cv2.imread("sponsor.png"), cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0, 0, image=frame, anchor=tkinter.NW)

    #Display 1.5 second
    time.sleep(1.5)

    #Display out/decision
    if decision == "out":
        decisionImg = "out.png"
    else:
        decisionImg = "not_out.png"
    frame = cv2.cvtColor(cv2.imread(decisionImg), cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0, 0, image=frame, anchor=tkinter.NW)


#Creating out function
def out():
    """Method used for out decision"""
    thread = threading.Thread(target=pending,args=("out",))
    thread.daemon = 1
    thread.start()

# Creating not out function
def not_out():
    """Method used for not out decision"""
    thread = threading.Thread(target=pending,args=("not_out",))
    thread.daemon = 1
    thread.start()

# Intializing window screen dimentions
SET_WIDTH = 650
SET_HEIGHT = 368

# Creating Window screen
window = tkinter.Tk()

#Changing Window background colour
window.configure(bg="Pink")

# Setting max and min size of the window
window.maxsize(SET_WIDTH,SET_HEIGHT+200)
window.minsize(SET_WIDTH,SET_HEIGHT+200)

# Assigning title to the window
window.title("Decision Review System(Mini Project BCA5)")

# Reading Welcome image
cv_img = cv2.cvtColor(cv2.imread("Welcome.png"),cv2.COLOR_BGR2RGB)
    
# Creating Canvas for Welcome image
canvas = tkinter.Canvas(window,width = SET_WIDTH, height = SET_HEIGHT)
photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(cv_img))

# Packing Welcome image to window screen
image_on_canvas = canvas.create_image(0,0,ancho=tkinter.NW,image=photo)
canvas.pack()

#Buttons to Control Playback

#Creating Browse Button
btn = tkinter.Button(window,bg="black",fg="white",text="Browse",width=50,command=browse_clip)
btn.pack()

#Creating Previous(fast) Button
btn = tkinter.Button(window,bg="black",fg="white",text="<<Previous(fast)",width=50,command=partial(play,-25))
btn.pack()

#Creating Previous(slow) Button
btn = tkinter.Button(window,bg="black",fg="white",text="<<Previous(slow)",width=50,command=partial(play,-2))
btn.pack()

#Creating Forward(fast) Button
btn = tkinter.Button(window,bg="black",fg="white",text="Foword(fast)>>",width=50,command=partial(play,25))
btn.pack()

#Creating Forward(slow) Button
btn = tkinter.Button(window,bg="black",fg="white",text="Foword(slow)>>",width=50,command=partial(play,2))
btn.pack()

#Creating Out Button
btn = tkinter.Button(window,bg="black",fg="white",text="Out!",width=50,command = out)
btn.pack()


#Creating Not Out Button
btn = tkinter.Button(window,bg="black",fg="white",text="Not Out!",width=50,command = not_out)
btn.pack()

#displaying window
window.mainloop();


