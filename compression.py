# Here's the content related to the Seminar 3

from pydub import AudioSegment
import librosa
import soundfile as sf
import numpy as np


def desample(audio, n):
    return audio[0::n], 44100//n
  
def convertSoundFile(audio, sr=44100, inputFormat="wav", outputFormat="mp3"):
    if isinstance(audio, str):
        audio = AudioSegment.from_file(audio, format=inputFormat)
        audio = audio.set_frame_rate(sr)
    return audio.export(f"sounds_mp3_audio.{outputFormat}", format=outputFormat)

def load_audio(audio, sr, inputFormat="wav"):
    if isinstance(audio, str):
        audio,_ = librosa.load(audio, sr=sr)
        return audio
    return audio.set_frame_rate(sr)
def save_audio(audio, sr):
    if isinstance(audio, str):
        audio = load_audio(audio, sr)
    sf.write("sounds_mp3_audio.wav", audio, sr, format="wav")
    