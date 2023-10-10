from moviepy.editor import AudioFileClip
import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog
from tkinter.messagebox import askokcancel
from widgets.clips import Clip, audio_queue
from audio_modifiers import modify_volume, export_sounds
from threading import Thread


class Editor:

    def __init__(self, display:ctk.CTkTabview) -> None:
        
        self.display = display

        self.joined_audio = None
        self.joined_video = None

        self.is_no_audio_update = True
        self.is_no_video_update = True

        self.tabview = ctk.CTkTabview(master=display)
        self.tabview.place(relx=0.15, rely=0.02, relwidth=0.35, relheight=0.8)

        self.tabview.add("audio files")
        self.tabview.set("audio files")

        self.audio_files_widgets = ctk.CTkScrollableFrame(self.tabview.tab("audio files"), width=300, height=460)
        self.audio_files_widgets.place(relwidth=1)

        self.clip_load_button = ctk.CTkButton(display, text="Load Files", command=self.load_files)
        self.clip_load_button.place(relx=0.22, rely=0.85, relwidth=0.2, relheight=0.08)

        self.audio_track = ctk.CTkScrollableFrame(self.display, height=25, orientation="vertical")
        self.audio_track.place(relx=0.55, rely=0.09, relwidth=0.24, relheight=0.73)

        #self.play_audio = ctk.CTkButton(self.display, 40, 40, 25, text="♫", font=("Arial", 40, "bold"), command=self.play_test_audio)
        #self.play_audio.place(relx=0.29, rely=0.12, relwidth=0.05, relheight=0.1)

        self.unify_value = tk.StringVar(value=0)
        self.auto_unify_value = tk.BooleanVar(value=False)

        audio_queue_label = ctk.CTkLabel(display, text="Audio queue")
        audio_queue_label.place(relx=0.62, rely=0.02, relwidth=0.1, relheight=0.05)

        self.export_button = ctk.CTkButton(self.display, text="Export", command=self.export_form)
        self.export_button.place(relx=0.58, rely=0.85, relwidth=0.18, relheight=0.08)

        self.export_window = None
        self.export_mode = tk.IntVar(value=0)
        self.include_video_mode = tk.BooleanVar(value=False)

        self.is_exporting = False


    def load_files(self):
        audio_file_types = [".mp3", ".wav", ".mp4"]

        opened_files = filedialog.askopenfilenames(title="Open audio file", filetypes=(("Audio files", audio_file_types), ("All files", "*.*")))
        for file in opened_files:
            new_clip = Clip(self.audio_files_widgets,self.audio_track,filename=file)
            new_clip.horizontal_widgets()
            new_clip.clip = AudioFileClip(file)


    def join_all_audio(self) -> bool:
        val = 0
        input_val = self.unify_value.get().strip()
        print(input_val, type(input_val))
        try:
            val = float(input_val)
        except:
            askokcancel(title="Invalid input", message="Value must be integer or floating point number")
            return False

        self.unify_value.set("40")
        print("START UNIFY")

        if len(audio_queue.keys()) > 0:
            for i in audio_queue.keys():
                print("UNIFY")
                modify_volume(audio_queue.get(i).filename, val)
            self.is_no_audio_update = True
            return True
        else:
            askokcancel(title="Empty queue", message="No audio files in a queue")

    
    def clean_window(self):
        try:
            self.export_window.destroy()
        except:
            ...
        self.export_window = None


    def export_form(self):
        if len(audio_queue.keys()) == 0:
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

            modify_audio_label = ctk.CTkLabel(self.export_window, text="Audio volume modifier")
            modify_audio_label.place(x=20, y=170)

            boost_value = ctk.CTkEntry(self.export_window, textvariable=self.unify_value, placeholder_text="40")
            boost_value.place(x=250, y=170)

            export_button = ctk.CTkButton(self.export_window, text="Export", command=self.export_with_settings)
            export_button.place(x=130, y=250)


    def export_with_settings(self):

        if self.is_exporting:
            askokcancel(title="In progress", message="Exporting is still in progress, wait until it ends")
            return
        
        self.is_exporting = True
        
        def export_func():
            self.export_audio()
            print("AUDIO EXPORTED")
            
            self.clean_window()
            self.is_exporting = False

            print("OPERATION END")
 
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
            print("**ERROR**")
            return
        print("END AUDIO JOIN")
        export_sounds(file_name)
        print("EXPORTED AUDIO")
        return file_name
    