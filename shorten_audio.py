from pydub import AudioSegment

# Load the downsampled audio
audio = AudioSegment.from_wav("final_audio_16k.wav")

# Trim to first 30 seconds (30,000 milliseconds)
short_audio = audio[:30000]

# Export the trimmed file
short_audio.export("short_final_audio.wav", format="wav")