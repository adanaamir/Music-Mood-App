import spotipy
from spotipy.oauth2 import SpotifyOAuth

red = "\033[31m"
blue = "\033[34m"
reset = "\033[0m"
yellow = "\033[33m"

option = {
1: "View your top tracks.",
2: "View your currently followed artist.",
3: "View your curently following users.",
4: "View your currently following playlist.",
5: "View your recently played.",
6: "View your top artists.",
7: "View your current playlists.",
8: "View your saved albums.",
9:" View your saved tracks.",
10: "View currently playing."
}
print(f"Hi! Ready to explore your Spotify Data?\nHere's what you can do:")
for key, val in option.items:
    print(f"{key} - {val}")

while True:
    try:
        op = int(input("Enter your option by number(1-10) "))
        if op in option:
            break
        else:
            print(f"{red}Error: Not an option.{reset}") 
    except ValueError:
        print(f"{red}Error: Invalid type \"str\" entered. Enter an int{reset}")

    redirect_url = "https://oauth.pstmn.io/v1/browser-callback"   #url and scope will go in __init__
    scope = (
        "user-top-read"
        "user-follow-read"
        "playlist-read-private"
        "user-read-recently-played "
        "user-library-read "
        "user-read-playback-state"
    )
def UserData():
    if op == 1:
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_url))
        results = sp.current_user_top_tracks(limit=10)
        for idx, track in enumerate(results['tracks']):
            print(f"{idx+1} Track: {yellow}{track['name']}{reset} by {track['artists'][0]['name']}, URL: {blue}{track['external_urls']['spotify']}{reset}")
    elif op == 2:
        results = sp.
        for artist in f