import os
import sys
import json
import spotipy
#import webbrowser
import requests
import spotipy.util as util
from json.decoder import JSONDecodeError
from datetime import datetime

my_username = "hj5uimud6gdownctltjhzcvk3"

#Erase cache and ask for user permission
try:
    token = util.prompt_for_user_token(my_username,scope="playlist-modify-private playlist-modify-public")
except:
    os.remove(f".cache-{my_username}")
    token = util.prompt_for_user_token(my_username,scope="playlist-modify-private playlist-modify-public")

#create spotify Object
spotifyObject = spotipy.Spotify(auth=token)

current_user = spotifyObject.current_user()
displayName = current_user["display_name"]
followers = current_user["followers"]["total"]
#print(json.dumps(current_user,sort_keys=True,indent=5 ))

print("Welcome to Playlist Generator, " + displayName)
print("You have " + str(followers) + " followers!")
print()

#Using the Spotify API rather than spotipy, just for testing
artist_info = requests.get(
    'https://api.spotify.com/v1/search',
    headers={'authorization':"Bearer " + token},
    params ={'q':'Nine+inch+nails','type':"artist"} 
)
print(artist_info.status_code)

while True:

    print("0 - Search for an artist")
    print("1 - exit")
    choice = input("Your choice: ")

    #search for artist to add,
    if choice == "0":
        print()
        search_term = input("Enter the artists name: ")
        search_results = spotifyObject.search(search_term,type='artist')
        #print(json.dumps(search_results,sort_keys=True,indent=5 ))
        if len(search_results["artists"]["items"]) > 0:
            artist_uri = search_results["artists"]["items"][0]["uri"]
            artist_top10 = spotifyObject.artist_top_tracks(artist_uri)
            playlist_name = search_term.lower()
            playlist_name = playlist_name.capitalize() + " Top 10"
            now = datetime.now()
            description = "A top ten playlist for " + search_term + str(now.strftime("%H:%M:%S"))
            top10_tracks_uris = []
            top10_tracks_names = []
            for i in range(10):
                top10_tracks_uris.append(artist_top10["tracks"][i]["uri"])
                top10_tracks_names.append(artist_top10["tracks"][i]["name"])
            response_object = spotifyObject.user_playlist_create(my_username,playlist_name,public=True,description=description)

            #print(json.dumps(artist_top10["tracks"][0]["uri"],sort_keys=True,indent=6))
        else:
            print("ERROR Artist not found")
    if choice == "1":
        break

#print(json.dumps(current_user,sort_keys=True,indent=5 ))
