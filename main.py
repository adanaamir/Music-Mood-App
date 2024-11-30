from dotenv import load_dotenv
import os, spotipy, requests, time
from requests_oauthlib import OAuth2Session
from requests.auth import HTTPBasicAuth 
from spotipy.oauth2 import SpotifyOAuth

class UserOptions:
    def __init__(self):
        self.op = None

    def get_option(self):
        print("1. Find Music by Mood\n2. Explore your Spotify Data")
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

class Login:
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

        print(f"\nLogging in")
        for _ in range(3):
            time.sleep(0.5)
            print(".", end="",flush=True)
        print()
        print("\033[32mSuccessfully Logged in\033[0m")
 
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
    def __init__(self, client_id, client_secret,response=None):
        self.client_id = client_id
        self.client_secret = client_secret
        self.response = response
        self.red = "\033[31m"
        self.blue = "\033[34m"
        self.reset = "\033[0m"
        self.yellow = "\033[33m"

        self.mood_to_genre = {
            "Happy": "pop",
            "Sad": "folk",
            "Chill": "chill",
            "Peaceful": "ambient",
            "Energetic": "dance",
            "Focused": "study",
            "Angry": "metal",
            "Motivational": "workout"
        }

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
        print(f"\n{self.yellow}What's your vibe today? We've got the music for it.{self.reset}")
        for key, val in self.moods.items():
            print(f"{key} - {val}")
        while True:
            self.op = input("Select your mood by number(1-8): ")
            if self.op in self.moods:
                self.selected_mood = self.moods[self.op]
                print(f"\nFeeling {self.selected_mood}? Lets find the perfect tracks!")
                break
            else:
                print(f"{self.red}Enter a valid option{self.reset}")

    def recommendationsLoop(self, fetch_results):
        while True:
            results = fetch_results()
            print()
            
            for idx, track in enumerate(results['tracks']):
                print(f"{idx+1} Track: {self.yellow}{track['name']}{self.reset} by {track['artists'][0]['name']}, URL: {self.blue}{track['external_urls']['spotify']}{self.reset}")

            try:
                option = input("\nType:\n\"C\" to get more recomendations \n\"E\" to exit \n\"L\" login to spotify: ").upper()
                
                if option == "C":
                    print("\nGetting more recommendations")
                    for _ in range(3):
                        time.sleep(0.5)
                        print(".", end="", flush=True)
                    print()
                    continue

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

    # def displayRecommendations(self, no_login=False):
    #     if no_login:
    #         self.getPublicRecommendations()
    #     else:
    #         self.getPersonalizedRecommendations()

    def getPublicRecommendations(self):
        self.genre = self.mood_to_genre[self.selected_mood]
    
        self.sp = spotipy.Spotify(client_credentials_manager=spotipy.oauth2.SpotifyClientCredentials(client_id=self.client_id, client_secret=self.client_secret))
        # print(self.sp.recommendation_genre_seeds())
        
        # available_genres = self.sp.recommendation_genre_seeds()
        # if self.genre not in available_genres['genres']:
        #     raise ValueError(f"Genre '{self.genre}' is not valid. Choose from {available_genres['genres']}")
        
        def fetch_results():
            return self.sp.recommendations(seed_genres=[self.genre], limit=10)
        
        self.recommendationsLoop(fetch_results)
    

    # def getPersonalizedRecommendations(self):
    #     redirect_url = "https://oauth.pstmn.io/v1/browser-callback"
    #     scope = "playlist-read-private"
    #     self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_url ,scope=scope))  
    #     self.genre = self.mood_to_genre[self.selected_mood]
        
    #     def fetch_results():
    #         return self.sp.recommendations(seed_genres=[self.genre], limit=10)
        
    #     self.recommendationsLoop(fetch_results)

class UserSpotifyDetails:
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.red = "\033[31m"
        self.blue = "\033[34m"
        self.reset = "\033[0m"
        self.yellow = "\033[33m"
        self.redirect_url = "https://oauth.pstmn.io/v1/browser-callback" 
        self.scope = (
            "user-top-read "
            "user-follow-read "
            "playlist-read-private "
            "user-read-recently-played "
            "user-library-read "
            "user-read-playback-state"
            )
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=self.client_id, client_secret=self.client_secret, redirect_uri=self.redirect_url, scope=self.scope))

    def userOptions(self):
        user_options = {
            1: "View your top tracks.",
            2: "View your currently followed artist.",
            3: "View your recently played.", 
            4: "View your top artists.",
            5: "View your current playlists.",
            6: "View your saved albums.",
            7: "View your liked tracks.", 
            8: "View currently playing.",
            9: "Logout"
        }
        print(f"\n{self.yellow}Hi! Ready to explore your Spotify Data?\nHere's what you can do:{self.reset}")
        for key, val in user_options.items():
            print(f"{key} - {val}")

        while True:
            try:
                self.user_op = int(input("Enter your option by number(1-10) "))
                if self.user_op in user_options:
                    break
                else:
                    print(f"{self.red}Error: Not an option.{self.reset}") 
            except ValueError:
                print(f"{self.red}Error: Invalid type \"str\" entered. Enter an int{self.reset}")
    
    def userChooseOption(self):
        while True:
            try:
                if self.user_op == 1:
                    self.viewTopTracks()
                    
                elif self.user_op == 2:
                    self.viewArtistsFollowed()
                    
                elif self.user_op == 3:
                    self.viewRecentlyPlayed()
                    
                elif self.user_op == 4:
                    self.usersTopArtists()

                elif self.user_op == 5:
                    self.viewCurrentPlaylists()

                elif self.user_op == 6:
                    self.viewSavedAlbums()

                elif self.user_op == 7:
                    self.viewSavedTracks()

                elif self.user_op == 8:
                    self.viewCurrentlyPlaying()
                elif self.user_op == 9:
                    logout()
                else:
                    print("Not an option. Enter a valid option")
                self.userOptions()
            except ValueError:
                print(f"{self.red}Error: Invalid type \"str\" entered. Enter an int")

    def viewTopTracks(self):
        results = self.sp.current_user_top_tracks(limit=20)
        print("\nFetching your top tracks")
        for _ in range(4):
            time.sleep(0.5)
            print(".", end="", flush=True)
        print()

        for idx, track in enumerate(results['items']):
            print(f"{idx+1} Track: {self.yellow}{track['name']}{self.reset} by {track['artists'][0]['name']}, URL: {self.blue}{track['external_urls']['spotify']}{self.reset}")

    def viewArtistsFollowed(self):  
        try:
            print("\nFetching your artists followed")
            results = self.sp.current_user_followed_artists()
            for _ in range(4):
                time.sleep(0.5)
                print(".", end="", flush=True)
            print()

            for artist in results['artists']['items']:
                print(f"{artist['name']}")
        except Exception as e:
            print(f"{self.red}An Error occured while fetching followed artists {e}{self.reset}")

    def viewRecentlyPlayed(self):
        try:
            print("\nFetching your recently played")
            result = self.sp.current_user_recently_played(limit=1)
            
            for _ in range(4):
                time.sleep(0.5)
                print(".", end="", flush=True)
            print()

            if result['items']:
                tracks = result['items'][0]['track']
                print(f"Your recently played Track is: {self.yellow}{tracks['name']} by {tracks['artists'][0]['name']}{self.reset}")
                
            else:
                print("No recent tracks played")
        except Exception as e:
            print(f"{self.red}An Error occured while fetching followed artists {e}{self.reset}")

    def usersTopArtists(self):
        try:
            print("\nFetching your top artists")
            result = self.sp.current_user_top_artists()
            for _ in range(4):
                time.sleep(0.5)
                print(".", end="", flush=True)
            print()

            for idx, artist in enumerate(result['items']):
                print(f"{idx+1}. {self.yellow}{artist['name']}{self.reset}")
        except Exception as e:
            print(f"{self.red}An Error occured while fetching followed artists {e}{self.reset}")

    def viewCurrentPlaylists(self):
        try:
            print("\nFetching your current playlists")
            result = self.sp.current_user_playlists()
            for _ in range(4):
                time.sleep(0.5)
                print(".", end="", flush=True)
            print()

            for idx, playlist in enumerate(result['items']):
                print(f"{idx+1}. {self.yellow}{playlist['name']}{self.reset}")
        except Exception as e:
            print(f"{self.red}An Error occured while fetching followed artists {e}{self.reset}")

    def viewSavedAlbums(self):
        try:
            print("\nFetching your liked albums")
            result = self.sp.current_user_saved_albums()
            for _ in range(4):
                time.sleep(0.5)
                print(".", end="", flush=True)
            print()

            for album in result['items']:
                print(f"- {self.yellow}{album['album']['name']}{self.reset}")
        except Exception as e:
            print(f"{self.red}An Error occured while fetching followed artists {e}{self.reset}")

    def viewSavedTracks(self):
        try:
            print("\nFetching your liked tracks")
            result = self.sp.current_user_saved_tracks()
            for _ in range(4):
                time.sleep(0.5)
                print(".", end="", flush=True)
            print()

            for idx, track in enumerate(result['items']):
                print(f"{idx+1}. {self.yellow}{track['track']['name']}{self.reset} by {self.blue}{track['track']['artists'][0]['name']}{self.reset}")
        except Exception as e:
            print(f"{self.red}An Error occured while fetching followed artists {e}{self.reset}")

    def viewCurrentlyPlaying(self):
        try:
            print("\nFetching your liked tracks")
            current_playing = self.sp.currently_playing()
            for _ in range(4):
                time.sleep(0.5)
                print(".", end="", flush=True)
            print()
            
            if current_playing and current_playing['is_playing']:
                print(f"Currently playing: {self.yellow}{current_playing['item']['name']}{self.reset} by {self.blue}{current_playing['item']['artists'][0]['name']}{self.reset}")
            else:
                print(f"{self.yellow}No track is currently playing.{self.reset}")
        except Exception as e:
            print(f"{self.red}An Error occured while fetching followed artists {e}{self.reset}")

def logout():
    cache_path = ".cache"
    if os.path.exists(".cache"):
        os.remove(cache_path)
        print("\nLogging out")
        for _ in range(4):
            time.sleep(0.5)
            print(".", end="",flush=True)
        print()
        print(f"\033[32mSuccessfully logged out\033[0m")
        exit()
    else:
        print("\n\033[33mNo account has been logged in. Please login to continue.\033[0m")

    # choice = UserOptions()
    # op = choice.get_option()


if __name__ == "__main__":
    load_dotenv()
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")

    if not client_id or not client_secret:
        print("MISSING CLIENT_ID OR CLIENT_SECRET")
        exit()

    choice = UserOptions()
    op = choice.get_option()

    if op == 1:
        recommend = PlaylistRecommendation(client_id,client_secret)
        recommend.enterMood()
        # recommend.displayRecommendations()
        recommend.getPublicRecommendations()

    elif op == 2:
        credentials = Login(client_id, client_secret)
        response = credentials.fetchingAccessToken()
        user_datails = UserSpotifyDetails(client_id, client_secret)
        user_datails.userOptions()
        user_datails.userChooseOption()
