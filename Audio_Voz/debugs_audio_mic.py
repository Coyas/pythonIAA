import speech_recognition as sr

# Specify the microphone device (if you know it)
# You can list available microphones using sr.Microphone.list_microphone_names()

mic = sr.Microphone(device_index=1)  # Change device_index if needed
print('hello eu sou ailton duarte e tens q falar como deve dser')

# Capture audio from the microphone
with mic as source:
    print("Listening...")
    audio = sr.Recognizer().listen(source, timeout=5, phrase_time_limit=10)
    try:
        text = sr.Recognizer().recognize_google(audio, language='pt-PT')
        print("You said: " + text)
    except sr.UnknownValueError:
        print("Could not understand the audio")
    except sr.RequestError:
        print("Could not request results from Google Speech Recognition service")
