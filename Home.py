#Main content of the app
import streamlit as st
from pydub import AudioSegment
from compression import *
from plots import *

st.set_page_config(
    page_title="Sound Player",
    page_icon="🔊",
    layout="wide",
    initial_sidebar_state="expanded",
    )

# Dictionary of our sounds
sounds = [
    {'name': "G Major Guitar Chord", 'path': 'sounds//G Major Guitar Chord.wav'},
    {'name': "Room Service House Bass", 'path': 'sounds//room_service_bass.m4a'},
    {'name': "Nirvana Guitar", 'path': 'sounds//Nirvana - Smell Like Teen Spirit (Guitar Only).mp3'},
    {'name': "Bass solo", 'path': "sounds//Incredible Victor Wooten solo bass jam.mp3"},
    {'name': "Custom (Upload your audio)", 'path': ""}
]


# Function to select sound and format
def st_soundSelector(sounds, formats=["mp3", "wav", "m4a", "aac", "ogg", "wma"]):
    selected_sound = st.sidebar.selectbox('Select sound:', [s['name'] for s in sounds])
    sound_index = [s['name'] for s in sounds].index(selected_sound)
    if selected_sound == 'Custom (Upload your audio)':
        uploaded_file = st.sidebar.file_uploader("Choose a file")
        if uploaded_file is not None:
            filename = uploaded_file.name
            with open(filename, "wb") as f:
                f.write(uploaded_file.getvalue())
            sounds[4]['path'] = filename
            sound_index = 4

    isOriginal = "(Original format)"
    originalFormat = sounds[sound_index]['path'][-3:]
    originalFormat_idx = formats.index(originalFormat) if originalFormat in formats else 0
    formats = [f"{format} {isOriginal}" if format == originalFormat else format for format in formats]

    selected_format = st.sidebar.selectbox('Select output format:', formats, index=originalFormat_idx)
    return sound_index, selected_format[:3]



def sidebar():
    st.sidebar.write("Customize your sound playback experience!")

    # Dropdown for selecting a sound format and sound
    sound_index, selected_format = st_soundSelector(sounds)

    # Slider for selecting sample rate
    sr_options = [8000, 16000, 22050, 24000, 44100, 48000]
    sr = int(st.sidebar.select_slider('Sample Rate (Hz):', options=sr_options, value=sr_options[-1]))

    # Button to play the sound
    st.sidebar.write('Play Original Sound')
    audio_path = sounds[sound_index]['path']
    st.sidebar.audio(audio_path, format=f'audio/{selected_format}')  # Plays audio
    size, unit = getSize(audio_path)
    st.sidebar.write(f"Size: {size:.2f} {unit} ")

    # Button to play the converted sound
    if st.sidebar.button('Play Converted Sound'):
        audio_path = sounds[sound_index]['path']
        st.write(f"Playing {audio_path} , {audio_path[-3:]} with a sample rate of {sr} Hz to {selected_format}")
        buffer = convertSoundFile(audio_path, sr, inputFormat=audio_path[-3:], outputFormat=selected_format)
        st.audio(buffer, format=f"audio/{selected_format}")
        size, unit = getSize(buffer)
        st.write(f"Converted sound size: {size:.2f} {unit} ")

    # Button to save the converted sound
    if st.sidebar.button('Save Converted Sound'):
        audio_path = sounds[sound_index]['path']
        new_audio = convertSoundFile(audio_path, sr, inputFormat=audio_path[-3:], outputFormat=selected_format)
        with open(f"sounds_mp3_audio.{selected_format}", "rb") as f:
            st.sidebar.download_button(label="Download Converted Sound", data=f, file_name=f"converted_sound.{selected_format}", mime=f"audio/{selected_format}")

    # Button for Magnitude Spectrum
    audio_path = sounds[sound_index]['path']
    y = load_audio(audio_path, sr)
    fig = plotSpectrum(y, sr)
    fig_signal= plotSignal(y, sr)
    
    st.pyplot(fig)
    st.plotly_chart(fig_signal, use_container_width=True)
    st.write(f"Plotting {audio_path} with a sample rate of {sr} Hz")
    #st.pyplot(fig_signal)
    # display the size of the audio file

    
def main():   
    # Title and subtitle for the app
    st.title("Acoustic Project 🔊")
    sidebar()


    
if __name__ == "__main__":
    main()