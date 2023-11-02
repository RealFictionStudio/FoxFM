from pytube import YouTube, Playlist, request
import customtkinter as ctk
from tkinter.filedialog import askdirectory
from tkinter.messagebox import askokcancel
import threading
import os

class Downloading:
    def __init__(self, master_display) -> None:
        self.master = master_display
        self.can_download = True
        
        self.download_toplevel:ctk.CTkToplevel
        self.loading_bar:ctk.CTkProgressBar
        self.cancel_button:ctk.CTkButton
        self.download_title:ctk.CTkLabel

        self.video_count = 0
        self.current_video_count = 0


    def destroy(self) -> None:
        self.download_toplevel.destroy()
        self.can_download = False
        print("\nDOWNLOAD END\n")


    def add_download_ui(self) -> None:
        self.loading_bar = ctk.CTkProgressBar(self.download_toplevel, orientation='horizontal', mode='determinate')
        self.loading_bar.set(0)
        self.cancel_button = ctk.CTkButton(self.download_toplevel, text="Cancel", command=self.destroy)
        self.loading_bar.place(x=100, y=100)
        self.cancel_button.place(x=130, y=250)
        self.download_title = ctk.CTkLabel(self.download_toplevel, text="", anchor="center")
        self.download_title.place(x=20, y=120)


    def update_video_count(self):
        self.current_video_count += 1

        if self.can_download and self.video_count == self.current_video_count:
            askokcancel(title="Download Progress", message="Download Compleated!")
            self.destroy()


    def start_download(self, urls:list[str], location:str) -> None:
        print("DOWNLOADING START DOWNLOAD")
        self.can_download = True
        self.video_count = len(urls)
        self.download_toplevel = ctk.CTkToplevel(self.master)
        self.download_toplevel.geometry("400x300")
        self.download_toplevel.title("Downloading...")
        self.download_toplevel.protocol("WM_DELETE_WINDOW", self.destroy)
        self.download_toplevel.resizable(False, False)
        self.video_count = len(urls)
        self.add_download_ui()

        for url in urls:
            if self.can_download:
                print("VIDEO START DOWNLOAD")
                self.loading_bar.set(0)
                self.download_video(url, location)


    def download_video(self, video_url:str, download_location:str) -> None:
        print("DOWNLOADING")
        try:
            video = YouTube(video_url)
            self.download_title.configure(text=video.title)
            stream = video.streams.get_audio_only()
            filesize = stream.filesize

            with open(f"{download_location}{os.sep}{video.title}.mp4", 'wb') as f:
                stream = request.stream(stream.url)
                downloaded = 0

                while True:
                    if not self.can_download:
                        break

                    chunk = next(stream, None)
                    print("CHUNK")
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        self.loading_bar.set(downloaded / filesize)
                    else:
                        break
        except:
            pass

        self.update_video_count()


class Downloader:
    def __init__(self, display, super_display) -> None:
        self.url = ctk.StringVar(master=display)
        self.url_entry = ctk.CTkEntry(display, textvariable=self.url, placeholder_text="https://www.youtube.com/")
        self.url_entry.place(relx=0.35, rely=0.55, relwidth=0.3, relheight=0.06)

        self.label = ctk.CTkLabel(display, text="Download from Youtube", font=("Arial", 20, "bold"))
        self.label.place(relx=0.35, rely=0.2, relwidth=0.3, relheight=0.1)
        self.url_label = ctk.CTkLabel(display, text="Paste video or playlist url")
        self.url_label.place(relx=0.35, rely=0.65, relwidth=0.3, relheight=0.06)

        self.download_button = ctk.CTkButton(display,text="Download", command=self.make_download)
        self.download_button.place(relx=0.4, rely=0.85, relwidth=0.2, relheight=0.1)

        self.super_display = super_display
        
        self.download_process = Downloading(display)


    def make_download(self) -> None:

        if self.url.get() == "":
            askokcancel(title="Invalid link", message="Download link is invalid")
            return

        url = self.url.get().strip()

        loc = askdirectory(title="Choose download directory")

        if type(loc) == tuple:
            print("EMPTY DIR")
            return
            
        if "playlist?list=" in url:
            playlist = Playlist(url)
            threading.Thread(target=self.download_process.start_download, args=(list(playlist.video_urls), loc), daemon=True).start()
        else:
            threading.Thread(target=self.download_process.start_download, args=([url], loc), daemon=True).start()
            