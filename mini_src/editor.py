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

        self.unify_value = tk.StringVar(value=0)
        self.auto_unify_value = tk.BooleanVar(value=False)

        audio_queue_label = ctk.CTkLabel(display, text="Audio queue")
        audio_queue_label.place(relx=0.62, rely=0.02, relwidth=0.1, relheight=0.05)

        self.export_button = ctk.CTkButton(self.display, text="Export", command=self.export_form)
        self.export_button.place(relx=0.58, rely=0.85, relwidth=0.18, relheight=0.08)

        self.export_window = None
        self.export_mode = tk.IntVar(value=0)
        self.include_video_mode = tk.BooleanVar(value=False)

        self.can_export = True
        self.export_progress = 0
        self.export_elements = 0 # file count + 1 (exporting whole file)


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

        self.unify_value.set("42")

        if len(audio_queue.keys()) > 0:
            self.export_elements = len(audio_queue.keys()) + 1
            for i in audio_queue.keys():
                if self.can_export:
                    modify_volume(audio_queue.get(i).filename, val)
                    self.update_export_bar()
                else:
                    return False
            self.is_no_audio_update = True
            return True
        else:
            askokcancel(title="Empty queue", message="No audio files in a queue")


    def cancel_export(self):
        self.can_export = False


    def add_export_ui(self):
        self.download_toplevel = ctk.CTkToplevel(self.master)
        self.download_toplevel.geometry("400x300")
        self.download_toplevel.title("Downloading...")
        self.download_toplevel.protocol("WM_DELETE_WINDOW", self.destroy)
        self.download_toplevel.resizable(False, False)

        self.loading_bar = ctk.CTkProgressBar(self.download_toplevel, orientation='horizontal', mode='determinate')
        self.loading_bar.set(0)
        self.cancel_button = ctk.CTkButton(self.download_toplevel, text="Cancel", command=self.destroy)
        self.loading_bar.place(x=100, y=100)
        self.cancel_button.place(x=130, y=250)
        self.download_title = ctk.CTkLabel(self.download_toplevel, text="")
        self.download_title.place(x=0, y=120)


    def update_export_bar(self):
        self.export_progress += 1
        self.loading_bar.set(self.export_progress / self.export_elements)
    
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
        
        def export_func():
            self.add_export_ui()
            self.export_audio()
            self.clean_window()
            self.export_progress = 0
 
        Thread(target=export_func, daemon=True).start()


    def export_audio(self) -> str:
        file_name = filedialog.asksaveasfilename(defaultextension=".wav", filetypes=[
            ("Wave file", ".wav")
        ])

        if file_name == "":
            return

        print("START AUDIO JOIN")
        res = self.join_all_audio()
        if not res:
            print("**ERROR**")
            return
        print("END AUDIO JOIN")
        export_sounds(file_name)
        self.loading_bar.set(1)
        print("EXPORTED AUDIO")
        askokcancel(title="Finished", message="Export Finished!")
        return file_name
    