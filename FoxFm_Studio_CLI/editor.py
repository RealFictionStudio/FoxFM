from tkinter.messagebox import askokcancel
from tkinter.filedialog import askopenfilename
from audio_modifiers import export_sounds, modify_volume

class Editor:
    def __init__(self) -> None:
        pass

    def edit(self):
        self.join_all_audio()
        export_sounds()
    
    def join_all_audio(self, audio_queue:list[str], modification_values:list[int]) -> bool:
        print(audio_queue)

        for k, v in enumerate(modification_values):
            if v == "":
                modification_values[k] = None
                continue
            try:
                val = float(v)
                modification_values[k] = val
            except:
                askokcancel(title="Invalid input", message="Value must be integer or floating point number")
                return False
                
        print(modification_values)

        if len(audio_queue) > 0:
            for i in audio_queue:
                if not modify_volume(i, modification_values):
                    return False
                #self.update_export_bar()
            return True
        else:
            askokcancel(title="Empty queue", message="No audio files in a queue")

