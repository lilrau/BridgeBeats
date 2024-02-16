import spotipy
import youtube_dl
from spotipy.oauth2 import SpotifyClientCredentials
from secret.credentials import Credentials

# Function to get tracks from Spotify playlist
def get_spotify_tracks(playlist_url):
    # Authenticate with Spotify API
    client_id = Credentials().get_id()
    client_secret = Credentials().get_secret()
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))

    # Extract playlist ID from the URL
    playlist_id = playlist_url.split('/')[-1].split('?')[0]

    # Get tracks from the playlist
    tracks = []
    results = sp.playlist_tracks(playlist_id)
    for item in results['items']:
        track_info = item['track']
        tracks.append({'artist': track_info['artists'][0]['name'], 'name': track_info['name']})
    return tracks

# Function to get tracks from YouTube playlist
def get_youtube_tracks(playlist_url):
    ydl_opts = {'extract_flat': 'in_playlist'}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(playlist_url, download=False)
        # Extract video titles
        tracks = [{'title': entry['title']} for entry in info_dict['entries']]
    return tracks
