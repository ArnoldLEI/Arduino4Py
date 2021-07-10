import firebase_admin
from firebase_admin import credentials
from  firebase_admin import db
import tkinter
import serial
import threading
import CASE01.OpenWerther as ow
import time
import sqlite3
from tkinter import font
from PIL import Image, ImageTk
from io import BytesIO
import random

cred = credentials.Certificate('Key.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://arduinoiot-7a69d-default-rtdb.asia-southeast1.firebasedatabase.app/'
})
def listererdoor(event):
    print(event.data)
    doorValue.set(event.data)
    if (event.data == 0):
        doorLabel.config(image=door_close_photo)
        doorLabel.image = door_close_photo
    elif (event.data == 1):
        doorLabel.config(image=door_open_photo)
        doorLabel.image = door_open_photo

def listererDHT11temp(event):
    print(event.data)
    tempValue.set(event.data)

def listererDHT11humi(event):
    print(event.data)
    humiValue.set(event.data)

def listensrFirebase():
    firebase_admin.db.reference("/door").listen(listererdoor)
    firebase_admin.db.reference("/dht11/temp").listen(listererDHT11temp)
    firebase_admin.db.reference("/dht11/humi").listen(listererDHT11humi)

def updatetemp():
    value = random.uniform(20,30)
    value = "%.2f" % value
    value = float(value)
    db.reference('/dht11/temp').set(value)

def updatehumi():
    value = random.uniform(50, 70)
    value = "%.2f" % value
    value = float(value)
    db.reference('/dht11/humi').set(value)

def updatedoor():
    if db.reference('/door').get() == 1:
        db.reference('/door').set(0)
    else:
        db.reference('/door').set(1)

root = tkinter.Tk()
root.geometry("800x600")
root.title = "firebase GUI"

myfont1 = font.Font(family='Helvetica', size=36, weight='bold')
myfont2 = font.Font(family='Helvetica', size=24)

door_open_photo  = ImageTk.PhotoImage(Image.open('OPENDOOR.png'))
door_close_photo = ImageTk.PhotoImage(Image.open('CLOSEDOOR.png'))


tempValue = tkinter.StringVar()
tempValue.set("00.00 C")

humiValue = tkinter.StringVar()
humiValue.set("00.00%")

doorValue = tkinter.StringVar()
doorValue.set('0')

updatetempButton = tkinter.Button(text='temp', command=lambda: updatetemp(), font=myfont2)
updatehumiButton = tkinter.Button(text='humi', command=lambda: updatehumi(), font=myfont2)
updatedoorButton = tkinter.Button(text='door', command=lambda: updatedoor(), font=myfont2)

tempLabel = tkinter.Label(root, textvariable=tempValue, font=myfont1, fg='#005100')
humiLabel = tkinter.Label(root, textvariable=humiValue, font=myfont1, fg='#00f')
doorLabel = tkinter.Label(root, image=door_close_photo, font=myfont1, fg='#00f')

root.rowconfigure((0,1), weight=1)  # 列 0, 列 1 同步放大縮小
root.columnconfigure((0, 1, 2), weight=1)  # 欄 0, 欄 1, 欄 2 ...同步放大縮小

tempLabel.grid(row=0, column=0, columnspan=1, sticky='EWNS')
humiLabel.grid(row=0, column=1, columnspan=1, sticky='EWNS')
doorLabel.grid(row=0, column=2, columnspan=1, sticky='EWNS')

updatetempButton.grid(row=1,   column=0, columnspan=1, sticky='EWNS')
updatehumiButton.grid(row=1,   column=1, columnspan=1, sticky='EWNS')
updatedoorButton.grid(row=1,   column=2, columnspan=1, sticky='EWNS')

t1 = threading.Thread(target = listensrFirebase)
t1.start()

root.mainloop()
