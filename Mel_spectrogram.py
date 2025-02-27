import os
import time
import librosa
import serial
import graphing

# Load audio file
BASE_DIR = "/Users/samcy/OneDrive - University of Waterloo/Harmonic-Forest/Music-Assets"
file_name = "25481__freqman__violin-minuet_boccherini-edit.wav"
file_path = os.path.join(BASE_DIR, file_name)
y, sr = librosa.load(file_path)

# Generate mel spectrogram
N_MELS = 300  # Number of frequency bands, should match with # of rods...
mel_spectrogram = librosa.feature.melspectrogram(y=y, sr=sr, n_fft=2048, hop_length=512, n_mels=N_MELS)
log_mel_spectrogram = librosa.power_to_db(mel_spectrogram)
graphing.show_mel_spectrogram(log_mel_spectrogram, sr)