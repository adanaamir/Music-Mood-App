from requests.auth import HTTPBasicAuth
from requests_oauthlib import OAuth2Session
from dotenv import load_dotenv   
import os , requests

load_dotenv()

#STEP1: GET ENV VARIABLES 
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
redirect_uri = "https://oauth.pstmn.io/v1/browser-callback"  #this can be any url 

authorization_base_url = "https://accounts.spotify.com/authorize"   #this and token_url are required necessary for OAuth
token_url = "https://accounts.spotify.com/api/token"

scope = ["user-top-read"]    #Permissions your app requests from the user

#STEP:2 Creating a session using OAuth to manage authetication process
spotify = OAuth2Session(client_id, scope=scope, redirect_uri=redirect_uri)

#STEP:3 This step generates the URL to redirect the user to Spotify for login and permission approval.
authorization_url, _ = spotify.authorization_url(authorization_base_url, prompt = 'login')
print("Please visit here and login: ", authorization_url)

#STEP:4 After the user logs in, Spotify redirects them to your redirect_url with an authorization code as a query parameter. The user then pastes the URL in exchange for an access token
redirect_response = input("\n\nPaste the full redirect URL here: ")

#STEP:5 Fetching the access token : in exchange with autho code from provided URL
auth = HTTPBasicAuth(client_id, client_secret)
token_info = spotify.fetch_token(token_url, auth=auth, authorization_response=redirect_response)  #fetchtoknk typically return the access toke inside the dic so thats why ie done the below step
token = token_info['access_token']   #extracting the access token


top_tracks_url = "https://api.spotify.com/v1/me/top/tracks"
headers = {
    "Authorization": f"Bearer {token}" 
}
response = requests.get(top_tracks_url, headers=headers)

#STEP:6 Using the access token
# r = spotify.get("https://api.spotify.com/v1/me")  #contains info about the user
if response.status_code != 200:
    print(f"Error: {response.status_code} - {response.text}")
    exit()

try:
    top_tracks = response.json()
except requests.exceptions.JSONDecodeError:
    print("Error: Failed to decode JSON response.")
    print(f"Response Content: {response.text}")
    exit()

print("\nFetching users top tracks...\n")

top_tracks = response.json()

for idx, tracks in enumerate(top_tracks['items']):
    print(f"{idx+1}. Track Name: {tracks['name']}, Artist: {tracks['artists'][0]['name']}")

if not top_tracks.get('items', []):
        print("No data was found")
        exit()