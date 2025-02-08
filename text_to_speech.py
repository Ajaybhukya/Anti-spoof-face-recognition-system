import pyttsx3
def text_to_speech(name):
    # Initialize the text-to-speech engine
    engine = pyttsx3.init()

    # Set properties like voice and speed (optional)
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)  # Use the first voice (change to [1] for the second)

    # Speak the provided text
    text=f"Hello {name}! Today attendance sent to mail"
    engine.say(text)
    engine.runAndWait()
    # Close the text-to-speech engine
    engine.stop()
def text_to_speech_direct(text):
    # Initialize the text-to-speech engine
    engine = pyttsx3.init()

    # Set properties like voice and speed (optional)
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)  # Use the first voice (change to [1] for the second)

    # Speak the provided text
    engine.say(text)
    engine.runAndWait()
    # Close the text-to-speech engine
    engine.stop()
