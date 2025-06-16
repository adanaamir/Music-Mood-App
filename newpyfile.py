from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from requests_oauthlib import OAuth2Session
from requests.auth import HTTPBasicAuth 
from hoverbehaviour import HoverBehavior
import webbrowser, os, threading, time, random
from kivy.uix.boxlayout import BoxLayout
from kivy.animation import Animation
from kivy.properties import BooleanProperty

class MainApp(MDApp):
    def build(self):
        return Builder.load_file('newtets.kv')

class PlaylistRecommendation:
    def __init__(self, client_id, client_secret,access_token):
        self.acecess_token = access_token
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
        pass
    
    def getPublicRecommendations(self):
        if self.selected_mood is None:
            raise ValueError(f"\033[31mError: No mood selected\033[0m")
        genre = self.mood_to_genre.get(self.selected_mood, None)
        
        if genre is None or genre not in self.genres:
            raise ValueError(f"\033[31mError: No genre mapped for the mood: {self.selected_mood}\033[0m")
        offset = random.randint(0,100)
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
        
        # while True:
        #     try:
        #         option = input("\nType:\n\"C\" to get more recommendations \n\"E\" to exit \n\"M\" to change mood \n\"S\" to view your Spotify details:\n").upper()
                        
        #         if option == "C":
        #             print("\nGetting more recommendations")
        #             for _ in range(4):
        #                 time.sleep(0.5)
        #                 print(".", end="",flush=True)
        #             print()
        #             self.getPublicRecommendations()

        #         elif option == "S":
        #             user_det = UserSpotifyDetails(client_id, client_secret)
        #             user_det.userOptions()
        #             user_det.userChooseOption()

        #         elif option == "E":
        #             print("\nExiting the program")
        #             for _ in range(4):
        #                 time.sleep(0.5)
        #                 print(".", end="",flush=True)
        #             print()
        #             exit()

        #         elif option == "M":
        #             self.enterMood()
        #             self.getPublicRecommendations()
        #         else:
        #             print(f"\033[31mIncorrect option.\033[0m")
        #     except Exception as e:
        #         print(f"\033[31m{e}\033[0m")




class Dashboard(Screen):
    pass

class WindowManager(ScreenManager):
    pass

class HoverButton(Button, HoverBehavior):
    def on_enter(self):
        Window.set_system_cursor("hand")
        self.background_color = [0.8, 0, 0.4, 1]
        
    def on_leave(self):
        Window.set_system_cursor("arrow")
        self.background_color = [1, 0, 0.498, 1]
        
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
    
    
    
MainApp().run()