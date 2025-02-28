import librosa
import numpy as np
import matplotlib.pyplot as plt

def analyze_frequency_buckets(audio_path, num_buckets=10):
    # Load audio file
    y, sr = librosa.load(audio_path)
    
    # Compute Short-Time Fourier Transform (STFT)
    D = librosa.stft(y)
    magnitude = np.abs(D)
    
    # Get frequency bins corresponding to STFT
    frequencies = librosa.fft_frequencies(sr=sr, n_fft=D.shape[0] * 2 - 2)
    
    # Create logarithmically spaced frequency buckets
    min_freq = 20  # Minimum frequency to analyze (Hz)
    max_freq = sr / 2  # Nyquist frequency
    bucket_edges = np.logspace(np.log10(min_freq), np.log10(max_freq), num=num_buckets + 1)
    
    # Assign frequencies to buckets
    bucket_indices = np.digitize(frequencies, bucket_edges) - 1
    bucket_indices = np.clip(bucket_indices, 0, num_buckets - 1)
    
    # Sum magnitudes for each bucket
    bucket_activations = np.zeros((num_buckets, magnitude.shape[1]))
    for i in range(num_buckets):
        mask = (bucket_indices == i)
        bucket_activations[i, :] = np.sum(magnitude[mask, :], axis=0)
    
    # Normalize across time frames (0-1 per frame)
    max_vals = bucket_activations.max(axis=0, keepdims=True)
    max_vals[max_vals == 0] = 1  # Avoid division by zero
    normalized_activations = bucket_activations / max_vals
    
    return normalized_activations, bucket_edges

def visualize_activations(normalized_activations, bucket_edges):
    plt.figure(figsize=(12, 6))
    
    # Create time axis
    time = np.linspace(0, len(normalized_activations[0]) * 0.1, len(normalized_activations[0]))
    
    # Plot each bucket's activation
    for i in range(len(normalized_activations)):
        plt.plot(time, normalized_activations[i], label=f'{bucket_edges[i]:.1f}-{bucket_edges[i+1]:.1f} Hz')
    
    plt.title('Frequency Bucket Activations Over Time')
    plt.xlabel('Time (s)')
    plt.ylabel('Normalized Amplitude')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.show()

def process_audio(audio_path):
    activations, edges = analyze_frequency_buckets(audio_path)
    visualize_activations(activations, edges)


