#import os
import numpy as np
#import librosa
#import librosa.display
#import matplotlib.pyplot as plt
import serial
import time
#import graphing

"""
BASE_DIR = "/Users/samcy/OneDrive - University of Waterloo/Harmonic-Forest/Music-Assets"
file_name = "just-major-sc.wav"
file_path = os.path.join(BASE_DIR, file_name)
N_MELS = 200  # Number of Mel bands
N_RODS = 10   # Number of physical rods (adjust based on hardware)

# Load audio
y, sr = librosa.load(file_path)
y_harmonic, y_percussive = librosa.effects.hpss(y)# possibly unecessary

# 1. Compute Mel spectrogram
mel_spectrogram = librosa.feature.melspectrogram(
    y=y_harmonic, sr=sr, n_fft=2048, hop_length=512, n_mels=N_MELS
)
log_mel = librosa.power_to_db(mel_spectrogram)
graphing.show_mel_spectrogram(log_mel, sr)

# 2. Extract fundamental frequencies and remove overtones
pitches, magnitudes = librosa.piptrack(y=y_harmonic, sr=sr, n_fft=2048, hop_length=512)
fundamental_mask = np.zeros_like(log_mel)

for t in range(pitches.shape[1]):
    # Find dominant pitch (fundamental frequency) in the current frame
    idx = magnitudes[:, t].argmax()
    pitch = pitches[idx, t]
    if pitch > 0:
        # Convert pitch to Mel band index
        mel_band = librosa.hz_to_mel(pitch)
        mel_bands = librosa.mel_frequencies(n_mels=N_MELS, fmin=0, fmax=sr/2)
        closest_band = np.abs(mel_bands - mel_band).argmin()
        fundamental_mask[closest_band, t] = 1  # Keep only the fundamental

# Apply the mask to isolate fundamentals (remove overtones)
fundamental_mel = log_mel * fundamental_mask
graphing.show_mel_spectrogram(fundamental_mel, sr)

# 3. Normalize amplitudes to [0, 1]
normalized = (fundamental_mel - fundamental_mel.min()) / (fundamental_mel.max() - fundamental_mel.min())

# 4. Split into N_RODS buckets (group Mel bands)
bands_per_rod = N_MELS // N_RODS
buckets = np.zeros((N_RODS, normalized.shape[1]))

for rod in range(N_RODS):
    start = rod * bands_per_rod
    end = (rod + 1) * bands_per_rod
    buckets[rod, :] = normalized[start:end, :].max(axis=0)  # Use max amplitude in the bucket

# 5. Visualize the bucketed data
plt.figure(figsize=(12, 6))
librosa.display.specshow(buckets, sr=sr, x_axis='time', y_axis='mel', cmap='viridis')
plt.colorbar(label='Normalized Amplitude')
plt.title(f'Normalized Fundamental Frequencies Split into {N_RODS} Rod Buckets')
plt.show()
"""
def send_to_arduino(normalized_activations, ARDUINO_PORT = 'COM4', BAUD_RATE = 115200):

    try:
        ser = serial.Serial(port=ARDUINO_PORT, baudrate=BAUD_RATE, timeout=1)
        print(f"Connected to Arduino on {ARDUINO_PORT}")
    except serial.SerialException as e:
        print(f"Failed to connect to Arduino: {e}")
        exit()

    # Send normalized amplitudes to Arduino
    try:
        for frame in range(normalized_activations.shape[1]):
            current_amplitudes = normalized_activations[:, frame]
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
