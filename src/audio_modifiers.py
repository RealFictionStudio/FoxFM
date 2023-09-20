from pydub import AudioSegment, silence


def add_silience(secs:int):
    return AudioSegment.silent(secs * 1000, 44100)


def devide_into_segments(aseg:AudioSegment, accuracy:int):
    return aseg[::accuracy]


def modify_volume():
    volume_boost = 10
    boosted = AudioSegment.empty()

    sil = silence.detect_silence(sound, silence_thresh=-40)
    print(sil)
    sou = silence.detect_nonsilent(sound, silence_thresh=-40)
    print(sou)

    boosted += sound[0:sou[0][0]]

    for i in range(len(sou)):
        boosted += sound[sou[i][0]:sou[i][1]] + volume_boost
        try:
            boosted += sound[sou[i][1]:sou[i+1][0]]
        except IndexError:
            ...
    
    boosted += sound[sil[-1][0]:sil[-1][1]]

    boosted.export("boosttest.wav", "wav")
