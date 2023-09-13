import customtkinter as ctk
from tkinter.messagebox import askokcancel
from copy import deepcopy
from moviepy.editor import AudioFileClip

pallet_id = 0
queue_audio_id = 0

audio_queue = {}
video_queue = {}

audio_changed = False
video_changed = False


def get_filename(filename:str):
    length = len(filename.split("/"))
    if length > 1:
        return filename.split("/")[length-1]
    else:
        length = len(filename.split("\\")) - 1
        return filename.split("\\")[length - 1]

class Clip():
    def __init__(self, display, vertical_display, filename:str, **kwargs) -> None:
        self.id = 0
        self.in_queue = False
        
        self.display = display
        self.clip = None
        self.filename = filename
        self.vertical_display = vertical_display

        self.frame = ctk.CTkFrame(display, 300, 50, 25, fg_color="grey")
        
        self.filename_label:ctk.CTkLabel
        self.add_button:ctk.CTkButton
        self.delete_button:ctk.CTkButton

        self.move_left:ctk.CTkButton
        self.move_right:ctk.CTkButton

        self.horizontal_rotation:bool


    def add_widgets(self, horizontal_widgets:bool):
        global pallet_id

        self.filename_label = ctk.CTkLabel(self.frame, text=get_filename(self.filename), width=100)
        self.filename_label.grid(row=1, column=5, padx=20, pady=5)

        if self.in_queue == False:
    
            self.frame.grid(row=pallet_id, column=5, padx=8, pady=5)
            pallet_id += 1

            self.horizontal_rotation = horizontal_widgets

            self.add_button = ctk.CTkButton(self.frame, width=50, height=28, corner_radius=25, text="+", 
                                            font=("Arial", 20, "bold"), fg_color="transparent", command=self.add_to_queue)
            self.add_button.grid(row=1, column=6, padx=10, pady=5)

            self.delete_button = ctk.CTkButton(self.frame, width=50, height=28, corner_radius=25, text="−", 
                                               font=("Arial", 20, "bold"), fg_color="transparent", command=self.del_horizontal)
            self.delete_button.grid(row=1, column=7, padx=10, pady=5)

        else:
            self.frame.grid(row=pallet_id, column=5, padx=5, pady=16)
            holder_label = ctk.CTkLabel(self.frame, text="\t   ")
            holder_label.grid(row=1, column=6, padx=10)
            pallet_id += 1
            
            self.delete_button = ctk.CTkButton(self.frame, width=50, height=28, corner_radius=25, text="−", 
                                               font=("Arial", 20, "bold"), fg_color="transparent", command=self.del_vertical)
            self.delete_button.grid(row=1, column=7, padx=10, pady=2)


    def add_to_queue(self):
        global queue_audio_id

        clip_copy = Clip(self.vertical_display, None, self.filename)
        clip_copy.in_queue = True
        clip_copy.horizontal_widgets()
        clip_copy.clip = self.clip
        clip_copy.id = queue_audio_id
        queue_audio_id += 1

        if type(self.clip) == AudioFileClip:
            global audio_queue, audio_changed
            audio_queue.update({f'{clip_copy.id}':clip_copy.clip})
            audio_changed = True
        else:
            global video_queue, video_changed
            video_queue.update({f'{clip_copy.id}':clip_copy.clip})
            video_changed = True


    def del_horizontal(self):
        res = askokcancel(title="Delete file", message="Delete file from palette?")
        if res:
            self.frame.destroy()

    def del_vertical(self):
        if type(self.clip) == AudioFileClip:
            global audio_queue, audio_changed
            del audio_queue[f'{self.id}']
            audio_changed = False
        else:
            global video_queue, video_changed
            del video_queue[f'{self.id}']
            video_changed = True

        self.frame.destroy()


    def horizontal_widgets(self):
        self.add_widgets(True)


    def vertical_widgets(self):
        self.add_widgets(False)