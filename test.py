import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Authentication with Spotify API
client_id = '48d62bb1397c400382b30fd056127305'  # Replace with your Spotify Client ID
client_secret = 'a52c56fac25d4f65b3a9d34bc43492ee'  # Replace with your Spotify Client Secret
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def get_tracks_by_mood(mood):
    # Example of mood-based genres (can also try with artist or track seeds)
    mood_genres = {
        'happy': ['pop', 'dance', 'house'],
        'sad': ['acoustic', 'indie-pop', 'alternative'],
        'energetic': ['rock', 'punk', 'metal'],
        'chill': ['ambient', 'lo-fi', 'jazz']
    }

    if mood.lower() not in mood_genres:
        print("Mood not recognized. Please enter a valid mood.")
        return

    # Fetch recommended tracks based on mood genres
    genres = mood_genres[mood.lower()]
    
    # Try to get recommendations
    try:
        recommendations = sp.recommendations(seed_genres=genres, limit=10)
        print(f"Here are some {mood} tracks for you:\n")

        for track in recommendations['tracks']:
            track_name = track['name']
            track_artist = track['artists'][0]['name']
            track_url = track['external_urls']['spotify']
            print(f"Track: {track_name}\nArtist: {track_artist}\nListen: {track_url}\n")
    except Exception as e:
        print(f"Error fetching recommendations: {e}")
        print(f"Attempting recommendations without seed_genres...")
        # Try a fallback approach without seed_genres
        try:
            recommendations = sp.recommendations(limit=10)
            print("Fallback recommendations:\n")
            for track in recommendations['tracks']:
                track_name = track['name']
                track_artist = track['artists'][0]['name']
                track_url = track['external_urls']['spotify']
                print(f"Track: {track_name}\nArtist: {track_artist}\nListen: {track_url}\n")
        except Exception as fallback_error:
            print(f"Error fetching fallback recommendations: {fallback_error}")

if __name__ == '__main__':
    user_mood = input("Enter your mood (happy, sad, energetic, chill): ").strip()
    get_tracks_by_mood(user_mood)