from pydub import AudioSegment, silence

# -1 = <-3;-4>
# each modify has +- 1 in real

def modify_volume(filename:str, volume_value:float, save_filename:str="output.wav"):
    audio_file = AudioSegment.from_file(filename)
    sil = silence.detect_silence(audio_file, silence_thresh=-40)
    sou = silence.detect_nonsilent(audio_file, silence_thresh=-40)

    boosted = AudioSegment.empty()
    boosted += audio_file[:sou[0][0]]

    volume_boost = volume_value - audio_file.dBFS
    
    for i in range(len(sou)):
        boosted += audio_file[sou[i][0]:sou[i][1]].apply_gain(volume_boost)
        try:
            boosted += audio_file[sou[i][1]:sou[i+1][0]]
        except IndexError:
            ...

    boosted += audio_file[sil[-1][0]:sil[-1][1]]

    boosted.export(save_filename)

