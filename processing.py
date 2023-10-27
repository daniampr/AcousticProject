import librosa
from scipy.signal import butter, lfilter, filtfilt

def lpf(y, sr, cutoff):
    '''
    Creates a low-pass filter to remove high frequencies from the audio signal
     @param audio: audio signal
     @param sr: sampling rate
     @param cutoff: cutoff frequency
     @return: filtered audio signal
    '''
    if y.dtype==str:
        y, sr = librosa.load(y)
    
    nyquist = 0.5 * sr
    normal_cutoff = cutoff / nyquist  # Normalize cutoff with Niquist frequency
    b, a = butter(1, normal_cutoff, btype='low', analog=False)

    y_filtered = lfilter(b, a, y)
    return y_filtered
# Checkear function

def hpf(audio, sr, cutoff):
    '''
    Creates a low-pass filter to remove high frequencies from the audio signal
     @param audio: audio signal
     @param sr: sampling rate
     @param cutoff: cutoff frequency
     @return: filtered audio signal
    '''
    if audio.dtype==str:  #case y is a path
        audio, sr = librosa.load(audio)
    
    # Design the Butterworth low-pass filter
    nyquist = 0.5 * sr
    normal_cutoff = cutoff / nyquist  # Normalize cutoff with Niquist frequency
    b, a = butter(5, normal_cutoff, btype='highpass', analog=False)

    # Apply the filter to the audio signal
    filtered = filtfilt(b, a, audio)
    return filtered

