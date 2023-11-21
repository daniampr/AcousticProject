# Here's the content related to the Seminar 1

import librosa
import numpy as np
import matplotlib.pyplot as plt


def plotSpectogram(y,fs=44100):
    fig, (ax1,ax2,ax3) = plt.subplots(3,figsize=(10,5),layout='constrained')
    ax1.plot(y)
    ax2.magnitude_spectrum(y,Fs=fs,c="r")
    ax3.magnitude_spectrum(y,Fs=fs,scale="dB",c="g")
    ax1.set_title("Signal")

    
    plt.show()