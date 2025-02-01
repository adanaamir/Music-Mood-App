import tkinter as tk
from PIL import Image, ImageTk
from requests.auth import HTTPBasicAuth
from oauthlib.oauth2 import OAuth2Session
import webbrowser
import os
from dotenv import load_dotenv

window = tk.Tk()
window.title("MUSIC MOOD APP")
window.geometry("1000x600")
window.configure(background="#faedd3")
redirect_response = None

canvas_section = tk.Canvas(window, width=1000, height=600, bg="#faedd3", highlightthickness=0)
canvas_section.pack(fill="both", expand=True)
canvas_section.create_rectangle(0, 0, 2000, 65, fill="#001c21")

dashboard_icon = "dashboard.png"
dash_image = Image.open(dashboard_icon)
dash_image = dash_image.resize((50,50))
dash_photo = ImageTk.PhotoImage(dash_image)
canvas_section.create_image(1800,10, image=dash_photo, anchor=tk.NW)

def showWelcomeScreen():
    clear_window()
    welcome_label = tk.Label(window, text = "WELCOME TO THE MUSIC MOOD APP.", foreground="black", background="#faedd3" ,font=("Helvetica", 16, "bold"))
    welcome_label.place(x=50, y=120)
    text_2 = tk.Label(window, text= "want to listen to some songs? or view your spotify details?", foreground="black", background="#faedd3" ,font=("Helvetica", 12))
    text_2.place(x=50, y=170)

def change_color_on_hover(button, enter_color, leave_color, enter_fg, leave_fg):
    button.bind("<Enter>", lambda e: button.config(background=enter_color, foreground=enter_fg))
    button.bind("<Leave>", lambda e: button.config(background=leave_color, foreground=leave_fg))

def show_loadScreen():
    global loading_screen
    loading_screen = tk.Label(window, text = "loading", font=("Helvetica", 12), background="#faedd3", foreground="black")
    loading_screen.place(x=50, y=300)
    add_dots(loading_screen, 0)
    
def add_dots(label, count):
    if count < 3:
        label.config(text=label.cget("text") + ".")
        label.after(500, add_dots, label, count+1)
    else:
        window.after(1, removeLoadingText)    #calling the remove function after 1 sec

def removeLoadingText():
    loading_screen.destroy()
    main()
    
def clear_window():
    for widget in window.winfo_children():
        if widget != canvas_section:  #making sure not to clear/destroy canvas
            widget.destroy()
                
class UserOptions:
    def __init__(self):
        self.op = None

    def get_option(self):
        option1 = tk.Label(window, text="1. Find Music by Mood", font=("Helvetica", 12), background="#faedd3", foreground="black")
        option1.place(x=50, y=450)
        option2 = tk.Label(window, text="2. Explore your Spotify Data", font=("Helvetica", 12), background="#faedd3", foreground="black")
        option2.place(x=50, y=480)

        self.option_entry = tk.Entry(window, font=("Helvetica", 12))
        self.option_entry.place(x=50, y=510)

        submit_button = tk.Button(window, text="Submit", command=self.submit_option, font=("Helvetica", 14), foreground="white", background="#001c21", cursor="hand2")
        submit_button.place(x=50, y=550)
        change_color_on_hover(submit_button, enter_color="#001215", leave_color="#001c21", enter_fg="white", leave_fg="white")

    def submit_option(self):
        try:
            self.op = int(self.option_entry.get())
            if self.op in [1, 2]:
                self.option_entry.destroy()
                self.proceed_with_option()
            else:
                print("Not an option. Enter a correct option (1/2)")
        except ValueError:
            print("Incorrect input. Enter an int.")

    def proceed_with_option(self):
        if self.op == 1:
            recommend = PlaylistRecommendation(client_id, client_secret, access_token)
            recommend.enterMood()
            recommend.getPublicRecommendations()
        elif self.op == 2:
            user_details = UserSpotifyDetails(client_id, client_secret)
            user_details.userOptions()
            user_details.userChooseOption()

class Login:
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret 
        self.redirect_url = "https://oauth.pstmn.io/v1/browser-callback"
        self.authorization_base_url = "https://accounts.spotify.com/authorize"
        self.spotify = OAuth2Session(self.client_id, scope=[], redirect_uri=self.redirect_url)

    def check_url(self):
        redirect_url = redirect_response.get("1.0", tk.END).strip()
        
        if redirect_url.startswith("https://"):
            message_label.config(text="Successfully Logged in", fg="green")
        else:
            message_label.config(text="Error: Invalid URL format. Ensure the URL starts with 'https://'.", fg="red")

    def authenticate_user(self):
        auth_url, _ = self.spotify.authorization_url(self.authorization_base_url, prompt='login')
        login_text = tk.Label(window, text = "\nVisit this URL to login: ", font=("Helvetica", 13, "bold"), foreground="black", bg="#faedd3")
        login_text.place(x=50, y=380)
        
        login_link = tk.Label(
            window,
            text=auth_url,
            font=("Italic", 11),
            fg="blue",
            cursor="hand2",
            wraplength= 1500,
            bg="#faedd3"
            ) 
        login_link.place(x=350, y=405)
        
        login_link.bind("<Button-1>", lambda event: webbrowser.open(auth_url))
        
        entry = tk.Label(window, text ="\nPaste the redirect URL here: ", font=("Helvetica", 13, "bold"), fg="black", bg="#faedd3")
        entry.place(x=50, y= 460)
        
        global redirect_response

        #creating a Text widget for multiline input and fr single , use "Entry"
        redirect_response = tk.Text(window, width = 120, height = 2)
        redirect_response.place(x=420, y=480)
                    
        submit_button = tk.Button(
        window,
        text="Submit",
        command= lambda: self.check_url(),
        font=("Helvetica", 14), foreground= "white", background="#001c21", cursor="hand2")
        submit_button.place(x=1000, y=550)
        change_color_on_hover(submit_button, enter_color="#001215", leave_color="#001c21", enter_fg="white", leave_fg="white")

    def fetchingAccessToken(self):
        if redirect_response:
            token_url = "https://accounts.spotify.com/api/token"
            auth = HTTPBasicAuth(self.client_id, self.client_secret)
            self.token_info = self.spotify.fetch_token(token_url, auth=auth, authorization_response=redirect_response.get("1.0", tk.END).strip())
        else:
            raise ValueError(f"\033[31mError: Token not found\033[0m")

        if self.token_info:
            return self.token_info['access_token']
        else:
            raise ValueError(f"\033[31mError: No token has been fetched. Please Login...\033[0m")    

def main():
    load_dotenv()
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")

    if not client_id or not client_secret:
        print("MISSING CLIENT_ID OR CLIENT_SECRET")
        exit()

    credentials = Login(client_id, client_secret)
    credentials.authenticate_user()

def start_user_options():
    access_token = credentials.fetchingAccessToken()
    choice = UserOptions()
    choice.get_option()

def commands():
    showWelcomeScreen() 
    get_started_button = tk.Button(window, text="Get Started!", command=show_loadScreen, font=("Helvetica", 14), foreground= "white", background="#001c21", cursor="hand2")
    get_started_button.place(x=50, y=230)    
    change_color_on_hover(get_started_button, enter_color="#001215", leave_color="#001c21", enter_fg="white", leave_fg="white")    
    
commands()
message_label = tk.Label(window, text="", font=("Helvetica", 9, "bold"), bg="#faedd3")
message_label.place(x=420, y=550)

window.mainloop()