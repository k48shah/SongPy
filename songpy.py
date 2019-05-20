from bs4 import BeautifulSoup
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC
from mutagen.easyid3 import EasyID3
from urllib.parse import quote
from urllib.request import urlopen, Request
from google_images_search import GoogleImagesSearch
import os
import requests
import shutil
import urllib.request
import youtube_dl
import itunespy


def audioSearch(audio_string):
    # Search for given mp3 file
    for root, dirs, files in os.walk('C:\\'):
        if audio_string in files:
            aString = str.join(root, audio_string)
            print("found: %s" % aString)
            return aString
    return "find"


# Search for all audio files to be added

def imgSearch(album):
    return
def textTags(audio, artist, album, title, arturl):
    # Change non-image tags
    #response = requests.get(arturl, stream=True)
    #ith open('img.jpg', 'wb') as out_file:
    #    shutil.copyfileobj(response.raw, out_file)
    #del response
    print(audio)
    track = EasyID3(title, filename=audio)
    track['artist'] = artist
    track['title'] = title
    track['tracknumber'] = '0'
    track['album'] = album
    track.save()

    track = EasyID3(title, filename=audio)
    audio.add_tags()
    """
    track.tags.add(
        APIC(
            encoding=3,
            mime='image/jpeg',
            type=3,
            desc=u'Cover',
            data=(urlopen(arturl)).read()
        )
    )
    track.save()
    """
def yturl(title, artist):
    query = urllib.parse.quote(artist + " " + title + " audio")
    print(query)
    url = "https://www.youtube.com/results?search_query=" + query
    response = urllib.request.urlopen(url)
    #html = response.read()
    soup = BeautifulSoup(response)
    chosenVid = 'https://www.youtube.com'
    print("Choose the video number you prefer \n")
    i = 1
    vidList = []
    for vid in soup.findAll(attrs={'class': 'yt-uix-tile-link'}):
        if not vid['href'].startswith("https://googleads.g.doubleclick.net/"):
            print(str(i) + ": " + chosenVid + vid['href'])
            vidList.insert(i-1, chosenVid + vid['href'])
            i = i + 1
    j = int(input()) - 1
    return vidList[j]


def vidDL(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


def findAlbum(title, artist):
    artistSearch = itunespy.search_artist(artist)
    tracks = itunespy.search_track(title)
    i = 1
    for x in tracks:
        i = i+1
        return x.collection_name


def main():
    print("Input file name with file type/ALL/EXIT: \n")
    audio_name = input("Input file name with file type/ALL/EXIT (DO NOT add .mp3 at the end of the file): \n")
    if audio_name != "ALL":
        aString = audioSearch(audio_name + ".mp3")
        if " - " in audio_name:
            artist_name, audio_title = audio_name.split(" - ")
            if " [" in audio_title:
                audio_title = audio_title.split(" [")[0]
            elif "[" in audio_title:
                audio_title = audio_title.split("[")[0]
            elif " (" in audio_title:
                audio_title = audio_title.split(" (")[0]
            elif "(" in audio_title:
                audio_title = audio_title.split("(")[0]
        elif "-" in audio_name:
            artist_name, audio_title = audio_name.split("-")
            if " [" in audio_title:
                audio_title = audio_title.split(" [")[0]
            elif "[" in audio_title:
                audio_title = audio_title.split("[")[0]
            elif " (" in audio_title:
                audio_title = audio_title.split(" (")[0]
            elif "(" in audio_title:
                audio_title = audio_title.split("(")[0]
        else:
            audio_title = audio_name
            track = itunespy.search_track(audio_title)
            artist_name = track[0].artist_name
        print(audio_title + artist_name)
        if aString == "find":
            print("Could not find file, checking videos for closest match")
            vidURL = yturl(audio_title, artist_name)
            vidDL(vidURL)

        album_title = findAlbum(audio_title, artist_name)

        # Find Album
        # Find Album Art
        aString = audioSearch(audio_name + ".mp3")
        textTags(aString, artist_name, album_title, audio_title, imgSearch(album_title))
    elif audio_name == "ALL":
        print("To Be Added")
    elif audio_name == "EXIT":
        print("program ended, restart the console if you wish to proceed again")
        return
    else:
        print("invalid input")
        main()


if __name__ == '__main__':
    main()