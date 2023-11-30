# Here's the content related to the Seminar 3

from pydub import AudioSegment
import librosa
import soundfile as sf
import numpy as np
import os
from io import BytesIO


def desample(audio, n):
    return audio[0::n], 44100//n
  
def convertSoundFile(audio, sr=44100, inputFormat="wav", outputFormat="mp3"):
    if outputFormat == "m4a" and inputFormat !="m4a":
        outputFormat = "mp3"
    if isinstance(audio, str):
        audio = AudioSegment.from_file(audio, format=inputFormat)
        audio = audio.set_frame_rate(sr)
        # Use an in-memory buffer 
        buffer = BytesIO()
        audio.export(buffer, format=outputFormat)
        buffer.seek(0)  # Reset the buffer to the start
        return buffer
    # case audio is numpy array
    elif isinstance(audio, np.ndarray):
        save_audio(audio, sr, outputFormat)

    #audio_array = (audio_array * 32767).astype(np.int16)

    

def load_audio(audio, sr, inputFormat="wav"):
    if isinstance(audio, str):
        audio,_ = librosa.load(audio, sr=sr)
        return audio
    return audio.set_frame_rate(sr)


def save_audio(audio, sr, outputFormat):
    # For cases we have a numpy array
    if isinstance(audio, str):
        audio = load_audio(audio, sr)
    sf.write(f"sounds_mp3_audio.{outputFormat}", audio, sr, format=outputFormat)
    
def getSize(path):
    try:
        if isinstance(path, BytesIO):
            path.seek(0, os.SEEK_END)  # Go to end of file
            size = path.tell()         # Get size
            path.seek(0)               
        else:
            size = os.path.getsize(path)
        
        if size > 1024 and size<=1048576:
            return size/1024, "KB"
        elif size >= 1048576:
            return size/1048576, "MB"
        else:
            return size, "bytes"
    except OSError as e:
        print(f"Error: {e}")
        return None
