import spotipy
import youtube_dl
from spotipy.oauth2 import SpotifyOAuth
from controller import getter
from secret.credentials import Credentials
from gui.colors import colored_text, ConsoleColors

def extract_ytb_playlist_name(youtube_playlist_url):
    # Extract playlist name from YouTube URL
    with youtube_dl.YoutubeDL({}) as ydl:
        info = ydl.extract_info(youtube_playlist_url, download=False)
        return info.get('title')

def create_spotify_playlist(youtube_playlist_url, spotify_playlist_name):
    # Get tracks from YouTube playlist
    youtube_tracks = getter.get_youtube_tracks(youtube_playlist_url)
    if not youtube_tracks:
        print("The YouTube playlist could not be found or accessed. Please check the URL and try again.")
        return

    # Extract original playlist name
    original_playlist_name = extract_ytb_playlist_name(youtube_playlist_url)
    
    # Sign the description
    description = f"This '{original_playlist_name}' playlist was created by BridgeBeats. For more, visit github.com/lilrau."

    # Authenticate with Spotify API
    client_id = Credentials().get_id()
    client_secret = Credentials().get_secret()
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret,redirect_uri='http://localhost:8888/callback', scope='playlist-modify-public'))

    # Create a new playlist on Spotify
    playlist = sp.user_playlist_create(sp.me()['id'], spotify_playlist_name, public=True, description=description)

    # Add tracks to the playlist in batches of 100
    for i in range(0, len(youtube_tracks), 100):
        batch = youtube_tracks[i:i+100]
        track_uris = []
        for track in batch:
            # Search for the track on Spotify
            results = sp.search(q=f"{track['title']}", type='track', limit=1)
            if results['tracks']['items']:
                track_uri = results['tracks']['items'][0]['uri']
                track_uris.append(track_uri)
                print(f"Found track {colored_text(track['title'], ConsoleColors.GREEN)} on Spotify. URI: {track_uri}")
            else:
                print(colored_text(f"Track '{track['title']}' NOT found on Spotify.", ConsoleColors.RED))

        if track_uris:
            sp.playlist_add_items(playlist_id=playlist['id'], items=track_uris)
            print(f"Added {len(track_uris)} tracks to the playlist.")
        else:
            print("None of the tracks from the YouTube playlist could be found on Spotify.")
