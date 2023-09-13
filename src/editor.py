from moviepy.editor import concatenate_audioclips, concatenate_videoclips, AudioFileClip, VideoFileClip, CompositeVideoClip, CompositeAudioClip, preview
import customtkinter as ctk
from tkinter import filedialog
from tkinter.messagebox import askokcancel
from widgets.clips import Clip, audio_queue, video_queue, audio_changed, video_changed

import os

class Editor:

    def __init__(self, display:ctk.CTkTabview) -> None:
        
        self.display = display

        self.joined_audio = None
        self.joined_video = None

        self.is_no_audio_update = True
        self.is_no_video_update = True

        self.tabview = ctk.CTkTabview(master=display)
        self.tabview.place(relx=0.02, rely=0, relwidth=0.25, relheight=0.8)

        self.tabview.add("audio")
        self.tabview.add("video")
        self.tabview.set("audio")

        self.audio_files_widgets = ctk.CTkScrollableFrame(self.tabview.tab("audio"), width=300, height=460)
        self.audio_files_widgets.grid(row=0, column=0, padx=0, pady=0)

        self.video_files_widgets = ctk.CTkScrollableFrame(self.tabview.tab("video"), width=300, height=460)
        self.video_files_widgets.grid(row=0, column=0, padx=0, pady=0)

        self.clip_load_button = ctk.CTkButton(display, text="Load Files", command=self.load_files)
        self.clip_load_button.place(relx=0.04, rely=0.85, relwidth=0.2, relheight=0.08)

        self.audio_track = ctk.CTkScrollableFrame(self.display, height=25, orientation="vertical")
        self.audio_track.place(relx=0.35, rely=0.1, relwidth=0.24, relheight=0.8)

        self.play_audio = ctk.CTkButton(self.display, 40, 40, 25, text="♫", font=("Arial", 40, "bold"), command=self.play_test_audio)
        self.play_audio.place(relx=0.29, rely=0.12, relwidth=0.05, relheight=0.1)

        self.video_track = ctk.CTkScrollableFrame(self.display, height=25, orientation="vertical")
        self.video_track.place(relx=0.7, rely=0.1, relwidth=0.24, relheight=0.8)

        self.play_video = ctk.CTkButton(self.display, 40, 40, 25, text="►", font=("Arial", 40, "bold"), command=self.play_test_audio)
        #self.play_video.place(relx=0.64, rely=0.12, relwidth=0.05, relheight=0.1)

        self.play_all = ctk.CTkButton(self.display, 40, 40, 25, text="►", font=("Arial", 40, "bold"), command=self.play_test_whole_clip)
        #self.play_all.place(relx=0.3, rely=0.58, relwidth=0.05, relheight=0.1)

        audio_queue_label = ctk.CTkLabel(display, text="Audio queue")
        audio_queue_label.place(relx=0.42, rely=0.05, relwidth=0.1, relheight=0.05)

        video_queue_label = ctk.CTkLabel(display, text="Video queue")
        video_queue_label.place(relx=0.77, rely=0.05, relwidth=0.1, relheight=0.05)


    def load_files(self):
        video_file_types = [".mp4"]
        audio_file_types = [".mp3", ".wav"]

        opened_files = filedialog.askopenfilenames(title="Open audio file", filetypes=(("audio files", audio_file_types),
                                                                                       ("video files", video_file_types)))
        for file in opened_files:
            ext = "." + file.split(".")[1]
            if ext in audio_file_types:
                new_clip = Clip(self.audio_files_widgets,self.audio_track,filename=file)
                new_clip.horizontal_widgets()
                new_clip.clip = AudioFileClip(file)
            else:
                new_clip = Clip(self.video_track,self.audio_files_widgets,filename=file)
                new_clip.horizontal_widgets()
                new_clip.clip = VideoFileClip(file)


    def join_all_audio(self):
        print(len(audio_queue))
        if len(audio_queue.items()) > 0:
            self.joined_audio = concatenate_audioclips([audio_queue[f] for f in audio_queue.keys()])
            audio_changed = False
        else:
            askokcancel(title="Empty queue", message="No audio files in a queue")

    
    def join_all_video(self):
        if len(video_queue.items()) > 0:
            self.joined_video = concatenate_videoclips([video_queue[f] for f in video_queue.keys()])
            video_changed = False
        else:
            askokcancel(title="Empty queue", message="No video files in a queue")
        

    def play_test_audio(self) -> None:
        if audio_changed or self.joined_audio is None:
            self.join_all_audio()

        preview(self.joined_audio)


    def play_test_video(self) -> None:
        if video_changed or self.joined_video is None:
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
        


