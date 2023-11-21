import compression
audio_path = "sounds//G Major Guitar Chord.wav"
sr=44100
selected_format="mp3"
new_audio = compression.convertSoundFile(audio_path,sr,inputFormat=audio_path[-3:],outputFormat=selected_format)
print(compression.load_audio("sounds_mp3_audio.mp3",sr))
