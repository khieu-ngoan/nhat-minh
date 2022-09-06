import os, argparse, json, uuid
import os.path
from pickle import FALSE
from os.path import exists
from datetime import datetime
import cv2
import PIL
from PIL import Image
# import wand.image
# from wand.image import Image
# import webp as WEBP_CONVERT
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

# TODO: Replace the following with your app's Firebase project configuration
# See: https://firebase.google.com/docs/web/learn-more#config-object
firebaseConfig = {
  'databaseURL': "https://nhatminh-images-default-rtdb.firebaseio.com/",
}
cred = credentials.Certificate("./nhatminh-images-adb45fdea658.json")
firebase_admin.initialize_app(cred, firebaseConfig)
# firebase_admin.initialize_app(cred)
imageDB = db.reference("/images")

# test=RealtimeDB.get()
# print(test)
# exit()

rootDir = os.path.dirname(os.path.abspath(__file__))+"/NhatMinh"
publicDir = os.path.dirname(os.path.abspath(__file__))+"/src/"
dateLimit = datetime(2019, 1, 1)

def thumbnail(file, firebaseId, replate=False):
    thumbnail = f"{rootDir}/thumbnail/{firebaseId}.jpg"
    if os.path.exists(thumbnail) and not replate:
        return thumbnail

    img_resize = 300
    img = Image.open(file).convert("RGB")
    basewidth = img_resize
    wpercent = (img_resize / float(img.size[0]))
    hsize = int((float(img.size[1]) * float(wpercent)))
    img_thumb = img.resize((basewidth, hsize), PIL.Image.ANTIALIAS)
    
    cropped = img_thumb.crop( (0,0,img_resize,img_resize) )
    # id = uuid.uuid4()
    thumbnail = f"{rootDir}/thumbnail/{firebaseId}.jpg"
    cropped.save(thumbnail,"jpeg")
    return thumbnail

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
                    src = filePath.replace(pathCheck, '')
                    images.append(src)
    # result=next( (z for i,z in imageDB.get().items() if z["src"] == src), None)
    # print( len(images) )
    
    for i,firebaseFile in imageDB.get().items():
        print(i, firebaseFile)
        if firebaseFile['src'] not in images:
            print(firebaseFile)
            exit()

def syncToFirebaseRealtime():
    for root, dirs, files in os.walk(rootDir):
        for file in files:
            if file.endswith(".jpg") or file.endswith(".JPG"):
                filePath = os.path.join(root, file) # create full path
                dir = os.path.dirname(filePath)
                dirBasename = os.path.basename(dir)
                if len(dirBasename) == 6:
                    date = datetime.strptime(dirBasename, '%y%m%d')
                    
                    if date >= dateLimit:
                        im = cv2.imread(filePath)
                        h, w, c = im.shape
                        imgFile = {
                            "src": filePath.replace(rootDir, '')[14::],
                            "width": 4,
                            "height": 3,
                            "date":date.strftime("%Y-%m-%d"),
                        }
                        if( w < h):
                            imgFile["width"] = 3
                            imgFile["height"] = 4

                        result=next( (z for i,z in imageDB.get().items() if z["src"] == imgFile["src"]), None)

                        # print(imgFile, result)
                        # exit()
                        if result == None: # insert to firebase
                            imageDB.push().set(imgFile)
   
def getSrc(imageObject):
    return imageObject.get('src')

def createJson(replate=False):
    imagesData=[]

    for id, image in imageDB.order_by_child("date").get().items():
        image["thumbnail"] = thumbnail(rootDir+image["src"], id, replate).replace(rootDir+"/", '')
        # image["date"] = datetime.strptime(image["date"], '%Y/%m/%d')
        imagesData.append(image)

    imagesData = sorted( imagesData, key=lambda x: x["src"], reverse = True)
    imagesData = sorted( imagesData, key=lambda x: x["date"], reverse = True )
    
    # for image in imagesData:
    #     print(image["date"])
    
    jsonFile = os.path.join(publicDir,"data.json")
    if os.path.exists(jsonFile):
        os.remove(jsonFile)
    jsonFile = open(jsonFile, "a")
    jsonFile.write(json.dumps(imagesData))

def convertIphone():
    # for file in *.HEIC; do convert $file ${file/%.HEIC/.jpg}; done
    return True

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--action', help='foo help')
    args = parser.parse_args()

    if args.action=='thumb' or args.action == 'thumbnail':
        return
    elif args.action=='fire' or args.action == 'firebase':
        syncToFirebaseRealtime()
    elif args.action == 'firebase-clean':
        cleanFirebase()
    elif args.action=='json':
        createJson(replate=False)
    else :
        syncToFirebaseRealtime()
        print(args)
        
    # syncToFirebaseRealtime()
    # createJson(replate=False)
    
    
    

if __name__ == "__main__":
    main()