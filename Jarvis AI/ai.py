from time import time
import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import pyjokes
import webbrowser
import pygame
import os

pygame.init()

def play_turned_on_sound():
    sound_file = os.path.join(os.getcwd(), 'audio', 'initialized.wav')
    pygame.mixer.init()
    pygame.mixer.music.load(sound_file)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    pygame.mixer.quit()

voice_recognizer = sr.Recognizer()
speech_engine = pyttsx3.init()

initialized_flag = False
last_command_time = time()

def speak(text):
    speech_engine.say(text)
    speech_engine.runAndWait()

def listen_command():
    global last_command_time
    try:
        with sr.Microphone() as source:
            print('Listening...')
            audio = voice_recognizer.listen(source)
            command = voice_recognizer.recognize_google(audio).lower()
            print(command)
            if 'jarvis' in command:
                command = command.replace('jarvis', '')
                current_time = datetime.datetime.now().strftime('%I:%M %p')
                speak('Sir, You have no event today, and local time is ' + current_time)
                last_command_time = time()
    except sr.UnknownValueError:
        speak("Sorry, I did not understand that.")
        command = ""
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        command = ""
    return command

def check_shutdown():
    global last_command_time
    current_time = time()
    if current_time - last_command_time > 60:
        speak("Sir, I am shutting down due to inactivity. See you later!")
        exit()

def about_the_ai():
    speak("I am Jarvis, a voice-activated assistant created using Python. My purpose is to assist you with various tasks and provide information. "
         "I can play music, tell jokes, provide the current time, and more. If you have any questions or need assistance, feel free to ask.")

def apologize():
    speak("I apologize, but I don't understand that command. Please provide a valid command.")
    run_jarvis()

def shutdown():
    speak("Shutting down...")
    exit()

def run_jarvis():
    global last_command_time, initialized_flag
    if not initialized_flag:
        play_turned_on_sound()
        initialized_flag = True

    check_shutdown()
    command = listen_command()
    if command:
        last_command_time = time()
        if 'play' in command:
            song = command.replace('play', '')
            speak('Playing ' + song)
            pywhatkit.playonyt(song)
        elif 'time' in command:
            current_time = datetime.datetime.now().strftime('%I:%M %p')
            speak('Current time is ' + current_time)
        elif 'facebook' in command:
            speak('Opening Facebook.')
            webbrowser.open('https://www.facebook.com/')
        elif 'email' in command:
            speak('Opening mail.')
            webbrowser.open('https://mail.google.com/')
        elif 'joke' in command:
            speak(pyjokes.get_joke())
        elif 'search' in command:
            search_query = command.replace('search', '')
            speak(f"Searching for {search_query}")
        elif 'about yourself' in command:
            about_the_ai()
        elif 'shutdown' in command or 'shut down' in  command or 'relax' in command:
            shutdown()
        else:
            apologize()

if __name__ == "__main__":
    while True:
        run_jarvis()