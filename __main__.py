import audio_file
import audio_to_arduino
import numpy as np
import time

violin = audio_file.audio_file("violin-c4.wav")
major_scale = audio_file.audio_file("just-major-sc.wav")
minuet_bocc = audio_file.audio_file("25481__freqman__violin-minuet_boccherini-edit.wav")

timer = time.time()

audio_to_arduino.send_to_arduino(minuet_bocc.get_normalized_activations(), minuet_bocc.get_audio_duration())
print(minuet_bocc.get_audio_duration()/minuet_bocc.get_normalized_activations().shape[1] * minuet_bocc.get_normalized_activations().shape[1])
print("End Time:", time.time()-timer)
#extract_frequencies.visualize_activations(normalized_activations,bucket_edges)
