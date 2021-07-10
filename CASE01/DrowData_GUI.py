# -*- coding: UTF-8 -*-
import tkinter
import serial
import threading
import CASE01.OpenWerther as ow
import time
import pandas as pd
import sqlite3
from tkinter import font
from PIL import Image, ImageTk
from io import BytesIO
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import *


def SHOW():
    conn = sqlite3.connect('iot.db')
    df = pd.read_sql_query("SELECT id, cds, temp, humi, ts FROM Env "
                           "order by ts desc limit 15", con=conn)
    df = df[::-1] # reverse
    print(df)

    root = tkinter.Tk()
    root.title("溫度走勢")
    f = Figure(figsize=(5,4), dpi=100)
    f_polt = f.add_subplot(111)
    canvs = FigureCanvasTkAgg(f, root)

    # 繪圖
    f_polt.plot(df['ts'], df['temp'], label="temp")  # 繪製折線圖
    f_polt.plot(df['ts'], df['humi'], label="humi")  # 繪製折線圖
    f_polt.grid(True)
    # 圖例
    plt.xlabel('time')
    plt.ylabel('value')
    #plt.xticks(rotation=90)
    f_polt.legend()
    #plt.show()
    canvs.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
    root.mainloop()

if __name__ == '__main__':
    SHOW()