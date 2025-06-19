from dotenv import load_dotenv
from flask import Flask, request
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.animation import Animation
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.behaviors import ButtonBehavior
from requests_oauthlib import OAuth2Session
from requests.auth import HTTPBasicAuth 
from kivy.lang import Builder
from kivy.factory import Factory
from hoverbehaviour import HoverBehavior
import webbrowser, os, threading, time, random

#-----------------------------------flask for redirecting------------------------------------------------
app = Flask(__name__)
redirect_response_url = None

@app.route("/callback")
def callback():
    global redirect_response_url
    redirect_response_url = request.url
    # print(f"\033[32mReceived redirect:\033[0m {redirect_response_url}")
    return "Login successful! You can close this window and return to the app."

def run_Server():
    app.run(port=8080)
    
def start_server():
    thread = threading.Thread(target=run_Server)
    thread.daemon = True
    thread.start()

#-----------------------------------------------kivy app------------------------------------------------------
class MainApp(MDApp):
    def build(self):
        load_dotenv()
        start_server()

        client_id = os.getenv("CLIENT_ID")
        client_secret = os.getenv("CLIENT_SECRET")
        self.login = Login(client_id=client_id, client_secret=client_secret)
        self.login.authenticate_user()

        self.sm = self.load_ui()
        Window.bind(on_key_down=self.on_key_down)
        return self.sm

    def load_ui(self):
        Builder.unload_file("frontend.kv")
        return Builder.load_file("frontend.kv")  # returns a ScreenManager

    def on_key_down(self, window, key, scancode, codepoint, modifier):
        if codepoint == 'r':
            print("🔁 Reloading KV file...")

            # Unload and reload the KV file
            Builder.unload_file("frontend.kv")
            new_ui = Builder.load_file("frontend.kv")

            # Remove old screens
            self.sm.clear_widgets()

            # Recreate new screens by name using Factory (fresh instances)
            for screen in new_ui.screens:
                screen_class = Factory.get(screen.__class__.__name__)
                new_screen = screen_class(name=screen.name)
                self.sm.add_widget(new_screen)

            print("✅ Reloaded successfully!")


    def spotify_login(self):
        self.background_color = [1, 0, 0.498, 1]
        if self.login.auth_url:
            webbrowser.open(self.login.auth_url)
        else:
            print("not ready")
            
    def check_redirect(self):
        global redirect_response_url
        while not redirect_response_url:
            time.sleep(1)

        self.login.redirect_response = redirect_response_url
        try:
            token = self.login.fetchingAccessToken()
            self.root.current = "dashboard"
        except Exception as e:
            print(f"\033[31mError fetching token:\033[0m {e}")
            
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
        # all_moods = "\n".join(f"{key} - {val}" for key, val in moods.items()) 
        # self.selected_mood = moods[self.op]
        
        dashboard_screen = self.sm.get_screen("dashboard")
        dashboard_screen.ids.vibe_label.text = "What's your vibe today? We've got the music for it."
        
        # dashboard_screen = self.sm.get_screen("dashboard")
        # dashboard_screen.ids.mood_list.text = all_moods
        
        
        print(f"\nFeeling \033[33m{self.selected_mood}\033[0m? Lets find the perfect tracks!")

class Login:
    def __init__(self, client_id, client_secret):
        os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
        self.client_id = client_id
        self.client_secret = client_secret 
        self.redirect_url = "http://localhost:8080/callback"
        self.authorization_base_url = "https://accounts.spotify.com/authorize"
        self.spotify = OAuth2Session(self.client_id, scope=[], redirect_uri=self.redirect_url)
        self.auth_url = None
        self.redirect_response = None
        
    def authenticate_user(self):
        auth_url, _ = self.spotify.authorization_url(self.authorization_base_url, prompt='login')
        self.auth_url = auth_url
        return auth_url
    
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

        # for key, val in moods.items():
        #     print(f"{key} - {val}")
        # while True:
        #     self.op = input("Select your mood by number(1-8): ")
        #     if self.op in moods:
        #         self.selected_mood = moods[self.op]
        #         print(f"\nFeeling \033[33m{self.selected_mood}\033[0m? Lets find the perfect tracks!")
        #         break
        #     else:
        #         print(f"\033[31mEnter a valid option\033[0m")

    # def getPublicRecommendations(self):
    #     if self.selected_mood is None:
    #         raise ValueError(f"\033[31mError: No mood selected\033[0m")
        
    #     genre = self.mood_to_genre.get(self.selected_mood, None)

    #     if genre is None or genre not in self.genres:
    #         raise ValueError(f"\033[31mError: No genre mapped for the mood: {self.selected_mood}\033[0m")

    #     offset = random.randint(0, 100)
    #     search_url = f"https://api.spotify.com/v1/search"
    #     params = {
    #         "q": f"genre: {genre}",
    #         "type": "track",
    #         "limit": 10,
    #         "offset": offset
    #     }
    #     headers = {"Authorization": f"Bearer {self.access_token}"}

    #     try:
    #         response = requests.get(search_url, headers=headers, params=params)

    #         if response.status_code == 200:
    #             results= response.json()
    #             tracks = results.get('tracks', {}).get('items', [])

    #             if not tracks:
    #                 raise ValueError(f"\033[31mError: No tracks found for genre '{genre}'\033[0m")
                    
    #             print("\nHere are some tracks for your vibe:")
    #             for idx, track in enumerate(tracks):
    #                 print(f"{idx+1}. Track: \033[33m{track['name']}\033[0m by {track['artists'][0]['name']}, URL: \033[34m{track['external_urls']['spotify']}\033[0m")

    #         else:
    #             raise ValueError(f"\033[31mError fetching genres: {response.status_code}\033[0m")
            
    #     except requests.exceptions.RequestException as e:
    #         raise ValueError(f"\033[31mError with request: {e}\033[0m")
        
    #     while True:
    #         try:
    #             option = input("\nType:\n\"C\" to get more recommendations \n\"E\" to exit \n\"M\" to change mood \n\"S\" to view your Spotify details:\n").upper()
                        
    #             if option == "C":
    #                 print("\nGetting more recommendations")
    #                 for _ in range(4):
    #                     time.sleep(0.5)
    #                     print(".", end="",flush=True)
    #                 print()
    #                 self.getPublicRecommendations()

    #             elif option == "S":
    #                 user_det = UserSpotifyDetails(client_id, client_secret)
    #                 user_det.userOptions()
    #                 user_det.userChooseOption()

    #             elif option == "E":
    #                 print("\nExiting the program")
    #                 for _ in range(4):
    #                     time.sleep(0.5)
    #                     print(".", end="",flush=True)
    #                 print()
    #                 exit()

    #             elif option == "M":
    #                 self.enterMood()
    #                 self.getPublicRecommendations()
    #             else:
    #                 print(f"\033[31mIncorrect option.\033[0m")
    #         except Exception as e:
    #             print(f"\033[31m{e}\033[0m")


class Dashboard(Screen):
    pass
class Screen1(Screen):
    pass
class Screen2(Screen):
    pass
class Screen3(Screen):
    pass

class WindowManager(ScreenManager):
    pass
    
class HoverButton(Button, HoverBehavior):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_down = ''
        self.background_color = [0.529, 0.012, 0.361, 1]

    def on_enter(self):
        Window.set_system_cursor("hand")
        self.background_color = [0.373, 0.008, 0.255, 1]
        
    def on_leave(self):
        Window.set_system_cursor("arrow")
        self.background_color = [0.529, 0.012, 0.361, 1]
        
class HoverMenu(Button, HoverBehavior):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_down = ''
        self.background_color = [1, 0, 0.498, 1]
        
    def on_enter(self):
        Window.set_system_cursor("hand")
        
    def on_leave(self):
        Window.set_system_cursor("arrow")

class SlidingDashboard(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.menu_open = False
        
    def toggle_menu(self):
        if self.menu_open:
            Animation(x=self.width, duration=0.3).start(self.ids.sidebar)
        else:
            Animation(x=self.width - 280, duration=0.3).start(self.ids.sidebar)
        self.menu_open = not self.menu_open
        
class mainoptions(ButtonBehavior, Image):
    def on_press(self):
        print("clicked")

MainApp().run()
