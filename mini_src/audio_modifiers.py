from pydub import AudioSegment, silence
import time
import os

# -1 = <-3;-4>
# each modify has +- 1 in real

all_modified_audios = []

can_export = True


def reset():
    all_modified_audios.clear()


def get_path_splitter() -> str:
    p = os.getcwd()

    if len(p.split("/")) > 1:
        return "/"
    else:
        return "\\"

        
# 0 - volume | 1 - fade-in | 2 - fade-out | 3 - deaf
def modify_volume(filename:str, modification_values:list[float]) -> bool:
    global can_export

    for k, v in enumerate(modification_values):
        if v is None:
            match k:
                case 0:
                    modification_values[k] = 30
                case _:
                    modification_values[k] = 0

    audio_file = AudioSegment.from_file(filename)
    sil = silence.detect_silence(audio_file, silence_thresh=-40)
    sou = silence.detect_nonsilent(audio_file, silence_thresh=-40)

    boosted = AudioSegment.empty()
    boosted += audio_file[:sou[0][0]]

    volume_boost = -abs(modification_values[0]) - audio_file.dBFS
    
    for i in range(len(sou)):
        print("LOOP BOOST")
        if not can_export:
            return False
        boosted += audio_file[sou[i][0]:sou[i][1]].apply_gain(volume_boost)
        try:
            boosted += audio_file[sou[i][1]:sou[i+1][0]]
        except IndexError:
            ...

    boosted += audio_file[sil[-1][0]:sil[-1][1]]

    sound_duration = len(boosted)

    fade_in = int(modification_values[1] * 1000)
    if fade_in > 0:
        boosted = boosted.fade(from_gain=-120.0, start=0, duration=fade_in)
    fade_out = int(modification_values[2] * 1000)
    if fade_out > 0:
        boosted = boosted.fade(to_gain=-120.0, start=sound_duration-fade_out, duration=fade_out)

    deaf = modification_values[3] * 1000

    boosted = boosted + AudioSegment.silent(duration=deaf)

    all_modified_audios.append(boosted)

    return True

    

def export_sounds(save_filename:str="") -> None:
    all_boosted = AudioSegment.empty()

    for ba in all_modified_audios:
        all_boosted = all_boosted + ba

    all_modified_audios.clear()

    if save_filename == "":
        splitter = get_path_splitter()

        if not os.path.exists(os.getcwd() + splitter + "temp"):
            os.mkdir("temp")

        temp_name = f"temp{splitter}temp_{time.time()}"
        all_boosted.export(temp_name, format='wav')
        return temp_name
    
    all_boosted.export(f"{save_filename}", format='wav', parameters=["-ac", "1"])
