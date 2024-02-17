import tkinter as tk
from tkinter import Scrollbar, messagebox
import customtkinter
from controller import getter
from PIL import Image, ImageTk
from controller.spotCreator import extract_ytb_playlist_name, create_spotify_playlist
from controller.ytbCreator import extract_spotify_playlist_name, create_youtube_playlist
from gui.colors import colored_text, ConsoleColors
import threading

# Functions
def getTracks():
    playlist_url = url.get()
    if "youtube.com" in playlist_url:
        tracks = getter.get_youtube_tracks(playlist_url)
        print(f"You{colored_text("Tube", ConsoleColors.BACKGROUND_RED)} playlist found! {len(tracks)} tracks imported.")
    elif "spotify.com" in playlist_url:
        tracks = getter.get_spotify_tracks(playlist_url)
        print(f"{colored_text('Spotify', ConsoleColors.BACKGROUND_GREEN)} playlist found! {len(tracks)} tracks imported.")
    else:
        print("Invalid URL. Please enter a valid YouTube or Spotify playlist URL.")

    # Clear list
    listbox.delete(0, tk.END)

    # Add tracks to list
    for index, track in enumerate(tracks, start=1):
        if 'artist' in track:
            listbox.insert(tk.END, f"{index}. {track['artist']} - {track['name']}")
        else:
            listbox.insert(tk.END, f"{index}. {track['title']}")
            
def convert():
    # Show pop-up
    def show_popup():
        tk.messagebox.showinfo("Converting", "The process is ongoing. Check the console for more information or please wait...")

    threading.Thread(target=show_popup).start()

    playlist_url = url.get()
    if "youtube.com" in playlist_url:
        spotify_playlist_name = extract_ytb_playlist_name(playlist_url)
        threading.Thread(target=create_spotify_playlist, args=(playlist_url, spotify_playlist_name)).start()
    elif "spotify.com" in playlist_url:
        youtube_playlist_name = extract_spotify_playlist_name(playlist_url)
        threading.Thread(target=create_youtube_playlist, args=(playlist_url, youtube_playlist_name)).start()
    else:
        print("Invalid URL. Please enter a valid YouTube or Spotify playlist URL.")
        

# System settings
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

# App frame
root = customtkinter.CTk()
root.geometry("810x540")
root.title("BridgeBeats - Your music playlist converter!")

# Elements
font = customtkinter.CTkFont(family="Cascadia Code PL")
title = customtkinter.CTkLabel(root, text="Insert a YouTube/Spotify link to get started!", font=font)
title.pack()
subtitle = customtkinter.CTkLabel(root, text="BETA TEST WARNING: This tool is in development stage. API bugs still happening :(", font=font, text_color="#303030")
subtitle.pack()

# Link Input
url = tk.StringVar()
link = customtkinter.CTkEntry(root, width=450, height=40, textvariable=url)
link.pack()

# Get tracks button
getTracksButton = customtkinter.CTkButton(root, text="Get Tracks", command=getTracks, fg_color="#FC6736", text_color="#1A1A1A", hover=True, hover_color="#c9552e", font=font)
getTracksButton.pack(padx=10, pady=10)

# Scrollable listbox
frame = tk.Frame(root)
frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

scrollbar = Scrollbar(frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

listbox = tk.Listbox(frame, yscrollcommand=scrollbar.set, font=font)
listbox.configure(bg="#343638", fg="#D6D6D6", selectbackground="#FC6736")
listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar.config(command=listbox.yview)

# Convert button
convertButton = customtkinter.CTkButton(root, text="Convert", command=convert, fg_color="#FC6736", text_color="#1A1A1A", hover=True, hover_color="#c9552e", font=font)
convertButton.pack(padx=10, pady=10)

# Add logo
logo_loc = "gui/assets/bridgebeats.jpg"
logo = Image.open(logo_loc)
logo = logo.resize((130, 130))
logo = ImageTk.PhotoImage(logo)
canvas = tk.Canvas(root, width=130, height=130, borderwidth=0, highlightthickness=0)
canvas.pack()
canvas.create_image(0, 0, anchor="nw", image=logo)

# Run app
def run():
    root.mainloop()
