import os
import time
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from requests_oauthlib import OAuth2Session
from requests.auth import HTTPBasicAuth
import requests

# Helper Functions
def print_loading_message(message):
    """Helper to print a loading message with a delay."""
    print(message, end="")
    for _ in range(3):
        time.sleep(0.5)
        print(".", end="", flush=True)
    print()

# Classes
class UserOptions:
    def get_option(self):
        print("1. Find Music by Mood\n2. Explore your Spotify Data")
        while True:
            try:
                option = int(input("Please enter an option (1/2): "))
                if option in [1, 2]:
                    return option
                print("Not a valid option. Please enter 1 or 2.")
            except ValueError:
                print("Invalid input. Please enter a number.")

class Login:
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_url = "https://oauth.pstmn.io/v1/browser-callback"
        self.scope = ["user-top-read"]
        self.spotify = OAuth2Session(
            self.client_id, scope=self.scope, redirect_uri=self.redirect_url
        )
        self.auth_url, _ = self.spotify.authorization_url(
            "https://accounts.spotify.com/authorize", prompt="login"
        )

    def authenticate_user(self):
        print(f"Visit this URL to login: {self.auth_url}")
        redirect_response = input("\nPaste the redirect URL here: ")
        token_url = "https://accounts.spotify.com/api/token"
        try:
            token_info = self.spotify.fetch_token(
                token_url,
                auth=HTTPBasicAuth(self.client_id, self.client_secret),
                authorization_response=redirect_response,
            )
            print("\033[32mSuccessfully Logged In!\033[0m")
            return token_info
        except Exception as e:
            print(f"Error during authentication: {e}")
            exit()

class PlaylistRecommendation:
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.mood_to_genre = {
            "Happy": "pop",
            "Sad": "acoustic",
            "Chill": "chill",
            "Peaceful": "ambient",
            "Energetic": "dance",
            "Focused": "study",
            "Angry": "metal",
            "Motivational": "workout",
        }

    def get_user_mood(self):
        moods = {str(i): mood for i, mood in enumerate(self.mood_to_genre, 1)}
        print("What's your vibe today?")
        for key, mood in moods.items():
            print(f"{key}. {mood}")
        while True:
            choice = input("Select your mood by number: ")
            if choice in moods:
                return moods[choice]
            print("Invalid selection. Please choose a valid number.")

    def recommend_tracks(self, mood):
        genre = self.mood_to_genre.get(mood)
        sp = spotipy.Spotify(
            client_credentials_manager=spotipy.oauth2.SpotifyClientCredentials(
                client_id=self.client_id, client_secret=self.client_secret
            )
        )
        recommendations = sp.recommendations(seed_genres=[genre], limit=10)
        print(f"\nTracks for your mood ({mood}):")
        for idx, track in enumerate(recommendations["tracks"]):
            print(f"{idx+1}. {track['name']} by {track['artists'][0]['name']}")
            print(f"   URL: {track['external_urls']['spotify']}")

class UserSpotifyDetails:
    def __init__(self, sp):
        self.sp = sp

    def display_user_data(self):
        options = {
            1: self.view_top_tracks,
            2: self.view_followed_artists,
            3: self.view_recently_played,
        }
        print("1. View your top tracks\n2. View followed artists\n3. View recently played")
        while True:
            try:
                choice = int(input("Enter your choice: "))
                if choice in options:
                    options[choice]()
                    return
                print("Invalid choice. Try again.")
            except ValueError:
                print("Invalid input. Please enter a number.")

    def view_top_tracks(self):
        tracks = self.sp.current_user_top_tracks(limit=10)["items"]
        print("Your top tracks:")
        for idx, track in enumerate(tracks):
            print(f"{idx+1}. {track['name']} by {track['artists'][0]['name']}")

    def view_followed_artists(self):
        artists = self.sp.current_user_followed_artists()["artists"]["items"]
        print("Artists you follow:")
        for artist in artists:
            print(artist["name"])

    def view_recently_played(self):
        tracks = self.sp.current_user_recently_played(limit=10)["items"]
        print("Recently played tracks:")
        for track in tracks:
            print(f"{track['track']['name']} by {track['track']['artists'][0]['name']}")

# Main Program
if __name__ == "__main__":
    load_dotenv()
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")

    if not client_id or not client_secret:
        print("Missing CLIENT_ID or CLIENT_SECRET in environment variables.")
        exit()

    user_option = UserOptions().get_option()

    if user_option == 1:
        recommender = PlaylistRecommendation(client_id, client_secret)
        mood = recommender.get_user_mood()
        recommender.recommend_tracks(mood)
    elif user_option == 2:
        login = Login(client_id, client_secret)
        token_info = login.authenticate_user()
        sp = spotipy.Spotify(auth=token_info["access_token"])
        user_details = UserSpotifyDetails(sp)
        user_details.display_user_data()
