import datetime
import webbrowser
from urllib.parse import quote_plus

import pyaudiowpatch as pyaudio
import pyttsx3
import speech_recognition as sr


# Lets SpeechRecognition use PyAudioWPatch on Windows.
sr.Microphone.get_pyaudio = staticmethod(lambda: pyaudio)

recognizer = sr.Recognizer()
engine = pyttsx3.init()


def speak(message):
    """Print and speak every assistant response."""
    print(f"Assistant: {message}")
    engine.say(message)
    engine.runAndWait()


def listen():
    """Listen through the microphone and convert speech to text."""
    try:
        with sr.Microphone() as source:
            print("\nListening...")
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=8)

        command = recognizer.recognize_google(audio).lower()
        print(f"You: {command}")
        return command

    except sr.WaitTimeoutError:
        speak("I did not hear anything. Please try again.")
    except sr.UnknownValueError:
        speak("Sorry, I did not understand that. Please repeat.")
    except sr.RequestError:
        speak("I cannot reach the speech recognition service. Please check your internet connection.")

    return ""


def handle_command(command):
    """Perform an action based on the spoken command."""
    if "hello" in command or "hi" in command:
        speak("Hello! How can I help you?")

    elif "time" in command:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The current time is {current_time}.")

    elif "date" in command or "day" in command:
        current_date = datetime.datetime.now().strftime("%A, %d %B %Y")
        speak(f"Today is {current_date}.")

    elif command.startswith("search for "):
        topic = command.replace("search for ", "", 1).strip()
        if topic:
            speak(f"Searching the web for {topic}.")
            webbrowser.open(f"https://www.google.com/search?q={quote_plus(topic)}")
        else:
            speak("Please say the topic you want to search for.")

    elif command.startswith("search "):
        topic = command.replace("search ", "", 1).strip()
        if topic:
            speak(f"Searching the web for {topic}.")
            webbrowser.open(f"https://www.google.com/search?q={quote_plus(topic)}")
        else:
            speak("Please say the topic you want to search for.")

    elif "exit" in command or "stop" in command or "goodbye" in command:
        speak("Goodbye! Have a nice day.")
        return False

    else:
        speak("Sorry, I do not know that command yet. Please try again.")

    return True


def main():
    speak("Hello! I am your voice assistant. You can ask me for the time, date, or a web search.")

    running = True
    while running:
        command = listen()

        if command:
            running = handle_command(command)


if __name__ == "__main__":
    main()