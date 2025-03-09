import audio_file
import audio_to_arduino
import numpy as np
import time
import os
from pydub import AudioSegment
from pydub.playback import play
import threading

def play_audio():
    play(audio)



minuet_bocc_path = "25481__freqman__violin-minuet_boccherini-edit.wav"
violin_c4_path = "violin-c4.wav"
major_scale_path = "just-major-sc.wav"

BASE_DIR="/Users/samcy/OneDrive - University of Waterloo/Harmonic-Forest/Music-Assets"
violinC4 = audio_file.audio_file(violin_c4_path, BASE_DIR=BASE_DIR)
major_scale = audio_file.audio_file(major_scale_path, BASE_DIR=BASE_DIR)
minuet_bocc = audio_file.audio_file(minuet_bocc_path, BASE_DIR=BASE_DIR)
target_audio = violinC4
audio_path = os.path.join(target_audio.audio_path)
audio = AudioSegment.from_file(audio_path, format="wav")
audio_thread = threading.Thread(target=play_audio)
audio_thread.start()

timer = time.time()
audio_to_arduino.send_to_arduino(target_audio.get_normalized_activations(), target_audio.get_audio_duration(), ARDUINO_PORT='COM5')
print("Total delay time",target_audio.get_audio_duration()/target_audio.get_normalized_activations().shape[1] * target_audio.get_normalized_activations().shape[1])
print("Empirical End Time:", time.time()-timer)
#extract_frequencies.visualize_activations(normalized_activations,bucket_edges)
