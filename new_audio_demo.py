import pyttsx3

# Initialize the TTS engine
engine = pyttsx3.init("sapi5")

# Get the list of available voices
voices = engine.getProperty("voices")
engine.setProperty('rate', 150)
# Print out all available voices
for index, voice in enumerate(voices):
    print(f"Voice {index}: {voice.name}")

# Set the desired voice by index (change the index to the desired voice)
desired_voice_index = 2 # Change this index to select a different voice
engine.setProperty('voice', voices[desired_voice_index].id)

# Speak a test phrase
engine.say("Hello hi do you like to use this voice to read you audio book")
engine.runAndWait()
