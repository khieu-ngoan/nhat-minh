import os, argparse, json, uuid
from datetime import datetime
import cv2
import PIL
from PIL import Image

#rootUrl = "https://quanict.github.io/NguyenKhieuNhatMinh/"
rootUrl = "/Minh/"
rootDir = os.path.dirname("/mnt/data/resource-git/NguyenKhieuNhatMinh/")
publicDir = os.path.dirname(os.path.abspath(__file__))+"/src/app"

def thumbnail(file):
    img_resize = 300
    img = Image.open(file).convert("RGB")
    basewidth = img_resize
    wpercent = (img_resize / float(img.size[0]))
    hsize = int((float(img.size[1]) * float(wpercent)))
    img_thumb = img.resize((basewidth, hsize), PIL.Image.ANTIALIAS)
    
    cropped = img_thumb.crop( (0,0,img_resize,img_resize) )
    thumbnail = f"{rootDir}/thumbnail/{uuid.uuid4()}.jpg"
    cropped.save(thumbnail,"jpeg")
    return thumbnail

def createData():
    imagesData=[]
    for root, dirs, files in os.walk(rootDir):
        for file in files:
            if file.endswith(".jpg"):
                filePath = os.path.join(root, file) # create full path
                dir = os.path.dirname(filePath)
                dirBasename = os.path.basename(dir)
                if len(dirBasename) == 6:
                    date = datetime.strptime(dirBasename, '%y%m%d')
                    limit = datetime(2022, 7, 1)
                    if date >= datetime(2022, 7, 1):
                        im = cv2.imread(filePath)
                        h, w, c = im.shape

                        imgFile = {
                            "src": filePath.replace(rootDir, rootUrl),
                            "thumbnail": thumbnail(filePath),
                            "width": 4,
                            "height": 3,
                            
                        }
                        if( w < h):
                            imgFile["width"] = 3
                            imgFile["height"] = 4

                        imagesData.append(imgFile)
    
    output_file = os.path.join(publicDir,"data.json")
    if os.path.exists(output_file):
        os.remove(output_file)
    output_file = open(output_file, "a")
    output_file.write(json.dumps(imagesData))

def main():
    ap = argparse.ArgumentParser()
    createData()
    
    

if __name__ == "__main__":
    main()