# This is a sample Python script.
import os
import sys
import json
import spotipy
import webbrowser
import spotipy.util as util
from json.decoder import JSONDecodeError


# Environmental Variables
# set SPOTIPY_CLIENT_ID='2f2019a6bd0e4a88b26a34577f2be1d8'
# set SPOTIPY_CLIENT_SECRET=' b75b2be1432541b98ad13052317d01dd'
# set SPOTIPY_REDIRECT_URI='https://google.com/'

# get username from terminal
username = sys.argv[1]

# erase cache and prompt for user permission
try:
    token = util.prompt_for_user_token(username)
except:
    os.remove(f".cache-{username}")
    token = util.prompt_for_user_token(username)

# create out Spotify Object
spotifyObject = spotipy.Spotify(auth=token)

# prints json in a readable format.
# print(json.dumps(VARIABLE, sort_keys=True, indent=4))

user = spotifyObject.current_user()

# print(json.dumps(user, sort_keys=True, indent=4))

displayName = user['display_name']
followers = user['followers']['total']

while True:
    print()
    print("Welcome to Spotipy " + displayName + "!")
    print(">>>>>  You have " + str(followers) + " followers.")
    print()
    print("0 - Search for artist")
    print("1 - exit")
    print()
    choice = input("Your choice: ")

    if int(choice) == 0:
        print()
        searchQuery = input("Ok, what's their name?: ")
        print()
        # get search results
        searchResults = spotifyObject.search(searchQuery, 1, 0, "artist")
        print(json.dumps(searchResults, sort_keys=True, indent=4))

        artist = searchResults['artists']['items'][0]
        print("Is their name " + artist['name'] + "?")
        print("They have " + str(artist['followers']['total']) + " followers.")
        print(artist['genres'][0])
        print()
        webbrowser.open(artist['images'][0]['url'])
        artistID = artist['id']

        # Album and track details
        trackURIs = []
        trackArt = []
        z = 0

        # Extract Album details
        albumResults = spotifyObject.artist_albums(artistID)
        albumResults = albumResults['items']

        for item in albumResults:
            print("ALBUM" + item['name'])
            albumID = item['id']
            albumArt = item['images'][0]['url']

            # Extract track data
            trackResults = spotifyObject.album_tracks(albumID)
            trackResults = trackResults['items']

            for item2 in trackResults:
                print(str(z) + ": " + item2['name'])
                trackURIs.append(item2['uri'])
                trackArt.append(albumArt)
                z += 1
            print()

        # see album art
        while True:
            songSelection = input("Enter a song number to see the album art associated with it (x to exit).")
            if songSelection == "x":
                break
            webbrowser.open(trackArt[int(songSelection)])

    # end the program
    if int(choice) == 1:
        break

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
#
#
# def print_hi(name):
#     # Use a breakpoint in the code line below to debug your script.
#     print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.
#
#
# # Press the green button in the gutter to run the script.
# if __name__ == '__main__':
#     print_hi('PyCharm')
#
# # See PyCharm help at https://www.jetbrains.com/help/pycharm/
