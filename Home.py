#Main content of the app
import streamlit as st
from pydub import AudioSegment
from compression import *
import processing
from plots import *


st.set_page_config(
    page_title="Acoustic Project",
    page_icon="🔊",
    layout="wide",
    initial_sidebar_state="expanded",
    )

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)


footer="""<style>
a:link , a:visited{
color: blue;
background-color: transparent;
text-decoration: underline;
}

a:hover,  a:active {
color: red;
background-color: transparent;
text-decoration: underline;
}

.footer {
position: fixed;
left: 0;
bottom: 0;
width: 100%;
background-color: transparent;
color: white;
text-align: center;
}
</style>
<div class="footer">
<p>Made with ❤️ by Raquel Maldonado, Juande Gutierrez, Claudia Guallarte, and Daniel Amirian <a style='display: block; text-align: center;'</p>
</div>
"""
st.markdown(footer,unsafe_allow_html=True)
# Dictionary of our sounds
sounds = [
    {'name': "G Major Guitar Chord", 'path': 'sounds//G Major Guitar Chord.wav'},
    {'name': "Room Service House Bass", 'path': 'sounds//room_service_bass.m4a'},
    {'name': "Nirvana Guitar", 'path': 'sounds//Nirvana - Smell Like Teen Spirit (Guitar Only).mp3'},
    {'name': "Bass solo", 'path': "sounds//Incredible Victor Wooten solo bass jam.mp3"},
    {'name': "Custom (Upload your audio)", 'path': ""}
]


# Function to select sound and format
def st_soundSelector(sounds, formats=["mp3", "wav", "m4a"]):
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

                
    # Dropdown for selecting a sound format
    f_formats = ["None", "HPF", "LPF"]
    selected_filter = st.sidebar.selectbox('Select the type of filter:', f_formats, index=0 )

    isOriginal = "(Original format)"
    originalFormat = sounds[sound_index]['path'][-3:]
    originalFormat_idx = formats.index(originalFormat) if originalFormat in formats else 0
    formats = [f"{format} {isOriginal}" if format == originalFormat else format for format in formats]

    selected_format = st.sidebar.selectbox('Select output format:', formats, index=originalFormat_idx)
    return sound_index, selected_format[:3], selected_filter



def sidebar():
    st.sidebar.write("Customize your sound playback experience!")

    # Dropdown for selecting a sound format and sound
    sound_index, selected_format, selected_filter = st_soundSelector(sounds)

    if selected_filter != "None":
        # Slider for selecting cutoff frequency
        cutoff_options = [20, 50, 70, 100, 400, 1000, 5000, 10000, 20000]
        cutoff = int(st.sidebar.select_slider('Cutoff Frequency (Hz):', options=cutoff_options, value=cutoff_options[-1]))

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
        st.write(f"Playing {sounds[sound_index]['name']} from {audio_path[-3:]} with a sample rate of {sr} Hz to {selected_format}")
        if selected_filter == "None":
            buffer = convertSoundFile(audio_path, sr, inputFormat=audio_path[-3:], outputFormat=selected_format)
            if selected_format=="m4a":
                selected_format="mp3"
            st.audio(buffer, format=f"audio/{selected_format}")
            size, unit = getSize(buffer)
        
        elif selected_filter == "HPF":
            filtered = processing.hpf(audio_path, sr, cutoff)
            save_audio(filtered, sr, outputFormat=selected_format)
            with open(f"sounds_mp3_audio.{selected_format}", "rb") as f:
               st.audio(f, format=f"audio/{selected_format}")
               size, unit = getSize(f"sounds_mp3_audio.{selected_format}")
               st.write(f"Converted sound size: {size:.2f} {unit} ")

        elif selected_filter== "LPF":  
            filtered = processing.lpf(audio_path, sr, cutoff)
            save_audio(filtered, sr, outputFormat=selected_format)
            with open(f"sounds_mp3_audio.{selected_format}", "rb") as f:
                st.audio(f, format=f"audio/{selected_format}")
                size, unit = getSize(f"sounds_mp3_audio.{selected_format}")
                st.write(f"Converted sound size: {size:.2f} {unit} ")

    # Button to save the converted sound
    if st.sidebar.button('Save Converted Sound'):
        audio_path = sounds[sound_index]['path']
        format= audio_path[-3:]
        
        if selected_filter == "HPF":
            filtered = processing.hpf(audio_path, sr, cutoff)
            convertSoundFile(filtered, sr, inputFormat=format, outputFormat=selected_format)
            with open(f"sounds_mp3_audio.{selected_format}", "rb") as f:
               st.sidebar.download_button(label="Download Converted Sound", data=f, file_name=f"converted_sound.{format}", mime=f"audio/{format}")

        elif selected_filter== "LPF":
            filtered = processing.lpf(audio_path, sr, cutoff)
            #save_audio(filtered, sr, outputFormat=selected_format)
            convertSoundFile(filtered, sr, inputFormat=format, outputFormat=selected_format)
            with open(f"sounds_mp3_audio.{selected_format}", "rb") as f:
                st.sidebar.download_button(label="Download Converted Sound", data=f, file_name=f"converted_sound.{format}", mime=f"audio/{format}")

        else:   
            new_audio = convertSoundFile(audio_path, sr, inputFormat=audio_path[-3:], outputFormat=selected_format)
        #with open(f"sounds_mp3_audio.{selected_format}", "wb") as f:
            st.sidebar.download_button(label="Download Converted Sound", data=new_audio, file_name=f"converted_sound.{selected_format}", mime=f"audio/{selected_format}")

    # Button for Magnitude Spectrum
    audio_path = sounds[sound_index]['path']
    format= audio_path[-3:]
    if selected_filter== "None":
        y = load_audio(audio_path, sr, inputFormat=selected_format)
    elif selected_filter== "HPF":
        y = processing.hpf(audio_path, sr, cutoff)        
        st.write(f"Filtered using a HPF with a cutoff frequency of {cutoff} Hz")    

    else:
        y = processing.lpf(audio_path, sr, cutoff)
        st.write(f"Filtered using a LPF with a cutoff frequency of {cutoff} Hz")    

    st.write(f"Plotting {sounds[sound_index]['name']} from {audio_path[-3:]} with a sample rate of {sr} Hz to {selected_format}")
    fig = plotSpectrum(y, sr)
    fig_signal= plotSignal(y, sr)
    
    st.pyplot(fig)
    st.plotly_chart(fig_signal, use_container_width=True)

    
def main():   
    # Title and subtitle for the app
    st.title("Acoustic Project 🔊")
    st.subheader("In this app you can play with different audio formats and filters, and see their plots. Enjoy!")
              
    sidebar()


    
if __name__ == "__main__":
    main()