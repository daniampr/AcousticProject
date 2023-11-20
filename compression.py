# Here's the content related to the Seminar 3

from pydub import AudioSegment
import numpy as np


def desample(audio, n):
    return audio[0::n], 44100//n
  
def convertSoundFile(audio, inputFormat="wav", outputFormat = "mp3"):
    audio = AudioSegment.from_file(audio, format = inputFormat)
    return audio.export("sounds_mp3_audio.mp3", format = outputFormat)

