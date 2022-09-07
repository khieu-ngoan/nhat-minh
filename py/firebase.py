import os
import cv2
from datetime import datetime
import firebase_admin
from firebase_admin import db
from .const import rootDir, dateLimit, imageDB
from .json import directory2Json

def syncToFirebaseRealtime():
    firebaseData = imageDB.get().items()
    for root, dirs, files in os.walk(rootDir):
        for file in files:
            if file.endswith(".jpg") or file.endswith(".JPG"):
                filePath = os.path.join(root, file) # create full path
                fileSrc = filePath.replace(rootDir, '')[13::]
                dir = os.path.dirname(filePath)
                dirBasename = os.path.basename(dir)
                if len(dirBasename) != 6:
                    return
                
                date = datetime.strptime(dirBasename, '%y%m%d')
                result=next( (z for i,z in firebaseData if z["src"] == fileSrc), None)
                if date < dateLimit or result != None:
                    return
                
                im = cv2.imread(filePath)
                h, w, c = im.shape
                imgFile = {
                    "src": fileSrc,
                    "width": 4,
                    "height": 3,
                    "date":date.strftime("%Y-%m-%d"),
                }
                if( w < h):
                    imgFile["width"] = 3
                    imgFile["height"] = 4

                result=next( (z for i,z in imageDB.get().items() if z["src"] == imgFile["src"]), None)

                if result == None:
                    print("add to firebase", imgFile)
                    imageDB.push().set(imgFile)
                    

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
    
    for i,firebaseFile in imageDB.get().items():
        if firebaseFile['src'] not in images:
            print(f"remove file [{firebaseFile['src']}]")
            db.reference('/images/{0}'.format(i)).delete()