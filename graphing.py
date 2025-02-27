import matplotlib.pyplot as plt
import librosa
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
def show_spec(spectrogram, sr, title=None):
    """
    Display a Mel spectrogram using matplotlib.

    Parameters:
        spectrogram (np.ndarray): The Mel spectrogram to display.
        sr (int): Sample rate of the audio.
        title (str): Title of the plot.
    """
    plt.figure(figsize=(10, 4))
    librosa.display.specshow(spectrogram, sr=sr, x_axis='time', y_axis='mel', cmap='viridis')
    plt.colorbar(format='%+2.0f dB')
    plt.title(title if title else 'Mel Spectrogram')
    plt.tight_layout()
    plt.show()
