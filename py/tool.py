import os
# import wand.image
# from wand.image import Image
# import webp as WEBP_CONVERT
import PIL
from PIL import Image
from .const import rootDir, imageDB, thumbWidth
from .file import getImages

def convertIphone():
    # for file in *.HEIC; do convert $file ${file/%.HEIC/.jpg}; done
    return True

def createThumbs(dirName, replate=False):
    filebaseData = imageDB.get().items()
    pathCheck = rootDir
    dirName = str(dirName)
    
    if len(dirName) > 0 :
        pathCheck += f"/nhat-minh-{dirName}"
    
    for root, dirs, files in os.walk(pathCheck):
        for file in files:
            filePath = os.path.join(root, file) # create full path
            dir = os.path.dirname(filePath)
            dirBasename = os.path.basename(dir)
            # print(file, file.endswith(".jpg"))
            if file.endswith(".jpg") != True or len(dirBasename) != 6:
                continue

           
            src = filePath.replace(pathCheck, '')
            firebaseId = next( (i for i,z in imageDB.get().items() if z["src"] == src), None)

            thumbnail = f"{dir}/../thumbnail/{firebaseId}.jpg"
            if os.path.exists(thumbnail) and not replate:
                continue

            
            img = Image.open(filePath).convert("RGB")
            
            wpercent = (thumbWidth / float(img.size[0]))
            heigthSize = int((float(img.size[1]) * float(wpercent)))
            img_thumb = img.resize((thumbWidth, heigthSize), PIL.Image.ANTIALIAS)
            cropped = img_thumb.crop( (0,0,thumbWidth,heigthSize) )
            cropped.save(thumbnail,"jpeg")

            print( f"resize file [{src}] ===>> thumbnail [{firebaseId}]")
            
            
               
    