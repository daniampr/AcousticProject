import streamlit as st
from io import BytesIO
from pydub import AudioSegment
from compression import convertSoundFile, load_audio
from utils import getSize


def play_st_audio(audio_data, format):
    # Check if audio_data is already an AudioSegment object
    if isinstance(audio_data, AudioSegment):
        audio_segment = audio_data
    else:
        # If it's a file-like object, read it into an AudioSegment
        audio_segment = AudioSegment.from_file(audio_data, format=format)

    # Convert the AudioSegment to a binary buffer
    buffer = BytesIO()
    audio_segment.export(buffer, format=format)
    buffer.seek(0)

    # Use the buffer in st.audio
    st.audio(buffer, format=f'audio/{format}')


st.set_page_config(
    page_title="Sound Player",
    page_icon="🔊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Title and subtitle for the app
st.title("Acoustic Project 🔊")
st.write("Customize your sound playback experience!")

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
        custom_path = uploaded_file.read()
        st.write("File size:", getSize(uploaded_file.size))
        sounds[-1]['path'] = custom_path
        sound_index = -1

# Dropdown for selecting a sound format
formats = ["mp3", "wav", "m4a", "aac", "flac", "ogg", "opus", "wma", "alac", "aiff"]
selected_format = st.selectbox('Select output format:', formats)

# Slider for selecting sample rate
sr_options = [8000, 16000, 22050, 24000, 44100, 48000]
sr = int(st.select_slider('Sample Rate (Hz):', options=sr_options, value=sr_options[-1]))

# Slider for selecting bit rate [to do]

# Create two columns for placing the buttons
_,_, col1, col2, col3,_,_ = st.columns(7)

# Button to play the sound
if col1.button('Play Original Sound'):
    audio_path = sounds[sound_index]['path']
    #audio= load_audio(audio_path, sr) #loads audio & changes sample rate
    st.audio(audio_path, format=f'audio/{selected_format}') #plays audio


if col2.button('Save Converted Sound'):
    audio_path = sounds[sound_index]['path']
    new_audio = convertSoundFile(audio_path,sr,inputFormat=audio_path[-3:],outputFormat=selected_format)   
    with open(f"sounds_mp3_audio.{selected_format}", "rb") as f:
        st.download_button(label="Download Converted Sound", data=f, file_name=f"converted_sound.{selected_format}", mime=f"audio/{selected_format}")
    

# Button to play the converted soundd
if col3.button('Play Converted Sound'):
    audio_path = sounds[sound_index]['path']
    new_audio = convertSoundFile(audio_path,sr,inputFormat=audio_path[-3:],outputFormat=selected_format)
    play_st_audio(new_audio, selected_format)