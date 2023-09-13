import pyaudio
import wave
import time
import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog
from tkinter.messagebox import showerror
import threading

ch_count=1 
rate=44100
fpb=1024


class Recorder:
    def __init__(self, display:ctk.CTkTabview) -> None:
        self.recording = False
        self.audio = pyaudio.PyAudio()
        self.device = self.audio.get_default_input_device_info()

        self.button = ctk.CTkButton(master=display, text="•", font=("Arial", 70, "bold"),
                                command=self.record_button)
        self.button.place(relx=0.35, rely=0.4, relwidth=0.11, relheight=0.15)

        self.resetbutton = ctk.CTkButton(master=display, text="⬇", font=("Arial", 40, "bold"),
                                command=self.reset_button)
        self.resetbutton.place(relx=0.2, rely=0.4, relwidth=0.11, relheight=0.15)
        
        self.label = ctk.CTkLabel(master=display, text="00:00:00", fg_color="transparent", font=("Arial", 30, "bold"))
        self.label.place(relx=0.5, rely=0.4, relheight=0.15, relwidth=0.2)

        self.device_selected = ctk.StringVar(value=self.device.get('name'))
        self.device_names = [self.audio.get_device_info_by_index(i).get('name').strip() for i in range(self.audio.get_device_count())]
   
        self.device_selector = ctk.CTkOptionMenu(master=display, values=self.device_names,
                                command=self.select_device, variable=self.device_selected)
        self.device_selector.place(relx=0.51, rely=0.55, relwidth=0.18)

        self.frames = []

        self.reset = False

    def select_device(self, *args) -> None:
        selected = self.device_selected.get()
        self.device = self.device_names.index(selected)

    def reset_button(self):
        if self.recording or self.resetbutton._text == "■":
            self.recording = False
            self.frames.clear()
            self.button.configure(text="•", font=("Arial", 70, "bold"))
            self.reset = True
        else:
            if len(self.frames):
                self.save_record()
                self.resetbutton.configure(text="■", font=("Arial", 40, "bold"))
            else:
                showerror("Saving Error", "Nothing is recorded")

    def record_button(self) -> None:
        if self.recording:
            self.recording = False
            self.button.configure(text="•", font=("Arial", 70, "bold"))
            self.resetbutton.configure(text="⬇", font=("Arial", 40, "bold"))

        else:
            self.recording = True
            self.button.configure(text="| |", font=("Arial", 25, "bold"))
            self.resetbutton.configure(text="■", font=("Arial", 40, "bold"))
            threading.Thread(target=self.record).start()


    def record(self) -> None:
        self.audio = pyaudio.PyAudio()
        
        stream = self.audio.open(input_device_index=self.device.get('index'), format=pyaudio.paInt16, channels=ch_count, rate=rate, input=True, frames_per_buffer=fpb)

        start = time.time()

        if len(self.frames) > 0:
            current_count_time = self.label._text.split(":")
            passed_earlier = int(current_count_time[0]) * 3600 + int(current_count_time[1]) * 60 + int(current_count_time[2])
        else:
            passed_earlier = 0

        while self.recording:
            data = stream.read(1024)
            self.frames.append(data)

            passed = time.time() - start + passed_earlier
            secs = passed % 60
            mins = passed // 60
            hours = mins // 60

            self.label.configure(text=f"{int(hours):02d}:{int(mins):02d}:{int(secs):02d}")

        if self.reset:
            self.reset = False
            self.label.configure(text="00:00:00")

        stream.stop_stream()
        stream.close()
        self.audio.terminate()
            


    def save_record(self):
        save_file = filedialog.asksaveasfilename(defaultextension=".wav", filetypes=[
            ("Wave file", ".wav")
        ])

        save = wave.open(save_file, "wb")
        save.setnchannels(ch_count)
        save.setsampwidth(self.audio.get_sample_size(pyaudio.paInt16))
        save.setframerate(rate)
        save.writeframes(b''.join(self.frames))
        save.close()

        self.frames.clear()