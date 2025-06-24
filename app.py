from dotenv import load_dotenv
from flask import Flask, request
from kivymd.app import MDApp
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import StringProperty
from kivy.uix.button import Button
from kivy.animation import Animation
from functools import partial
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.behaviors import ButtonBehavior
from requests_oauthlib import OAuth2Session
from requests.auth import HTTPBasicAuth 
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.factory import Factory
from hoverbehaviour import HoverBehavior
import webbrowser, os, threading, time, random, requests

#-----------------------------------flask for redirecting------------------------------------------------
app = Flask(__name__)
redirect_response_url = None

@app.route("/callback")
def callback():
    global redirect_response_url
    redirect_response_url = request.url
    return "Login successful! You can close this window and return to the app."

def run_Server():
    app.run(port=8080)
    
def start_server():
    thread = threading.Thread(target=run_Server)
    thread.daemon = True
    thread.start()

#---------------------------------------------kivy app------------------------------------------------------
class MainApp(MDApp):
    def build(self):
        load_dotenv()
        start_server()

        self.client_id = os.getenv("CLIENT_ID")
        self.client_secret = os.getenv("CLIENT_SECRET")
        self.login = Login(client_id=self.client_id, client_secret=self.client_secret)
        self.login.authenticate_user()

        self.sm = self.load_ui()
        Window.bind(on_key_down=self.on_key_down)
        return self.sm

    def load_ui(self):
        Builder.unload_file("frontend.kv")
        return Builder.load_file("frontend.kv") 

    #---------------------auto reload current screen------------------------
    def on_key_down(self, window, key, scancode, codepoint, modifier):
        if codepoint == 'r':
            print("🔁 Reloading KV file...")

            # Step 1: Save current screen name
            current_screen = self.sm.current

            # Step 2: Reload the .kv file
            Builder.unload_file("frontend.kv")
            new_ui = Builder.load_file("frontend.kv")

            # Step 3: Clear and add fresh screens
            self.sm.clear_widgets()
            for screen in new_ui.screens:
                screen_class = Factory.get(screen.__class__.__name__)
                new_screen = screen_class(name=screen.name)
                self.sm.add_widget(new_screen)

            # Step 4: Go back to the screen we were on
            self.sm.current = current_screen

            print(f"✅ Reloaded and stayed on '{current_screen}'")

    #---------------------------continue-------------------------------------
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

        #------SETTING THE REDIRECT RESPONSE HERE-------
        self.login.redirect_response = redirect_response_url
        try:
            token = self.login.fetchingAccessToken()
            self.access_token = token
            self.root.current = "dashboard"
        except Exception as e:
            print(f"\033[31mError fetching token:\033[0m {e}")

    def enterMood(self, selected_mood):
        self.selected_mood = selected_mood
        screen = self.sm.get_screen("screen1")

        screen.ids.mood_select_label.markup = True
        screen.ids.mood_select_label.text = f"Feeling [color=#683C3C]{self.selected_mood}[/color]? Let's find the perfect tracks!"
        
        self.loading_messages = random.choice([
            "Fetching your perfect playlists",
            "Tuning into your vibe",
            "Finding tracks that match your soul",
            "Please wait. the vibes are downloading",
            "Hang tight! The beat is loading",
            "Scanning musical frequencies",
            "Summoning good energy & good music"
        ])
        
        #-----------------loading effect----------------------
        self.dot_count = 0
        screen.ids.random_msg.text = self.loading_messages

        self.dot_event = Clock.schedule_interval(self.update_dots, 0.5)
        Clock.schedule_once(self.stop_dot_loading, 4)

    def update_dots(self, dt):
        screen = self.sm.get_screen("screen1")
        self.dot_count = (self.dot_count + 1) % 4 
        dots = '.' * self.dot_count
        screen.ids.random_msg.text = f"{self.loading_messages}{dots}"

    def stop_dot_loading(self, dt):
        self.dot_event.cancel()
        screen = self.sm.get_screen("screen1")
        screen.ids.random_msg.text = ""
        threading.Thread(target=self.getPublicRecommendations()).start()
    
    #----------------------------displaying music----------------------------
    def getPublicRecommendations(self):    
        screen = self.sm.get_screen("screen1") 
        container = screen.ids.tracks_container
        container.clear_widgets()
        
        self.genres = [
            "pop", "folk", "chill", "ambient", "dance", "study", "metal", "workout", "rock", "hiphop" 
        ]
        mood_to_genre = {
            "Happy": "pop",
            "Sad": "folk",
            "Chill": "chill",
            "Peaceful": "ambient",
            "Energetic": "dance",
            "Focused": "study",
            "Angry": "metal",
            "Motivational": "workout"
        }
        genre = mood_to_genre.get(self.selected_mood, None)
        offset = random.randint(0, 100)
        search_url = f"https://api.spotify.com/v1/search"
        params = {
            "q": f"genre: {genre}",
            "type": "track",
            "limit": 10,
            "offset": offset
        }
        headers = {"Authorization": f"Bearer {self.access_token}"}

        response = requests.get(search_url, headers=headers, params=params)

        if response.status_code == 200:
            results= response.json()
            tracks = results.get('tracks', {}).get('items', [])
            screen.ids.track_text.text = "Here are some tracks for your vibe\n"
            
            if not tracks:
                raise ValueError(f"\033[31mError: No tracks found for genre '{genre}'\033[0m")
            
            for track in tracks:
                name = track['name']
                artist = track['artists'][0]['name']
                url = track['external_urls']['spotify']
                
                track_card = TrackCard()  
                track_card.ids.track_label.text = f"{name} by {artist}"              
                track_card.ids.spotify_button.bind(on_release=partial(self.open_spotify, url))

                container.add_widget(track_card)
                
        else:
            error_msg = f"\033[31mError fetching genres: {response.status_code}\033[0m"
            print(error_msg)
    
    def open_spotify(self, url, *args):
        webbrowser.open(url)

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
class TrackCard(BoxLayout):
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
        
class mainoptions(HoverBehavior, ButtonBehavior, Image):
    mood_name = StringProperty("")
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(pos=self._update_hover_area, size=self._update_hover_area)
        self.original_y = None

    def _update_hover_area(self, *args):
        pass
    
    def on_enter(self):
        Window.set_system_cursor("hand")
        if self.original_y is None:
            self.original_y = self.y

        #animating "bop" 
        Animation.cancel_all(self) 
        Animation(y=self.original_y + 10, duration=0.15).start(self)

    def on_leave(self):
        Window.set_system_cursor("arrow")

        #animating back to original position
        Animation.cancel_all(self)
        Animation(y=self.original_y, duration=0.15).start(self)

class BasicImageHover(ButtonBehavior, HoverBehavior, Image):
    def on_enter(self):
        Window.set_system_cursor("hand")
        
    def on_leave(self):
        Window.set_system_cursor("arrow")
        
class BasicButtonHover(Button, HoverBehavior):
    def on_enter(self):
        Window.set_system_cursor("hand")
        
    def on_leave(self):
        Window.set_system_cursor("arrow")

MainApp().run()
