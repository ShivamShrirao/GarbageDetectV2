from google.cloud import storage
import os
import datetime
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import googlemaps
import numpy as np
try:
    cred = credentials.Certificate('../../smart-waste-locator-firebase-adminsdk-ljjzx-495a7e327a.json')
    # Initialize the app with a service account, granting admin privileges
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://smart-waste-locator.firebaseio.com/'
    })
except:
    print("Already Initialized")


def get_index():
    ref = db.reference('Detected/')
    indexes = dict()
    for i in ref.get().values():
        x = i['TimeStamp'].split('/')
        if i['Pincode'] not in indexes.keys():
            indexes[i['Pincode']] = 0
        now = datetime.datetime.now()
        date = datetime.date(int(x[2]),int(x[1]),int(x[0]))
        difference = now.date() - date
        d_factor = 1
        for _ in range(difference.days):
            d_factor = 1 + 0.5*d_factor

        indexes[i['Pincode']] += i['contourArea']*d_factor
        
    return indexes

def add_indexes():
    ref_to_add = db.reference('/Indexes')
    ref_to_add.set(
    get_index())
    return True


if __name__ == "__main__":
    print(add_indexes())
    
