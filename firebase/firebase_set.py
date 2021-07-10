import firebase_admin
from firebase_admin import credentials
from  firebase_admin import db

cred = credentials.Certificate('Key.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://arduinoiot-7a69d-default-rtdb.asia-southeast1.firebasedatabase.app/'
})


'''db.reference('/dht11').set({
    'humi':10.1,
    'temp':20.2
})'''

db.reference('/dht11/humi').set(30.3)

print('OK')