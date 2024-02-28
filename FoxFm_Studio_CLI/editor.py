from tkinter.messagebox import askokcancel
from tkinter.filedialog import askopenfilename
from audio_modifiers import export_sounds, modify_volume

def join_all_audio(audio_queue:list[str], modification_values:list[int]) -> bool:
        print(audio_queue)
        input()

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

mod_values = [30, 0, 0, 4]
filenames = ['/home/blob/Pulpit/FoxFM/FoxFm_Studio_CLI/Shrek Soundtrack   9. Smash Mouth - All Star.mp4', '/home/blob/Pulpit/FoxFM/FoxFm_Studio_CLI/I\'m A Believer (From "Shrek" Motion Picture Soundtrack).mp4', "/home/blob/Pulpit/FoxFM/FoxFm_Studio_CLI/Shrek 2 Soundtrack   13. Eddie Murphy & Antonio Banderas - Livin' La Vida Loca.mp4", '/home/blob/Pulpit/FoxFM/FoxFm_Studio_CLI/Fearless Hero (Hero Version).mp4', '/home/blob/Pulpit/FoxFM/FoxFm_Studio_CLI/La Vida Es Una.mp4']

join_all_audio(filenames, mod_values)
export_sounds(input("FILENAME: "))