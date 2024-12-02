from dotenv import load_dotenv
import os, spotipy, time
from requests_oauthlib import OAuth2Session
from requests.auth import HTTPBasicAuth 
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials

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

class Login:
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret 
        redirect_url = "https://oauth.pstmn.io/v1/browser-callback"
        authorization_base_url = "https://accounts.spotify.com/authorize"
        scope = []

        self.spotify = OAuth2Session(self.client_id, scope=scope, redirect_uri=redirect_url)
        authorization_url, _ = self.spotify.authorization_url(authorization_base_url, prompt='login')
        print(f"\nVisit here and login: \033[34m{authorization_url}\033[0m")

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

        auth = HTTPBasicAuth(self.client_id, self.client_secret)
        token_info = self.spotify.fetch_token(token_url, auth=auth, authorization_response=self.redirect_response)
        return token_info['access_token']

class PlaylistRecommendation:
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id, client_secret))
        try:
            available_genres = self.sp.recommendations_available_genre_seeds()['genres']
            print(f"Available genres: {available_genres}")
        except Exception as e:
            print(f"\033[31m{e}\033[0m")

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
        self.selected_mood = None

    def enterMood(self):
        moods = {
            "1" : "Happy",
            "2" : "Sad",
            "3" : "Chill",
            "4" : "Peaceful", 
            "5" : "Energetic",
            "6" : "Focused",
            "7" : "Angry",
            "8" : "Motivational" 
        }
        print(f"\n\033[33mWhat's your vibe today? We've got the music for it.\033[0m")
        for key, val in moods.items():
            print(f"{key} - {val}")
        while True:
            self.op = input("Select your mood by number(1-8): ")
            if self.op in moods:
                self.selected_mood = moods[self.op]
                print(f"\nFeeling \033[33m{self.selected_mood}\033[0m? Lets find the perfect tracks!")
                break
            else:
                print(f"\033[31mEnter a valid option\033[0m")
        
    def getPublicRecommendations(self):
        if self.selected_mood is None:
            raise ValueError(f"\033[31mError: No mood selected\033[0m")
        
        genre = self.mood_to_genre[self.selected_mood]
        
        available_genres = self.sp.recommendations_available_genre_seeds()['genres']
        print(f"Available genres: {available_genres}")

        if genre not in available_genres:
            raise ValueError(f"\033[31mGenre '{genre}' is not valid. Choose from {available_genres}\033[0m")
        try:
            results = self.sp.recommendations(seed_genres=[genre], limit=10)
            if 'tracks' not in results:
                raise ValueError(f"\033[31mError: No tracks found for genre '{genre}'\033[0m")
        
            print("\nHere are some tracks for your vibe:")
            while True:
                for idx, track in enumerate(results['tracks']):
                    print(f"{idx+1} Track: \033[33m{track['name']}\033[0m by {track['artists'][0]['name']}, URL: \033[34m{track['external_urls']['spotify']}\033[0m")

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
                        print(f"\033[31mIncorrect option.\033[0m")
                except ValueError:
                    print("Incorrect \nType: \"int\" entered. Enter a str.")
        except Exception as e:
            print(f"\033[31m{e}\033[0m")

class UserSpotifyDetails:
    def __init__(self, client_id, client_secret):
        # self.sp = sp
        self.client_id = client_id
        self.client_secret = client_secret
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
        print(f"\n\033[33mHi! Ready to explore your Spotify Data?\nHere's what you can do:\033[0m")
        for key, val in user_options.items():
            print(f"{key} - {val}")

        while True:
            try:
                self.user_op = int(input("Enter your option by number(1-10) "))
                if self.user_op in user_options:
                    break
                else:
                    print(f"\033[31mError: Not an option.\033[0m") 
            except ValueError:
                print(f"\033[31mError: Invalid type \"str\" entered. Enter an int\033[0m")
    
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
                print(f"\033[31mError: Invalid type \"str\" entered. Enter an int")

    def viewTopTracks(self):
        results = self.sp.current_user_top_tracks(limit=20)
        print("\nFetching your top tracks")
        for _ in range(4):
            time.sleep(0.5)
            print(".", end="", flush=True)
        print()

        for idx, track in enumerate(results['items']):
            print(f"{idx+1} Track: \033[33m{track['name']}\033[0m by {track['artists'][0]['name']}, URL: \033[34m{track['external_urls']['spotify']}\033[0m")

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
            print(f"\033[31mAn Error occured while fetching followed artists {e}\033[0m")

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
                print(f"Your recently played Track is: \033[33m{tracks['name']} by {tracks['artists'][0]['name']}\033[0m")
                
            else:
                print("No recent tracks played")
        except Exception as e:
            print(f"\033[31mAn Error occured while fetching followed artists {e}\033[0m")

    def usersTopArtists(self):
        try:
            print("\nFetching your top artists")
            result = self.sp.current_user_top_artists()
            for _ in range(4):
                time.sleep(0.5)
                print(".", end="", flush=True)
            print()

            for idx, artist in enumerate(result['items']):
                print(f"{idx+1}. \033[33m{artist['name']}\033[0m")
        except Exception as e:
            print(f"\033[31mAn Error occured while fetching followed artists {e}\033[0m")

    def viewCurrentPlaylists(self):
        try:
            print("\nFetching your current playlists")
            result = self.sp.current_user_playlists()
            for _ in range(4):
                time.sleep(0.5)
                print(".", end="", flush=True)
            print()

            for idx, playlist in enumerate(result['items']):
                print(f"{idx+1}. \033[33m{playlist['name']}\033[0m")
        except Exception as e:
            print(f"\033[31mAn Error occured while fetching followed artists {e}\033[0m")

    def viewSavedAlbums(self):
        try:
            print("\nFetching your liked albums")
            result = self.sp.current_user_saved_albums()
            for _ in range(4):
                time.sleep(0.5)
                print(".", end="", flush=True)
            print()

            for album in result['items']:
                print(f"- \033[33m{album['album']['name']}\033[0m")
        except Exception as e:
            print(f"\033[31mAn Error occured while fetching followed artists {e}\033[0m")

    def viewSavedTracks(self):
        try:
            print("\nFetching your liked tracks")
            result = self.sp.current_user_saved_tracks()
            for _ in range(4):
                time.sleep(0.5)
                print(".", end="", flush=True)
            print()

            for idx, track in enumerate(result['items']):
                print(f"{idx+1}. \033[33m{track['track']['name']}\033[0m by \033[34m{track['track']['artists'][0]['name']}\033[0m")
        except Exception as e:
            print(f"\033[31mAn Error occured while fetching followed artists {e}\033[0m")

    def viewCurrentlyPlaying(self):
        try:
            print("\nFetching your currently playing track")
            current_playing = self.sp.currently_playing()
            for _ in range(4):
                time.sleep(0.5)
                print(".", end="", flush=True)
            print()
            
            if current_playing and current_playing['is_playing']:
                print(f"Currently playing: \033[33m{current_playing['item']['name']}\033[0m by \033[34m{current_playing['item']['artists'][0]['name']}\033[0m")
            else:
                print(f"\033[33mNo track is currently playing.\033[0m")
        except Exception as e:
            print(f"\033[31mAn Error occured while fetching followed artists {e}\033[0m")

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
        recommend.getPublicRecommendations()

    elif op == 2:
        credentials = Login(client_id, client_secret)
        access_token = credentials.fetchingAccessToken()
        user_datails = UserSpotifyDetails(client_id, client_secret)
        user_datails.userOptions()
        user_datails.userChooseOption()
