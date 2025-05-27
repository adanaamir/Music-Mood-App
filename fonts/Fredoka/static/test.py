from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivymd.app import MDApp
from kivy.uix.image import Image
from kivy.utils import get_color_from_hex
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView

class MainApp(MDApp):
    def build(self):
        layout = FloatLayout()
        welcome_text = "WELCOME   T0   SPOTIFY   APP   RECOMMENDATION"
        font="newfonts/static/Montserrat-SemiBold.ttf"
        
        img1 = Image(source='images/download_new.jpeg',
                    allow_stretch=True,
                    keep_ratio=False,
                    size_hint=(1,1),
                    pos_hint={'x': 0, 'y': 0},
                    color= (1,1,1, 0.3)
                )
        layout.add_widget(img1)
        
        #scroll bar
        scroll_view = ScrollView(
            size_hint=(1, 1),
            pos_hint={'x': 0, 'y': 0}
        )

        scroll_layout = GridLayout(
            cols=1,
            size_hint_y=None,
            padding=[20, 20, 20, 20],   #left, top, right, bottom
            spacing=10
        )
        scroll_layout.bind(minimum_height=scroll_layout.setter('height'))

        #adding my wdigets to the scroll view
        self.main_label = Label(
            text=welcome_text,
            font_name=font,
            size_hint=(1, None),
            # height=140,
            font_size="25sp",
            halign="left",
            valign="top",
            color=get_color_from_hex("#FF007BFF")
        )
        self.main_label.bind(size=self.main_label.setter('text_size'))

        
        # glitch layers
        self.glitchlayer = Label(
            text=welcome_text,
            font_name=font,
            size_hint=(1, None),
            # height=140,
            font_size="25sp",
            halign="left",
            valign="top",
            color=get_color_from_hex("#FF007B84")
            )
        self.glitchlayer.bind(size=self.glitchlayer.setter('text_size'))
        
        
        self.text2 = Label(
            text="want to listen to some songs? or view your spotify details?",
            font_name=font,
            size_hint=(1, None),
            height=100,
            font_size="16sp",
            valign="top",
            halign="left",
            color=get_color_from_hex("#FFFFFFF8")
        )
        self.text2.bind(size=self.text2.setter('text_size'))
        
        
        
        scroll_layout.add_widget(self.glitchlayer)
        scroll_layout.add_widget(self.main_label)
        scroll_layout.add_widget(self.text2)
   
        scroll_view.add_widget(scroll_layout)
        layout.add_widget(scroll_view)
        
        return layout


MainApp().run()
