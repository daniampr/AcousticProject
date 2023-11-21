# Here's the content related to the Seminar 3

from pydub import AudioSegment
import librosa
import numpy as np


def desample(audio, n):
    return audio[0::n], 44100//n
  
def convertSoundFile(audio, sr=44100, inputFormat="wav", outputFormat="mp3"):
    if isinstance(audio, str):
        audio = AudioSegment.from_file(audio, format=inputFormat)
        audio = audio.set_frame_rate(sr)
    return audio.export("sounds_mp3_audio.mp3", format=outputFormat)

def load_audio(audio, sr, inputFormat="wav"):
    if isinstance(audio, str):
        audio,_ = librosa.load(audio, sr=sr)
        return audio
    return audio.set_frame_rate(sr)