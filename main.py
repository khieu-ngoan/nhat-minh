import os, argparse
import os.path
from os.path import exists
import PIL
from PIL import Image
from py.json import directory2Json, createJson
from py.firebase import syncToFirebaseRealtime, cleanFirebase, cdnMigrate
from py.tool import createThumbs
from py.file import underMigrate


def getSrc(imageObject):
    return imageObject.get('src')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--action', help='foo help')
    args = parser.parse_args()

    print(args)
    exit()
    if args.action=='thumb' or args.action == 'thumbnail':
        createThumbs(22)
        return
    elif args.action == 'firebase':
        syncToFirebaseRealtime()
        # cdnMigrate()
    elif args.action == 'firebase-clean':
        cleanFirebase()
    elif args.action=='json':
        createJson(22)
    elif args.action=='upgrade':
        syncToFirebaseRealtime()
        createThumbs(22)
        createJson(22)
    else :
        # underMigrate(19)
        print("no action")
    # syncToFirebaseRealtime()
    # createJson(replate=False)
    
if __name__ == "__main__":
    main()