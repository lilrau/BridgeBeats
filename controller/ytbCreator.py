import os
import googleapiclient.discovery
import googleapiclient.errors
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from google_auth_oauthlib.flow import InstalledAppFlow
from secret.credentials import Credentials
from controller import getter
from gui.colors import colored_text, ConsoleColors

# Define the scopes
SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]

def extract_spotify_playlist_name(spotify_playlist_url):
    # Initialize Spotipy client
    client_credentials_manager = SpotifyClientCredentials(Credentials().get_id(), Credentials().get_secret())
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    # Extract playlist ID from URL
    playlist_id = spotify_playlist_url.split('/')[-1]

    # Get playlist details
    playlist = sp.playlist(playlist_id)

    # Extract playlist name
    playlist_name = playlist['name']

    return playlist_name

def create_youtube_playlist(spotify_playlist_url, youtube_playlist_name):
    # Define the scopes
    SCOPES = ["https://www.googleapis.com/auth/youtube"]

    # Load the credentials from json
    creds = None
    if os.path.exists('ytb_credentials/client_secret.json'):
        creds = InstalledAppFlow.from_client_secrets_file(
            'ytb_credentials/client_secret.json', SCOPES).run_local_server(port=0)

    # Construa o serviço YouTube API usando as credenciais
    youtube = googleapiclient.discovery.build('youtube', 'v3', credentials=creds)

    # Create YouTube playlist
    try:
        request = youtube.playlists().insert(
            part="snippet,status",
            body={
                "snippet": {
                    "title": youtube_playlist_name,
                    "description": f"This playlist was created from {youtube_playlist_name} using BridgeBeats. For more, acess github.com/lilrau.",
                    "tags": ["BridgeBeats"]
                },
                "status": {
                    "privacyStatus": "public"  # Change this to "private" if you want a private playlist
                }
            }
        )
        response = request.execute()
        playlist_id = response["id"]
        print(f"{colored_text('Playlist created successfully!', ConsoleColors.BACKGROUND_GREEN)} Playlist ID:", playlist_id)

        # Get tracks from Spotify playlist
        spotify_tracks = getter.get_spotify_tracks(spotify_playlist_url)

        # Add tracks to the YouTube playlist
        for track in spotify_tracks:
            try:
                # Search for the track on YouTube
                search_response = youtube.search().list(
                    q=f"{track['artist']} - {track['name']}",
                    part="id",
                    maxResults=1
                ).execute()

                # Add the first result to the playlist
                video_id = search_response["items"][0]["id"]["videoId"]
                youtube.playlistItems().insert(
                    part="snippet",
                    body={
                        "snippet": {
                            "playlistId": playlist_id,
                            "position": 0,
                            "resourceId": {
                                "kind": "youtube#video",
                                "videoId": video_id
                            }
                        }
                    }
                ).execute()

                print(f"Added {colored_text({track['artist']} - {track['name']}, ConsoleColors.GREEN)} to the playlist.")
            except Exception as e:
                print(f"{colored_text(f"Error adding {track['artist']} - {track['name']} to the playlist:", ConsoleColors.RED)}", e)

    except googleapiclient.errors.HttpError as e:
        print(f"{colored_text('An error occurred while creating the playlist:', ConsoleColors.RED)}", e)
        return
