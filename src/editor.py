from moviepy.editor import concatenate_audioclips, concatenate_videoclips, AudioFileClip, VideoFileClip, CompositeVideoClip, CompositeAudioClip, preview
import customtkinter as ctk
from tkinter import filedialog
from widgets.clips import VideoClip, AudioClip
from widgets.scroll_object import Scroll_Object


class Editor:

    def __init__(self, display:ctk.CTkTabview) -> None:
        
        self.display = display

        self.audio_files = []
        self.video_files = []

        self.joined_audio:AudioFileClip
        self.joined_video:VideoFileClip
        self.is_no_audio_update = True
        self.is_no_video_update = True

        self.tabview = ctk.CTkTabview(master=display)
        self.tabview.place(relx=0.02, rely=0, relwidth=0.25, relheight=0.8)

        self.tabview.add("audio")
        self.tabview.add("video")
        self.tabview.set("audio")

        self.audio_files_widgets = Scroll_Object(self.tabview.tab("audio"), width=300, height=400)
        self.audio_files_widgets.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.clip_load_button = ctk.CTkButton(display, text="Load Files", command=self.load_files)
        self.clip_load_button.place(relx=0.04, rely=0.9, relwidth=0.2, relheight=0.08)

        self.video_files_widgets = Scroll_Object(self.tabview.tab("video"), width=300, height=550)
        self.video_files_widgets.place(relx=0, rely=0, relwidth=1, relheight=1)


    def load_files(self):
        video_file_types = [".mp4"]
        audio_file_types = [".mp3", ".wav"]

        opened_files = filedialog.askopenfilenames(title="Open audio file", filetypes=(("audio files", audio_file_types),
                                                                                       ("video files", video_file_types)))
        for file in opened_files:
            ext = "." + file.split(".")[1]
            if ext in audio_file_types:
                nc = AudioFileClip(self.audio_files_widgets, file)
                AudioClip(self.audio_files_widgets, nc)
                self.audio_files.append(nc)
            else:
                nc = VideoFileClip(self.video_files_widgets, file)
                VideoClip(self.audio_files_widgets, nc)
                self.video_files.append(nc)


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
        


