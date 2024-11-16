from requests.auth import HTTPBasicAuth
from requests_oauthlib import OAuth2Session
from dotenv import load_dotenv   
import os 

load_dotenv()

#STEP1: GET ENV VARIABLES 
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
redirect_uri = "https://oauth.pstmn.io/v1/browser-callback"

authorization_base_url = "https://accounts.spotify.com/authorize"
token_url = "https://accounts.spotify.com/api/token"

scope = [    #Permissions your app requests from the user
    "user-read-email",
    "playlist-read-collaborative"
]

#STEP:2 Creating a session using OAuth to manage authetication process
spotify = OAuth2Session(client_id, scope=scope, redirect_uri=redirect_uri)

#STEP:3 This step generates the URL to redirect the user to Spotify for login and permission approval.
authorization_url, state = spotify.authorization_url(authorization_base_url)
print("Please go here and authorize: ", authorization_url)

#STEP:4 After the user logs in, Spotify redirects them to your redirect_url with an authorization code as a query parameter. The user then pastes the URL in exchange for an access token
redirect_response = input("\n\nPaste the full redirect URL here: ")

#STEP:5 Fetching the access token : in exchange with autho code from provided URL
auth = HTTPBasicAuth(client_id, client_secret)
token = spotify.fetch_token(token_url, auth=auth, authorization_response=redirect_response)

#STEP:6 Using the access token
r = spotify.get("https://api.spotify.com/v1/me")
print(f"\n{r.content}")