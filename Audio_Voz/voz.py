import speech_recognition as sr

# Initialize recognizer and microphone
recognizer = sr.Recognizer()
mic = sr.Microphone(device_index=1)  # Adjust device index as needed

print("Adjusting for ambient noise...")
with mic as source:
    recognizer.adjust_for_ambient_noise(source)
    print("Listening for your command...")

    try:
        # Timeout of 5 seconds to wait for the first sound
        audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)  # timeout and phrase_time_limit
        print("Audio captured, attempting to recognize speech...")
        
        # Attempt to recognize speech
        text = recognizer.recognize_google(audio, language='pt-PT')  # Change language if needed
        print("You said: " + text)

    except sr.WaitTimeoutError:
        print("Error: No speech detected. Please speak clearly.")
    except sr.UnknownValueError:
        print("Error: Could not understand the audio. Please try again.")
    except sr.RequestError as e:
        print(f"Error: Could not request results from Google Speech Recognition service; {e}")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
