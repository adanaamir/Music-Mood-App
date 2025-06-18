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