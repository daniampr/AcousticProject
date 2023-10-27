# TO-DO: Set up a function that will compress the data changing to MP3 format
# TO-DO: Set up a function that will decompress the data changing to WAV format
# TO-DO: Set up a desampling function
from pydub import AudioSegment

import numpy as np
def desample(audio, n):
    return audio[0::n], 44100//n
  
def wav_to_mp3(wav_audio):
    wav_audio = AudioSegment.from_file(wav_audio, format = "wav")
    return wav_audio.export("sounds_mp3_audio.mp3", format = "mp3")

