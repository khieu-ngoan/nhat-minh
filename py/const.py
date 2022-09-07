import os
import firebase_admin
from firebase_admin import credentials, db
from datetime import datetime

# TODO: Replace the following with your app's Firebase project configuration
# See: https://firebase.google.com/docs/web/learn-more#config-object
cert = credentials.Certificate("./nhatminh-images-adb45fdea658.json")
options = { 'databaseURL': "https://nhatminh-images-default-rtdb.firebaseio.com/", }
firebase_admin.initialize_app( cert, options)
imageDB = db.reference("/images")
dateLimit = datetime(2019, 1, 1)
rootDir = os.path.dirname(os.path.abspath(__file__))+"/../NhatMinh"