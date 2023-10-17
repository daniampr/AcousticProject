import numpy as np
import matplotlib.pyplot as plt

import librosa
y, sr = librosa.load("./AcousticProject/Incredible Victor Wooten solo bass jam.mp3")
D = librosa.stft(y)  # STFT of y
S_db = librosa.amplitude_to_db(np.abs(D), ref=np.max)
fig, ax = plt.subplots()
img = librosa.display.specshow(S_db, x_axis='time', y_axis='log', ax=ax)
ax.set(title='Using a logarithmic frequency axis')
fig.colorbar(img, ax=ax, format="%+2.f dB")
