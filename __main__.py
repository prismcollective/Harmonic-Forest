import audio_file
import audio_to_arduino
import numpy as np
import time
import os
import pygame
import threading
# Function to play audio and allow interruption
stop_audio_flag = False
def play_audio():
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() and not stop_audio_flag:
        time.sleep(0.1)  

minuet_bocc_path = "25481__freqman__violin-minuet_boccherini-edit.wav"
violin_c4_path = "violin-c4.wav"
major_scale_path = "just-major-sc.wav"
claire_path = "2009-03-30-clairdelune_64kb.wav"
fur_elise_path = "fur-elise-beethoven-216331.wav"
symphony_5_path = "Ludwig_van_Beethoven_-_symphony_no._5_in_c_minor_op._67_-_i._allegro_con_brio.wav"
campanella_path = "Liszt___Paganini_-_Etude_No.3__La_campanella__64kb.wav"
blue_danube_path = "iiif-service_mbrsrs_mbrsjukebox_dlc_victor_31450_02_c271_10_dlc_victor_31450_02_c271_10-full-full-0-full-default.wav"
nocturne_path = "Frederic Chopin - Nocturne No. 2 In E Flat Major Op.9 No.2 (From Blue Lagoon).wav"
BASE_DIR="/Users/samcy/OneDrive - University of Waterloo/Harmonic-Forest/Music-Assets"
violinC4 = audio_file.audio_file(violin_c4_path, BASE_DIR=BASE_DIR)
major_scale = audio_file.audio_file(major_scale_path, BASE_DIR=BASE_DIR)
minuet_bocc = audio_file.audio_file(minuet_bocc_path, BASE_DIR=BASE_DIR)
claire = audio_file.audio_file(claire_path, BASE_DIR=BASE_DIR)
fur_elise = audio_file.audio_file(fur_elise_path, BASE_DIR=BASE_DIR)
symphony_5 = audio_file.audio_file(symphony_5_path, BASE_DIR=BASE_DIR)
campanella = audio_file.audio_file(campanella_path, BASE_DIR=BASE_DIR)
blue_danube = audio_file.audio_file(blue_danube_path, BASE_DIR=BASE_DIR)
nocturne = audio_file.audio_file(nocturne_path, BASE_DIR=BASE_DIR)
target_audio = symphony_5
print(target_audio.bucket_edges.shape[0])
audio_path = target_audio.audio_path
#Uncomment below to visualize activations
target_audio.visualize_activations()
pygame.mixer.init()
pygame.mixer.music.load(audio_path)
audio_thread = threading.Thread(target=play_audio)
audio_thread.start()
try:
    timer = time.time()
    audio_to_arduino.send_to_arduino(major_scale.get_normalized_activations(), 
                                     major_scale.get_audio_duration(), 
                                     ARDUINO_PORT='COM5')
    
    print("Total delay time:", major_scale.get_audio_duration())
    print("Empirical Play Time:", time.time() - timer)
    print("Actual Audio Duration:", major_scale.get_audio_duration())

    while pygame.mixer.music.get_busy():
        time.sleep(0.5)  # Allow music to continue playing

except KeyboardInterrupt:
    print("\nKeyboardInterrupt detected - Stopping audio...")
    stop_audio_flag = True
    pygame.mixer.music.stop()
    audio_thread.join()  
    print("Audio stopped. Exiting program.")

#extract_frequencies.visualize_activations(normalized_activations,bucket_edges)
