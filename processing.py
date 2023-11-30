# Here's the content related to the Seminar 2


import librosa
from scipy.signal import butter, lfilter, filtfilt

def lpf(audio, sr, cutoff):
    if type(audio)==str:  #case y is a path
        audio, sr = librosa.load(audio, sr=sr)
    b, a = butter(10, cutoff, fs=sr, btype='low', analog=False)
    y_filtered = lfilter(b, a, audio)
    return y_filtered


def hpf(audio, sr, cutoff):
    '''
    Creates a low-pass filter to remove high frequencies from the audio signal
    Parameters
     @param audio: audio signal
     @param sr: sampling rate
     @param cutoff: cutoff frequency
     @return: filtered audio signal
    '''
    if type(audio)==str:  #case y is a path
        audio, sr = librosa.load(audio, sr=sr)
    
    # Design the Butterworth low-pass filter
    nyquist = 0.5 * sr
    normal_cutoff = cutoff / nyquist  # Normalize cutoff with Niquist frequency
    b, a = butter(10, normal_cutoff, btype='highpass', analog=False)

    # Apply the filter to the audio signal
    filtered = filtfilt(b, a, audio)
    return filtered



