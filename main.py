import numpy as np
import matplotlib.pyplot as plt
import librosa
#from processing import lpf, hpf
from compression import desample, wav_to_mp3
from IPython.display import Audio
#from playsound import playsound
from pydub import AudioSegment



def main():
   # audio, sr = librosa.load("sounds\g-major_chordAcoustic.wav", sr=44100)
   # print(sr)
    #print("loaded")
   # playsound(audio)
   # audio_2, sr= desample(audio, 2)
   # playsound(audio_2)
    new_mp3= wav_to_mp3("g-major_chordAcoustic.wav")
    print("loaded mp3")
if __name__ == "__main__":
    main()
    