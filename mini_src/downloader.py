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
        self.loading_bar = ctk.CTkProgressBar(self.download_toplevel, orientation='horizontal', mode='determinate')
        self.download_title = ctk.CTkLabel(self.download_toplevel, text="")
        self.video_count_label = ctk.CTkLabel(self.download_toplevel, text="0/0")
        self.cancel_button = ctk.CTkButton(self.download_toplevel, text="Cancel", command=self.destroy)

        self.video_count = 0
        self.current_video_count = 0


    def destroy(self) -> None:
        self.download_toplevel.destroy()
        self.can_download = False


    def add_download_ui(self) -> None:
        self.loading_bar.pack()
        self.download_title.pack()
        self.cancel_button.place(x=350, y=80)


    def update_video_count(self):
        self.current_video_count += 1
        self.video_count_label.configure(text=f"{self.current_video_count}/{self.video_count}")

        if self.can_download and self.video_count == self.current_video_count:
            askokcancel(title="Download Progress", message="Download Compleated!")
            self.destroy()


    def start_download(self, urls:list[str], location:str) -> None:
        self.can_download = True
        self.video_count = len(urls)
        self.download_toplevel = ctk.CTkToplevel(self.master)
        self.download_toplevel.geometry("400x100")
        self.download_toplevel.protocol("WM_DELETE_WINDOW", self.destroy)
        self.download_toplevel.resizable(False, False)
        self.video_count = len(urls)
        self.add_download_ui()

        for url in urls:
            if self.can_download:
                threading.Thread(target=self.download_video, args=(url, location), daemon=True)

    def download_video(self, video_url:str, download_location:str) -> None:
        try:
            video = YouTube(video_url)
            stream = video.streams.get_audio_only()
            filesize = stream.filesize

            with open(f"{download_location}{os.sep}{video.title}.mp4", 'wb') as f:
                stream = request.stream(stream.url)
                downloaded = 0

                while True:
                    if not self.can_download:
                        break

                    chunk = next(stream, None)
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        self.loading_bar.set(downloaded / filesize)
                    else:
                        break
        except:
            askokcancel(title="Error", message=f"Download error while downloading\n{video_url}")

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

        self.download_button = ctk.CTkButton(display,text="Download", fg_color="green", command=self.start_download)
        self.download_button.place(relx=0.4, rely=0.85, relwidth=0.2, relheight=0.1)

        self.super_display = super_display
        
        self.download_process = Downloading(display)


    def start_download(self):
        if self.can_download:
            self.download_thread = threading.Thread(target=self.make_download(), daemon=True)
            self.download_thread.start()
        else:
            self.can_download = False
            self.download_button.configure(text="Configure...")

    
    def reset_button(self) -> None:
        self.download_button.configure(fg_color="green", text="Download")
        self.url_label.configure(text="Paste video or playlist url")


    def make_download(self) -> None:

        if self.url.get() == "":
            askokcancel(title="Invalid link", message="Download link is invalid")
            return

        url = self.url.get().strip()

        if url.startswith("https://www.youtube.com/") or url.startswith("https://youtube.com/") or url.startswith("https://youtu.be/"):

            loc = askdirectory(title="Choose download directory")

            if type(loc) == tuple:
                print("EMPTY DIR")
                return
            
            self.download_button.configure(state="disabled")
            self.url_entry.configure(state="disabled")
            
            if self.can_download:
                if "playlist?list=" in url:
                    playlist = Playlist(url)
                    self.download_process.start_download(list(playlist.video_urls()), loc)
                else:
                    self.download_process.start_download([url], loc)
            else:
                print("CANT DOWNLOAD")

            self.url_entry.configure(state="normal")
            askokcancel(title="Done", message="Download completed")

        else:
            askokcancel(title="Invalid link", message="Download link is invalid")

        self.reset_button()
        self.can_download = True