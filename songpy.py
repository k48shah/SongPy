from bs4 import BeautifulSoup
import eyed3
from urllib.parse import quote
from urllib.request import urlopen, Request
from google_images_search import GoogleImagesSearch
import os
import requests
import shutil
import coverpy
import urllib.request
import youtube_dl
import itunespy


def audioSearch(audio_string):
    # Search for given mp3 file
    for root, dirs, files in os.walk('C:\\'):
        if audio_string in files:
            aString = str.join(root, audio_string)
            print("found: " + aString)
            return aString
    return "find"


# Search for all audio files to be added


def imgSearch(album, title):
    c = coverpy.CoverPy()
    while True:
        print (album)
        album = album.split(" - ")
        print (title)
        i = title + album
        if i == 'exit':
            exit()

        try:
            query = c.get_cover(i)
            print("Name: %s" % query.name)
            print("EntityType: %s" % query.type)
            print("Artist: %s" % query.artist)
            print("Album: %s" % query.album)
            print(query.artwork())
            print("QueryUrl: %s" % query.url)
        except coverpy.exceptions.NoResultsException as e:
            print("Nothing found.")
    return

def textTags(audio, artist, album, title):
    print(audio)
    track = eyed3.load(os.path.dirname(os.path.abspath(__file__)) + r"\\" + audio).tag

    track.artist = artist
    track.album_artist = artist
    track.title = title
    track.album = album
    track.save()

    os.rename(os.path.dirname(os.path.abspath(__file__)) + r"\\" + audio, os.path.dirname(os.path.abspath(__file__)) + r"\\" + artist + " - " + title + '.mp3')

    arturl = imgSearch(album, title)
    """
    track.tags.add(
        APIC(
            encoding=3,
            mime='image/jpeg',
            type=3,
            desc=u'Cover',
            data=(urlopen(url)).read()
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
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
        filename = filename.strip('.m4a')
        filename = filename + '.mp3'
        print(filename)
        filename = filename.strip('.webm')
        return filename


def findAlbum(title, artist):
    tracks = itunespy.search_track(title)
    i = 1
    for x in tracks:
        if x.artist_name == artist:
            return x.collection_name


def main():
    audio_name = input("Input file name with file type/ALL/EXIT (DO NOT add .mp3 at the end of the file): \n")
    filename = ''
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
            filename = vidDL(vidURL)
        album_title = findAlbum(audio_title, artist_name)
        arturl = ''
        # Find Album Art
        aString = audioSearch(audio_name + ".mp3")
        textTags(filename, artist_name, album_title, audio_title)
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