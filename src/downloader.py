import pytube
import os
import customtkinter as ctk
from tkinter.filedialog import askdirectory
from tkinter.messagebox import askokcancel
from tkinter.ttk import Progressbar

class Downloader:
    def __init__(self, display, super_display) -> None:
        self.url = ctk.StringVar(master=display)
        self.url_entry = ctk.CTkEntry(display, textvariable=self.url, placeholder_text="https://www.youtube.com/")
        self.url_entry.place(relx=0.35, rely=0.55, relwidth=0.3, relheight=0.06)

        self.label = ctk.CTkLabel(display, text="Download from Youtube", font=("Arial", 20, "bold"))
        self.label.place(relx=0.35, rely=0.2, relwidth=0.3, relheight=0.1)
        self.url_label = ctk.CTkLabel(display, text="Paste video or playlist url")
        self.url_label.place(relx=0.35, rely=0.65, relwidth=0.3, relheight=0.06)

        self.download_button = ctk.CTkButton(display,text="Download", command=self.choose_download)
        self.download_button.place(relx=0.4, rely=0.85, relwidth=0.2, relheight=0.1)

        self.super_display = super_display
        self.downloading = None

        self.downloading_bar_object = None


    def downloading_bar(self):
        self.downloading = ctk.CTkToplevel(self.super_display)
        self.downloading.geometry("400x150")

        self.downloading_bar_object = Progressbar(self.downloading, mode="determinate", orient="horizontal")
        self.downloading_bar_object.place(relx=0.15, rely=0.5, relwidth=0.8, relheight=0.1)
        

    def download_playlist(self, playlist_url:str, download_location:str) -> None:
        playlist = pytube.Playlist(playlist_url)
        video_names = [v.title for v in playlist.videos]

        for i in range(len(playlist.video_urls)):
            v_object = pytube.YouTube(playlist.video_urls[i])
            
            try:
                v_object.streams.get_audio_only().download(download_location)
            except:
                askokcancel(title="Error", message=f"Download error while downloading\n{playlist.video_urls[i]}")

            self.downloading_bar_object['value'] += 100 / len(playlist.video_urls)

    def download_video(self, video_url:str, download_location:str) -> None:
        video = pytube.YouTube(video_url)
        try:
            video.streams.get_audio_only().download(download_location)
        except:
            askokcancel(title="Error", message=f"Download error while downloading\n{video_url}")
        self.downloading_bar_object['value'] = 100


    def choose_download(self) -> None:

        if self.url.get() == "":
            askokcancel(title="Invalid link", message="Download link is invalid")
            return
        
        loc = askdirectory(title="Choose download directory")     

        url = self.url.get().strip()
        if url.startswith("https://www.youtube.com/") and url != "https://www.youtube.com/":
            self.url_entry.configure(state="disabled")
            self.download_button.configure(state="disabled")
            self.downloading_bar()
            
            if "www.youtube.com/playlist?list=" in url:
                self.download_playlist(playlist_url=url, download_location=loc)
            else:
                self.download_video(video_url=url, download_location=loc)

            self.url_entry.configure(state="normal")
            self.download_button.configure(state="normal")
            self.downloading.destroy()
            askokcancel(title="Done", message="Download completed")

        else:
            askokcancel(title="Invalid link", message="Download link is invalid")