from dotenv import load_dotenv
import os, spotipy, requests
from requests_oauthlib import OAuth2Session
from requests.auth import HTTPBasicAuth 

class UserOptions:
    def __init__(self):
        pass

class Credentials:
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret

    def loadCredentials(self):
        load_dotenv()
        self.client_id = os.getenv("CLIENT_ID")
        self.client_secret = os.getenv("CLIENT_SECRET")
        self.redirect_url = "https://oauth.pstmn.io/v1/browser-callback"

        self.authorization_base_url = "https://accounts.spotify.com/authorize"
        self.token_url = "https://accounts.spotify.com/api/token"

        self.scope = ["user-top-read"]

    def authorization(self):
        self.spotify = OAuth2Session(self.client_id, scope=self.scope, redirect_uri=self.redirect_url)
        authorization_url, _ = self.spotify.authorization_url(self.authorization_base_url, prompt='login')
        print(f"Please visit here and login: {authorization_url}")

        self.redirect_response = input("Please paste the redirect URL here: ")

    def fetchingAccessToken(self):
        auth = HTTPBasicAuth(self.client_id, self.client_secret)
        token_info = self.spotify.fetch_token(self.token_url, auth=auth, authorization_response=self.redirect_response)
        token = token_info['access_token']

        top_tracks_url = "https://api.spotify.com/v1/me/top/tracks"
        headers = {
            "Authorization": f"Bearer: {token}"
        }
        self.response = requests.get(top_tracks_url, headers=headers)

class TopTracks(Credentials):
    def __init__(self, client_id, client_secret):
        super().__init__(client_id, client_secret)
    

