import os
from pytube import YouTube, request
from tkinter.messagebox import askokcancel
from tkinter.filedialog import askdirectory

def download_video(video_url:str, download_location:str) -> None:
        try:
            video = YouTube(video_url)

            stream = video.streams.get_audio_only()
            filesize = stream.filesize

            if f"{video.title}.mp4" in os.listdir(download_location):
                print("FILE EXIST")
                with open(f"{download_location}{os.sep}{video.title}.mp4", 'wb') as f:
                    f.write("".encode())

            with open(f"{download_location}{os.sep}{video.title}.mp4", 'wb') as f:
                stream = request.stream(stream.url)
                downloaded = 0

                while True:

                    chunk = next(stream, None)
                    print("CHUNK")
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        #self.loading_bar.set(downloaded / filesize)
                    else:
                        break
        except Exception as e:
            print(e)
            askokcancel(title="Error occured", message=str(e))


download_video(input("URL: "), askdirectory())