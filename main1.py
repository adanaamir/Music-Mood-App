#The reason you're using dotenv here is to securely manage your credentials by storing them in a .env file,
# rather than hardcoding them directly in your script.
from dotenv import load_dotenv   
import os   #os is often used for working with environment variables (here im retrieving the env variables that are loaded from your .env file) 
import base64
from requests import post, get
import json

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

def get_token():
    auth_string = client_id + ":" + client_secret  #now that i have this string, i need to encode it (done in next step)
    auth_bytes = auth_string.encode("utf-8")   #encoding this using "utf-8", then im gonna encode this using base64 (done in next step)
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")     #converting the returned base64 object into a string so that we can pass it with headers when we send requests to the say account center api

    url = "https://accounts.spotify.com/api/token"   #url to which i wanna send request to

    headers = {   #headers are gonna be associated with our requests, we're gonna send a post request to the upper url --- These are required by spotify
        "Authorization": "Basic " + auth_base64,  #here we are sending our autho data, where we will verify that everything is correct and a token will be sent to us
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}  #as it said on the website, i need to pass in a grant type, which here is client credentials 
    
    #now we are ready to formulate a response, it will send an HTTP post request to spotifys api
    result = post(url, headers=headers, data=data)  #here we will get a json data, we will convert it to a python dictionary(next step)
    json_result = json.loads(result.content)   #loads mean load from string

    #parsing  my token, it will be stored in field called access token
    token = json_result["access_token"]
    return token

def get_auth_header(token):
    return {"Authorization": "Bearer " + token}   #autho header for any future requests

#function that allows us to search for an artist
def search_for_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)   #getting the header (function) i made earlier
    query = f"q={artist_name}&type=artist&limit=1"  #if i was looking for an artist as well as track, then then type would be artist,track -- limit=1 means that when i search for an artist, the post popular one pops out

    query_url = url+ "?" + query
    result = get(query_url, headers=headers) 
    json_result = json.loads(result.content)["artists"]["items"]
    
    if len(json_result) == 0:
        print("No artist with this name exists")
        return None
    return json_result[0]  #else return the very first result

def get_songs_by_artist(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"   #here i have my base url, and iam looking for a specific artist 
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)["tracks"]
    return json_result

token = get_token()
result = search_for_artist(token, "Chase Atlantic")
artist_id = result["id"]
songs = get_songs_by_artist(token, artist_id)

for idx, song in enumerate(songs):   #printing top 10 songs by the artist
    print(f"{idx+1}. {song['name']}")  #prints the songs rank and name
