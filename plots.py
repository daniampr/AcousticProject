# Here's the content related to the Seminar 1
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go


def plotSignal(y, fs, title='Signal Plot', xlabel='Time [s]', ylabel='Amplitude'):
    """
    Plots a signal using Plotly.

    param signal: The signal data (numpy array).
    param fs: Sampling rate.
    param title: Title of the plot.
    param xlabel: Label for the x-axis.
    param ylabel: Label for the y-axis.
    return: Plotly figure object.
    """
    t = np.linspace(0, len(y)/fs, len(y))  # Time vector based on signal length and sampling rate
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=t, y=y, mode='lines', name='Signal'))

    # Update layout
    fig.update_layout(title=title, xaxis_title=xlabel, yaxis_title=ylabel)

    return fig
  

def plotSpectrum(y,fs=44100):
    fig ,(ax1,ax2) = plt.subplots(ncols=1,nrows=2,figsize=(10,5),layout='constrained')
    ax1.magnitude_spectrum(y,Fs=fs,c="r")
    ax1.set_title(f"Magnitude Spectrum at a sample rate of {fs} Hz")
    ax2.specgram(y,Fs=fs)
    ax2.set_title(f"Spectrogram at a sample rate of {fs} Hz")
    ax2.set_xlabel("Time [s]")
    ax2.set_ylabel("Frequency [Hz]")
    return fig