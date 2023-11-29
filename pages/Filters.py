import streamlit as st
from pydub import AudioSegment
from compression import *
import processing
import plots

st.set_page_config(
    page_title="Filtering Sounds",
    page_icon="🔊",
    layout="wide",
    initial_sidebar_state="expanded",
)
# Title and subtitle for the app
st.title("Acoustic Project 🔊")
st.sidebar.write("Let's filter your sound!")

# Dictionary of our sounds
sounds = [
    {'name': "G Major Guitar Chord", 'path': 'sounds//G Major Guitar Chord.wav'},
    {'name': "Room Service House Bass", 'path': 'sounds//room_service_bass.m4a'},
    {'name': "Nirvana Guitar", 'path': 'sounds//Nirvana - Smell Like Teen Spirit (Guitar Only).mp3'},
    {'name': "Bass solo", 'path': "sounds//Incredible Victor Wooten solo bass jam.mp3"},
    {'name': "Custom (Upload your audio)", 'path': ""}
]

# Dropdown for selecting a sound
selected_sound = st.sidebar.selectbox('Select sound:', [s['name'] for s in sounds]) #returns name
sound_index= [s['name'] for s in sounds].index(selected_sound) #returns index
if selected_sound == 'Custom (Upload your audio)':
    uploaded_file = st.sidebar.file_uploader("Choose a file")
    if uploaded_file is not None:
        filename = uploaded_file.name
        with open(filename, "wb") as f:
            f.write(uploaded_file.getvalue())
        sounds[4]['path'] = filename
        sound_index = 4

# Dropdown for selecting a sound format
f_formats = ["HPF", "LPF"]
selected_filter = st.sidebar.selectbox('Select the type of filter:', f_formats)

# Slider for selecting sample rate
sr_options = [8000, 16000, 22050, 24000, 44100, 48000]
sr = int(st.sidebar.select_slider('Sample Rate (Hz):', options=sr_options, value=sr_options[-1]))

# Slider for selecting cutoff frequency
cutoff_options = [20, 50, 70, 100, 400, 1000, 5000, 10000, 20000]
cutoff = int(st.sidebar.select_slider('Cutoff Frequency (Hz):', options=cutoff_options, value=cutoff_options[-1]))
# Create two columns for placing the buttons
col1, col2= st.sidebar.columns(2)

# Button to play the sound
audio_path = sounds[sound_index]['path']
st.sidebar.write('Original Sound:')
st.sidebar.audio(audio_path, format=f'audio/{audio_path[-3:]}') #plays audio
    
if col1.button('Save Converted Sound'):
    audio_path = sounds[sound_index]['path']
    original_audio = load_audio(audio_path, sr)
    if selected_filter == "HPF":
        filtered_audio = processing.hpf(original_audio, sr, cutoff)
        save_audio(filtered_audio, sr)
    else:
        filtered_audio = processing.lpf(original_audio, sr, cutoff)
        save_audio(filtered_audio, sr)
    
    with open(f"sounds_mp3_audio.wav", "rb") as f:
        st.sidebar.download_button(label="Download Converted Sound", data=f, file_name=f"converted_sound.wav", mime=f"audio/wav")
    
# Button to play the converted soundd
if col2.button('Play Filtered Sound'):
    audio_path = sounds[sound_index]['path']
    y = load_audio(audio_path, sr)
    if selected_filter == "HPF":
        filtered_audio = processing.hpf(y, sr, cutoff)
        save_audio(filtered_audio, sr)
    elif selected_filter == "LPF":
        filtered_audio = processing.lpf(y, sr, cutoff)
        save_audio(filtered_audio, sr)
    with open(f"sounds_mp3_audio.wav", "rb") as f:
        st.sidebar.audio(f, format=f'audio/wav')


#if cc.button('Plot Signal and Magnitude Spectrum'):
audio_path = sounds[sound_index]['path']
y = load_audio(audio_path, sr)
if selected_filter == "HPF":
    filtered_audio = processing.hpf(y, sr, cutoff)
elif selected_filter == "LPF":
    filtered_audio = processing.lpf(y, sr, cutoff)
else:
    filtered_audio= y
fig = plots.plotSpectrum(filtered_audio, sr)
fig_signal= plots.plotSignal(filtered_audio, sr)
    
st.pyplot(fig)
st.plotly_chart(fig_signal, use_container_width=True)
st.write(f"Plotting {audio_path} with a sample rate of {sr} Hz")