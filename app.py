from kivymd.app import MDApp
from kivy.lang import Builder
from dotenv import load_dotenv
from kivy.uix.button import Button
from kivy.core.window import Window
from requests_oauthlib import OAuth2Session
from hoverbehaviour import HoverBehavior
import webbrowser, os

class MainApp(MDApp):
    def build(self):
        load_dotenv()
        client_id = os.getenv("CLIENT_ID")
        client_secret = os.getenv("CLIENT_SECRET")
        self.login = Login(client_id=client_id, client_secret= client_secret)
        self.login.authenticate_user()
        
        return Builder.load_file('frontend.kv')
    
    def spotify_login(self):
        self.background_color = [1, 0, 0.498, 1]
        if self.login.auth_url:
            return webbrowser.open(self.login.auth_url)
        else:
            print("not ready")
        
class Login:
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret 
        self.redirect_url = "https://oauth.pstmn.io/v1/browser-callback"
        self.authorization_base_url = "https://accounts.spotify.com/authorize"
        self.spotify = OAuth2Session(self.client_id, scope=[], redirect_uri=self.redirect_url)
        self.auth_url = None
        
    def authenticate_user(self):
        auth_url, _ = self.spotify.authorization_url(self.authorization_base_url, prompt='login')
        self.auth_url = auth_url
        return auth_url
    
class HoverButton(Button, HoverBehavior):
    def on_enter(self):
        Window.set_system_cursor("hand")
        self.background_color = [0.8, 0, 0.4, 1]
        
    def on_leave(self):
        Window.set_system_cursor("arrow")
        self.background_color = [1, 0, 0.498, 1]
MainApp().run()
