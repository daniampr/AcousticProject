import streamlit as st
from pydub import AudioSegment
from compression import convertSoundFile
from utils import getSize

st.set_page_config(
    page_title="Sound Player",
    page_icon="🔊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Title and subtitle for the app
st.title("Advanced Sound Player 🔊")
st.write("Customize your sound playback experience!")

# Dictionary of our sounds
sounds = [
    {'name': "G Major Guitar Chord", 'path': 'sounds/G Major Guitar Chord.wav'},
    {'name': "Room Service House Bass", 'path': 'sounds/room_service_bass.m4a'},
    {'name': "Nirvana Guitar", 'path': 'sounds/Nirvana - Smell Like Teen Spirit (Guitar Only).mp3'},
    {'name': "Bass solo", 'path': "sounds/Incredible Victor Wooten solo bass jam.mp3"},
    {'name': "Custom (Upload your audio)", 'path': ""}
]

# Dropdown for selecting a sound
selected_sound = st.selectbox('Select sound:', [s['name'] for s in sounds]) #returns name
sound_index= [s['name'] for s in sounds].index(selected_sound) #returns index
if selected_sound == 'Custom (Upload your audio)':
    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file is not None:
        custom_path = uploaded_file.read()
        st.write("File size:", getSize(uploaded_file.size))
        sounds[-1]['path'] = custom_path
        sound_index = -1

# Dropdown for selecting a sound format
formats = ["mp3", "wav", "m4a", "aac", "flac", "ogg", "opus", "wma", "alac", "aiff"]
selected_format = st.selectbox('Select output format:', formats)

# Slider for selecting sample rate
sample_rate_options = [8000, 16000, 22050, 24000, 44100, 48000]
sample_rate = st.select_slider('Sample Rate (Hz):', options=sample_rate_options, value=sample_rate_options[-1])

# Slider for selecting bit rate [to do]

# Create two columns for placing the buttons
_,_, col1, col2, col3,_, _ = st.columns(7)

# Button to play the sound
if col1.button('Play Original Sound'):
    audio = sounds[sound_index]['path']
    st.audio(audio, format=f'audio/{selected_format}')
    
if col2.button('Save Converted Sound'):
    audio = sounds[sound_index]['path']
    new_audio = convertSoundFile(audio, selected_format)
    st.download_button(label="Download Converted Sound", data=new_audio, file_name=f"converted_sound.{selected_format}")
    

# Button to play the converted soundd
if col3.button('Play Converted Sound'):
    
    audio = sounds[sound_index]['path']
    new_audio = convertSoundFile(audio, selected_format)
    
    st.audio(new_audio, format=f'audio/{selected_format}')
