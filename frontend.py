from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.screen import MDScreen  # Screen management
from kivymd.uix.button import MDRaisedButton, MDIconButton, MDFloatingActionButton  # Buttons
from kivymd.uix.label import MDLabel  # Labels with Material Design
from kivymd.uix.textfield import MDTextField  # Input fields
from kivymd.uix.toolbar import MDTopAppBar  # Top navigation bar
from kivymd.uix.menu import MDDropdownMenu  # Dropdown menus
from kivy.properties import ListProperty,BooleanProperty
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout  # Arranging widgets vertically/horizontally
from kivy.uix.gridlayout import GridLayout  # For structured layouts
from kivy.uix.scrollview import ScrollView  # Enables scrolling
from kivymd.uix.behaviors.hover_behavior import HoverBehavior
from kivymd.uix.progressbar import MDProgressBar  # Progress bar (for loading UI or music)
from kivy.core.audio import SoundLoader  # Load & play audio
from kivy.network.urlrequest import UrlRequest  # Fetch online data (if needed)
from kivymd.uix.pickers import MDColorPicker  # If you want users to pick themes
from kivymd.theming import ThemeManager  # To apply global themes
from backend import UserOptions, Login,  PlaylistRecommendation, UserSpotifyDetails

class GetStartedHover(MDRaisedButton, HoverBehavior):
    hover_color = ListProperty([0.6, 0, 0.3, 1]) 
    default_color = ListProperty([0.8, 0, 0.4, 1])
    
    def on_enter(self):
        self.md_bg_color = self.hover_color
        Window.set_system_cursor("hand")  

    def on_leave(self):
        self.md_bg_color = self.default_color
        Window.set_system_cursor("arrow") 
    
class HoverText(MDRaisedButton, HoverBehavior):
    hover_color = ListProperty([0.6, 0, 0.3, 1]) 
    default_color = ListProperty([0, 0, 0, 1])
    
    def on_enter(self):
        self.md_bg_color = self.hover_color
        Window.set_system_cursor("hand") 
        
    def on_leave(self):
        self.md_bg_color = self.default_color
        Window.set_system_cursor("arrow") 

class MainApp(MDApp):
    def build(self):
        return Builder.load_file("frontend.kv")
        
    def getting_started_scroll(self):
        scroll_view = self.root.ids.scroll_view
        target_section = self.root.ids.getting_started

        scroll_view.scroll_to(target_section)
        
    def home_scroll(self):
        scroll_view = self.root.ids.scroll_view
        scroll_view.scroll_y = 1  #this scrolls to the top
        
    def linkToLogin(self):
        auth_url, _ = Login.autheticate_user()
        
MainApp().run()

