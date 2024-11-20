from dotenv import load_dotenv
import os, spotipy, requests
from requests_oauthlib import OAuth2Session
from requests.auth import HTTPBasicAuth 
from spotipy.oauth2 import SpotifyOAuth

class UserOptions:
    def __init__(self):
        print("1. Get playlists recommended according to the mood entered\n2. Log-in to your spotify to get your top tracks displayed")
        while True:
            try:          
                self.op = int(input("Please enter any option(1/2): "))
                if self.op == 1:
                    PlaylistRecommendation
                    break
                elif self.op == 2:
                    Credentials
                    break
                else:
                    print("Not an option. Enter a correct option")
            except ValueError:   #its always better to add ths in loop so it keeps prompting incase of incorrect response 
                print("Incorrect type: \"str\" entered. Enter an int.")

class Credentials:
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret

    def URLS(self):     
        self.redirect_url = "https://oauth.pstmn.io/v1/browser-callback"

        self.authorization_base_url = "https://accounts.spotify.com/authorize"
        self.token_url = "https://accounts.spotify.com/api/token"

        self.scope = ["user-top-read"]

    def authorization(self):
        self.spotify = OAuth2Session(self.client_id, scope=self.scope, redirect_uri=self.redirect_url)
        authorization_url, _ = self.spotify.authorization_url(self.authorization_base_url, prompt='login')
        print(f"\nVisit here and login: {authorization_url}")

        while True:  #error
            try: 
                self.redirect_response = input("\nPaste the redirect URL here: ")  
                break
            except ValueError:
                print("Invalid URL format.")  #

    def fetchingAccessToken(self):
        auth = HTTPBasicAuth(self.client_id, self.client_secret)
        token_info = self.spotify.fetch_token(self.token_url, auth=auth, authorization_response=self.redirect_response)
        token = token_info['access_token']

        top_tracks_url = "https://api.spotify.com/v1/me/top/tracks"
        headers = {
            "Authorization": f"Bearer {token}"
        }
        self.response = requests.get(top_tracks_url, headers=headers)

        if self.response.status_code != 200:
            print(f"Error: {self.response.status_code} - {self.response.text}")
            exit()

class PlaylistRecommendation(Credentials):
    def __init__(self, client_id, client_secret):
        super().__init__(client_id, client_secret)
        self.op = None

    def enterMood(self):
        self.moods = {
            "1" : "Happy",
            "2" : "Sad",
            "3" : "Chill",
            "4" : "Peaceful", 
            "5" : "Energetic/Upbeat",
            "6" : "Focused",
            "7" : "Angry",
            "8" : "Motivational" 
        }
        print(f"Select a mood by number")
        for key, val in self.moods.items():
            print(f"{key} - {val}")
        while True:
            self.op = input("Enter mood choice(1-8): ")
            if self.op in self.moods:
                print(f"\nYour entered mood: {self.moods[self.op]}\n")
                break
            else:
                print("Enter a valid option")

    def authorization(self):
        if os.path.exists(".cache"):
            os.remove(".cache")

        self.redirect_url = "https://oauth.pstmn.io/v1/browser-callback"
        self.scope = "playlist-read-private" 

        mood_to_genre = {
            "Happy": "pop",
            "Sad": "acoustic",
            "Chill": "chill",
            "Peaceful": "ambient",
            "Energetic/Upbeat": "dance",
            "Focused": "focus",
            "Angry": "metal",
            "Motivational": "work-out"
        }
        selected_mood = self.moods[self.op]
        genre = mood_to_genre[selected_mood]

        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=self.redirect_url ,scope=self.scope))
        results = sp.recommendations(seed_genres=[genre],limit=10)

        for idx, track in enumerate(results['tracks']):
            print(f"{idx+1} Track: {track['name']} by {track['artists'][0]['name']}, URL: {track['external_urls']['spotify']}")

class TopTracks(Credentials):
    def __init__(self, client_id, client_secret,response):
        super().__init__(client_id, client_secret)
        self.response = response

        if self.response.status_code != 200:
            print(f"\nError: {self.response.status_code} - {self.response.text}")
            exit()
        try:
            self.top_tracks = self.response.json()
        except requests.exceptions.JSONDecodeError:
            print(f"\nError: Failed to decode the JSON response - {self.response.text}")
            exit()
    
    def displayTopTracks(self):
        print("\nFetching user's top tracks...\n")

        for idx, track in enumerate(self.top_tracks['items']):
            print(f"{idx+1}. Track Name: {track['name']} Artist Name: {track['artists'][0]['name']}")

        if not self.top_tracks.get('items', []):
            print("No data was found")
            exit()


load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

op = UserOptions()

recommend = PlaylistRecommendation(client_id, client_secret)
recommend.enterMood()
recommend.authorization()

credentials = Credentials(client_id, client_secret)
credentials.URLS()
credentials.authorization()
credentials.fetchingAccessToken()

top_tracks = TopTracks(client_id, client_secret, credentials.response)
top_tracks.displayTopTracks()

