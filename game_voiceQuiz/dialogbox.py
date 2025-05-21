import tkinter as tk
from tkinter import simpledialog
import speech_recognition as sr
from PIL import Image, ImageTk

class VoiceInputDialog(simpledialog.Dialog):
    def __init__(self, parent, title, voice_assistant):
        self.voice_assistant = voice_assistant
        super().__init__(parent, title)

    def body(self, master):
        label = tk.Label(master, text="Enter a state name or click the mic:")
        label.pack(pady=5)

        entry_frame = tk.Frame(master)
        entry_frame.pack()

        self.entry = tk.Entry(entry_frame, width=30)
        self.entry.pack(side=tk.LEFT, padx=(0, 5))

        mic_image = Image.open("mics.gif").resize((20, 20))
        self.mic_photo = ImageTk.PhotoImage(mic_image)

        mic_button = tk.Button(entry_frame, image=self.mic_photo, command=self.use_voice)
        mic_button.pack(side=tk.LEFT)

        return self.entry  # Sets initial focus

    def buttonbox(self):
        box = tk.Frame(self)

        tk.Button(box, text="OK", width=10, command=self.get_text_input).pack(side=tk.LEFT, padx=5)
        tk.Button(box, text="Cancel", width=10, command=self.cancel).pack(side=tk.LEFT, padx=5)

        self.bind("<Return>", lambda event: self.get_text_input())
        self.bind("<Escape>", self.cancel)

        box.pack()

    def get_text_input(self):
        self.result = self.entry.get()
        self.ok()

    def use_voice(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            self.voice_assistant.speak("Listening... please say a state name.")
            try:
                audio = recognizer.listen(source, timeout=5)
                text = recognizer.recognize_google(audio)
                self.voice_assistant.speak(f"I heard: {text}")
                self.entry.delete(0, tk.END)
                self.entry.insert(0, text)

                self.result = text
                self.ok()
            except sr.UnknownValueError:
                self.voice_assistant.speak("Sorry, I could not understand what you said.")
            except sr.RequestError:
                self.voice_assistant.speak("Could not reach the speech service.")
            except sr.WaitTimeoutError:
                self.voice_assistant.speak("Listening timed out. Please try again.")
