# Python 3

## Uses
# pip install mutagen

import os
from pickle import FALSE
import mutagen.mp4 # m4a was removed, use mp4
import mutagen.id3
import imageio
import json

# These are "constants" for the program to use.  
# I like to keep most of in not all of the passed in args as consts.
# I also do this so that some sections that use the FILE_EXTS look cleaner.
# Not always needed, but it is nice

# Type of files to track
FILE_EXTS = (".m4a")

#Path to json file
DATA_FILE = "AlbumInfo.json"

# The Dic to look for files
FILE_ROOT = "M:\\Rips\\Things I Overheard While Talking to Myself"

SAVE_CHANGES = True
UPDATE_TRACK_NAME = True

# Mathching a simple name to mutagen key for mp4/m4a files.
# It's much easier then remembering the mutKey for each prop.
mp4MetaDataKey = {
    "trackTitle"      : { "mutKey": "\xa9nam" , "Type":"Text"           , "desc": "track title"                                                     },
    "album"           : { "mutKey": "\xa9alb" , "Type":"Text"           , "desc": "album"                                                           },
    "artist"          : { "mutKey": "\xa9ART" , "Type":"Text"           , "desc": "artist"                                                          },
    "albumArtist"     : { "mutKey": "aART"    , "Type":"Text"           , "desc": "album artist"                                                    },
    "composer"        : { "mutKey": "\xa9wrt" , "Type":"Text"           , "desc": "composer"                                                        },
    "year"            : { "mutKey": "\xa9day" , "Type":"Text"           , "desc": "year"                                                            },
    "comment"         : { "mutKey": "\xa9cmt" , "Type":"Text"           , "desc": "comment"                                                         },
    "description"     : { "mutKey": "desc"    , "Type":"Text"           , "desc": "description (usually used in podcasts)"                          },
    "purchaseDate"    : { "mutKey": "purd"    , "Type":"Text"           , "desc": "purchase date"                                                   },
    "grouping"        : { "mutKey": "\xa9grp" , "Type":"Text"           , "desc": "grouping"                                                        },
    "genre"           : { "mutKey": "\xa9gen" , "Type":"Text"           , "desc": "genre"                                                           },
    "lyrics"          : { "mutKey": "\xa9lyr" , "Type":"Text"           , "desc": "lyrics"                                                          },
    "pcURL"           : { "mutKey": "purl"    , "Type":"Text"           , "desc": "podcast URL"                                                     },
    "pcEpisodeGUID"   : { "mutKey": "egid"    , "Type":"Text"           , "desc": "podcast episode GUID"                                            },
    "pcCategory"      : { "mutKey": "catg"    , "Type":"Text"           , "desc": "podcast category"                                                },
    "pcKeywords"      : { "mutKey": "keyw"    , "Type":"Text"           , "desc": "podcast keywords"                                                },
    "encodedBy"       : { "mutKey": "\xa9too" , "Type":"Text"           , "desc": "encoded by"                                                      },
    "copyright"       : { "mutKey": "cprt"    , "Type":"Text"           , "desc": "copyright"                                                       },
    "albSorOrd"       : { "mutKey": "soal"    , "Type":"Text"           , "desc": "album sort order"                                                },
    "albArtistSorOrd" : { "mutKey": "soaa"    , "Type":"Text"           , "desc": "album artist sort order"                                         },
    "artistSorOrd"    : { "mutKey": "soar"    , "Type":"Text"           , "desc": "artist sort order"                                               },
    "titleSorOrd"     : { "mutKey": "sonm"    , "Type":"Text"           , "desc": "title sort order"                                                },
    "composerSorOrd"  : { "mutKey": "soco"    , "Type":"Text"           , "desc": "composer sort order"                                             },
    "showSorOrd"      : { "mutKey": "sosn"    , "Type":"Text"           , "desc": "show sort order"                                                 },
    "showName"        : { "mutKey": "tvsh"    , "Type":"Text"           , "desc": "show name"                                                       },
    "work"            : { "mutKey": "\xa9wrk" , "Type":"Text"           , "desc": "work"                                                            },
    "movement"        : { "mutKey": "\xa9mvn" , "Type":"Text"           , "desc": "movement"                                                        },
    "isACompilation"  : { "mutKey": "cpil"    , "Type":"Boolean "       , "desc": "Part of a compilation"                                           },
    "isAGaplessAlbum" : { "mutKey": "pgap"    , "Type":"Boolean "       , "desc": "Part of a gapless album"                                         },
    "isAPodCast"      : { "mutKey": "pcst"    , "Type":"Boolean "       , "desc": "Podcast (iTunes reads this only on import)"                      },
    "trackData"       : { "mutKey": "trkn"    , "Type":"Tuples of ints" , "desc": "track number, total tracks"                                      },
    "diskData"        : { "mutKey": "disk"    , "Type":"Tuples of ints" , "desc": "disc number, total discs"                                        },
    "tempo"           : { "mutKey": "tmpo"    , "Type":"Integer"        , "desc": "tempo/BPM"                                                       },
    "moveCount"       : { "mutKey": "\xa9mvc" , "Type":"Integer"        , "desc": "Movement Count"                                                  },
    "moveIndex"       : { "mutKey": "\xa9mvi" , "Type":"Integer"        , "desc": "Movement Index"                                                  },
    "workMove"        : { "mutKey": "shwm"    , "Type":"Integer"        , "desc": "work/movement"                                                   },
    "mediaKind"       : { "mutKey": "stik"    , "Type":"Integer"        , "desc": "Media Kind"                                                      },
    "hdVideo"         : { "mutKey": "hdvd"    , "Type":"Integer"        , "desc": "HD Video"                                                        },
    "contentRating"   : { "mutKey": "rtng"    , "Type":"Integer"        , "desc": "Content Rating"                                                  },
    "tvEpisode"       : { "mutKey": "tves"    , "Type":"Integer"        , "desc": "TV Episode"                                                      },
    "tvSeason"        : { "mutKey": "tvsn"    , "Type":"Integer"        , "desc": "TV Season"                                                       },
    "coverArtwork"    : { "mutKey": "covr"    , "Type":"Others"         , "desc": "cover artwork, list of MP4Cover objects (which are tagged strs)" },
    "ID3v1Genre"      : { "mutKey": "gnre"    , "Type":"Others"         , "desc": "ID3v1 genre. Not supported, use ‘\xa9gen’ instead."              }
}

def loadInMetaData(path):
    file = open(path)
    metaData = json.load(file)
    return metaData

def outputJson(path, jsonData):
    json_object = json.dumps(jsonData)
    with open( os.path.join(path, "outputJson.json") , "w") as outfile:
        outfile.write(json_object)

def makePicture(path, fileName):

    data = imageio.v2.imread( os.path.join(path, fileName) )

    format = mutagen.mp4.MP4Cover.FORMAT_JPEG

    pic = mutagen.mp4.MP4Cover(data, format)

    return pic

# Pulls out the disc number from the folder name
def getDiscNumFromDir(dir):
    discNum = dir.replace("Disc ", "")
    return int(discNum)

# Pulls out the Track Number from the file name
def getTrackFromFileName(fileName):
    track = fileName.replace("Track ", "")
    track = track.replace(".m4a", "")
    return int(track)

# Goes through and does a pre-flight gathing of details
# ex: Number of discs, Number of Tracks etc.
# TODO: Intergrate as part of the main loop to reduce time
def gatherInfo(allMetaData, albumPath):
    albumData = allMetaData["albumData"]

    # We will be filling in the track data if its not there.
    # We will also be gathering other details such as folder location
    # so we can iterate over each track with out having to do this deep dive for-loop-ception
    if "trackData" not in allMetaData:
        allMetaData["trackData"] = []

    albumData["totalDiscs"]  = 0
    albumData["totalTracks"] = 0

    # I walk the line, I walk the line
    trackCount = 1
    for root, dirs, files, in os.walk(albumPath):

        # only at root
        if len(dirs) > 0:
            albumData["totalDiscs"] = len(dirs)
            continue

        # for each disc
        for track in files:
            allMetaData["trackData"].append({
                "name" : track, # TODO: may need to look into how to manage the track name
                "num"  : trackCount,
                "disc" : getDiscNumFromDir(os.path.basename(root)),
                "path" : root
            })
            trackCount += 1
    
    
    albumData["totalTracks"] = len(allMetaData["trackData"])

# Simple function to update all info for just one track
def updateTrack(allMetaData, track, pic):
    fullTrackPath = os.path.join(track["path"], track["name"])
    audio = mutagen.mp4.MP4(fullTrackPath)
    albumData = allMetaData["albumData"]
    audio['covr'] = [pic] # TODO: Replace with mutegen key map?

    # Replace all base data of the track
    # Json input file should match using mp4MetaDataKey's
    for dataKey in albumData:
        if dataKey in mp4MetaDataKey:
            audio[mp4MetaDataKey[dataKey]["mutKey"]] = albumData[dataKey]

    newTrackName = "Track " + str(track["num"])

    # Special cases

    audio["trkn"] = [(track["num"], albumData["totalTracks"])] # TODO: Replace with mutegen key map?

    if UPDATE_TRACK_NAME:
        audio["\xa9nam"] = newTrackName # TODO: Replace with mutegen key map?

    if allMetaData["options"]["saveChanges"]:
        audio.save()

    # Need to save meta data first before chaing the file name
    if allMetaData["options"]["updateTrackNames"] and UPDATE_TRACK_NAME:
        os.rename(fullTrackPath, os.path.join(track["path"], newTrackName + ".m4a"))

    print(audio.pprint())

def main(albumPath):

    allMetaData = loadInMetaData(  os.path.join(albumPath, DATA_FILE) )
    
    pic = makePicture(albumPath, allMetaData["albumData"]["albumArt"])

    gatherInfo(allMetaData, albumPath)

    # For testing
    outputJson(albumPath, allMetaData)

    for track in allMetaData["trackData"]:
        print("-------------------------")
        updateTrack(allMetaData, track, pic)
        print("-------------------------")
  
# This is just in case I screw up.... and I have.... hence why it exists lol
def revertFileNames(offSet, path):
    # TODO: Calculate offSet programmatically
    for root, dirs, files, in os.walk(path):
        for name in files:
            if name.endswith(FILE_EXTS):
                audio = mutagen.mp4.MP4( os.path.join(root, name) )
                trkn = getTrackFromFileName(name) - offSet
                audio["trkn"] = [(trkn,0)]
                audio["\xa9nam"] = "Track " + str(trkn)
                audio.save()
                os.rename(os.path.join(path, name), os.path.join(path, "Track " + str(trkn) + ".m4a"))

def fixTrackNum(path, totalTrackCount):
    for root, dirs, files, in os.walk(path):
        for name in files:
            if name.endswith(FILE_EXTS):
                audio = mutagen.mp4.MP4( os.path.join(root, name) )
                trkn = getTrackFromFileName(name)
                audio["trkn"] = [(trkn,totalTrackCount)]
                audio.save()

def printFiles(path):
    for root, dirs, files, in os.walk(path):
        for name in files:
            if name.endswith(FILE_EXTS):
                audio = mutagen.mp4.MP4( os.path.join(root, name) )
                print("-------------------------")
                print(audio.pprint())

# TODO: Load in cmd args

main(FILE_ROOT)

# revertFileNames(0)

# fixTrackNum()

#printFiles()
