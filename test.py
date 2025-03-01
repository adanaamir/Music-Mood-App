from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivymd.app import MDApp
from kivy.uix.behaviors import HoverBehavior
from kivymd.uix.label import MDLabel

KV = '''
BoxLayout:
    orientation: 'vertical'
    padding: 20
    spacing: 20

    HoverLabel:
        text: "Hover over me!"
        font_style: "H5"
        theme_text_color: "Custom"
        text_color: 1, 1, 1, 1  # Default color (white)
'''

class HoverLabel(MDLabel, HoverBehavior):
    def on_enter(self):
        self.text_color = (1, 0, 0, 1)  # Change to red on hover

    def on_leave(self):
        self.text_color = (1, 1, 1, 1)  # Change back to white

class TestApp(MDApp):
    def build(self):
        return Builder.load_string(KV)

TestApp().run()
