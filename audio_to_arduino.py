import os
import time
import numpy as np
import matplotlib.pyplot as plt
import librosa
import serial
BASE_DIR = "/Users/samcy/OneDrive - University of Waterloo/Harmonic-Forest/Music-Assets"
file_name = "25481__freqman__violin-minuet_boccherini-edit.wav"
file_path = os.path.join(BASE_DIR, file_name)
y, sr = librosa.load(file_path)
N_MELS = 6  # Number of frequency bands, should match with # of rods...
mel_spectrogram = librosa.feature.melspectrogram(y=y, sr=sr, n_fft=2048, hop_length=512, n_mels=N_MELS)
log_mel_spectrogram = librosa.power_to_db(mel_spectrogram)
normalized = (log_mel_spectrogram - log_mel_spectrogram.min()) / (log_mel_spectrogram.max() - log_mel_spectrogram.min())

# Set up serial connection
ARDUINO_PORT = 'COM3'  # Replace with your Arduino's port
BAUD_RATE = 9600

try:
    ser = serial.Serial(port=ARDUINO_PORT, baudrate=BAUD_RATE, timeout=1)
    print(f"Connected to Arduino on {ARDUINO_PORT}")
except serial.SerialException as e:
    print(f"Failed to connect to Arduino: {e}")
    exit()

# Send normalized amplitudes to Arduino
try:
    for frame in range(normalized.shape[1]):
        current_amplitudes = normalized[:, frame]
        # Convert amplitudes to a string (e.g., "0.5,0.7,0.3,...")
        data_str = ','.join(f"{amp:.2f}" for amp in current_amplitudes)
        ser.write(data_str.encode())  # Send data to Arduino
        print(f"Sent: {data_str}")
        time.sleep(0.1)  # Adjust delay to match Arduino's processing speed
except KeyboardInterrupt:
    print("Interrupted by user")
finally:
    ser.close()  # Close serial connection
    print("Serial connection closed")