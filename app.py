from dotenv import load_dotenv
from flask import Flask, request
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.properties import StringProperty
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.animation import Animation
from functools import partial
from kivy.uix.image import Image
from kivy.properties import ListProperty, NumericProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.behaviors import ButtonBehavior
from requests_oauthlib import OAuth2Session
from requests.auth import HTTPBasicAuth 
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.factory import Factory
from hoverbehaviour import HoverBehavior
import webbrowser, os, threading, time, random, requests, spotipy
from spotipy.oauth2 import SpotifyOAuth
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.toast import toast
from kivy.graphics import PushMatrix, PopMatrix, Scale
from numpy import dot
from numpy.linalg import norm
#-----------------------------------flask for redirecting------------------------------------------------
app = Flask(__name__)
redirect_response_url = None

@app.route("/callback")
def callback():
    global redirect_response_url
    redirect_response_url = request.url
    return "Login successful! You can close this window and return to the app."

def run_Server():
    app.run(port=8080)
    
def start_server():
    thread = threading.Thread(target=run_Server)
    thread.daemon = True
    thread.start()

#---------------------------------------------kivy app------------------------------------------------------
class MainApp(MDApp):
    about_dialog = None
    contact_dialog = None
    display_name = StringProperty("")
    
    def build(self):
        load_dotenv()
        start_server()

        self.client_id = os.getenv("CLIENT_ID")
        self.client_secret = os.getenv("CLIENT_SECRET")
        self.redirect_url = "http://localhost:8080/callback"
        self.sp = None
        self.scope = (
            "user-top-read "
            "user-follow-read "
            "playlist-read-private "
            "user-read-recently-played "
            "user-library-read "
            "user-read-playback-state"
        )
        
        self.login = Login(client_id=self.client_id, client_secret=self.client_secret)
        
        self.sm = self.load_ui()
        Window.bind(on_key_down=self.on_key_down)
        
        return self.sm

    # ------------------ SCREEN SWITCHING ----------------------

    def login_user(self):
        self.sp = spotipy.Spotify(
            auth_manager=SpotifyOAuth(
                client_id=self.client_id,
                client_secret=self.client_secret,
                redirect_uri=self.redirect_url,
                scope=self.scope
            ),
            requests_timeout=10, retries=5, status_retries=5, backoff_factor=0.5
        )

        user_data = self.sp.current_user()
        self.display_name = user_data['display_name']
    
    #------------------POP UP BOX FOR ABOUT US AND CONTACT US---------------
    def show_about_us(self):
        if not self.about_dialog:
            self.about_dialog = MDDialog(
            title="About This Project",
            text="This is a personal project built using Spotify's API for mood-based song recommendations.\nMade for learning purposes",
            buttons=[
                MDFlatButton(
                    text="Close",
                    on_release=self.close_about,
                )
            ],
        )
        self.about_dialog.open()
        
    def show_contact(self):
        if not self.contact_dialog:
            self.contact_dialog = MDDialog(
            title="Contact",
            text="This is a student project. No official support — Though you can check out: \nGithub: https://github.com/adanaamir\nLinkedin: https://www.linkedin.com/in/adan-aamir",
            buttons=[
                MDFlatButton(
                    text="Close",
                    on_release=self.close_contact,
                )
            ],
        )
        self.contact_dialog.open()
        
    def close_about(self, *args):
        self.about_dialog.dismiss()
        self.about_dialog = None

    def close_contact(self, *args):
        self.contact_dialog.dismiss()
        self.contact_dialog = None

    def load_ui(self):
        Builder.unload_file("frontend.kv")
        return Builder.load_file("frontend.kv") 
    
    def scroll_artist_right(self):
        scroll = self.root.get_screen('screen1').ids.artist_scroll
        new_x = min(scroll.scroll_x + 0.2, 1.01)
        Animation(scroll_x=new_x, d=0.3, t= 'out_quad').start(scroll) 

    def scroll_artist_left(self):
        scroll = self.root.get_screen('screen1').ids.artist_scroll
        if scroll.scroll_x <= 0.01:
            return
        new_x = max(scroll.scroll_x - 0.2, 0)
        Animation(scroll_x=new_x, d=0.3, t= 'out_quad').start(scroll)     

    #---------------------auto reload current screen------------------------
    def on_key_down(self, window, key, scancode, codepoint, modifier):
        if codepoint == 'r':
            print("🔁 Reloading KV file...")

            current_screen = self.sm.current

            Builder.unload_file("frontend.kv")
            new_ui = Builder.load_file("frontend.kv")

            self.sm.clear_widgets()
            for screen in new_ui.screens:
                screen_class = Factory.get(screen.__class__.__name__)
                new_screen = screen_class(name=screen.name)
                self.sm.add_widget(new_screen)

            self.sm.current = current_screen

            print(f"✅ Reloaded and stayed on '{current_screen}'")

    #---------------------------continue-------------------------------------
    def spotify_login(self):
        self.background_color = [1, 0, 0.498, 1]
        
        self.login.authenticate_user()
        if self.login.auth_url:
            webbrowser.open(self.login.auth_url)
        else:
            print("not ready")
            
    def check_redirect(self):
        global redirect_response_url
        while not redirect_response_url:
            time.sleep(1)

        #---------------------------SETTING THE REDIRECT RESPONSE HERE-----------------------------
        self.login.redirect_response = redirect_response_url
        
        try:
            token = self.login.fetchingAccessToken()
            self.access_token = token
            
            self.login_user()
            
            for screen_name in ["dashboard", "screen1", "screen2", "screen3", "aiscreen"]:
                try:
                    screen = self.sm.get_screen(screen_name)
                    screen.ids.displayname_label.text = self.display_name
                
                except Exception as e:
                    print(f"Could not update displayname_label for {screen_name}: {e}")
            
            self.root.current = "dashboard"
            
        except Exception as e:
            print(f"\033[31mError fetching token:\033[0m {e}")


    def enterMood(self, selected_mood):
        self.selected_mood = selected_mood
        screen = self.sm.get_screen("screen1")

        screen.ids.mood_select_label.markup = True
        screen.ids.mood_select_label.text = f"Feeling [color=#683C3C]{self.selected_mood}[/color]? Let's find the perfect tracks!"
        
        self.loading_messages = random.choice([
            "Fetching your perfect playlists",
            "Tuning into your vibe",
            "Finding tracks that match your soul",
            "Please wait. the vibes are downloading",
            "Hang tight! The beat is loading",
            "Scanning musical frequencies",
            "Summoning good energy & good music"
        ])
        
        #-----------------loading effect----------------------
        self.dot_count = 0
        screen.ids.random_msg.text = self.loading_messages

        self.dot_event = Clock.schedule_interval(self.update_dots, 0.5)
        Clock.schedule_once(self.stop_dot_loading, 4)

    def update_dots(self, dt):
        screen = self.sm.get_screen("screen1")
        self.dot_count = (self.dot_count + 1) % 4 
        dots = '.' * self.dot_count
        screen.ids.random_msg.text = f"{self.loading_messages}{dots}"

    def stop_dot_loading(self, dt):
        self.dot_event.cancel()
        screen = self.sm.get_screen("screen1")
        screen.ids.random_msg.text = ""
        
        #setting the artist frame to 0
        screen.ids.artist_scroll.clear_widgets()
        
        screen.ids.artist_scroll_r.opacity = 0
        screen.ids.artist_scroll_r.size_hint = (0, 0)
        screen.ids.artist_scroll_r.size = (0, 0)
        
        screen.ids.artist_scroll_l.opacity = 0
        screen.ids.artist_scroll_l.size_hint = (0, 0)
        screen.ids.artist_scroll_l.size = (0, 0)
        
        threading.Thread(target=self.getPublicRecommendations()).start()
    
    #----------------------------displaying TRACKS----------------------------
    def getPublicRecommendations(self):    
        screen = self.sm.get_screen("screen1") 
        container = screen.ids.tracks_container
        container.clear_widgets()
        
        self.genres = [
            "pop", "folk", "chill", "ambient", "dance", "study", "metal", "workout", "rock", "hiphop" 
        ]
        mood_to_genre = {
            "Happy": "pop",
            "Sad": "folk",
            "Chill": "chill",
            "Peaceful": "ambient",
            "Energetic": "dance",
            "Focused": "study",
            "Angry": "metal",
            "Motivational": "workout"
        }
        genre = mood_to_genre.get(self.selected_mood, None)
        offset = random.randint(0, 100)
        search_url = f"https://api.spotify.com/v1/search"
        params = {
            "q": f"genre: {genre}",
            "type": "track",
            "limit": 10,
            "offset": offset
        }
        headers = {"Authorization": f"Bearer {self.access_token}"}

        response = requests.get(search_url, headers=headers, params=params)

        if response.status_code == 200:
            results= response.json()
            tracks = results.get('tracks', {}).get('items', [])
            screen.ids.track_text.text = "Here are some tracks for your vibe\n"
            
            if not tracks:
                raise ValueError(f"\033[31mError: No tracks found for genre '{genre}'\033[0m")
            
            for track in tracks:
                name = track['name']
                artist = track['artists'][0]['name']
                url = track['external_urls']['spotify']
                
                track_card = TrackCard()  
                track_card.ids.track_label.text = f"{name} by {artist}"              
                track_card.ids.spotify_button.bind(on_release=partial(self.open_spotify, url))

                container.add_widget(track_card)
                
                # while True:
                #     try:
                #         if option == "C":
                #             print("\nGetting more recommendations")
                #             for _ in range(4):
                #                 time.sleep(0.5)
                #                 print(".", end="",flush=True)
                #             print()
                #             self.getPublicRecommendations()
                            
                #         else:
                #             print(f"\033[31mIncorrect option.\033[0m")
                #     except Exception as e:
                #         print(f"\033[31m{e}\033[0m")
                        
        else:
            error_msg = f"\033[31mError fetching genres: {response.status_code}\033[0m"
            print(error_msg)
    
    def open_spotify(self, url, *args):
        webbrowser.open(url)
        
    def resetScreen2(self):
        screen = self.sm.get_screen("screen2")
        
        #-----------------------------CLEARING LABELS-------------------------------
        screen.ids.fetchingtrackstext.text = ""
        screen.ids.artistsfollowed.text = ""
        screen.ids.recentlyplayed.text = ""
        screen.ids.topartists.text = ""
        screen.ids.currentplaylists.text = ""
        screen.ids.liked_albums.text = ""
        screen.ids.liked_tracks.text = ""
        screen.ids.currently_playing_track.text = ""
        screen.ids.notrackplaying.text = ""
        
        #-----------------------------CLEARING TRACKS----------------------------------    
        screen.ids.tracks_container.clear_widgets()
        screen.ids.tracks2_container.clear_widgets()
        screen.ids.tracks3_container.clear_widgets()
        screen.ids.tracks4_container.clear_widgets()
        screen.ids.tracks5_container.clear_widgets()
        screen.ids.tracks6_container.clear_widgets()
        screen.ids.tracks6part_container.clear_widgets()
        screen.ids.tracks7_container.clear_widgets()
        screen.ids.tracks8_container.clear_widgets()
        
    #--------------------------------------------------USER DETAILS---------------------------------------
    def viewTopTracks(self):
        self.resetScreen2()
        
        screen = self.sm.get_screen("screen2")
        results = self.sp.current_user_top_tracks(limit=20)
        
        if results:
            screen.ids.fetchingtrackstext.text = "Your top tracks are.."
            
            for track in results['items']:
                track_card = UserDetailsTrackCard()
                track_card.ids.user_details_tracks.markup = True
                url = track['external_urls']['spotify']
                
                track_card.ids.user_details_tracks.text = f"[color=#0C1843]{track['name']}[/color] by {track['artists'][0]['name']}"
                track_card.ids.view_button.bind(on_release=partial(self.open_spotify, url))
                
                screen.ids.tracks_container.add_widget(track_card)
        else:
            print("User has no top tracks")


    def viewArtistsFollowed(self):  
        self.resetScreen2()
        
        screen = self.sm.get_screen("screen2")
        try:
            results = self.sp.current_user_followed_artists()

            if results:
                screen.ids.artistsfollowed.text = "Your currently followed artists are.."
                
                for artist in results['artists']['items']:
                    track_card = artistsFollowedTrackCard()
                    track_card.ids.artistsfollowedtext.markup = True
                    track_card.ids.artistsfollowedtext.text = f"{artist['name']}"
                    
                    screen.ids.tracks2_container.add_widget(track_card)   
            else:
                print("User follows no artists.")
        except Exception as e:
            print(f"\033[31mAn Error occured while fetching followed artists {e}\033[0m")


    def viewRecentlyPlayed(self):
        self.resetScreen2()
        screen = self.sm.get_screen("screen2")
        
        try:
            screen.ids.recentlyplayed.text = "Your recently played track is.."
            result = self.sp.current_user_recently_played(limit=1)

            if result['items']:
                track_card = recentlyPlayedTrackCard()
                track_card.ids.recentlyplayedTrackText.markup = True
                
                tracks = result['items'][0]['track']
                track_card.ids.recentlyplayedTrackText.text = f"[color=#0C1843]{tracks['name']}[/color] by {tracks['artists'][0]['name']}"
            
                screen.ids.tracks3_container.add_widget(track_card)
            else:
                print("No recent tracks played")
        except Exception as e:
            print(f"\033[31mAn Error occured while fetching followed artists {e}\033[0m")


    def usersTopArtists(self):
        self.resetScreen2()
        screen = self.sm.get_screen("screen2")
        
        try:
            screen.ids.topartists.text = "Fetching your top artists..."
            result = self.sp.current_user_top_artists()

            for artist in result['items']:
                track_card = artistsFollowedTrackCard()
                track_card.ids.topartiststrack.text = f"{artist['name']}"
        
                screen.ids.tracks4_container.add_widget(track_card)
        except Exception as e:
            print(f"\033[31mAn Error occured while fetching followed artists {e}\033[0m")


    def viewCurrentPlaylists(self):
        self.resetScreen2()
        screen = self.sm.get_screen("screen2")
        
        try:
            screen.ids.currentplaylists.text = "Your current playlists are.."
            result = self.sp.current_user_playlists()

            for playlist in result['items']:
                track_card = artistsFollowedTrackCard()  
                track_card.ids.curr_playliststext.text = f"{playlist['name']}"

                screen.ids.tracks5_container.add_widget(track_card)
        
        except Exception as e:
            print(f"\033[31mAn Error occured while fetching followed artists {e}\033[0m")
    
    
    def viewSavedAlbums(self):
        self.resetScreen2()
        screen = self.sm.get_screen("screen2")
        
        try:
            screen.ids.liked_albums.text = "Your Liked albums are.."
            result = self.sp.current_user_saved_albums()

            albums = result['items']

            for album in albums:
                track_card = artistsFollowedTrackCard()  
                track_card.ids.liked_albumstext.text = f"{album['album']['name']}"
                
                if len(albums) == 1:
                    screen.ids.tracks6part_container.add_widget(track_card)
                else:
                    screen.ids.tracks6_container.add_widget(track_card)
                
        except Exception as e:
            print(f"\033[31mAn Error occured while fetching followed artists {e}\033[0m")
    
    
    def viewSavedTracks(self):
        self.resetScreen2()
        screen = self.sm.get_screen("screen2")
        
        try:
            screen.ids.liked_tracks.text = "Your Liked tracks are.."
            result = self.sp.current_user_saved_tracks()

            if result:
                for track in result['items']:
                    track_card = artistsFollowedTrackCard() 
                    track_card.ids.liked_trackstext.markup = True 
                    track_card.ids.liked_trackstext.text = f"[color=#0C1843]{track['track']['name']}[/color] by {track['track']['artists'][0]['name']}"
            
                    if len(track) == 1:
                        screen.ids.tracks6part_container.add_widget(track_card)
                    else:
                        screen.ids.tracks7_container.add_widget(track_card)
            else:
                print("You havent liked any tracks yet!.")
        except Exception as e:
            print(f"\033[31mAn Error occured while fetching followed artists {e}\033[0m")


    def viewCurrentlyPlaying(self):
        self.resetScreen2()
        screen = self.sm.get_screen("screen2")
        
        try:
            screen.ids.currently_playing_track.text = "Your currently playing track is.."
            current_playing = self.sp.currently_playing()
            
            track_card = recentlyPlayedTrackCard()
            track_card.ids.current_playing_trackstext.markup = True

            if current_playing and current_playing['is_playing']:
                track_card.ids.current_playing_trackstext.text = f"[color=#0C1843]{current_playing['item']['name']}[/color] by {current_playing['item']['artists'][0]['name']}"
                screen.ids.tracks8_container.add_widget(track_card)
            else:
                screen.ids.notrackplaying.markup = True
                screen.ids.notrackplaying.text = f"[color=#0C1843]You aren't listening to any tracks yet![/color]"
        except Exception as e:
            print(f"\033[31mAn Error occured while fetching followed artists {e}\033[0m")
    
    def getAIrecommendations(self):
        screen = self.sm.get_screen("screen3")

        if self.sp is None:
            print("Spotify client not found. Logging in...")
            return

        try:
            screen.ids.tracks_container.clear_widgets()
            result = self.sp.current_user_playlists()

            for playlist in result['items']:
                track_card = PlaylistsDisplayTrackCard()
                track_card.ids.curr_playlists.text = f"{playlist['name']}"
                track_card.ids.songcounttext.text = f"songs: {playlist['tracks']['total']}"

                pid = playlist['id']
                pname = playlist['name']

                track_card.ids['enlargeHoverCard'] = track_card.ids.get('enlargeHoverCard')

                track_card.ids['enlargeHoverCard'].bind(on_release=lambda instance, pid=pid, pname=pname: self.open_playlist(pid, pname))
                screen.ids.tracks_container.add_widget(track_card)

        except Exception as e:
            print(f"\033[31mAn Error occurred while fetching playlists: {e}\033[0m")

    def open_playlist(self, pid, pname):
        aiscreen = self.sm.get_screen('aiscreen')
        aiscreen.selected_playlist_id = pid
        aiscreen.selected_playlist_name = pname
        aiscreen.load_playlist_tracks(pid, pname)
        self.sm.current = 'aiscreen'
        
    def CosineSimilarity(self):
        track_ids = [track['id'] for track in self.tracks_list]
        audio_features = sp.audio_features(track_ids)
        
        song_vectors = {}
        for i, features in enumerate(audio_features):
            if features is None: 
                continue
            vector = [
                features['danceability'],
                features['energy'],
                features['valence'],
                features['tempo'],
                features['acousticness'],
                features['instrumentalness']         
            ] 
            song_vectors[track_ids[i]] = vector
            
    def cosine_similarity(a, b):
        return dot(a, b) / (norm(a) * norm(b))
    
    recommendations = {}
    
    for id1, vec1 in song_vectors.items():
        sim_scores = []
        for id2, vec2 in song_vectors.items():
            if id1 == id2:
                continue
            score = cosine_similarity(vec1, vec2)
            sim_scores.append((id2, score))
            
        sim_scores.sort(key=lambda x: x[1], reverse=True)
        top_similar = [item[0] for item in sim_scores[:5]]
        recommendations[id1] = top_similar
        
    def showCosineRec(self, selected_track_id):
        similar_ids = recommendations.get(selected_track_id, [])
        for sid in similar_ids:
            print("Recommended:", track_name_map[sid])
            

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

#------------------------------SCREENS--------------------------------------
class Dashboard(Screen):
    pass
class Screen1(Screen):
    pass
class Screen2(Screen):
    pass

class Screen3(Screen):
    def on_enter(self):
        app = MDApp.get_running_app()
        app.getAIrecommendations()
        
class AIscreen(Screen):
    tracks_list = ListProperty([])
    selected_playlist_id = StringProperty("")
    selected_playlist_name = StringProperty("")
    
    def load_playlist_tracks(self, playlist_id, playlist_name):
        all_tracks = []
        offset = 0
        sp = MDApp.get_running_app().sp

        while True:
            result = sp.playlist_tracks(playlist_id, limit=100, offset=offset)
            items = result.get("items", [])
            if not items:
                break

            for item in items:
                track = item["track"]
                name = track["name"]
                artists = ", ".join([a["name"] for a in track["artists"]])
                all_tracks.append(f"{name} - {artists}")
            offset += len(items)

        self.tracks_list = all_tracks
        self.displayTracks()

    def displayTracks(self):
        container = self.ids.tracks_container
        container.clear_widgets()

        for track in self.tracks_list:
            label = Label(
                text=track,
                size_hint_y=None,
                height=55,
                halign='left',
                valign='middle',
                font_size=22,
                color=(0.678, 0.129, 0.278, 1),
                text_size=(850, 55),
                font_name="tracksfont/Noto_Sans_JP/static/NotoSansJP-Bold.ttf"
            )
            label.bind(
                texture_size=lambda instance, size: setattr(instance, 'height', size[1]),
                size=label.setter('text_size')
            )
            container.add_widget(label)        
        
class TrackCard(BoxLayout):
    pass
class UserDetailsTrackCard(BoxLayout):
    pass
class artistsFollowedTrackCard(BoxLayout):
    pass
class recentlyPlayedTrackCard(BoxLayout):
    pass
class PlaylistsDisplayTrackCard(BoxLayout):
    pass

class WindowManager(ScreenManager):
    pass
  
#------------------------HOVER ANIMATIONS--------------------------------
class HoverButton(Button, HoverBehavior):
    radius = ListProperty([18])
    bg_color = ListProperty([0.384, 0.141, 0.353, 1])
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_down = ''
        self.background_color = 0,0,0,0

    def on_enter(self):
        Window.set_system_cursor("hand")
        self.bg_color = [0.302, 0.071, 0.192, 1]
        self.radius = [18]
        
    def on_leave(self):
        Window.set_system_cursor("arrow")
        self.bg_color = [0.384, 0.141, 0.353, 1]
        self.radius = [18]
        
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
        
class mainoptions(HoverBehavior, ButtonBehavior, Image):
    mood_name = StringProperty("")
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(pos=self._update_hover_area, size=self._update_hover_area)
        self.original_y = None

    def _update_hover_area(self, *args):
        pass
    
    def on_enter(self):
        Window.set_system_cursor("hand")
        if self.original_y is None:
            self.original_y = self.y

        Animation.cancel_all(self) 
        Animation(y=self.original_y + 10, duration=0.15).start(self)

    def on_leave(self):
        Window.set_system_cursor("arrow")

        Animation.cancel_all(self)
        Animation(y=self.original_y, duration=0.15).start(self)

class BasicImageHover(ButtonBehavior, HoverBehavior, Image):
    def on_enter(self):
        Window.set_system_cursor("hand")
        
    def on_leave(self):
        Window.set_system_cursor("arrow")
        
class BasicButtonHover(Button, HoverBehavior):
    def on_enter(self):
        Window.set_system_cursor("hand")
        
    def on_leave(self):
        Window.set_system_cursor("arrow")
        
class EnlargeHover(HoverBehavior, ButtonBehavior, Image):
    mood_name = StringProperty("")
    scale = NumericProperty(1.0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._scale_transform = Scale(1.0, 1.0, 1.0)
        with self.canvas.before:
            PushMatrix()
            self._scale_transform = Scale(1.0, 1.0, 1.0, origin=self.center)
        with self.canvas.after:
            PopMatrix()

        self.bind(pos=self._update_origin, size=self._update_origin)
        self.bind(scale=self._apply_scale)
        Clock.schedule_once(self._update_origin, 0)

    def _update_origin(self, *args):
        self._scale_transform.origin = self.center

    def _apply_scale(self, instance, value):
        self._scale_transform.x = value
        self._scale_transform.y = value

    def on_enter(self):
        Window.set_system_cursor("hand")
        Animation.cancel_all(self)
        Animation(scale=1.1, duration=0.2, t='out_quad').start(self)

    def on_leave(self):
        Window.set_system_cursor("arrow")
        Animation.cancel_all(self)
        Animation(scale=1.0, duration=0.2, t='out_quad').start(self)


MainApp().run()
