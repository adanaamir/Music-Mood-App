from dotenv import load_dotenv
import os
from requests_oauthlib import OAuth2Session
from requests.auth import HTTPBasicAuth

load_dotenv()

#STEP: 1 SETUP ENV VARIABLES
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
redirect_url = "https://oauth.pstmn.io/v1/browser-callback"  #this can be any url

token_url = "https://accounts.spotify.com/api/token"          #this and below url are part of the OAuth 2.0 authentication flow
authorization_base_url = "https://accounts.spotify.com/authorize"

scope = [           # these are the permissions your app requests from the user
    "user-read-email",
    "playlist-read-collaborative"
]

# STEP:2 CREATING A SESSION TO MANAGE THE AUTHORIZATION PROCESS
#here scope specifies the permissions your app is requesting from the user. (accessing users email, and to access playlists)
#the redirect_url is used when user approves(or denys) the requested permission
spotify = OAuth2Session(client_id, scope=scope, redirect_uri=redirect_url)

# STEP:3 GENERATING AUTHORIZATION URL
#redirecting user to spotify for authentication
authorization_url, state = spotify.authorization_url(authorization_base_url)
print("Please go here and authorize: ", authorization_url)  #authorization_url is the url that youll use to redirect user for them to login and authorize your app

#STEP:4 HANDLING THE REDIRECT RESPONSE
#After the user logs in and authorizes, Spotify redirects them to your redirect_url with an authorization code as a query parameter. they then enter that url
redirect_response = input("\n\n Paste the full redirect URL here: ")

#STEP:5 FETCHING THE ACCESS TOKEN
#now using the auth code from the redirect url, exchange it with an access token
auth = HTTPBasicAuth(client_id, client_secret)
token = spotify.fetch_token(token_url, auth=auth, authorization_response=redirect_response)

#STEP:6 USING THE ACCESS TOKEN
r = spotify.get("https://api.spotify.com/v1/me") #fetching user profile
print(f"\n{r.content}")