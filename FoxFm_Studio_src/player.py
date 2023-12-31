import threading
import customtkinter as ctk
from tkinter.filedialog import askopenfilename
from tkinter.ttk import Progressbar, Style
from tkinter import VERTICAL
import wave
from pyaudio import PyAudio

CHUNK = 1024

class Player:
    def __init__(self, display) -> None:
        self.is_existing = True
        self.file = ""
        self.can_play = False
        self.timing = False

        self.devices:dict

        self.play_object = ctk.CTkButton(display, text="Play", command=self.play_button)
        self.play_object.place(relx=0.05, rely=0.65, relwidth=0.4, relheight=0.1)

        self.load_file = ctk.CTkButton(display, text="Load file", command=self.select_file)
        self.load_file.place(relx=0.05, rely=0.77, relwidth=0.4, relheight=0.1)

        #self.device_selector = ctk.CTkOptionMenu(display, values=self.get_output_devices())
        #self.device_selector.set(str(self.get_default_output_device()))
        #self.device_selector.place(relx=0.05, rely=0.58, relwidth=0.4)

        self.file_name_label = ctk.CTkLabel(display, text="Load a file", font=("Arial", 20))
        self.file_name_label.place(relx=0.05, rely=0.25, relwidth=0.4, relheight=0.1)

        s = Style()
        s.configure("green.Vertical.TProgressbar", foreground='grey', background='green')

        self.progressbar = Progressbar(display, orient=VERTICAL, style="green.Vertical.TProgressbar", mode='determinate', maximum=100, value=0)
        self.progressbar.place(relx=0.65, rely=0.2, relwidth=0.25, relheight=0.6)

        self.timer = ctk.CTkLabel(display, text="00:00:00", font=("Arial", 60))
        self.timer.place(relx=0.05, rely=0.43, relwidth=0.4, relheight=0.1)

        self.secs, self.mins, self.hours = 0,0,0
        self.playing_thread:threading.Thread


    def select_file(self):
        recent_file = self.file
        self.file = askopenfilename(title="Select audio file", filetypes=[('Wave files', '*.wav')])
        if self.file == "" or self.file == ():
            return
        
        filename = self.file.split('/')[-1]
        filename = filename.split('\\')[-1]
        
        if len(filename) > 45:
            filename = filename[:45]
        self.file_name_label.configure(text=filename)

        if recent_file != self.file and self.file != ():
            self.playing_thread = threading.Thread(target=self.play_file, daemon=True)
            self.playing_thread.start()
        

    def get_default_output_device(self):
        p = PyAudio()
        dn = p.get_default_output_device_info().get('name')
        p.terminate()
        return dn
    

    def get_output_devices(self):
        p = PyAudio()
        ol = [p.get_device_info_by_index(d).get('name') for d in range(p.get_device_count()) if p.get_device_info_by_index(d).get('maxOutputChannels') > 0]
        p.terminate()
        self.devices = dict(zip(ol, [i for i in range(len(ol))]))
        return ol
    

    def run_timer(self):
        if self.secs < 59:
            self.secs += 1
        else:
            self.secs = 0
            if self.mins < 59:
                self.mins += 1
            else:
                self.mins = 0
                self.hours += 1

        self.timer.configure(text=f"{str(self.hours).rjust(2,'0')}:{str(self.mins).rjust(2,'0')}:{str(self.secs).rjust(2,'0')}")
    

    def play_button(self):
        if self.file:
            texts = ["Play", "Stop"]
            self.can_play = not self.can_play
            self.play_object.configure(text=texts[int(self.can_play)])


    def play_file(self):
        if self.file == "":
            return
        
        filename = self.file
        
        wf = wave.open(self.file, 'rb')

        # Create an interface to PortAudio
        p = PyAudio()

        # Open a .Stream object to write the WAV file to
        # 'output = True' indicates that the sound will be played rather than recorded
        stream = p.open(format = p.get_format_from_width(wf.getsampwidth()),
                        channels = wf.getnchannels(),
                        rate = wf.getframerate(),
                        output = True,
                        )

        duration = wf.getnframes() / float(wf.getframerate())
        timer_chunk = duration / (wf.getnframes() / CHUNK)
        # Read data in chunks
        data = wf.readframes(CHUNK)
        index = 0
        timer = 0.0
        self.secs, self.mins, self.hours = 0,0,0
        # Play the sound by writing the audio data to the stream
        while data != '':
            if self.can_play:

                if timer >= 1:
                    timer = 0.0
                    self.run_timer()
                else:
                    timer += timer_chunk

                dl = list(data)
                if len(dl) == 0:
                    break
                val = (sum(dl)/len(dl))%100

                if index >= 3:
                    self.progressbar['value'] = val
                    index = 0

                index += 0.8
                stream.write(data)
                data = wf.readframes(CHUNK)
            else:
                self.progressbar['value'] = 0
            
            if filename != self.file and self.file.strip() != "" or self.is_existing == False:
                break

        self.can_play = False
        self.timing = False
        self.play_object.configure(text="Play")

        # Close and terminate the stream
        stream.close()
        p.terminate()
