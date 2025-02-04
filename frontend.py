# frontend.py
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from backend import Login

class MyApp(App):
    def login(self, instance):
        client_id = ""
        client_secret = ""
        
        login = Login(client_id, client_secret)
        login.autheticate_user()
        access_token = login.fetchingAccessToken()
        
        self.label.text = f"Successfully Logged in! Access Token: {access_token}"
        
    def build(self):
        layout = BoxLayout(orientation = 'vertical')
        self.label = Label(text="Click to login with Spotify")
        button = Button(text="Login with Spotify")
        button.bind(on_press = self.label)
        layout.add_widget(self.label)
        layout.add_widget(button)
        return layout

if __name__ == '__main__':
    MyApp().run()        
