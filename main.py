import os, argparse
import os.path
from os.path import exists
import PIL
from PIL import Image
from py.json import directory2Json, createJson
from py.firebase import syncToFirebaseRealtime, cleanFirebase

# TODO: Replace the following with your app's Firebase project configuration
# See: https://firebase.google.com/docs/web/learn-more#config-object
# firebaseConfig = {
#   'databaseURL': "https://nhatminh-images-default-rtdb.firebaseio.com/",
# }
# cred = credentials.Certificate("./nhatminh-images-adb45fdea658.json")
# firebase_admin.initialize_app(cred, firebaseConfig)
# firebase_admin.initialize_app(cred)
# imageDB = db.reference("/images")

# test=RealtimeDB.get()
# print(test)
# exit()

rootDir = os.path.dirname(os.path.abspath(__file__))+"/NhatMinh"
publicDir = os.path.dirname(os.path.abspath(__file__))+"/src/"
# dateLimit = datetime(2019, 1, 1)

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


def getSrc(imageObject):
    return imageObject.get('src')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--action', help='foo help')
    args = parser.parse_args()

    if args.action=='thumb' or args.action == 'thumbnail':
        return
    elif args.action == 'firebase':
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