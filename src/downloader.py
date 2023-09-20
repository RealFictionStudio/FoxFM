import pytube
import os

def download_playlist(playlist_url:str, download_location:str):
    playlist = pytube.Playlist(playlist_url)
    video_names = [v.title for v in playlist.videos]

    for i in range(len(playlist.video_urls)):
        v_object = pytube.YouTube(playlist.video_urls[i])
        try:
            v_object.streams.get_audio_only().download(download_location)
        except:
            continue

        os.rename(download_location + video_names[i] + ".mp4", download_location + video_names[i] + ".wav")


def download_video(video_url, download_location):
    video = pytube.YouTube(video_url)
    try:
        video.streams.get_audio_only().download(download_location)
    except:
        ...