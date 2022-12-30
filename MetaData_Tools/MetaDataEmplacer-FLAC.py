# Python 3

## Uses
# pip install mutagen

import os
from mutagen.flac import FLAC
import mutagen.id3

# These are "constants" for the program to use.  
# I like to keep most of in not all of the passed in args as consts.
# I also do this so that some sections that use the FILE_EXTS look cleaner.
# Not always needed, but it is nice

# Type of files to track
FILE_EXTS = (".flac")#(".mp3", ".m4a", ".flac", ".alac")

# The Dic to look for files
FILE_LOCA = "M:\\Rips\\Unknown artist\\Itchy Tasty - Disc 1"
ALBUM_ART = "ItchyTasty-Art.jpg"

# Metadata for tracks 
metaUpdate = {
    "AUTHOR"      : "Alex Aniel",
    "ARTITS"      : "Cindy Kay",
    "ALBUM"       : "Tichy Tasty - An Unofficial History of Resident Evil",
    "GENRE"       : "Audio Book",
    "ALBUMARTIST" : "Blackstone Publishing",
    "DISK"        : "1"
}

SAVE_CHANGES = True

def makePicture(path, fileName):
    pic = mutagen.flac.Picture()

    with open(path + "\\" + fileName, "rb") as f:
        pic.data = f.read()
    
    pic.type = mutagen.id3.PictureType.COVER_FRONT
    pic.mime = u"image/jpg"
    pic.width = 500
    pic.height = 500
    pic.depth = 16 # color depth

    return pic

def main():
    
    tracks = []

    pic = makePicture(FILE_LOCA, ALBUM_ART)

    for root, dirs, files, in os.walk(FILE_LOCA):
        for name in files:
            if name.endswith(FILE_EXTS):
                tracks.append(name)
                audio = FLAC(root + "\\" + name)

                audio.pictures.append(pic)

                for metaKey in metaUpdate:
                    audio[metaKey] = metaUpdate[metaKey]

                if SAVE_CHANGES:
                    audio.save()
                
                print("-------------------------")
                print(audio.pprint())
            print("-------------------------")


# TODO: Load in cmd args

main()


