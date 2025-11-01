
import os
import queue
import sounddevice as sd
import pyttsx3
from vosk import Model, KaldiRecognizer
import json

# Load VOSK model
model_path = "vosk-model-small-en-us-0.15"
if not os.path.exists(model_path):
    print("Please download the VOSK model and put it in this folder!")
    exit()

model = Model(model_path)
recognizer = KaldiRecognizer(model, 16000)

# Setup voice
engine = pyttsx3.init()

# Queue for audio
q = queue.Queue()

def callback(indata, frames, time, status):
    q.put(bytes(indata))

def listen():
    with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                           channels=1, callback=callback):
        print("🎙 Say something...")
        while True:
            data = q.get()
            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                text = result.get("text", "")
                if text:
                    return text

def speak(text):
    print("🧠 Assistant:", text)
    engine.say(text)
    engine.runAndWait()

# Simple brain
def answer(question):
    q = question.lower()
    if "hello" in q:
        return "Hello! How can I help you?"
    elif "your name" in q:
        return "I'm your offline assistant."
    elif "time" in q:
        import datetime
        return "The time is " + datetime.datetime.now().strftime("%I:%M %p")
    elif "bye" in q:
        return "Goodbye!"
    else:
        return "I heard you say " + question

# Main loop
while True:
    text = listen()
    print("🗣 You said:", text)
    if "bye" in text:
        speak("Goodbye!")
        break
    reply = answer(text)
    speak(reply)
