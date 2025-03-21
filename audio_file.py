import os
import librosa
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter1d
class audio_file:  
    def __init__(self, audio_path, 
                 BASE_DIR="/Users/samcy/OneDrive - University of Waterloo/Harmonic-Forest/Music-Assets", 
                 num_buckets=8, 
                 normalized_activations_filename=None, 
                 bucket_edges_filename=None):
        
        self.audio_path = os.path.join(BASE_DIR, audio_path)
        self.BASE_DIR = BASE_DIR
        self.num_buckets = num_buckets  # Should match the number of rods
        self.audio_length = 0

        # Generate filenames if not provided
        self.normalized_activations_filename = (
            normalized_activations_filename if normalized_activations_filename 
            else f"{audio_path}-na.npy"
        )
        self.bucket_edges_filename = (
            bucket_edges_filename if bucket_edges_filename 
            else f"{audio_path}-be.npy"
        )

        # Analyze frequency buckets
        #if the file exists and its number of buckets is equal to the number requested
        if(os.path.exists(self.normalized_activations_filename) and np.load(self.bucket_edges_filename).shape[0] == self.num_buckets+1):
            self.normalized_activations = np.load(self.normalized_activations_filename)
            self.bucket_edges = np.load(self.bucket_edges_filename)
            self.audio_length = librosa.get_duration(path = self.audio_path)
        else:
            self.normalized_activations, self.bucket_edges = self.analyze_frequency_buckets(self.audio_path, self.num_buckets)
            self.generate_arrays()
        
        self.apply_gaussian_filter()
            
    def apply_gaussian_filter(self, sigma = 1):
        for i in range(self.num_buckets):
            self.normalized_activations[i] = gaussian_filter1d(self.normalized_activations[i], sigma=sigma)
    def analyze_frequency_buckets(self, audio_path, num_buckets=8, frame_duration_ms=100):
    # Load audio file
        y, sr = librosa.load(audio_path)
        self.audio_length = librosa.get_duration(y = y, sr = sr)
        # Calculate hop length in samples based on frame duration
        hop_length = int(frame_duration_ms * sr / 1000)
        
        # Compute Short-Time Fourier Transform (STFT) with fixed hop length
        D = librosa.stft(y, hop_length=hop_length)
        magnitude = np.abs(D)
        
        # Get frequency bins corresponding to STFT
        frequencies = librosa.fft_frequencies(sr=sr, n_fft=D.shape[0] * 2 - 2)
        
        # Create logarithmically spaced frequency buckets
        min_freq = 50  # Minimum frequency to analyze (Hz)
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
    
    def generate_arrays(self):
        np.save(self.normalized_activations_filename, self.normalized_activations)
        np.save(self.bucket_edges_filename, self.bucket_edges)

    def visualize_activations(self):
        plt.figure(figsize=(12, 6))
        
        # Create time axis
        time = np.linspace(0, len(self.normalized_activations[0]) * 0.1, len(self.normalized_activations[0]))
        
        # Plot each bucket's activation
        for i in range(len(self.normalized_activations)):
            plt.plot(time, self.normalized_activations[i], label=f'{self.bucket_edges[i]:.1f}-{self.bucket_edges[i+1]:.1f} Hz')
        
        plt.title('Frequency Bucket Activations Over Time')
        plt.xlabel('Time (s)')
        plt.ylabel('Normalized Amplitude')
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.tight_layout()
        plt.show()
    
    def visualize_single_bucket(self, bucket_num):
        plt.figure(figsize=(12, 6))
        
        # Create time axis
        time = np.linspace(0, len(self.normalized_activations[0]) * 0.1, len(self.normalized_activations[0]))
        
        # Plot each bucket's activation
        
        plt.plot(time, self.normalized_activations[bucket_num], label=f'{self.bucket_edges[bucket_num]:.1f}-{self.bucket_edges[bucket_num+1]:.1f} Hz')
        
        plt.title('Frequency Bucket Activations Over Time')
        plt.xlabel('Time (s)')
        plt.ylabel('Normalized Amplitude')
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.tight_layout()
        plt.show()

    def get_audio_duration(self):
        return self.audio_length
    
    def get_normalized_activations(self):
        return self.normalized_activations
    
    def get_bucket_edges(self):
        return self.bucket_edges
   