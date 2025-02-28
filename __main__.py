import extract_frequencies
import audio_to_arduino
import numpy as np
normalized_activations = np.load('normalized-activations.npy')
bucket_edges = np.load('bucket-edges.npy')

extract_frequencies.visualize_activations(normalized_activations,bucket_edges)
audio_to_arduino.send_to_arduino(normalized_activations)