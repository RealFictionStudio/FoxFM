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

        self.devices:dict

        self.play_object = ctk.CTkButton(display, text="Play", command=self.play_button)
        self.play_object.place(relx=0.05, rely=0.65, relwidth=0.4, relheight=0.1)

        self.load_file = ctk.CTkButton(display, text="Load file", command=self.select_file)
        self.load_file.place(relx=0.05, rely=0.77, relwidth=0.4, relheight=0.1)

        self.device_selector = ctk.CTkOptionMenu(display, values=self.get_output_devices())
        self.device_selector.set(str(self.get_default_output_device()))
        self.device_selector.place(relx=0.05, rely=0.58, relwidth=0.4)

        self.file_name_label = ctk.CTkLabel(display, text="", font=("Arial", 20))
        self.file_name_label.place(relx=0.05, rely=0.25, relwidth=0.4, relheight=0.1)


    def select_file(self):
        self.file = askopenfilename(title="Select audio file", filetypes=[('Wave files', '*.wav')])
        if self.file == "":
            return
        
        self.file = self.file.split('/')[-1]
        self.file = self.file.split('\\')[-1]
        
        if len(self.file) > 45:
            self.file = self.file[:45]
        self.file_name_label.configure(text=self.file)

        threading.Thread(target=self.play_file, daemon=True).start()
        

    def get_default_output_device(self):
        p = pyaudio.PyAudio()
        dn = p.get_default_output_device_info().get('name')
        p.terminate()
        return dn
    

    def get_output_devices(self):
        p = pyaudio.PyAudio()
        ol = [p.get_device_info_by_index(d).get('name') for d in range(p.get_device_count()) if p.get_device_info_by_index(d).get('maxOutputChannels') > 0]
        p.terminate()
        self.devices = dict(zip(ol, [i for i in range(len(ol))]))
        return ol
    

    def play_button(self):
        texts = ["Play", "Stop"]
        self.can_play = not self.can_play
        self.play_object.configure(text=texts[int(self.can_play)])


    def play_file(self):
        if self.file == "":
            return
        
        filename = self.file
        
        wf = wave.open(self.file, 'rb')

        # Create an interface to PortAudio
        p = pyaudio.PyAudio()

        # Open a .Stream object to write the WAV file to
        # 'output = True' indicates that the sound will be played rather than recorded
        stream = p.open(format = p.get_format_from_width(wf.getsampwidth()),
                        channels = wf.getnchannels(),
                        rate = wf.getframerate(),
                        output = True,
                        output_device_index=self.devices.get(self.device_selector.get())
                        )

        # Read data in chunks
        data = wf.readframes(CHUNK)

        # Play the sound by writing the audio data to the stream
        while data != '':
            if self.can_play:
                dl = list(data)
                stream.write(data)
                data = wf.readframes(CHUNK)
            
            if filename != self.file:
                break

        # Close and terminate the stream
        stream.close()
        p.terminate()

