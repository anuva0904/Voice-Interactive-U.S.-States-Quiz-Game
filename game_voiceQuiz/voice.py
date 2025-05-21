import pyttsx3
import speech_recognition as sr
from pyttsx3 import voice


class VoiceAssistant:
    def __init__(self):
        """

        :rtype: object
        """
        self.engine = pyttsx3.init()
        self.recognizer = sr.Recognizer()
        print("Hello, i am you voice assistant")

    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()


    def listen(self):
       r = sr.Recognizer()
       with sr.Microphone() as source:
        r.energy_threshold = 10000
        r.adjust_for_ambient_noise(source)
        print("listening...")
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            print(text)
            return text
        except:
            return "Sorry, I didn't get you!"


