import datetime
import os

import firebase_admin
from firebase_admin import credentials, firestore


cred = credentials.Certificate(os.path.dirname(__file__)+"/../hackday-2022-126c3-firebase-adminsdk-fdhbf-3e76c0b50a.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

DEVICE_ID = os.environ["DEVICE_ID"]
db.collection(u'devices').document(DEVICE_ID).set({}, merge=True)


def send_gps_log(dt: datetime.datetime, lat: float, lng: float, id: str):
    doc_ref = db.collection(u'devices').document(DEVICE_ID)
    gps_log = {
        u'time': dt,
        u'latitude': lat,
        u'longitude': lng,
        u'id': id,
    }
    doc_ref.update({u'gpsLogs': firestore.ArrayUnion([gps_log])})


def send_gps_id(id: str):
    doc_ref = db.collection(u'devices').document(DEVICE_ID)
    doc_ref.update({u'gpsIdOnAlerted': firestore.ArrayUnion([id])})
