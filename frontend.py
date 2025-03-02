from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.screen import MDScreen  # Screen management
from kivymd.uix.button import MDRaisedButton, MDIconButton, MDFloatingActionButton  # Buttons
from kivymd.uix.label import MDLabel  # Labels with Material Design
from kivymd.uix.textfield import MDTextField  # Input fields
from kivymd.uix.toolbar import MDTopAppBar  # Top navigation bar
from kivymd.uix.navigationdrawer import MDNavigationDrawer  # Side menu
from kivymd.uix.dialog import MDDialog  # Popups and dialogs
from kivymd.uix.menu import MDDropdownMenu  # Dropdown menus
from kivy.uix.image import Image  # To add background images
from kivy.properties import ListProperty,BooleanProperty
from kivy.core.window import Window
from kivy.uix.relativelayout import RelativeLayout  # Helps with layered positioning
from kivy.uix.boxlayout import BoxLayout  # Arranging widgets vertically/horizontally
from kivy.uix.gridlayout import GridLayout  # For structured layouts
from kivy.uix.scrollview import ScrollView  # Enables scrolling
from kivymd.uix.behaviors.hover_behavior import HoverBehavior
from kivymd.uix.snackbar import MDSnackbar  # Toast-like notifications
from kivymd.uix.progressbar import MDProgressBar  # Progress bar (for loading UI or music)
from kivy.core.audio import SoundLoader  # Load & play audio
from kivy.network.urlrequest import UrlRequest  # Fetch online data (if needed)
from kivymd.uix.pickers import MDColorPicker  # If you want users to pick themes
from kivymd.theming import ThemeManager  # To apply global themes

KV = '''
MDScreen:
    canvas.before:
        Color:
            rgba: 0, 0, 0, 1 
        Rectangle:
            pos: self.pos
            size: Window.size
    
    Image:
        id: img2
        source: "Delete free icons designed by Roundicons_new.png"
        opacity: 1
        size_hint_y: None
        size_hint_x: 1
        height: dp(55)
        allow_stretch: True
        keep_ratio: False
        pos_hint: {"top": 0.99} 

    HoverText:
        text: "Home"
        font_size: dp(15)
        md_bg_color: 0, 0, 0, 1
        text_color: 1, 1, 1, 1 
        pos_hint: {"center_x": 0.13, "y": 0.92} 
        on_release: app.home_scroll()
        font_name: "Unbounded-VariableFont_wght.ttf"
        
    HoverText:
        text: "Explore Your Data"
        font_size: dp(15)
        md_bg_color: 0, 0, 0, 1
        text_color: 1, 1, 1, 1 
        pos_hint: {"center_x": 0.33, "y": 0.92} 
        on_release: app.home_scroll()
        font_name: "Unbounded-VariableFont_wght.ttf"
        
    HoverText:
        text: "MoodBoard"
        font_size: dp(15)
        md_bg_color: 0, 0, 0, 1
        text_color: 1, 1, 1, 1 
        pos_hint: {"center_x": 0.59, "y": 0.92} 
        on_release: app.home_scroll()
        font_name: "Unbounded-VariableFont_wght.ttf"
        
    HoverText:
        text: "Account"
        font_size: dp(15)
        md_bg_color: 0, 0, 0, 1
        text_color: 1, 1, 1, 1 
        pos_hint: {"center_x": 0.8, "y": 0.92} 
        on_release: app.home_scroll()
        font_name: "Unbounded-VariableFont_wght.ttf"
            
    ScrollView:
        id: scroll_view
        size_hint_y: None
        height: Window.height - dp(63)
        do_scroll_x: False 
        do_scroll_y: True  

        MDBoxLayout:
            orientation: "vertical"
            size_hint_y: None
            height: self.minimum_height
            padding: [0, dp(60), 0, 0]

            FloatLayout:
                size_hint_y: None
                height: dp(600)
                
                Image:
                    id: img1
                    source: "Billie Eilish NDA vevo.jpeg"
                    opacity: 0.7
                    size_hint_y: None
                    width: root.width  
                    height: dp(180)
                    pos_hint: {"center_x": 0.8, "y": 0.7}     
                
                Image:
                    id: img3
                    source: "the marias poster.jpeg"
                    allow_stretch: True
                    keep_ratio: True
                    size_hint_x: 1
                    opacity: 0.3
                    size_hint_y: None
                    height: dp(900)
                    pos_hint: {"center_x": 0.86, "y": -0.99}  

                Image:
                    id: img4
                    source: "download_new.jpeg"
                    allow_stretch: True
                    keep_ratio: True
                    size_hint_x: 1
                    opacity: 0.2
                    size_hint_y: None
                    height: dp(1000)
                    pos_hint: {"center_x": 0.1, "y": -0.4}  
                
                # Image:
                #     id: img5
                #     source: "download (10).jpeg"
                #     allow_stretch: True
                #     keep_ratio: True
                #     size_hint_x: 1
                #     opacity: 0.3
                #     size_hint_y: None
                #     height: dp(1000)
                #     pos_hint: {"center_x": 0.3, "y": -2} 
        
                Label:
                    text: "WELCOME  TO  THE  MUSIC  MOOD  APP"
                    font_size: dp(20)
                    bold: True
                    font_name: "Unbounded-VariableFont_wght.ttf"
                    pos_hint: {"center_x": 0.2, "top": 1.515}
                    color: (1, 0, 1, 0.3) 
                    
                MDLabel:
                    text: "WELCOME  TO  THE  MUSIC  MOOD  APP"
                    font_size: dp(20)
                    bold: True
                    color: (1, 0, 1, 1)
                    pos_hint: {"center_x": 0.52, "top": 1.515}
                    font_name: "Unbounded-VariableFont_wght.ttf"
                    
                MDLabel:
                    text: "want to listen to some songs? or view your spotify details?"
                    font_size: dp(15)
                    bold: False
                    pos_hint: {"center_x": 0.52, "top": 1.44}
                    color: (0.8, 0.8, 0.8, 1)
                    font_name: "Unbounded-VariableFont_wght.ttf"

                MDLabel:
                    text: "BILLIE EILISH"
                    font_size: dp(14)
                    bold: False
                    pos_hint: {"center_x": 1.26, "top": 1.15}
                    color: (0.8, 0.8, 0.8, 1)
                    font_name: "Unbounded-VariableFont_wght.ttf"
                    
                MDLabel:
                    text: "107.9M monthly listeners"
                    font_size: dp(12)
                    bold: False
                    pos_hint: {"center_x": 1.239, "top": 1.1}
                    color: (0.8, 0.8, 0.8, 1)
                    font_name: "Unbounded-VariableFont_wght.ttf"
                    
                # MDLabel:
                #     text: "MITSKI"
                #     font_size: dp(14)
                #     bold: False
                #     pos_hint: {"center_x": 0.68, "top": 0.56}
                #     color: (0.8, 0.8, 0.8, 1)
                #     font_name: "Unbounded-VariableFont_wght.ttf"
                    
                # MDLabel:
                #     text: "Be the Cowboy-2018"
                #     font_size: dp(12)
                #     bold: False
                #     pos_hint: {"center_x": 0.65, "top": 0.51}
                #     color: (0.8, 0.8, 0.8, 1)
                #     font_name: "Unbounded-VariableFont_wght.ttf"

            #BUTTONS                
                GetStartedHover:
                    text: "Get Started"
                    font_size: dp(16)
                    md_bg_color: 0.8, 0, 0.4
                    text_color: 1, 1, 1, 1 
                    pos_hint: {"center_x": 0.2, "y": 0.5} 
                    on_release: app.getting_started_scroll()
       
            BoxLayout:
                id: getting_started
                size_hint_y: None
                height: dp(400)
                
                # Label:
                #     text: "Now you are at the next section!"
                #     font_size: dp(20)
                #     color: 1, 1, 1, 1 
'''
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
        return Builder.load_string(KV)

    def getting_started_scroll(self):
        scroll_view = self.root.ids.scroll_view
        target_section = self.root.ids.getting_started

        scroll_view.scroll_to(target_section)
        
    def home_scroll(self):
        scroll_view = self.root.ids.scroll_view
        scroll_view.scroll_y = 1 #this scrolls to the top
        

    
MainApp().run()

