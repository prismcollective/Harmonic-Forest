import os
import time
import numpy as np
import matplotlib.pyplot as plt
import librosa
import serial

def show_mel_bands(filter_banks, source):
    plt.figure(figsize = (25, 10))
    librosa.display.specshow(filter_banks, sr = source, x_axis = "linear")
    plt.colorbar(format="%+2.f")
    plt.show()

def show_mel_spectrogram(logarithmic_spectrogram, sr):
    plt.figure(figsize = (25, 10))
    librosa.display.specshow(logarithmic_spectrogram, x_axis = "time", y_axis = "mel", sr = sr)
    plt.colorbar(format = "%+2.f")
    plt.show()

# Load audio file
BASE_DIR = "/Users/samcy/OneDrive - University of Waterloo/Harmonic-Forest/Music-Assets"
file_name = "25481__freqman__violin-minuet_boccherini-edit.wav"
file_path = os.path.join(BASE_DIR, file_name)
y, sr = librosa.load(file_path)

# Generate mel spectrogram
N_MELS = 6  # Number of frequency bands, should match with # of rods...
mel_spectrogram = librosa.feature.melspectrogram(y=y, sr=sr, n_fft=2048, hop_length=512, n_mels=N_MELS)
log_mel_spectrogram = librosa.power_to_db(mel_spectrogram)

