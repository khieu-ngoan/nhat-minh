import os, argparse
import os.path
from os.path import exists
import PIL
from PIL import Image
from py.json import directory2Json, createJson
from py.firebase import syncToFirebaseRealtime, cleanFirebase, cdnMigrate, syncToMySql
from py.tool import createThumbs
from py.file import underMigrate


def getSrc(imageObject):
    return imageObject.get('src')

# py main.py --action=thumb
# py main.py --action=firebase
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--action', help='foo help')
    args = parser.parse_args()

    if args.action=='thumb' or args.action == 'thumbnail':
        createThumbs(22)
        return
    elif args.action == 'to-sql':
        syncToMySql()
        # cdnMigrate()
    elif args.action == 'firebase-clean':
        cleanFirebase()
    elif args.action=='json':
        createJson(22)
    elif args.action=='upgrade':
        syncToMySql()
        createThumbs(22)
        createJson(22)
    else :
        # underMigrate(19)
        print("no action")
    # syncToFirebaseRealtime()
    # createJson(replate=False)
    
if __name__ == "__main__":
    main()