import numpy as np
import extract_frequencies
import os

BASE_DIR = "/Users/samcy/OneDrive - University of Waterloo/Harmonic-Forest/Music-Assets"
file_name = "just-major-sc.wav"
file_path = os.path.join(BASE_DIR, file_name)

normalized_activations, bucket_edges = extract_frequencies.analyze_frequency_buckets(file_path, num_buckets = 8)


np.save('major-scale.npy', normalized_activations)
np.save('major-scale-buckets.npy', bucket_edges)
