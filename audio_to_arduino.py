import numpy as np
import serial
import time


def send_to_arduino(normalized_activations, audio_length, ARDUINO_PORT = "COM5", BAUD_RATE = 115200):

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
            data_str += '\n' # delimiter
            ser.write(data_str.encode())  # Send data to Arduino
            #print(f"Sent: {data_str}")
            time.sleep(audio_length/normalized_activations.shape[1])  # Adjust delay to match Arduino's processing speed
    except KeyboardInterrupt:
        print("Interrupted by user")
    finally:
        ser.write("RESET\n".encode())
        ser.close()  # Close serial connection
        print("Serial connection closed")
