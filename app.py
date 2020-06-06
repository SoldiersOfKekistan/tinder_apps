"""
This is a local Tinder application.
Use Up/Down arrow keys to navigate between profiles.
Use Left/Right arrow keys to navigate between pictures.

Requires tkinter and Pillow.
"""

from path import Path
import os
from tkinter import *
from PIL import Image, ImageTk
import random

"""
To browse different folders, modify the root variable.
.women   -> women's folder set in path.py
.men     -> men's   folder set in path.py
[number] -> number of directory to show
"""
root = Path().women[0]

def show_profile():
    global win, current_image, images, image_index, path, name_label, bio_label, pic_label
    image_index = 0
    images = os.listdir(path)
    images.remove("info.txt")

    img = Image.open(path+"/"+ images[0])
    ratio = min(display[0]/img.size[0], display[1]/img.size[1])
    resized = img.resize((int(ratio*img.size[0]), int(ratio*img.size[1])))
    current_image = ImageTk.PhotoImage(resized)
    pic_label.configure(image=current_image)

    name = path.split("/")[-1].split("_")[0]
    name_label.configure(text=name)
    bio_text = ""
    with open(path+"/info.txt", "r", encoding="utf-8", errors='replace') as info:
        bio_text = info.read()
    bio_label.configure(text=bio_text)

def next_image(event):
    global win, images, image_index, current_image, path, pic_label
    if image_index < len(images)-1:
        image_index += 1
        img = Image.open(path+"/"+ images[image_index])
        ratio = min(display[0]/img.size[0], display[1]/img.size[1])
        resized = img.resize((int(ratio*img.size[0]), int(ratio*img.size[1])))
        current_image = ImageTk.PhotoImage(resized)
        pic_label.configure(image=current_image)

def prev_image(event):
    global win, images, image_index, current_image, path, pic_label
    if image_index > 0:
        image_index -= 1
        img = Image.open(path+"/"+ images[image_index])
        ratio = min(display[0]/img.size[0], display[1]/img.size[1])
        resized = img.resize((int(ratio*img.size[0]), int(ratio*img.size[1])))
        current_image = ImageTk.PhotoImage(resized)
        pic_label.configure(image=current_image)

def next_profile(event):
    global profiles, path, root, profile_index
    path = root+"/"+profiles[profile_index]
    if profile_index < len(profiles):
        profile_index += 1
    show_profile()

def prev_profile(event):
    global profiles, path, root, profile_index
    path = root+"/"+profiles[profile_index-2]
    if profile_index > 0:
        profile_index -= 1
    show_profile()


win = Tk()
pic_label = Label(win)
pic_label.pack()
name_label = Label(win, font=("Times", 16, "bold"))
name_label.pack()
bio_label = Label(win)
bio_label.pack()
display = (1000, 600)

profiles = os.listdir(root)
random.shuffle(profiles)
current_image = 0
image_index = 0
profile_index = 0
images = []
path = root+"/"+profiles[0]
show_profile()
win.bind("<Left>", prev_image)
win.bind("<Right>", next_image)
win.bind("<Up>", next_profile)
win.bind("<Down>", prev_profile)
