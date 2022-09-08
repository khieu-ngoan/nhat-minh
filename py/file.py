
import os
from firebase_admin import db
from .const import rootDir
from .const import imageDB

def getImages(dirName):
    images = []
    pathCheck = rootDir
    dirName = str(dirName)
    
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
    return images

def underMigrate(dirName):
    pathCheck = rootDir
    dirName = str(dirName)
    
    if len(dirName) > 0 :
        pathCheck += f"/nhat-minh-{dirName}"
    dbFiles = imageDB.get()
    
    for root, dirs, files in os.walk(pathCheck):
        for file in files:
            if file.endswith(".jpg") or file.endswith(".JPG"):
                if file[0] != '_':
                    continue

                filePath = os.path.join(root, file) # create full path
                fileNew =  f"{root}/{file[1::]}"
                if os.path.exists(fileNew):
                    print(f"file [{file[1::]}] is existed")

                src = filePath.replace(rootDir, '')[13::]
                firebaseId = next( (i for i, z in dbFiles.items() if z["src"] == src), None)
                firebaseFile = dbFiles.get(firebaseId)
                firebaseFile['src'] = fileNew.replace(rootDir, '')[13::]
                os.rename(filePath, fileNew)
                db.reference('/images/{0}'.format(firebaseId)).update(firebaseFile)

                print( f"rename file [{file}]" )