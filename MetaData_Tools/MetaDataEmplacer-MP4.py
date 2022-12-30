# Python 3

## Uses
# pip install mutagen

import os
from pickle import FALSE
import mutagen.mp4 # m4a was removed, use mp4
import mutagen.id3
import imageio

# These are "constants" for the program to use.  
# I like to keep most of in not all of the passed in args as consts.
# I also do this so that some sections that use the FILE_EXTS look cleaner.
# Not always needed, but it is nice

# Type of files to track
FILE_EXTS = (".m4a")

# The Dic to look for files
FILE_ROOT = "M:\\Rips\\Unknown artist"
FILE_LOCA = "M:\\Rips\\Unknown artist\\Tichy Tasty - An Unofficial History of Resident Evil"
ALBUM_ART = "ItchyTasty-Art.jpg"

SAVE_CHANGES = True
UPDATE_TRACK_NAME = True
TRACK_COUNT = 177

# Metadata for tracks 
metaUpdate = {
    "\xa9alb": "Tichy Tasty - An Unofficial History of Resident Evil",
    "aART"   : "Blackstone Publishing",
    "\xa9ART": "Alex Aniel",
    "\xa9gen": "Audio Book",
    "\xa9wrt": "Cindy Kay",
    "disk"   : [(7, 7)]
}

def makePicture(path, fileName):

    data = imageio.v2.imread(path + "\\" + fileName)

    format = mutagen.mp4.MP4Cover.FORMAT_JPEG

    pic = mutagen.mp4.MP4Cover(data, format)

    return pic

def getTrackFromFileName(fileName):
    track = fileName.replace("Track ", "")
    track = track.replace(".m4a", "")
    return int(track)

def main(trackCount):
    
    tracks = []

    pic = makePicture(FILE_ROOT, ALBUM_ART)

    for root, dirs, files, in os.walk(FILE_LOCA):
        for name in files:
            if name.endswith(FILE_EXTS):
                tracks.append(name)
                audio = mutagen.mp4.MP4(root + "\\" + name)

                audio['covr'] = [pic]

                for metaKey in metaUpdate:
                    audio[metaKey] = metaUpdate[metaKey]

                newTrackName = ""

                if UPDATE_TRACK_NAME:
                    # Saving og track number in the need to revert
                    trackNum = audio["trkn"][0][0] + trackCount
                    audio["trkn"] = [(trackNum, 0)]
                    newTrackName  = "Track " + str(trackNum)
                    audio["\xa9nam"] = newTrackName

                if SAVE_CHANGES:
                    audio.save()

                # Need to save meta data first before chaing the file name
                if UPDATE_TRACK_NAME:
                    os.rename((FILE_LOCA + "\\" + name), (FILE_LOCA + "\\" + newTrackName + ".m4a"))

                print("-------------------------")
                print(audio.pprint())
            print("-------------------------")

# This is just in case I screw up.... and I have.... hence why it exists lol
def revertFileNames(offSet):
    # TODO: Calculate offSet programmatically
    for root, dirs, files, in os.walk(FILE_LOCA):
        for name in files:
            if name.endswith(FILE_EXTS):
                audio = mutagen.mp4.MP4(root + "\\" + name)
                trkn = getTrackFromFileName(name) - offSet
                audio["trkn"] = [(trkn,0)]
                audio["\xa9nam"] = "Track " + str(trkn)
                audio.save()
                os.rename((FILE_LOCA + "\\" + name), (FILE_LOCA + "\\" + "Track " + str(trkn) + ".m4a"))

def fixTrackNum():
    for root, dirs, files, in os.walk(FILE_LOCA):
        for name in files:
            if name.endswith(FILE_EXTS):
                audio = mutagen.mp4.MP4(root + "\\" + name)
                trkn = getTrackFromFileName(name)
                audio["trkn"] = [(trkn,TRACK_COUNT)]
                audio.save()

def printFiles():
    for root, dirs, files, in os.walk(FILE_LOCA):
        for name in files:
            if name.endswith(FILE_EXTS):
                audio = mutagen.mp4.MP4(root + "\\" + name)
                print("-------------------------")
                print(audio.pprint())

# TODO: Load in cmd args

# main(TRACK_COUNT)

# revertFileNames(0)

# fixTrackNum()

printFiles()
