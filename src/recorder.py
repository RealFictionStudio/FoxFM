import pyaudio
import wave
import time
import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog
import threading


class Recorder:
    def __init__(self, display:ctk.CTkTabview) -> None:
        self.recording = False
        self.audio = pyaudio.PyAudio()
        self.device = self.audio.get_default_input_device_info()

        self.button = ctk.CTkButton(master=display, text="•", font=("Arial", 70, "bold"),
                                command=self.record_button)
        self.button.place(relx=0.3, rely=0.4, relwidth=0.11, relheight=0.15)

        self.resetbutton = ctk.CTkButton(master=display, text="■", font=("Arial", 40, "bold"),
                                command=self.record_button)
        self.resetbutton.place(relx=0.17, rely=0.4, relwidth=0.11, relheight=0.15)
        
        self.label = ctk.CTkLabel(master=display, text="00:00:00", fg_color="transparent", font=("Arial", 30, "bold"))
        self.label.place(relx=0.5, rely=0.4, relheight=0.15, relwidth=0.2)

        self.device_selected = tk.StringVar(master=display)
        self.device_selected.set(self.device.get('name'))
        self.device_names = [self.audio.get_device_info_by_index(i).get('name') for i in range(self.audio.get_device_count())]
   
        self.device_selector = tk.OptionMenu(display, self.device_selected, self.device.get('name'), *self.device_names, command=self.select_device)
        self.device_selector.place(relx=0.5, rely=0.55, relheight=0.08, relwidth=0.2)

        self.frames = []

    def select_device(self, *args) -> None:
        selected = self.device_selected.get()
        self.device = self.device_names.index(selected)

    def record_button(self) -> None:
        if self.recording:
            self.recording = False
        else:
            self.recording = True
            if len(self.frames):
                self.label.configure(text="00:00:00")
            threading.Thread(target=self.record).start()


    def record(self, ch_count:int=1, rate:int=44100, fpb:int=1024) -> None:
        self.audio = pyaudio.PyAudio()
        
        stream = self.audio.open(input_device_index=self.device.get('index'), format=pyaudio.paInt16, channels=ch_count, rate=rate, input=True, frames_per_buffer=fpb)

        start = time.time()

        while self.recording:
            data = stream.read(1024)
            self.frames.append(data)

            passed = time.time() - start
            secs = passed % 60
            mins = passed // 60
            hours = mins // 60

            self.label.configure(text=f"{int(hours):02d}:{int(mins):02d}:{int(secs):02d}")

        stream.stop_stream()
        stream.close()
        self.audio.terminate()
                
        save_file = filedialog.asksaveasfilename(defaultextension=".wav", filetypes=[
            ("Wave file", ".wav")
        ])

        if type(save_file) != str:
            self.recording = False
            return

        save = wave.open(save_file, "wb")
        save.setnchannels(ch_count)
        save.setsampwidth(self.audio.get_sample_size(pyaudio.paInt16))
        save.setframerate(rate)
        save.writeframes(b''.join(self.frames))
        save.close()

        self.frames.clear()


