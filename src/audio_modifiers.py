from pydub import AudioSegment, silence
import math


def add_silience(secs:int):
    return AudioSegment.silent(secs * 1000, 44100)


def devide_into_segments(aseg:AudioSegment, accuracy:int):
    return aseg[::accuracy]


def modify_volume(file_name:str, volume_boost:float):
    sound = AudioSegment.from_file(file_name)
    boosted = AudioSegment.empty()

    sil = silence.detect_silence(sound, silence_thresh=-40)
    sou = silence.detect_nonsilent(sound, silence_thresh=-40)

    boosted += sound[0:sou[0][0]]

    for i in range(len(sou)):
        boosted += sound[sou[i][0]:sou[i][1]] + volume_boost
        try:
            boosted += sound[sou[i][1]:sou[i+1][0]]
        except IndexError:
            ...
    
    boosted += sound[sil[-1][0]:sil[-1][1]]

    boosted.export(f"{file_name[-1]}_boosted.wav", "wav")


def unify_volume_levels(file_names:list[str], volume_value:float=0):
    audio_files = []
    mean = 0
    for i in file_names:
        n_seg = AudioSegment.from_file(i)
        audio_files.append(n_seg)
        mean += n_seg.dBFS

    mean /= len(audio_files)

    if volume_value != 0:
        mean = volume_value

    for i in audio_files:
        modify_volume(i, mean)