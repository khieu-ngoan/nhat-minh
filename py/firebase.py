import os
from urllib import response
import uuid
import cv2
from datetime import datetime
from firebase_admin import db
from .const import rootDir, dateLimit, imageRef
from .const import API_CREATE, API_FIND_FILE
from .json import directory2Json
import requests

## --------------------------------------------------------
## document 
## https://firebase.google.com/docs/admin/setup#python
## --------------------------------------------------------

def syncToFirebaseRealtime():
    # firebaseData = imageDB.get().items()
    # dbFiles = imageDB.get()

    for root, dirs, files in os.walk(rootDir):
        for file in files:
            if file.endswith(".jpg") or file.endswith(".JPG"):
                filePath = os.path.join(root, file) # create full path
                fileSrc = filePath.replace(rootDir, '')[13::]
                dir = os.path.dirname(filePath)
                dirBasename = os.path.basename(dir)
                
                if dirBasename =='thumbnail' or len(dirBasename) != 6:
                    # print(f"skip add by dir-name [{dirBasename}/{file}]")
                    continue
                
                date = datetime.strptime(dirBasename, '%y%m%d')
                # result=next( (z for i,z in dbFiles if z["src"] == fileSrc), None)
                # Create a query against the collection
                result = imageRef.where(u'src', u'==', fileSrc)
                
                # print( , len(result.get()))
                
                # exit()
                if date < dateLimit or len(result.get()) > 0 :
                    # print(f"skip add by {date} [{dirBasename}/{file}]", result)
                    continue
                
                im = cv2.imread(filePath)
                h, w, c = im.shape
                imgFile = {
                    "src": fileSrc,
                    "width": 4,
                    "height": 3,
                    "date":date.strftime("%Y-%m-%d"),
                    "cdn": "nhat-minh-"+date.strftime("%y")
                }
                if( w < h):
                    imgFile["width"] = 3
                    imgFile["height"] = 4

                # result=next( (z for i,z in imageDB.get().items() if z["src"] == imgFile["src"]), None)

                # if result == None:
                #     print("add to firebase", imgFile)
                print(f"add new to firebase [{dirBasename}/{file}]")
                # imageDB.push().set(imgFile)
                
                imageRef.document().set(imgFile)
                print(imgFile)
                # exit()

def syncToMySql():
    dirWalk = f"{rootDir}nhat-minh-22"
    print(f"check dir [{dirWalk}]")
    for root, dirs, files in os.walk(dirWalk):
        for file in files:
            if file.endswith(".jpg") or file.endswith(".JPG"):
                filePath = os.path.join(root, file) # create full path
                fileSrc = filePath.replace(rootDir, '')[12::]
                dir = os.path.dirname(filePath)
                dirBasename = os.path.basename(dir)
                
                if dirBasename =='thumbnail' or len(dirBasename) != 6:
                    # print(f"skip add by dir-name [{dirBasename}/{file}]")
                    print(f"[{dirBasename}/{file}] format is incorrect")
                    continue
                
                date = datetime.strptime(dirBasename, '%y%m%d')
                if date < dateLimit:
                    print(f"[{dirBasename}/{file}] is out of date")
                    # print(response.content)
                    continue
                
                response = requests.post(API_FIND_FILE, data={"src":fileSrc})

                if response.status_code==200 :
                    print(f"[{fileSrc}] [response-status={response.status_code}] is out of date")
                    # print(response.content)
                    continue
                
                im = cv2.imread(filePath)
                h, w, c = im.shape
                imgFile = {
                    "src": fileSrc,
                    "code": uuid.uuid4().urn[9::],
                    "width": 4,
                    "height": 3,
                    "date":date.strftime("%Y-%m-%d"),
                    "cdn": "nhat-minh-"+date.strftime("%y")
                }
                if( w < h):
                    imgFile["width"] = 3
                    imgFile["height"] = 4

                print(f"add new to DB [{dirBasename}/{file}] ====> [src={fileSrc}]")
                response = requests.post(API_CREATE, data=imgFile)
                if response.status_code!=201 :
                    print("got error ", response.status_code, imgFile, response.text)
                    exit()

def cleanFirebase(dirName=''):
    images = []
    pathCheck = rootDir
    if len(dirName) > 0 :
        pathCheck += f"/nhat-minh-{dirName}"
    
    for root, dirs, files in os.walk(pathCheck):
        for file in files:
            if file.endswith(".jpg") or file.endswith(".JPG"):
                filePath = os.path.join(root, file) # create full path
                dir = os.path.dirname(filePath)
                dirBasename = os.path.basename(dir)
                if len(dirBasename) == 6:
                    src = filePath.replace(pathCheck, '')[13::]
                    images.append(src)
    
    directory2Json(images, rootDir)
    
    for i,firebaseFile in imageDBRealtime.get().items():
        if firebaseFile['src'] not in images:
            print(f"remove file [{firebaseFile['src']}]")
            db.reference('/images/{0}'.format(i)).delete()

def cdnMigrate():
    for i,firebaseFile in imageDBRealtime.get().items():
        
        # if 'cdn' in firebaseFile.keys():
        #     continue
       
        if firebaseFile['date'].find('/') > -1 :
            date = datetime.strptime(firebaseFile['date'], '%Y/%m/%d')
            
        elif firebaseFile['date'].find('-') > -1 :
            date = datetime.strptime(firebaseFile['date'], '%Y-%m-%d')
            
        firebaseFile['date'] = date.strftime("%Y-%m-%d")
        
        if date.strftime("%Y") == "2022" :
            firebaseFile['cdn'] = 'nhat-minh-22'
        elif date.strftime("%Y") == "2021" :
            firebaseFile['cdn'] = 'nhat-minh-21'
        elif date.strftime("%Y") == "2020" :
            firebaseFile['cdn'] = 'nhat-minh-20'
        elif date.strftime("%Y") == "2019" :
            firebaseFile['cdn'] = 'nhat-minh-19'
        
        print(i, firebaseFile['src'])
        # exit()

        db.reference('/images/{0}'.format(i)).update(firebaseFile)
        # print(i, firebaseFile, date)
        # exit()