__author__ =  "Richard Meng @ UC Berkeley" 

# PLEASE SUPPORT LEGAL COPIES AND ONLY USE FOR PERSONAL PURPOSES!

import json, urllib
import os, sys
from shutil import copyfile
import urllib2

# UTILITIES
def requestNeteaseJSON(songID):
	url = "http://music.163.com/api/song/detail/?id="+str(songID)+"&ids=%5B"+str(songID)+"%5D&csrf_token="
	songJSON = json.load(urllib.urlopen(url))
	return songJSON

def check_connectivity():
    try:
        response=urllib2.urlopen('http://music.163.com',timeout=1)
        return True
    except urllib2.URLError as err: pass
    return False

if platform.system() == 'Darwin':
	fromPath = os.path.expanduser("~/Library/Containers/com.netease.163music/Data/Caches/online_play_cache/")
	toPath = os.path.expanduser("~/Desktop/NeteaseCacheMusic/")
if platform.system() == 'Windows':
	fromPath = os.path.expanduser("~\\AppData\\Local\\Netease\\CloudMusic\\Cache\\Cache\\")
	toPath = os.path.expanduser("~\\Desktop\\NeteaseCacheMusic\\")

dirs = os.listdir(fromPath)
songDict = {}

if not os.path.exists(toPath):
    os.makedirs(toPath)
    open(toPath+".HISTORY", 'a').close()

HISTORY = open(toPath + ".HISTORY", 'a')
HISTORYREAD = open(toPath + ".HISTORY")

def processCachedSongs():
	counter = 0
	for f in dirs:
		if f.endswith(".uc!") or f.endswith(".uc"):
			idx = f.find("-_-")
			if idx > 0:
				songID = f[:idx]
				with open(toPath + ".HISTORY") as fl:
					if str(songID) not in fl.read():
						copyfile(fromPath+f, toPath+f)
						songDict[str(songID)] = toPath + f
					
	for f in dirs:
		if f.endswith(".info"):
			with open(fromPath+f) as jsonData:
				tempData = json.load(jsonData)
				songID = tempData["songId"]
				if str(songID) in songDict:
					songJSON = requestNeteaseJSON(songID)
					if songJSON:
						HISTORY.write(str(songID) + "\n")
						songName = songJSON["songs"][0]["name"]
						songArtist = songJSON["songs"][0]["album"]["artists"][0]["name"]
						newSongName = songName + "-" + songArtist + ".mp3"
						os.rename(songDict[str(songID)], toPath + newSongName)
						counter += 1
						# print(newSongName+" has been saved to NeteaseCacheMusic folder on your Desktop")
	HISTORY.close()
	return counter

def main():
	if check_connectivity():
		print("Processing Songs...")
		print(str(processCachedSongs()) + " songs has been processed.")

	else: print("Network connection is lost. Please check network connection!")

main()


