from dotenv import load_dotenv
import os, spotipy, requests, random, webbrowser, ctypes
from requests_oauthlib import OAuth2Session
from requests.auth import HTTPBasicAuth 
from spotipy.oauth2 import SpotifyOAuth
import tkinter as tk 
from tkinter import messagebox
import tkinter.font as tkFont
from PIL import Image, ImageTk

ctypes.windll.shcore.SetProcessDpiAwareness(1)

window = tk.Tk()
window.title("MUSIC MOOD APP")

window.geometry("1000x600")
window.configure(background="#faedd3")

canvas_section = tk.Canvas(window, width=1000, height=600, bg="#faedd3", highlightthickness=0)
canvas_section.pack(fill="both", expand=True)
canvas_section.create_rectangle(0, 0, 2000, 65, fill="#001c21")

dashboard_icon = "dashboard.png"
dash_image = Image.open(dashboard_icon)
dash_image = dash_image.resize((50,50))
dash_photo = ImageTk.PhotoImage(dash_image)

canvas_section.create_image(1800,10, image=dash_photo, anchor=tk.NW)

def showWelcomeScreen():
    clear_window()
    welcome_label = tk.Label(window, text = "WELCOME TO THE MUSIC MOOD APP.", foreground="black", background="#faedd3" ,font=("Helvetica", 16, "bold"))
    welcome_label.place(x=50, y=120)
    text_2 = tk.Label(window, text= "want to listen to some songs? or view your spotify details?", foreground="black", background="#faedd3" ,font=("Helvetica", 12))
    text_2.place(x=50, y=170)

def change_color_on_hover(button, enter_color, leave_color, enter_fg, leave_fg):
    button.bind("<Enter>", lambda e: button.config(background=enter_color, foreground=enter_fg))
    button.bind("<Leave>", lambda e: button.config(background=leave_color, foreground=leave_fg))

def show_loadScreen():
    loading_screen = tk.Label(window, text = "loading", font=("Helvetica", 12), background="#faedd3", foreground="black")
    loading_screen.place(x=50, y=300)
    window.after(1000, main)
    
    add_dots(loading_screen, 0)
    
def add_dots(label, count):
    if count < 3:
        label.config(text=label.cget("text") + ".")
        label.after(500, add_dots, label, count+1)
    else:
        window.after(1000, main)    #calling the main function after 1 sec

def clear_window():
    for widget in window.winfo_children():
        if widget != canvas_section:  #making sure not to clear/destroy canvas
            widget.destroy()
  
def check_url():
    redirect_url = redirect_response.get("1.0", tk.END).strip()
    if redirect_url.startswith("https://"):
        messagebox.showinfo("Success", "Valid URL")
    else:
        messagebox.showerror("Error", "Invalid URL format. Ensure the URL starts with 'https://'.")
                
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
        self.redirect_url = "https://oauth.pstmn.io/v1/browser-callback"
        self.authorization_base_url = "https://accounts.spotify.com/authorize"
        self.spotify = OAuth2Session(self.client_id, scope=[], redirect_uri=self.redirect_url)

    def autheticate_user(self):
        auth_url, _ = self.spotify.authorization_url(self.authorization_base_url, prompt='login')
        login_text = tk.Label(window, text = "\nVisit this URL to login: ", font=("Helvetica", 13, "bold"), foreground="black", bg="#faedd3")
        login_text.place(x=50, y=380)
        
        login_link = tk.Label(
            window,
            text=auth_url,
            font=("Italic", 11),
            fg="blue",
            cursor="hand2",
            wraplength= 1500,
            bg="#faedd3"
            ) 
        login_link.place(x=350, y=405)
        
        login_link.bind("<Button-1>", lambda event: webbrowser.open(auth_url))
        
        entry = tk.Label(window, text ="\nPaste the redirect URL here: ", font=("Helvetica", 13, "bold"), fg="black", bg="#faedd3")
        entry.place(x=50, y= 460)
                
        #creating a Text widget for multiline input and fr single , use "Entry"
        self.redirect_response = tk.Text(window, width = 50, height = 2)
        self.redirect_response.place(x=200, y=100)
                
        submit_button = tk.Button(
            window,
            text="Submit",
            command= lambda: check_url
            )
        submit_button.place(x=250, y=150)

        
    # def loading_dots(self, label, count):
    #     if count < 6:
    #         dots = '.' * (count % 4)
    #         label.config(text=f"Logging in{dots}")
    #         count +=1
    #         label.after(500, self.loading_dots, label, count)  #updating every 0.5 secs
        
    #     else:
    #         label.config(text= "Successfully Logged in", fg="green")
 
    def fetchingAccessToken(self):
        if self.redirect_response:
            token_url = "https://accounts.spotify.com/api/token"
            auth = HTTPBasicAuth(self.client_id, self.client_secret)
            self.token_info = self.spotify.fetch_token(token_url, auth=auth, authorization_response=self.redirect_response)
        else:
            raise ValueError(f"\033[31mError: Token not found\033[0m")

        if self.token_info:
            return self.token_info['access_token']
        else:
            raise ValueError(f"\033[31mError: No token has been fetched. Please Login...\033[0m")

class PlaylistRecommendation:
    def __init__(self, client_id, client_secret, access_token):
        self.access_token = access_token
        self.client_id = client_id
        self.client_secret = client_secret
        self.genres = [
            "pop", "folk", "chill", "ambient", "dance", "study", "metal", "workout", "rock", "hiphop" 
        ]

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
        
        genre = self.mood_to_genre.get(self.selected_mood, None)

        if genre is None or genre not in self.genres:
            raise ValueError(f"\033[31mError: No genre mapped for the mood: {self.selected_mood}\033[0m")

        offset = random.randint(0, 100)
        search_url = f"https://api.spotify.com/v1/search"
        params = {
            "q": f"genre: {genre}",
            "type": "track",
            "limit": 10,
            "offset": offset
        }
        headers = {"Authorization": f"Bearer {self.access_token}"}

        try:
            response = requests.get(search_url, headers=headers, params=params)

            if response.status_code == 200:
                results= response.json()
                tracks = results.get('tracks', {}).get('items', [])

                if not tracks:
                    raise ValueError(f"\033[31mError: No tracks found for genre '{genre}'\033[0m")
                    
                print("\nHere are some tracks for your vibe:")
                for idx, track in enumerate(tracks):
                    print(f"{idx+1}. Track: \033[33m{track['name']}\033[0m by {track['artists'][0]['name']}, URL: \033[34m{track['external_urls']['spotify']}\033[0m")

            else:
                raise ValueError(f"\033[31mError fetching genres: {response.status_code}\033[0m")
            
        except requests.exceptions.RequestException as e:
            raise ValueError(f"\033[31mError with request: {e}\033[0m")
        
        while True:
            try:
                option = input("\nType:\n\"C\" to get more recommendations \n\"E\" to exit \n\"M\" to change mood \n\"S\" to view your Spotify details:\n").upper()
                        
                if option == "C":
                    print("\nGetting more recommendations")
                    # for _ in range(4):
                    #     time.sleep(0.5)
                    #     print(".", end="",flush=True)
                    # print()
                    # self.getPublicRecommendations()

                # elif option == "S":
                #     user_det = UserSpotifyDetails(client_id, client_secret)
                #     user_det.userOptions()
                #     user_det.userChooseOption()

                # elif option == "E":
                #     print("\nExiting the program")
                #     for _ in range(4):
                #         time.sleep(0.5)
                #         print(".", end="",flush=True)
                #     print()
                #     exit()

                elif option == "M":
                    self.enterMood()
                    self.getPublicRecommendations()
                else:
                    print(f"\033[31mIncorrect option.\033[0m")
            except Exception as e:
                print(f"\033[31m{e}\033[0m")

class UserSpotifyDetails:
    def __init__(self, client_id, client_secret):
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
            9: "Logout",
            10: "Find music by mood"
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
                elif self.user_op == 10:
                    ...
                    # user_rec = PlaylistRecommendation(client_id, client_secret, access_token)
                    # user_rec.enterMood()
                    # user_rec.getPublicRecommendations()
                    
                else:
                    print("Not an option. Enter a valid option")
                self.userOptions()
            except ValueError:
                print(f"\033[31mError: Invalid type \"str\" entered. Enter an int")

    def viewTopTracks(self):
        results = self.sp.current_user_top_tracks(limit=20)

        if results:
            print("\nFetching your top tracks...")
            for idx, track in enumerate(results['items']):
                print(f"{idx+1} Track: \033[33m{track['name']}\033[0m by {track['artists'][0]['name']}, URL: \033[34m{track['external_urls']['spotify']}\033[0m")
        else:
            print("User has no top tracks.")

    def viewArtistsFollowed(self):  
        try:
            print("\nFetching your artists followed...")
            results = self.sp.current_user_followed_artists()

            if results:
                for artist in results['artists']['items']:
                    print(f"{artist['name']}")
            else:
                print("User follows no artists.")
        except Exception as e:
            print(f"\033[31mAn Error occured while fetching followed artists {e}\033[0m")
                

    def viewRecentlyPlayed(self):
        try:
            print("\nFetching your recently played...")
            result = self.sp.current_user_recently_played(limit=1)

            if result['items']:
                tracks = result['items'][0]['track']
                print(f"Your recently played Track is: \033[33m{tracks['name']} by {tracks['artists'][0]['name']}\033[0m")
                
            else:
                print("No recent tracks played")
        except Exception as e:
            print(f"\033[31mAn Error occured while fetching followed artists {e}\033[0m")

    def usersTopArtists(self):
        try:
            print("\nFetching your top artists...")
            result = self.sp.current_user_top_artists()

            for idx, artist in enumerate(result['items']):
                print(f"{idx+1}. \033[33m{artist['name']}\033[0m")
        except Exception as e:
            print(f"\033[31mAn Error occured while fetching followed artists {e}\033[0m")

    def viewCurrentPlaylists(self):
        try:
            print("\nFetching your current playlists...")
            result = self.sp.current_user_playlists()

            for idx, playlist in enumerate(result['items']):
                print(f"{idx+1}. \033[33m{playlist['name']}\033[0m")
        except Exception as e:
            print(f"\033[31mAn Error occured while fetching followed artists {e}\033[0m")

    def viewSavedAlbums(self):
        try:
            print("\nFetching your liked albums...")
            result = self.sp.current_user_saved_albums()

            for album in result['items']:
                print(f"- \033[33m{album['album']['name']}\033[0m")
        except Exception as e:
            print(f"\033[31mAn Error occured while fetching followed artists {e}\033[0m")

    def viewSavedTracks(self):
        try:
            print("\nFetching your liked tracks...")
            result = self.sp.current_user_saved_tracks()

            if result:
                for idx, track in enumerate(result['items']):
                    print(f"{idx+1}. \033[33m{track['track']['name']}\033[0m by \033[34m{track['track']['artists'][0]['name']}\033[0m")
            else:
                print("User has no top tracks.")
        except Exception as e:
            print(f"\033[31mAn Error occured while fetching followed artists {e}\033[0m")

    def viewCurrentlyPlaying(self):
        try:
            print("\nFetching your currently playing track...")
            current_playing = self.sp.currently_playing()
            
            if current_playing and current_playing['is_playing']:
                print(f"Currently playing: \033[33m{current_playing['item']['name']}\033[0m by \033[34m{current_playing['item']['artists'][0]['name']}\033[0m")
            else:
                print(f"\033[33mNo track is currently playing.\033[0m")
        except Exception as e:
            print(f"\033[31mAn Error occured while fetching followed artists {e}\033[0m")

def logout():
    cache_path = ".cache"
    if os.path.exists(cache_path):
        os.remove(cache_path)
        print("\nLogging out")
        # for _ in range(4):
        #     time.sleep(0.5)
        #     print(".", end="",flush=True)
        # print()
        # print(f"\033[32mSuccessfully logged out\033[0m")
        # exit()
    else:
        print(f"\n\033[31mNo account has been logged in. Please login to continue.\033[0m")

def main():
    load_dotenv()
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")

    if not client_id or not client_secret:
        print("MISSING CLIENT_ID OR CLIENT_SECRET")
        exit()

    credentials = Login(client_id, client_secret)
    credentials.autheticate_user()
    access_token = credentials.fetchingAccessToken()

    choice = UserOptions()
    op = choice.get_option()

    if op == 1:
        recommend = PlaylistRecommendation(client_id,client_secret, access_token)
        recommend.enterMood()
        recommend.getPublicRecommendations()

    elif op == 2:
        user_datails = UserSpotifyDetails(client_id, client_secret)
        user_datails.userOptions()
        user_datails.userChooseOption()
   

showWelcomeScreen() 
get_started_button = tk.Button(window, text="Get Started!", command=show_loadScreen, font=("Helvetica", 14), foreground= "white", background="#001c21", cursor="hand2")
get_started_button.place(x=50, y=230)    
change_color_on_hover(get_started_button, enter_color="#001215", leave_color="#001c21", enter_fg="white", leave_fg="white")    

window.mainloop()
