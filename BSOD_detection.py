# Using color and keywords match
import cv2
import os
import numpy as np
import pytesseract
from pytesseract import Output
import tkinter
from tkinter import *
from tkinter import ttk

# Function to check if path name entered is a image file or a folder
def imgfileFormat():
    path = imgpath_entry.get()
    extensions = ['.jpg', '.jpeg', '.png']
    try:
        if path.endswith(tuple(extensions)):
            t.delete('1.0', END)
            print(path)
            t.insert(END, path+"\n")
            img = cv2.imread(path)

            result = bsdetection(img)
            if (result == "Blue screen detected"):
                print(result)
                t.insert(END, result + "\n\n")
            elif (result == "No Blue Screen Detected"):
                print(result)
                t.insert(END, result + "\n\n")
        else:
            t.delete('1.0', END)
            for filename in os.listdir(path):
                if filename.endswith(tuple(extensions)):
                    print(filename)
                    t.insert(END, filename + "\n")
                    open(path + ".txt", "a").write("\n" + filename)
                    img = cv2.imread(os.path.join(path, filename))

                    result = bsdetection(img)
                    if (result == "Blue screen detected"):
                        print(result)
                        t.insert(END, result + "\n\n")
                        open(path + ".txt", "a").write("\n" + "Blue screen is detected")
                    elif (result == "No Blue Screen Detected"):
                        print(result)
                        t.insert(END, result + "\n\n")
                        open(path + ".txt", "a").write("\n" + "Blue screen is not detected")
    except OSError:
        print("\nImage file can't be found! \nEnter a valid file or folder name!")
        t.delete('1.0', END)
        t.insert(END, "\nImage file can't be found! \nEnter a valid file or folder name!\n\n")


# Function to check if path name entered is a video file or a folder
def vidfileFormat():
    path = vidpath_entry.get()
    extensions = ['.mp4', '.mkv']
    try:
        t.delete('1.0', END)
        if path.endswith(tuple(extensions)):
            frameRate(path)
        else:
            t.delete('1.0', END)
            for filename in os.listdir(path):
                if filename.endswith(tuple(extensions)):
                    frameRate(path + "/" + filename)
    except OSError:
        print("\nVideo file can't be found! \nEnter a valid file or folder name!")
        t.delete('1.0', END)
        t.insert(END, "\nVideo file can't be found! \nEnter a valid file or folder name!\n")

# Function to create a folder to store the frames of video file
def framesFolder(path):
    try:
        # creating a folder
        folderName = path + '.vidframes'
        if not os.path.exists(folderName):
            os.makedirs(folderName)
            print("Folder created")

        # if not created then raise error
    except OSError:
        print('Error: Creating directory of ' + folderName)


# Function to extract frames from video file
def captureFrame(vidpath, sec, count):
    # Read the video from specified path
    vidcap = cv2.VideoCapture(vidpath)
    vidcap.set(cv2.CAP_PROP_POS_MSEC, sec * 1000)
    hasFrames, image = vidcap.read()
    if hasFrames:
        name = vidpath + '.vidframes/frame' + str(count) + '.jpg'
        print('Creating...' + name)

        # writing the extracted images
        cv2.imwrite(name, image)

    return hasFrames


# Function to set frame rate to extract frames from video file
def frameRate(vidpath):
    rate = int(rate_entry.get())

    # Calling function to create folder
    framesFolder(vidpath)

    sec = 0
    count = 1
    # Calling function to extract frames
    success = captureFrame(vidpath, sec, count)
    while success:
        count = count + 1
        sec = sec + rate
        sec = round(sec, 2)
        success = captureFrame(vidpath, sec, count)

    print("Done extracting")

    # Calling function to detect BSoD
    vidBSdetection(vidpath)


# Function to check if bswords match words in the frame (even 1)
def wordMatch(bswords, framewords):
    match = list(set(bswords) & set(framewords))
    # print(sorted(match))
    # print(sorted(bswords))

    # if all the words in bswords list match with the words in match list
    if sorted(match) == sorted(bswords):
        # print(match)
        return True
    else:
        return False  # no matching


# Function to check if blue color is detected in the frame
def colorDetect(mask):
    # if there are any white pixels on mask, sum will be > 0
    hasBlue = np.sum(mask)
    if hasBlue > 0:
        # print('Blue detected!')
        return True
    else:
        return False


def check(path, str):
    with open(path + '.txt') as f:
        datafile = f.readlines()
        # found = False
    for line in datafile:
        if str in line:
            # found = True
            return True
    return False

# Print final output in terminal
def output(path):
    str = "\n*****************************************************************\n"
    if check(path, "Blue screen is detected"):
        str += 'BSoD Detected\n'
    else:
        str += 'No BSoD Detected\n'
    str += "*****************************************************************\n"

    return str


# Function to check the three conditions of detecting a BSoD
def bsdetection(img):
    # Pytesseract file path
    pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'

    # List of BSoD keywords
    bswords = ['error', 'problem', 'ran', 'info,', 'collecting']
    # bswords = ['Your', 'ran', 'into', 'a', 'problem', 'and', 'needs', 'to', 'restart.',
    #            "We're", 'just', 'collecting', 'some', 'error', 'info,', 'then', "we'll"]

    lower_range = np.array([0, 150, 250])
    upper_range = np.array([128, 255, 255])

    # Rescaling the image
    image = cv2.resize(img, None, fx=1.6, fy=1.6, interpolation=cv2.INTER_CUBIC)
    # Blurring
    image = cv2.blur(image, (3, 3))
    # Binary thresholding the image
    (thresh, image) = cv2.threshold(image, 70, 250, cv2.THRESH_BINARY)

    # img = cv2.imread(filename)
    text = pytesseract.image_to_data(image, output_type=Output.DICT)
    imgwords = text['text']
    # print(imgwords)

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_range, upper_range)
    blue_ratio = (mask > 0).mean()

    if ((colorDetect(mask)) and (wordMatch(bswords, imgwords)) and (blue_ratio >= 0.9)):
        return "Blue screen detected"
    else:
        return "No Blue Screen Detected"


# Function to check every frame for bs detection
def vidBSdetection(path):
    folderName = path + '.vidframes'
    t.insert(END, "\n" + path + "\n")
    for filename in os.listdir(folderName):
        print(filename)
        open(path + ".txt", "a").write("\n" + filename)
        img = cv2.imread(os.path.join(folderName, filename))

        result = bsdetection(img)
        if (result == "Blue screen detected"):
            print(result)
            open(path + ".txt", "a").write("\n" + "Blue screen is detected")
        elif (result == "No Blue Screen Detected"):
            print(result)
            open(path + ".txt", "a").write("\n" + "Blue screen is not detected")

    print(output(path))
    t.insert(END, output(path) + "\n")

    cv2.waitKey(0)


# Driver Code
if __name__ == '__main__':

    # GUI
    window1 = tkinter.Tk()
    window1.geometry("500x580")
    window1.resizable(0, 0)
    window1.configure(bg='#a7cfeb')
    window1.title("BSoD Detector")
    wlcm_label = tkinter.Label(window1, text="Welcome to BSoD Detector", background="#a7cfeb", width=30, height=2, font=("arial", 15, "bold"))
    wlcm_label.pack()

    rate_label = tkinter.Label(window1, font="Helvetica 9 bold", background="#a7cfeb", text="File Format :")
    rate_label.place(x=30, y=75)

    # Function called if Image format is selected
    def imageSelected():
        vid_frame.place_forget()
        img_frame.place(relheight=0.2, relwidth=0.9, x=30, y=120, anchor= NW)

    # Function called if Video format is selected
    def videoSelected():
        img_frame.place_forget()
        vid_frame.place(relheight=0.3, relwidth=0.9, x=30, y=120, anchor= NW)

    v = StringVar(window1, "1")
    rb1 = Radiobutton(window1, text="Image", variable=v, value="1", indicator=0,
                    background="light blue", width=8, height=1, command=imageSelected)
    rb1.place(x=140, y=72)
    rb2 = Radiobutton(window1, text="Video", variable=v, value="2", indicator=0,
                    background="light blue", width=8, height=1, command=videoSelected)
    rb2.place(x=206, y=72)

    # Creating frames in window1
    img_frame = Frame(window1, background="#a7cfeb")
    img_frame.place(relheight=0.2, relwidth=0.9, x=30, y=120, anchor= NW)
    vid_frame = Frame(window1, background="#a7cfeb")

    result_label = tkinter.Label(window1, font="Helvetica 9 bold", background="#a7cfeb", text="Latest Result :")
    result_label.place(x=30, y=250)

    # TextBox
    t = Text(window1, width=50, height=15, wrap=NONE, background='light gray', foreground='black')
    t.place(x=50, y=280)

    #Image frame
    imgpath_label = tkinter.Label(img_frame, font="Helvetica 9 bold", background="#a7cfeb", text="Image File/Folder :")
    imgpath_label.place(x=0, y=10)

    imgpath_entry = tkinter.Entry(img_frame, width=50)
    imgpath_entry.place(x=110, y=10)

    # Video frame
    vidpath_label = tkinter.Label(vid_frame, font="Helvetica 9 bold", background="#a7cfeb", text="Video File/Folder :")
    vidpath_label.place(x=0, y=0)

    vidpath_entry = tkinter.Entry(vid_frame, width=50)
    vidpath_entry.place(x=110, y=0)

    rate_label = tkinter.Label(vid_frame, font="Helvetica 9 bold", background="#a7cfeb", text="Frame Rate :")
    rate_label.place(x=0, y=41)

    rate_entry = tkinter.Entry(vid_frame, width=30)
    rate_entry.place(x=110, y=41)

    def typeChosen(choice):
        if choice == '1':
            imgfileFormat()
        elif choice == '2':
            vidfileFormat()

    def refresh():
        t.delete('1.0', END)

    # Button
    button1 = ttk.Button(window1, text="CHECK", command=lambda: typeChosen(v.get()))
    button1.place(x=210, y=200)

    button2 = ttk.Button(window1, text="Refresh", command=refresh)
    button2.place(x=300, y=540)

    button2 = ttk.Button(window1, text="Close", command=window1.destroy)
    button2.place(x=380, y=540)

    window1.mainloop()