# Here's the content related to the Seminar 1

import librosa
import numpy as np
import matplotlib.pyplot as plt


def plotSpectogram(path):
    y, sr = librosa.load(path)
    spec = np.fft.fft(y)
    # shifted_spec=np.fft.fftshift(spec)
    freq = np.fft.fftfreq(y.shape[-1])
    D = librosa.stft(y)
    S_db = librosa.amplitude_to_db(np.abs(D), ref=np.max)
    # fig, (ax1,ax2) = plt.subplots(2)
    plt.plot(freq, spec.real, freq, spec.imag)
    
    
    # plt.magnitude_spectrum(y)
    # img = librosa.display.specshow(S_db, x_axis='time', y_axis='log', ax=ax2)
    # ax2.set(title='Using a logarithmic frequency axis')
    # fig.colorbar(img, ax=ax2, format="%+2.f dB")
    
    
    plt.show()
plotSpectogram("sounds/room_service_bass.m4a")