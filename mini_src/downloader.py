import pytube
import customtkinter as ctk
from tkinter.filedialog import askdirectory
from tkinter.messagebox import askokcancel


class Downloading:
    def __init__(self, master_display) -> None:
        self.master = master_display
        self.can_download = True


    def destroy(self):
        self.master.destroy()


    def download_video(self, video_url:str, download_location:str) -> None:
        video = pytube.YouTube(video_url)
        try:
            video.streams.get_audio_only().download(download_location)
        except:
            askokcancel(title="Error", message=f"Download error while downloading\n{video_url}")


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
                    playlist = pytube.Playlist(url)
                    video_names = [v.title for v in playlist.videos]

                    for k, v in enumerate(playlist.video_urls):
                        self.url_label.configure(text=video_names[k])
                        self.download_process.download_video(v, loc)
                else:
                    self.download_video(video_url=url, download_location=loc)
            else:
                print("CANT DOWNLOAD")

            self.url_entry.configure(state="normal")
            askokcancel(title="Done", message="Download completed")

        else:
            askokcancel(title="Invalid link", message="Download link is invalid")

        self.reset_button()
        self.can_download = True