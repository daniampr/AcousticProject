import streamlit as st
from pydub import AudioSegment
from compression import convertSoundFile, load_audio,save_audio
from utils import getSize
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
st.write("Let's filter your sound!")

# Dictionary of our sounds
sounds = [
    {'name': "G Major Guitar Chord", 'path': 'sounds//G Major Guitar Chord.wav'},
    {'name': "Room Service House Bass", 'path': 'sounds//room_service_bass.m4a'},
    {'name': "Nirvana Guitar", 'path': 'sounds//Nirvana - Smell Like Teen Spirit (Guitar Only).mp3'},
    {'name': "Bass solo", 'path': "sounds//Incredible Victor Wooten solo bass jam.mp3"},
    {'name': "Custom (Upload your audio)", 'path': ""}
]

# Dropdown for selecting a sound
selected_sound = st.selectbox('Select sound:', [s['name'] for s in sounds]) #returns name
sound_index= [s['name'] for s in sounds].index(selected_sound) #returns index
if selected_sound == 'Custom (Upload your audio)':
    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file is not None:
        filename = uploaded_file.name
        with open(filename, "wb") as f:
            f.write(uploaded_file.getvalue())
        sounds[4]['path'] = filename
        sound_index = 4

# Dropdown for selecting a sound format
f_formats = ["HPF", "LPF"]
selected_filter = st.selectbox('Select the type of filter:', f_formats)
formats = ["mp3", "wav", "m4a", "aac", "ogg", "wma"]
selected_format = st.selectbox('Select output format:', formats)

# Slider for selecting sample rate
sr_options = [8000, 16000, 22050, 24000, 44100, 48000]
sr = int(st.select_slider('Sample Rate (Hz):', options=sr_options, value=sr_options[-1]))

# Slider for selecting cutoff frequency
cutoff_options = [100, 400, 1000, 5000, 10000, 20000]
cutoff = int(st.select_slider('Cutoff Frequency (Hz):', options=cutoff_options, value=cutoff_options[-1]))
# Create two columns for placing the buttons
_,_, col1, col2, col3,_, _ = st.columns(7)

# Button to play the sound
if col1.button('Play Original Sound'):
    audio_path = sounds[sound_index]['path']
    st.audio(audio_path, format=f'audio/{selected_format}') #plays audio
    
if col2.button('Save Converted Sound'):
    audio_path = sounds[sound_index]['path']
    original_audio = load_audio(audio_path, sr)
    if selected_filter == "HPF":
        filtered_audio = processing.hpf(original_audio, sr, cutoff)
        save_audio(filtered_audio, sr)
        convertSoundFile("sounds_mp3_audio.wav", sr, inputFormat="wav", outputFormat=selected_format)

    else:
        filtered_audio = processing.lpf(original_audio, sr, cutoff)
        save_audio(filtered_audio, sr)
        convertSoundFile("sounds_mp3_audio.wav", sr, inputFormat="wav", outputFormat=selected_format)
    
    with open(f"sounds_mp3_audio.{selected_format}", "rb") as f:
        st.download_button(label="Download Converted Sound", data=f, file_name=f"converted_sound.{selected_format}", mime=f"audio/{selected_format}")
    
# Button to play the converted soundd
if col3.button('Play Filtered Sound'):
    audio_path = sounds[sound_index]['path']
    y = load_audio(audio_path, sr)
    if selected_filter == "HPF":
        filtered_audio = processing.hpf(y, sr, cutoff)
        save_audio(filtered_audio, sr)
    elif selected_filter == "LPF":
        filtered_audio = processing.lpf(y, sr, cutoff)
        save_audio(filtered_audio, sr)
    with open(f"sounds_mp3_audio.wav", "rb") as f:
        st.audio(f, format=f'audio/wav')
# Create two columns for placing the buttons
_,_, _, cc, _,_, _ = st.columns(7)
if cc.button('Plot Signal and Magnitude Spectrum'):
    audio_path = sounds[sound_index]['path']
    y = load_audio(audio_path, sr)
    if selected_filter == "HPF":
        filtered_audio = processing.hpf(y, sr, cutoff)
    elif selected_filter == "LPF":
        filtered_audio = processing.lpf(y, sr, cutoff)
    fig = plots.plotSpectrum(filtered_audio,sr)
    st.pyplot(fig)