import firebase_admin
from firebase_admin import credentials
from  firebase_admin import db

cred = credentials.Certificate('Key.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://arduinoiot-7a69d-default-rtdb.asia-southeast1.firebasedatabase.app/'
})

door = db.reference('/door').get()
temp = db.reference('/dht11/temp').get()
humi = db.reference('/dht11/humi').get()
dht11 = db.reference('/dht11').get()


def listerer(event):
    print(event.data)

firebase_admin.db.reference("/door").listen(listerer)