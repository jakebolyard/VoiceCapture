import tkinter as tk
from threading import Thread
from queue import Queue
import pyaudio
import subprocess
import json
import torch
from vosk import Model, KaldiRecognizer
from unittest import result
import numpy as np

messages = Queue()
recordings = Queue()

CHANNELS = 1
FRAME_RATE = 16000
RECORD_SECONDS = 5
AUDIO_FORMAT = pyaudio.paInt16
SAMPLE_SIZE = 2
model = Model(model_name="vosk-model-en-us-0.22")
rec = KaldiRecognizer(model, FRAME_RATE)
rec.SetWords(True)

class VoiceCapture:
    def __init__(self, textField, canvas):
        #self.root = tk.Tk()
        #self.root.title("Voice Capture")
        self.textField = textField
        self.canvas = canvas
        self.isRunning = False
        #self.output_text = tk.Text(self.root, wrap="word", height=10, width=40)
        #self.output_text.pack(pady=10)

        #self.start_button = tk.Button(self.root, text="Start", command=self.start_action)
        #self.start_button.pack(pady=10)

        #self.stop_button = tk.Button(self.root, text="Stop", command=self.stop_action)
        #self.stop_button.pack(pady=10)

    def start_action(self):
        messages.put(True)
        self.isRunning = True
        #self.display_text("Start button clicked")
        #self.find_microphone()
                
        record = Thread(target=self.recordMicrophone)
        record.start()

        transcribe = Thread(target=self.speech_recognition)
        transcribe.start()      

    def stop_action(self):
        messages.get()
        self.isRunning = False
        self.display_text("Stop button clicked")

    def display_text(self, text):
        #current_pos = self.output_text.index(tk.INSERT)
        #self.output_text.insert(current_pos, text + "\n")
        current_pos = self.textField.index(tk.INSERT)
        self.textField.after(0, self.textField.insert, current_pos, text + "\n")

    def find_microphone(self):
        p = pyaudio.PyAudio()        
        for i in range(p.get_device_count()):
            name = p.get_device_info_by_index(i)['name']
            index = p.get_device_info_by_index(i)['index']
            self.display_text("Index: " + str(index) + " Name: " + name + "\n")
            #print(p.get_device_info_by_index(i))

    def recordMicrophone(self, chunk=1024):
        p = pyaudio.PyAudio()
        
        stream = p.open(format=AUDIO_FORMAT,
                        channels=CHANNELS,
                        rate=FRAME_RATE,
                        input=True,
                        input_device_index=1,
                        frames_per_buffer=chunk
                        )
        
        frames = []

        while not messages.empty():
            data = stream.read(chunk)
            self.update_amplitude(data)
            frames.append(data)
            #print(str(len(frames)))

            if len(frames) > (FRAME_RATE * RECORD_SECONDS) / chunk:
                recordings.put(frames.copy())
                frames = []      

        stream.stop_stream()
        stream.close()
        p.terminate()

    def speech_recognition(self):
        while not messages.empty():            
            frames = recordings.get()
            #print(str(frames))
            rec.AcceptWaveform(b''.join(frames))
            result = rec.Result()
            text = json.loads(result)["text"]           

            #cased = subprocess.check_output('python recasepunc/recasepunc.py predict recasepunc/checkpoint', shell=True, text=True, input=text)
            #output_text.append_stdout(cased)
            #print(text)
            self.display_text(text)
        
    def update_amplitude(self, in_data):
        audio_data = np.frombuffer(in_data, dtype=np.int16)
        amplitude = np.abs(audio_data).mean()
        self.draw_amplitude(amplitude)
        
        #return (in_data, pyaudio.paContinue)
    
    def draw_amplitude(self, amplitude):
        self.canvas.delete("amplitude_bar")
        width, height = 100, 100
        bar_height = amplitude * height / self.canvas.winfo_height()  # Normalize amplitude to fit canvas
        self.canvas.create_rectangle(0, height - bar_height, width, height, fill="blue", tags="amplitude_bar")
        #print(str(amplitude))

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    window = VoiceCapture()
    window.run()
