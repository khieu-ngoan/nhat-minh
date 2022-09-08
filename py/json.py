import json, os.path
from datetime import datetime
from .const import imageDB, publicDir

def directory2Json(imagesData, exportDir):
    # imagesData = sorted( imagesData, key=lambda x: x["src"], reverse = True)
    # imagesData = sorted( imagesData, key=lambda x: x["date"], reverse = True )
    
    # for image in imagesData:
    #     print(image["date"])
    
    jsonFile = os.path.join(exportDir,"data.json")
    if os.path.exists(jsonFile):
        os.remove(jsonFile)
    jsonFile = open(jsonFile, "a")
    jsonFile.write(json.dumps(imagesData))

def createJson(cdn):
    imagesData=[]

    for id, firebaseFile in imageDB.order_by_child("date").get().items():
        date = datetime.strptime(firebaseFile['date'], '%Y-%m-%d')
        
        if date.strftime("%y") != str(cdn):
            continue
        
        imagesData.append(firebaseFile)

    
    imagesData = sorted( imagesData, key=lambda x: x["src"], reverse = True)
    imagesData = sorted( imagesData, key=lambda x: x["date"], reverse = True )
    
    jsonFile = os.path.join(publicDir,f"data-{str(cdn)}.json")
    if os.path.exists(jsonFile):
        os.remove(jsonFile)
    jsonFile = open(jsonFile, "a")
    jsonFile.write(json.dumps(imagesData))