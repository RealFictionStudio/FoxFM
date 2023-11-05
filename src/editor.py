from moviepy.editor import concatenate_videoclips, AudioFileClip, VideoFileClip, CompositeVideoClip, CompositeAudioClip
import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog
from tkinter.messagebox import askokcancel
from widgets.clips import Clip, audio_queue, video_queue, video_changed
from audio_modifiers import modify_volume, export_sounds
import os
from threading import Thread


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
        self.audio_track.place(relx=0.35, rely=0.08, relwidth=0.24, relheight=0.8)

        #self.play_audio = ctk.CTkButton(self.display, 40, 40, 25, text="♫", font=("Arial", 40, "bold"), command=self.play_test_audio)
        #self.play_audio.place(relx=0.29, rely=0.12, relwidth=0.05, relheight=0.1)

        self.unify_value = tk.StringVar(value=0)
        self.auto_unify_value = tk.BooleanVar(value=False)


        self.video_track = ctk.CTkScrollableFrame(self.display, height=25, orientation="vertical")
        self.video_track.place(relx=0.7, rely=0.08, relwidth=0.24, relheight=0.8)

        #self.play_video = ctk.CTkButton(self.display, 40, 40, 25, text="►", font=("Arial", 40, "bold"), command=self.play_test_audio)
        #self.play_video.place(relx=0.64, rely=0.12, relwidth=0.05, relheight=0.1)

        #self.play_all = ctk.CTkButton(self.display, 40, 40, 25, text="►", font=("Arial", 40, "bold"), command=self.play_test_whole_clip)
        #self.play_all.place(relx=0.3, rely=0.58, relwidth=0.05, relheight=0.1)

        audio_queue_label = ctk.CTkLabel(display, text="Audio queue")
        audio_queue_label.place(relx=0.42, rely=0.03, relwidth=0.1, relheight=0.05)

        video_queue_label = ctk.CTkLabel(display, text="Video queue")
        video_queue_label.place(relx=0.77, rely=0.03, relwidth=0.1, relheight=0.05)

        self.export_button = ctk.CTkButton(self.display, text="Export", command=self.export_form)
        self.export_button.place(relx=0.55, rely=0.9, relwidth=0.18, relheight=0.08)

        self.export_window = None
        self.export_mode = tk.IntVar(value=0)
        self.include_video_mode = tk.BooleanVar(value=False)

        self.audio_playtest = False
        self.is_exporting = False


    def load_files(self):
        video_file_types = [".mp4"]
        audio_file_types = [".mp3", ".wav", ".mp4"]

        opened_files = filedialog.askopenfilenames(title="Open audio file", filetypes=(("audio files", audio_file_types),
                                                                                       ("video files", video_file_types)))
        for file in opened_files:
            ext = "." + file.split(".")[1]
            if ext in audio_file_types:
                new_clip = Clip(self.audio_files_widgets,self.audio_track,filename=file)
                new_clip.horizontal_widgets()
                new_clip.clip = AudioFileClip(file)
            else:
                new_clip = Clip(self.video_files_widgets,self.video_track,filename=file)
                new_clip.horizontal_widgets()
                new_clip.clip = VideoFileClip(file)


    def join_all_audio(self) -> bool:
        val = 0
        try:
            val = float(self.unify_value.get().strip())
        except:
            askokcancel(title="Invalid input", message="Value must be integer or floating point number")
            return False

        print("START UNIFY")

        if len(audio_queue.keys()) > 0:
            for i in audio_queue.keys():
                print("UNIFY")
                modify_volume(audio_queue.get(i).filename, val)
            self.is_no_audio_update = True

        else:
            askokcancel(title="Empty queue", message="No audio files in a queue")

    
    def join_all_video(self):
        if len(video_queue.items()) > 0:
            self.joined_video = concatenate_videoclips([video_queue[f] for f in video_queue.keys()])
            self.is_no_video_update = True
        else:
            askokcancel(title="Empty queue", message="No video files in a queue")
        

    def play_test_video(self) -> None:
        if video_changed or self.joined_video is None:
            self.join_all_video()

        # preview video
        

    def play_test_whole_clip(self) -> None:
        ...

    
    def clean_window(self):
        try:
            self.export_window.destroy()
        except:
            ...
        self.export_window = None


    def export_form(self):
        if len(audio_queue.keys()) == 0 and len(video_queue.keys()) == 0:
            askokcancel(title="Empty queue", message="Audio and Video queue are empty")
            return
        elif self.export_window is not None:
            askokcancel(title="Operation in process", message="Export window already opened")
            return
        else:
            self.export_window = ctk.CTkToplevel(self.display)
            self.export_window.geometry("400x300")
            self.export_window.resizable(False,False)
            self.export_window.title("Export")
            self.export_window.protocol("WM_DELETE_WINDOW", self.clean_window)

            mode1 = ctk.CTkRadioButton(self.export_window, text="Audio length based", value=0, variable=self.export_mode)
            mode1.place(x=10,y=30)
            mode2 = ctk.CTkRadioButton(self.export_window, text="Video length based", value=1, variable=self.export_mode)
            mode2.place(x=250,y=30)

            

            include_video = ctk.CTkCheckBox(self.export_window, text="Include video", variable=self.include_video_mode, onvalue=True, offvalue=False)
            include_video.place(x=10, y=100)

            auto_mode = ctk.CTkCheckBox(self.export_window, text="Based on mean", variable=self.auto_unify_value, onvalue=True, offvalue=False)
            auto_mode.place(x=10, y=170)
            boost_value = ctk.CTkEntry(self.export_window, textvariable=self.unify_value)
            boost_value.place(x=250, y=170)

            if len(audio_queue.keys()) == 0:
                mode1.configure(state="disabled")
                auto_mode.configure(state="disabled")
                boost_value.configure(state="disabled")

            if len(video_queue.keys()) == 0:
                mode2.configure(state="disabled")
                include_video.configure(state="disabled")

            export_button = ctk.CTkButton(self.export_window, text="Export", command=self.export_with_settings)
            export_button.place(x=130, y=250)

            if mode1.cget("state") ==  mode2.cget("state") == "disabled":
                export_button.configure(state="disabled")


    def export_with_settings(self):

        if self.is_exporting:
            askokcancel(title="In progress", message="Exporting is still in progress, wait until it ends")
            return
        
        self.is_exporting = True
        
        def export_func():
            if self.include_video_mode.get():
                if self.export_mode.get() == 0:
                    self.export_whole_clip(True)
                else:
                    self.export_whole_clip(False)
            else:
                self.export_audio()
            
            self.clean_window()
            self.unify_value = None
            self.is_exporting = False
 
        Thread(target=export_func).start()


    def export_audio(self) -> str:
        file_name = filedialog.asksaveasfilename(defaultextension=".wav", filetypes=[
            ("Wave file", ".wav")
        ])

        if file_name == "":
            askokcancel(title="Invalid input", message="Empty filename")
            return

        print("START AUDIO JOIN")
        res = self.join_all_audio()
        if not res:
            return
        print("END AUDIO JOIN")
        export_sounds(file_name)
        print("EXPORTED AUDIO")
        return file_name
    

    def export_video(self) -> str:
        file_name = filedialog.asksaveasfilename(defaultextension=".mp4", filetypes=[
            ("MP4 file", ".mp4")
        ])

        if file_name == "":
            askokcancel(title="Invalid input", message="Empty filename")
            return

        self.join_all_video()
        self.joined_video.write_videofile(file_name)
        return file_name   
    
    
    def export_whole_clip(self, mode:bool) -> str:
        # Mode:
            # True -> based on audio length
            # False -> based on video length

        res = self.join_all_audio()
        if not res:
            return
        self.join_all_video()

        file_name = filedialog.asksaveasfilename(defaultextension=".mp4", filetypes=[
            ("MP4 file", ".mp4")
        ])

        if file_name == "":
            askokcancel(title="Invalid input", message="Empty filename")
            return

        temp_sound_file = export_sounds()

        if mode:
            duration = self.joined_audio.duration
            final_video = CompositeVideoClip([self.joined_video.set_duration(duration)])

            export = final_video.set_audio(AudioFileClip(temp_sound_file))
            export.write_videofile(file_name)
        
        else:
            duration = self.joined_video.duration
            final_audio = CompositeAudioClip([AudioFileClip(temp_sound_file).set_duration(duration)])

            export = self.joined_video.set_audio(final_audio)
            export.write_videofile(file_name, fps=32)

        try:
            os.remove(temp_sound_file)
        except Exception as e:
            askokcancel(f"{e}")

        return file_name
        


