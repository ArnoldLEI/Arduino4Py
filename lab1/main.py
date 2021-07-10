
import cv2
from lab1 import Config
import lab1.Face_capture_positives as cap
import lab1.Face_training as train
import lab1.Face_recognition as recogn
import os
import shutil


def menu():
    while True:
        print('----------------')
        print('1.拍照 + 訓練')
        print('2.辨識')
        print('9.離開')
        print('----------------')
        n = int(input('請選擇:'))

        if n == 1:
            shutil.rmtree(Config.TRAINING_FOLDER)
            my_name = input('ENG NAME: ')
            Config.MY_NAME = my_name
            cap.capture()
            cv2.waitKey(1)
            train.train()
        elif n == 2:
            my_name = input('ENG NAME: ')
            Config.MY_NAME = my_name
            score = recogn.recognizer()
            print("score:", score)
            cv2.waitKey(1)
        elif n == 9:
            print("Exit")
            break

if '__main__' == __name__:
    menu()


