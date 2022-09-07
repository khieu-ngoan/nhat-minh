import os, argparse
import os.path
from os.path import exists
import PIL
from PIL import Image
from py.json import directory2Json, createJson
from py.firebase import syncToFirebaseRealtime, cleanFirebase
from py.tool import createThumbs


def getSrc(imageObject):
    return imageObject.get('src')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--action', help='foo help')
    args = parser.parse_args()

    if args.action=='thumb' or args.action == 'thumbnail':
        createThumbs(19)
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