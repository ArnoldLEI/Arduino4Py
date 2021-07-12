import tkinter
import serial
import threading
import CASE01.OpenWerther as ow
import time
import sqlite3
from tkinter import font
from PIL import Image, ImageTk
from io import BytesIO
import lab1.Face_recognition as recogn
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import lab1.Face_capture_positives as cap
import lab1.Face_training as train

cred = credentials.Certificate('../firebase/Key.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://arduinoiot-7a69d-default-rtdb.asia-southeast1.firebasedatabase.app/'
})

COM_PORT = 'COM3'  # 指定通訊埠名稱
BAUD_RATES = 9600  # 設定傳輸速率(鮑率)
play = True
data = ""
conn = sqlite3.connect('iot.db', check_same_thread=False)

buzeer_on = 16
buzeer_off = 32
door_open = 80
door_close = 180


def createTable():
    sql = 'create table if not exists Env(' \
          'id integer not null primary key autoincrement,' \
          'cds real,' \
          'temp real,' \
          'humi real,' \
          'ts timestamp default current_timestamp ' \
          ')'
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()


def InsertData():
    sql = '''
            INSERT INTO Env(cds, temp, humi) 
            VALUES (%d,%.1f,%.1f)
          ''' % (int(cdsValue.get().split(" ")[0]),
                 float(tempValue.get().split(" ")[0]),
                 float(humiValue.get().split(" ")[0]))
    cursor = conn.cursor()
    cursor.execute(sql)
    print("INERTINTOSUCCES: ", cursor.lastrowid)
    conn.commit()


def ExecInsertData():
    while play:
        time.sleep(10)
        InsertData()


def receiveData():
    postflag = 1
    while play:
        try:
            global ser
            data_row = ser.readline()  # 讀取一行(含換行符號\r\n)原始資料
            global data
            data = data_row.decode()  # 預設是用 UTF-8 解碼
            data = data.strip("\n")
            data = data.strip("\r")  # 除去換行符號
            print(data)
            if postflag == 1:
                firstPostToFireBase(data)
                postflag = 0

            threading.Thread(target=lambda: postToFirebase(data)).start()

            respText.set(data)
            try:

                values = data.split(",")
                cdsValue.set("%d lu" % (float(values[0])))
                tempValue.set("%.1f C" % (float(values[1])))
                humiValue.set("%.1f %%" % (float(values[2])))

                if (int(values[3]) == 16):
                    sendButton0.config(image=buzeer_open_photo)
                    sendButton0.image = buzeer_open_photo
                elif (int(values[3]) == 32):
                    sendButton0.config(image=buzeer_close_photo)
                    sendButton0.image = buzeer_close_photo
                if (int(values[4]) == 180):
                    sendButton4.config(image=door_close_photo)
                    sendButton4.image = door_close_photo
                elif (int(values[4]) == 80):
                    sendButton4.config(image=door_open_photo)
                    sendButton4.image = door_open_photo
            except:
                pass

        except Exception as e:
            print("Serial closed....", e)
            respText.set("Serial closed")

            # 重新連線
            try:
                ser = serial.Serial(COM_PORT, BAUD_RATES)
            except Exception as e:
                print("Serial closed....", e)
            # break
    conn.close()

def firstPostToFireBase(data):
    logArray = data.split(",")
    db.reference('/led').set(int(logArray[3]))
    db.reference('/buzeer').set(0)
    if int(logArray[4]) == door_close:
        db.reference('/door').set(0)
    elif int(logArray[4]) == door_open:
        db.reference('/door').set(1)

def postToFirebase(data):
    # ------------------------------------------------
    # firebase set log
    db.reference('/log/data').set(data)
    db.reference('/log/time/str').set(time.ctime())
    db.reference('/log/time/long').set(time.time())
    # ------------------------------------------------
    # firebase set 結構資料配置
    # 752,24.80,42.00,0,20
    logArray = data.split(",")
    db.reference('/cds').set(int(logArray[0]))
    db.reference('/dht11/temp').set(float(logArray[1]))
    db.reference('/dht11/humi').set(float(logArray[2]))
    #db.reference('/led').set(int(logArray[3]))


    if int(logArray[3]) == buzeer_off:
        db.reference('/buzeer').set(0)

    '''if int(logArray[4]) == door_close:
        db.reference('/door').set(0)
    elif int(logArray[4]) == door_open:
        db.reference('/door').set(1)'''


def sendData(n):
    data_row = n + "#"  # "#" 代表結束符號
    sentdata = data_row.encode()
    ser.write(sentdata)
    print("send: ", data_row, sentdata)
    if n == 1 or n == 2 or n == 3:
        db.reference("/led").set(n)
    elif n == 8:
        db.reference("/door").set(1)
    elif n == 4:
        db.reference("/door").set(0)
    elif n == buzeer_off:
        db.reference('/buzeer').set(0)
    elif n == buzeer_on:
        db.reference('/buzeer').set(1)


def openthedoor():
    door = int(data.split(",")[4])
    if door == 80:
        sendData('8')
    elif door == 180:
        sendData('4')

def cv():
    score = recogn.recognizer()
    print("score: ", score)
    if score < 2000:
        sendData('4')


def faceListsner(event):
    if (event.data == 1):
        db.reference("/face").set(0)
        cv()
def execFaceListsner():
    # 監聽 firebase face 資料
    db.reference("/face").listen(faceListsner)

def buzeerListsner(event):
    if event.data == 1:
        sendData('16')

def execbuzeerListsner():
    # 監聽 firebase face 資料
    db.reference("/buzeer").listen(buzeerListsner)

def doorListsner(event):
    if event.data == 1:
        sendData('4')
    elif event.data == 0:
        sendData('8')
def execDoorListsner():
    # 監聽 firebase face 資料
    db.reference("/door").listen(doorListsner)

def ledListsner(event):
    if event.data == 1:
        #db.reference("/led").set(1)
        print(event.data)
        sendData('1')
    elif event.data == 2:
        #db.reference("/led").set(2)
        print(event.data)
        sendData('2')
    elif event.data == 3:
        #db.reference("/led").set(3)
        print(event.data)
        sendData('3')
    time.sleep(3)


def execLedListsner():
    # 監聽 firebase led 資料
    db.reference("/led").listen(ledListsner)


def getOpenWeatherData():
    status_code, main, icon, temp, feels_like, humidity = ow.openweather()
    if (status_code == 200):
        owmainValue.set(main)

        raw_data = ow.openweatherIcon(icon)
        im = Image.open(BytesIO(raw_data))
        photo = ImageTk.PhotoImage(im)
        owiconLabel.config(image=photo)
        owiconLabel.image = photo

        owtempValue.set("%.1f C" % float(temp - 273.15))
        owfeelsLikeValue.set("%.1f C" % float(feels_like - 273.15))
        owhumidityValue.set("%.1f %%" % float(humidity))

        # "#" 代表結束符號
        sendData("A%.2f,%.2f" % ((float(temp) - 273.15), float(humidity)))

    else:
        owmainValue.set('錯誤碼：' + str(status_code))


if __name__ == '__main__':

    # createTable()
    try:
        ser = serial.Serial(COM_PORT, BAUD_RATES)
    except Exception as e:
        print("Serial exception: ", e)



    root = tkinter.Tk()
    root.geometry("800x600")
    root.title = "Arduino GUI"

    myfont1 = font.Font(family='Helvetica', size=36, weight='bold')
    myfont2 = font.Font(family='Helvetica', size=24)

    clear_photo = ImageTk.PhotoImage(Image.open('CLEAN.png'))
    red_photo = ImageTk.PhotoImage(Image.open('RED_LED.png'))
    green_photo = ImageTk.PhotoImage(Image.open('GREEN_LED.png'))
    yellow_photo = ImageTk.PhotoImage(Image.open('YELLO.png'))
    door_open_photo = ImageTk.PhotoImage(Image.open('OPENDOOR.png'))
    door_close_photo = ImageTk.PhotoImage(Image.open('CLOSEDOOR.png'))
    buzeer_open_photo = ImageTk.PhotoImage(Image.open('BUZEROPEN.png'))
    buzeer_close_photo = ImageTk.PhotoImage(Image.open('BUZERCLOSE.png'))
    face_photo = ImageTk.PhotoImage(Image.open('FACE.png'))

    respText = tkinter.StringVar()
    respText.set("0,0.0,0.0")

    cdsValue = tkinter.StringVar()
    cdsValue.set("0 lu")

    tempValue = tkinter.StringVar()
    tempValue.set("00.00 C")

    humiValue = tkinter.StringVar()
    humiValue.set("00.00%")

    owmainValue = tkinter.StringVar()
    owmainValue.set("")
    owtempValue = tkinter.StringVar()
    owtempValue.set("")
    owfeelsLikeValue = tkinter.StringVar()
    owfeelsLikeValue.set("")
    owhumidityValue = tkinter.StringVar()
    owhumidityValue.set("")

    sendButton0 = tkinter.Button(text='16', image=buzeer_close_photo, command=lambda: sendData('16'), font=myfont2)
    sendButton1 = tkinter.Button(text='1', image=red_photo, command=lambda: sendData('1'), font=myfont2)
    sendButton2 = tkinter.Button(text='2', image=green_photo, command=lambda: sendData('2'), font=myfont2)
    sendButton3 = tkinter.Button(text='3', image=yellow_photo, command=lambda: sendData('3'), font=myfont2)
    sendButton4 = tkinter.Button(text='4', image=door_close_photo, command=lambda: openthedoor(), font=myfont2)
    sendButton5 = tkinter.Button(text='F', image=face_photo, command=lambda: cv(), font=myfont2)

    # 爬蟲視窗------------------------------------------------------------
    owmainButton = tkinter.Button(textvariable=owmainValue, command=lambda: getOpenWeatherData(), font=myfont2)
    owiconLabel = tkinter.Label(root, image=None)
    owtempLabel = tkinter.Label(root, textvariable=owtempValue, font=myfont2, fg='#005100')
    owfeelsLikeLabel = tkinter.Label(root, textvariable=owfeelsLikeValue, font=myfont2, fg='#005100')
    owhumidityLabel = tkinter.Label(root, textvariable=owhumidityValue, font=myfont2, fg='#ff0000')
    # 爬蟲視窗------------------------------------------------------------

    receiveLabel = tkinter.Label(root, textvariable=respText)
    cdsLabel = tkinter.Label(root, textvariable=cdsValue, font=myfont1, fg='#ff0000')
    tempLabel = tkinter.Label(root, textvariable=tempValue, font=myfont1, fg='#005100')
    humiLabel = tkinter.Label(root, textvariable=humiValue, font=myfont1, fg='#00f')

    root.rowconfigure((0, 1, 2), weight=1)  # 列 0, 列 1 同步放大縮小
    root.columnconfigure((0, 1, 2, 3, 4, 5, 6), weight=1)  # 欄 0, 欄 1, 欄 2 ...同步放大縮小

    sendButton0.grid(row=0, column=0, columnspan=1, sticky='EWNS')
    sendButton1.grid(row=0, column=1, columnspan=1, sticky='EWNS')
    sendButton2.grid(row=0, column=2, columnspan=1, sticky='EWNS')
    sendButton3.grid(row=0, column=3, columnspan=1, sticky='EWNS')
    sendButton4.grid(row=0, column=4, columnspan=1, sticky='EWNS')
    sendButton5.grid(row=0, column=5, columnspan=1, sticky='EWNS')

    # 爬蟲視窗------------------------------------------------------------
    owmainButton.grid(row=1, column=0, columnspan=2, sticky='EWNS')
    owiconLabel.grid(row=1, column=2, columnspan=1, sticky='EWNS')
    owtempLabel.grid(row=1, column=3, columnspan=1, sticky='EWNS')
    owfeelsLikeLabel.grid(row=1, column=4, columnspan=1, sticky='EWNS')
    owhumidityLabel.grid(row=1, column=5, columnspan=1, sticky='EWNS')

    # 爬蟲視窗------------------------------------------------------------

    cdsLabel.grid(row=2, column=0, columnspan=2, sticky='EWNS')
    tempLabel.grid(row=2, column=2, columnspan=2, sticky='EWNS')
    humiLabel.grid(row=2, column=4, columnspan=2, sticky='EWNS')
    receiveLabel.grid(row=3, column=0, columnspan=6, sticky='EWNS')

    t1 = threading.Thread(target=receiveData)
    t1.start()


    t2 = threading.Thread(target=getOpenWeatherData)
    t2.start()

    t3 = threading.Thread(target=ExecInsertData)
    t3.start()

    t4 = threading.Thread(target=execFaceListsner)
    t4.start()

    t5 = threading.Thread(target=execLedListsner)
    t5.start()

    t6 = threading.Thread(target=execDoorListsner)
    t6.start()

    t6 = threading.Thread(target=execbuzeerListsner)
    t6.start()


    root.mainloop()
