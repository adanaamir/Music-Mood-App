from dotenv import load_dotenv   
import os, spotipy
from spotipy.oauth2 import SpotifyOAuth

load_dotenv()

if os.path.exists(".cache"):
    os.remove(".cache")
    
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
redirect_url = "https://oauth.pstmn.io/v1/browser-callback"  

scope = "playlist-read-private"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_url,scope=scope))

results= sp.current_user_playlists()
for idx, item in enumerate(results['items']):
    print(idx+1, item['name'])