from dotenv import load_dotenv
import os, spotipy, requests, time
from requests_oauthlib import OAuth2Session
from requests.auth import HTTPBasicAuth 
from spotipy.oauth2 import SpotifyOAuth

class UserOptions:
    def __init__(self):
        self.op = None

    def get_option(self):
        print("1. Get playlists recommended according to the mood entered\n2. Log-in to your spotify to get your top tracks displayed")
        while True:
            try:
                self.op = int(input("Please enter any option(1/2): "))
                if self.op in [1,2]:
                    break
                else:
                    print("Not an option. Enter a correct option(1/2)")
            except ValueError:   
                print("Incorrect \nType: \"str\" entered. Enter an int.")
        return self.op

class Credentials:
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret 
        blue = "\033[34m"
        self.reset = "\033[0m"  
        self.red = "\033[31m" 
        redirect_url = "https://oauth.pstmn.io/v1/browser-callback"
        authorization_base_url = "https://accounts.spotify.com/authorize"
        scope = ["user-top-read"]

        self.spotify = OAuth2Session(self.client_id, scope=scope, redirect_uri=redirect_url)
        authorization_url, _ = self.spotify.authorization_url(authorization_base_url, prompt='login')
        print(f"\nVisit here and login: {blue}{authorization_url}{self.reset}")

        while True: 
            try:
                self.redirect_response = input("\nPaste the redirect URL here: ")  
                if self.redirect_response.startswith("https://"):
                    break
                else:
                    print("Incorrect URL format")
            except ValueError:
                print("Invalid URL format. Ensure the url starts with \"https://\"")
 
    def fetchingAccessToken(self):
        token_url = "https://accounts.spotify.com/api/token"
        top_tracks_url = "https://api.spotify.com/v1/me/top/tracks"

        auth = HTTPBasicAuth(self.client_id, self.client_secret)
        token_info = self.spotify.fetch_token(token_url, auth=auth, authorization_response=self.redirect_response)
        token = token_info['access_token']

        headers = {
            "Authorization": f"Bearer {token}"
        }
        response = requests.get(top_tracks_url, headers=headers)

        if response.status_code != 200:
            print(f"Error: {self.red}{response.status_code} - {response.text}{self.reset}")
            exit()
        
        return response

class PlaylistRecommendation:
    def __init__(self, client_id, client_secret, response):
        self.client_id = client_id
        self.client_secret = client_secret
        self.response = response
        self.red = "\033[31m"
        self.blue = "\033[34m"
        self.reset = "\033[0m"
        self.yellow = "\033[33m"

    def enterMood(self):
        self.moods = {
            "1" : "Happy",
            "2" : "Sad",
            "3" : "Chill",
            "4" : "Peaceful", 
            "5" : "Energetic",
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
                self.selected_mood = self.moods[self.op]
                print(f"\nYour entered mood: {self.selected_mood}")
                break
            else:
                print(f"{self.red}Enter a valid option{self.reset}")

    def authorization(self):
        if os.path.exists(".cache"):
            os.remove(".cache")

        redirect_url = "https://oauth.pstmn.io/v1/browser-callback"
        scope = "playlist-read-private"

        mood_to_genre = {
            "Happy": "pop",
            "Sad": "acoustic",
            "Chill": "chill",
            "Peaceful": "ambient",
            "Energetic": "dance",
            "Focused": "study",
            "Angry": "metal",
            "Motivational": "work-out"
        }
        self.genre = mood_to_genre[self.selected_mood]

        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_url ,scope=scope))
        
        print("\nFetching recommended playlists") 
        for _ in range(3):
            time.sleep(0.5)
            print(".", end="", flush=True)
        print()

    def displayRecommendations(self):
        while True:
            results = self.sp.recommendations(seed_genres=[self.genre],limit=10)
            print()
            
            for idx, track in enumerate(results['tracks']):
                print(f"{idx+1} Track: {self.yellow}{track['name']}{self.reset} by {track['artists'][0]['name']}, URL: {self.blue}{track['external_urls']['spotify']}{self.reset}")

            try:
                option = input("\nType:\n\"C\" to get more recomendations \n\"E\" to exit \n\"L\" login to spotify: ").upper()
                
                if option == "C":
                    print("\nFetching more recommendtions")
                    for _ in range(3):
                        time.sleep(0.5)
                        print(".", end="", flush=True)
                    print()
                    continue
                    
                elif option == "L":
                    if self.response is None:
                        print("\nGetting the URL for log-in")
                        for _ in range(4):
                            time.sleep(0.5)
                            print(".", end="", flush=True)
                        print()
                        credentials = Credentials(self.client_id, self.client_secret)
                        self.response = credentials.fetchingAccessToken()

                    if self.response:
                        top_track = TopTracks(self.response)
                        top_track.displayTopTracks()
                        break
                    else:
                        print(f"{self.red}Error: Unable to fetch response{self.reset}")
                        break

                elif option == "E":
                    print("\nExiting the program", end="", flush=True)
                    for _ in range(3):
                        time.sleep(0.5)
                        print(".", end="", flush=True)
                    print()
                    exit()
                else:
                    print(f"{self.red}Incorrect option.{self.reset}")
            except ValueError:
                print("Incorrect \nType: \"int\" entered. Enter a str.")

class TopTracks:
    def __init__(self,response):
        self.response = response
        self.red = "\033[31m"
        self.blue = "\033[34m"
        self.reset = "\033[0m"
        self.yellow = "\033[33m"

        if response.status_code != 200:
            print(f"\n{self.red}Error: {response.status_code} - {response.text}{self.reset}")
            exit()
        try:
            self.top_tracks = self.response.json()
        except requests.exceptions.JSONDecodeError:
            print(f"\n{self.red}Error: Failed to decode the JSON response - {response.text}{self.reset}")
            exit()

    def displayTopTracks(self):
        while True:
            print("\nFetching user's top tracks", end="", flush=True)
            for _ in range(3):
                time.sleep(0.5)
                print(".", end="" ,flush=True)
            print()

            if not self.top_tracks.get('items', []):
                print("No data was found")
                exit()

            for idx, track in enumerate(self.top_tracks['items']):
                print(f"{idx+1}. {self.yellow}Track Name: {track['name']}{self.reset} Artist Name: {track['artists'][0]['name']}")

            try: 
                option = input("\nType:\n\"C\" to get more recomendations \n\"E\" to exit \n\"M\" enter mood: ").upper()
                if option == "C":
                    print("\nFetching more recommendtions")
                    for _ in range(3):
                        time.sleep(0.5)
                        print(".", end="", flush=True)
                    print()
                    continue
                
                elif option == "M":
                    playlist_recommendation = PlaylistRecommendation(client_id, client_secret,response)
                    print()
                    playlist_recommendation.enterMood()
                    playlist_recommendation.authorization()
                    playlist_recommendation.displayRecommendations()
                    break

                elif option == "E":
                    print("\nExiting the program", end="", flush=True)
                    for _ in range(3):
                        time.sleep(0.5)
                        print(".", end="", flush=True)
                    print()
                    exit()    
                else:
                    print("Invalid option.")
            except ValueError:
                    print("Incorrect \nType: \"int\" entered. Enter a str.")

if __name__ == "__main__":
    load_dotenv()
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")

    if not client_id or not client_secret:
        print("MISSING CLIENT_ID OR CLIENT_SECRET")
        exit()

    response = None    
    choice = UserOptions()
    op = choice.get_option()

    if op == 1:
        recommend = PlaylistRecommendation(client_id, client_secret, response)
        recommend.enterMood()
        recommend.authorization()
        recommend.displayRecommendations()

    elif op == 2:
        credentials = Credentials(client_id, client_secret)
        response = credentials.fetchingAccessToken()
        print("r2", response)
        top_tracks = TopTracks(response)
        top_tracks.displayTopTracks()