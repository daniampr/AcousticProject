# Here's the content related to the Seminar 1

import matplotlib.pyplot as plt


def plotSpectrum(y,fs=44100):
    fig ,(ax1,ax2) = plt.subplots(ncols=1,nrows=2,figsize=(10,5),layout='constrained')
    ax1.magnitude_spectrum(y,Fs=fs,c="r")
    ax2.specgram(y,Fs=fs)
    return fig