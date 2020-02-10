import os
import sys
import json
import spotipy
#import webbrowser
import spotipy.util as util
from json.decoder import JSONDecodeError

my_username = "hj5uimud6gdownctltjhzcvk3"

#Erase cache and ask for user permission
try:
    token = util.prompt_for_user_token(my_username)
except:
    os.remove(f".cache-{my_username}")
    token = util.prompt_for_user_token(my_username)

#create spotify Object
spotifyObject = spotipy.Spotify(auth=token)

current_user = spotifyObject.current_user()
displayName = current_user["display_name"]
followers = current_user["followers"]["total"]
#print(json.dumps(current_user,sort_keys=True,indent=5 ))


while True:
    print("Welcome to Playlist Generator, " + displayName)
    print("You have " + str(followers) + " followers!")
    print()
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
            top10_tracks_uris = []
            for i in range(10):
                top10_tracks_uris.append(artist_top10["tracks"][i]["uri"])
            print(top10_tracks_uris)

            #print(json.dumps(artist_top10["tracks"][0]["uri"],sort_keys=True,indent=6))
        else:
            print("ERROR Artist not found")
    if choice == "1":
        break

#print(json.dumps(current_user,sort_keys=True,indent=5 ))
