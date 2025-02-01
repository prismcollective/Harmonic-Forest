import os
import numpy as np
import matplotlib.pyplot as plt
import librosa
# Magnitude vs. Frequency graph plot
def plot_magnitude_spectrum(signal : str, title : str, sr : int, f_ratio = 1):
    ft = np.fft.fft(signal)
    magnitude_spectrum = np.abs(ft)
    # plot magnitude spectrum
    plt.figure(figsize = (18,5))
    frequency = np.linspace(0,sr,len(magnitude_spectrum)) # create frequency divisions equal to the length of the magnitude spectrum
    num_frequency_bins = int(len(frequency) * f_ratio)
    plt.plot(frequency[:num_frequency_bins], magnitude_spectrum[:num_frequency_bins])
    plt.xlabel("Frequency (Hz)")
    plt.title(title)
    plt.show()

#https://www.youtube.com/watch?v=R-5uxKTRjzM&t=336s&ab_channel=ValerioVelardo-TheSoundofAI
BASE_DIR = "/Users/samcy/OneDrive - University of Waterloo/Harmonic-Forest/Music Assets"
violin_file = "violin-c4.wav"
piano_file = "piano-c_C_major.wav"
fur_elise_file = "fur-elise-beethoven-216331.wav"
violin_c4, sr = librosa.load(os.path.join(BASE_DIR,violin_file))
piano_c5, sr = librosa.load(os.path.join(BASE_DIR,piano_file))

fur_elise, sr = librosa.load(os.path.join(BASE_DIR,fur_elise_file))
violin_FT = np.fft.fft(violin_c4) # move to frequency domain


plot_magnitude_spectrum(piano_c5, "Piano C5", sr, 0.1)

plot_magnitude_spectrum(violin_c4, "Violin C4", sr, 0.1)

#next steps do short time fourier transform