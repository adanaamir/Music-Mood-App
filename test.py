import os, spotipy
from spotipy.oauth2 import SpotifyClientCredentials

if os.path.exists(".cache"):
    os.remove(".cache")

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id= "48d62bb1397c400382b30fd056127305", client_secret= "a52c56fac25d4f65b3a9d34bc43492ee"))

genres = sp.recommendation_genre_seeds()
print("Available genres for recommendations:")
for genre in genres['genres']:
    print(genre)