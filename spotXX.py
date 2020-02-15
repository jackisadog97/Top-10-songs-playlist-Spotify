import os
import sys
import json
import spotipy
#import webbrowser
import requests
import spotipy.util as util
from json.decoder import JSONDecodeError
from datetime import datetime
import urllib.request
import base64

my_username = 
client_id = 
client_s = 
client_r = 

#Erase cache and ask for user permission
try:
    token = util.prompt_for_user_token(my_username,scope="playlist-modify-private playlist-modify-public ugc-image-upload",client_id=client_id,client_secret=client_s,redirect_uri=client_r)
except:
    os.remove(f".cache-{my_username}")
    token = util.prompt_for_user_token(my_username,scope="playlist-modify-private playlist-modify-public ugc-image-upload")

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
'''
artist_info = requests.get(
    'https://api.spotify.com/v1/search',
    headers={'authorization':"Bearer " + token},
    params ={'q':'Nine+inch+nails','type':"artist"} 
)'''

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
            playlist_name = search_results["artists"]["items"][0]["name"]
            playlist_name = playlist_name.upper() + " \nTop 10"
        #get artist image for playlist
            image_url = search_results["artists"]["items"][0]["images"][1]["url"]
            urllib.request.urlretrieve(image_url,"artist_image.jpeg")
            with open("artist_image.jpeg","rb") as f:
                encoded_string = base64.b64encode(f.read())


            now = datetime.today()
            description = "A top ten playlist for " + search_term.upper() + ". Created on the " + now.strftime('%d-%m-%Y')
            top10_tracks_uris = []
            top10_tracks_names = []
            for i in range(10):
                top10_tracks_uris.append(artist_top10["tracks"][i]["uri"])
                top10_tracks_names.append(artist_top10["tracks"][i]["name"])
            response_object = spotifyObject.user_playlist_create(my_username,playlist_name,public=True,description=description)
            #print(json.dumps(response_object,sort_keys=True,indent=5))
            playlist_id = response_object["id"]
            print(playlist_id)
            spotifyObject.user_playlist_add_tracks(my_username,playlist_id,top10_tracks_uris)
            spotifyObject.playlist_upload_cover_image(playlist_id,encoded_string)
            
            if os.path.isfile("artist_image.jpeg"):
                os.remove('artist_image.jpeg')
            
            '''
artist_info = requests.get(
    'https://api.spotify.com/v1/search',
    headers={'authorization':"Bearer " + token},
    params ={'q':'Nine+inch+nails','type':"artist"} 
)'''



            #print(json.dumps(artist_top10["tracks"][0]["uri"],sort_keys=True,indent=6))
        else:
            print("ERROR Artist not found")
    if choice == "1":
        break

#print(json.dumps(current_user,sort_keys=True,indent=5 ))
