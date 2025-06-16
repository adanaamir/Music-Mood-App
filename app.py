from dotenv import load_dotenv
from flask import Flask, request
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from requests_oauthlib import OAuth2Session
from requests.auth import HTTPBasicAuth 
from hoverbehaviour import HoverBehavior
import webbrowser, os, threading, time

#flask for redirecting
app = Flask(__name__)
redirect_response_url = None

@app.route("/callback")
def callback():
    global redirect_response_url
    redirect_response_url = request.url
    print(f"\033[32mReceived redirect:\033[0m {redirect_response_url}")
    return "Login successful! You can close this window and return to the app."

def run_Server():
    app.run(port=8080)
    
def start_server():
    thread = threading.Thread(target=run_Server)
    thread.daemon = True
    thread.start()

#kivy app
class MainApp(MDApp):
    def build(self):
        load_dotenv()
        start_server()
        
        client_id = os.getenv("CLIENT_ID")
        client_secret = os.getenv("CLIENT_SECRET")
        self.login = Login(client_id=client_id, client_secret= client_secret)
        self.login.authenticate_user()
        
        self.sm = Builder.load_file('frontend.kv')
        return self.sm
    
    def spotify_login(self):
        self.background_color = [1, 0, 0.498, 1]
        if self.login.auth_url:
            webbrowser.open(self.login.auth_url)
        else:
            print("not ready")
            
    def check_redirect(self):
        global redirect_response_url
        while not redirect_response_url:
            print("Waiting for Spotify redirect...")
            time.sleep(1)

        self.login.redirect_response = redirect_response_url
        try:
            token = self.login.fetchingAccessToken()
            print(f"\033[32mAccess Token:\033[0m {token}")
            self.root.current = "dashboard"
        except Exception as e:
            print(f"\033[31mError fetching token:\033[0m {e}")
        
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
        
# class HoverMenu(Button, HoverBehavior):
#     def on_enter(self):
#         Window.set_system_cursor("hand")
        
#     def on_leave(self):
#         Window.set_system_cursor("arrow")

MainApp().run()
