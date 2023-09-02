import pyaudio
import wave
import time
import os
import tkinter as tk
import threading
from widgets.window import window

audio = pyaudio.PyAudio()


class Recorder:
    def __init__(self) -> None:
        self.recording = False
        self.can_record = True
        self.device = audio.get_default_input_device_info()

        self.button = tk.Button(master=window.record_tab, text="REC", font=("Arial", 50, "bold"),
                                command=self.record_button)
        self.button.pack()
        
        self.label = tk.Label(master=window.record_tab, text="00:00:00")
        self.label.pack()

        self.selected_device_label = tk.Label(master=window.record_tab, text=f"{self.device.get('name')}")
        self.selected_device_label.pack()

        self.device_selected = tk.StringVar(window.record_tab)
        self.device_selected.set(self.device.get('name'))

        self.device_names = [audio.get_device_info_by_index(i).get('name') for i in range(audio.get_device_count())]
   
        self.device_selector = tk.OptionMenu(window.record_tab, self.device_selected, self.device.get('name'), *self.device_names, command=self.select_device)
        self.device_selector.pack()

    def select_device(self, *args):
        selected = self.device_selected.get()
        self.device = self.device_names.index(selected)
        self.selected_device_label.config(text=selected)

    def record_button(self) -> None:
        if self.recording:
            self.recording = False
            self.button
        elif self.can_record:
            self.recording = True
            self.can_record = False
            self.label = tk.Label(text="00:00:00")
            self.button.config(fg="red")
            threading.Thread(target=self.record).start()


    def record(self, record_name:str="new_record", ch_count:int=1, rate:int=44100, fpb:int=1024) -> None:
        stream = audio.open(input_device_index=self.device.get('index'), format=pyaudio.paInt16, channels=ch_count, rate=rate, input=True, frames_per_buffer=fpb)
        frames = []

        start = time.time()

        while self.recording:
            data = stream.read(1024)
            frames.append(data)

            passed = time.time() - start
            secs = passed % 60
            mins = passed // 60
            hours = mins // 60

            self.label.config(text=f"{int(hours):02d}:{int(mins):02d}:{int(secs):02d}")

        stream.stop_stream()
        stream.close()
        audio.terminate()

        if record_name.endswith(".wav"):
            record_name = record_name[:-4]

        i = 1

        if os.path.exists(f"{record_name}.wav"):
            while True:
                if os.path.exists(f"{record_name}({i}).wav"):
                    i += 1
                else:
                    record_name = f"{record_name}({i}).wav"
                    break
                

        save = wave.open(f"{record_name}.wav", "wb")
        save.setnchannels(ch_count)
        save.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
        save.setframerate(rate)
        save.writeframes(b''.join(frames))
        save.close()
        self.can_record = True

