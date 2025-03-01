from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
import requests  # To send data to the backend

class LoginScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)

        self.username = TextInput(hint_text="Enter Username", multiline=False)
        self.password = TextInput(hint_text="Enter Password", password=True, multiline=False)
        self.status_label = Label(text="")  # To show response from backend
        self.login_button = Button(text="Login", on_press=self.login)

        self.add_widget(self.username)
        self.add_widget(self.password)
        self.add_widget(self.status_label)
        self.add_widget(self.login_button)

    def login(self, instance):
        data = {
            "username": self.username.text,
            "password": self.password.text
        }
        response = requests.post("http://127.0.0.1:5000/login", json=data)

        if response.status_code == 200:
            self.status_label.text = "Login Successful!"
        else:
            self.status_label.text = "Invalid Credentials"

class MyApp(App):
    def build(self):
        return LoginScreen()

if __name__ == "__main__":
    MyApp().run()
