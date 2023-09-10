from moviepy.editor import concatenate_audioclips, concatenate_videoclips, AudioFileClip, VideoFileClip, CompositeVideoClip, CompositeAudioClip, preview
import customtkinter as ctk
from tkinter import filedialog
from widgets.audioclip import AudioClip

class Editor:

    def __init__(self, display:ctk.CTkTabview) -> None:
        
        self.display = display

        self.audio_files = []
        self.video_files = []

        self.joined_audio:AudioFileClip
        self.joined_video:VideoFileClip
        self.is_no_audio_update = True
        self.is_no_video_update = True

    
    def load_audio(self):
        audio_files = filedialog.askopenfilenames(title="Open audio file", filetypes=(("MP3 (Lossy compression)", "*.mp3"),
                                                                        ("Wave (Lossless compression)", "*.wav")))
        for file in audio_files:
            AudioClip(self.display, file)

    def add_audio_to_queue(self, file_name:str) -> None:
        self.audio_files.append(AudioFileClip(file_name))
        self.is_no_audio_update = False


    def delete_audio_from_queue(self, clip_name:str) -> None:
        self.audio_files.pop(clip_name)
        self.is_no_audio_update = False


    def add_video_to_clip(self, file_name:str) -> None:
        self.video_files.append(VideoFileClip(file_name))
        self.is_no_video_update = False


    def delete_video_from_clip(self, clip_name:str) -> None:
        self.video_files.pop(clip_name)
        self.is_no_video_update = False


    def join_all_audio(self) -> bool:
        if len(self.audio_files) > 0:
            self.joined_audio = concatenate_audioclips(self.audio_files)
            self.is_no_audio_update = True
            return True
        else:
            return False

    
    def join_all_video(self) -> bool:
        if len(self.video_files) > 0:
            self.joined_video = concatenate_videoclips(self.video_files)
            self.is_no_video_update = True
            return True
        else:
            return False
        

    def play_test_audio(self) -> None:
        if not self.is_no_audio_update:
            self.join_all_audio()

        preview(self.joined_audio)


    def play_test_video(self) -> None:
        if not self.is_no_video_update:
            self.join_all_video()

        # preview video
        

    def play_test_whole_clip(self) -> None:
        ...


    def export_audio(self, file_name:str="output_audio") -> bool:
        if not self.join_all_audio():
            return False
        
        self.joined_audio.write_audiofile(file_name + ".wav")
        return True
    

    def export_video(self, file_name:str="output_video") -> bool:
        if not self.join_all_video():
            return False

        self.joined_video.write_videofile(file_name + ".mp4")
        return True   
    
    
    def export_whole_clip(self, mode:bool, file_name:str="output") -> bool:
        # True -> based on audio length
        # False -> based on video length

        if not self.join_all_audio() and mode or not self.join_all_video() and not mode:
            return False

        if mode:
            duration = self.joined_audio.duration
            final_video = CompositeVideoClip([self.joined_video.set_duration(duration)])

            export = final_video.set_audio(self.joined_audio)
            export.write_videofile(file_name + ".mp4")
        
        else:
            duration = self.joined_video.duration
            final_audio = CompositeAudioClip([self.joined_audio.set_duration(duration)])

            export = self.joined_video.set_audio(final_audio)
            export.write_videofile(file_name + ".mp4", fps=32)

        return True
        


