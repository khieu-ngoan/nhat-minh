import json
import os.path

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