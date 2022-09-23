import json, os.path, requests
from datetime import datetime
from .const import imageDBRealtime, publicDir, API_IMAGES

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
    # for img in imageDBFirestore:
    response = requests.get(API_IMAGES+ '?year=20'+str(cdn))

    if response.status_code!=200 :
        print("data is empty")
        exit()

    # for model in response.json()['data']:
    #     date = datetime.strptime(model['date'], '%Y-%m-%d')
        
    #     if date.strftime("%y") != str(cdn):
    #         continue
    #     firebaseFile['src'] = f"{firebaseFile['cdn']}{firebaseFile['src']}"
    #     firebaseFile['thumbnail'] = f"{firebaseFile['cdn']}/thumbnail/{id}.jpg"
        
    #     imagesData.append(firebaseFile)

    
    # imagesData = sorted( imagesData, key=lambda x: x["src"], reverse = True)
    # imagesData = sorted( imagesData, key=lambda x: x["date"], reverse = True )
    
    imagesData = response.json()['data']
    jsonFile = os.path.join(publicDir,f"data-{str(cdn)}.json")
    if os.path.exists(jsonFile):
        os.remove(jsonFile)
    jsonFile = open(jsonFile, "a")
    jsonFile.write(json.dumps(imagesData))