import threading
import customtkinter as ctk
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import askokcancel
import wave
import pyaudio

CHUNK = 1024

class Player:
    def __init__(self, display) -> None:
        self.file = ""
        self.can_play = False

        self.play_object = ctk.CTkButton(display, command=self.play_button)
        self.play_object.place(relx=0.3, rely=0.7)

        self.device_selector = ctk.CTkOptionMenu(display, values=self.get_output_devices())

    def select_file(self):
        self.file = askopenfilename(title="Select audio file")
        if self.file == "":
            return
        

    def get_default_output_device(self):
        p = pyaudio.PyAudio()
        dn = p.get_default_output_device_info().get('name')
        p.terminate()
        return dn
    

    def get_output_devices(self):
        p = pyaudio.PyAudio()
        ol = [p.get_device_info_by_index(d).get('name') for d in range(p.get_device_count()) if p.get_device_info_by_index(d).get('maxOutputChannels') > 0]
        p.terminate()
        return ol

    def play_button(self):
        self.can_play = not self.can_play


    def play_file(self):
        if self.file == "":
            return
        
        wf = wave.open(self.file, 'rb')

        # Create an interface to PortAudio
        p = pyaudio.PyAudio()

        # Open a .Stream object to write the WAV file to
        # 'output = True' indicates that the sound will be played rather than recorded
        stream = p.open(format = p.get_format_from_width(wf.getsampwidth()),
                        channels = wf.getnchannels(),
                        rate = wf.getframerate(),
                        output = True)

        # Read data in chunks
        data = wf.readframes(CHUNK)

        # Play the sound by writing the audio data to the stream
        while data != '' and self.can_play:
            dl = list(data)
            print(sum(dl)/len(dl))
            
            stream.write(data)
            data = wf.readframes(CHUNK)

        # Close and terminate the stream
        stream.close()
        p.terminate()

