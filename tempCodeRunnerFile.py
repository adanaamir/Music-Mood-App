from dotenv import load_dotenv
import os, spotipy, time, requests, random
from requests_oauthlib import OAuth2Session
from requests.auth import HTTPBasicAuth 
from spotipy.oauth2 import SpotifyOAuth
from kivymd.app import MDApp
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout


class MainApp(MDApp):
    def build(self):
        layout = BoxLayout(orientation="vertical")  
        self.label = Label(
            text = "WELCOME   ADAN\nT0   SPOTIFY   APP   RECOMMENDATION.",
            font_name = "newfonts/Unbounded-Bold.ttf" , 
            size_hint = (1,None),
            height=1750,
            font_size = "20sp",
            halign = "center",
            valign = "top"
        )
        layout.add_widget(self.label)
        
        return layout

MainApp().run()