import os, requests, PIL
from PIL import Image
from .const import rootDir, thumbWidth, API_FIND_FILE

def convertIphone():
    # for file in *.HEIC; do convert $file ${file/%.HEIC/.jpg}; done
    return True

def createThumbs(dirName, replate=False):
    # filebaseData = imageDBRealtime.get().items()
    pathCheck = rootDir
    dirName = str(dirName)
    
    if len(dirName) > 0 :
        pathCheck += f"/nhat-minh-{dirName}"
    
    for root, dirs, files in os.walk(pathCheck):
        for file in files:
            filePath = os.path.join(root, file) # create full path
            dir = os.path.dirname(filePath)
            dirBasename = os.path.basename(dir)
            
            if file.endswith(".jpg") != True or len(dirBasename) != 6:
                continue
           
            src = filePath.replace(pathCheck, '')
            
            response = requests.post(API_FIND_FILE, data={"src":src})
            if response.status_code != 200 :
                continue

            uuid = response.json()['data'][0]['code']

            thumbnail = f"{dir}/../thumbnail/{uuid}.jpg"
            if os.path.exists(thumbnail) and not replate:
                continue

            img = Image.open(filePath).convert("RGB")
            wpercent = (thumbWidth / float(img.size[0]))
            heigthSize = int((float(img.size[1]) * float(wpercent)))
            img_thumb = img.resize((thumbWidth, heigthSize), PIL.Image.ANTIALIAS)
            cropped = img_thumb.crop( (0,0,thumbWidth,heigthSize) )
            cropped.save(thumbnail,"jpeg")

            print( f"resize file [{src}] ===>> thumbnail [{uuid}]")
            
    