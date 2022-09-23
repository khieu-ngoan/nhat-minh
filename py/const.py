import os
import firebase_admin
from firebase_admin import credentials, db, firestore
from datetime import datetime

# TODO: Replace the following with your app's Firebase project configuration
# See: https://firebase.google.com/docs/web/learn-more#config-object
cert = credentials.Certificate("./nhatminh-images-adb45fdea658.json")
options = { 'databaseURL': "https://nhatminh-images-default-rtdb.firebaseio.com/", }
firebase_admin.initialize_app( cert, options)
imageDBRealtime = db.reference("/images")
# Create a query against the collection
imageRef = firestore.client().collection("images")
imageDBFirestore = imageRef.document()
imageDBStream = imageRef.stream()
dateLimit = datetime(2019, 1, 1)

rootDir = os.path.dirname(os.path.abspath(__file__))+"/../NhatMinh"
publicDir = os.path.dirname(os.path.abspath(__file__))+"/../src/"

thumbWidth = 100

API_HOST        = "http://tiengnhatdehieu.loc/photos/api/photo"
API_CREATE      = API_HOST+"/create"
API_FIND_FILE   = API_HOST+"/find"
API_IMAGES      = API_HOST+"/list"