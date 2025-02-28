const int num_rods = 2;  // Number of electromagnets
int em_pins[num_rods] = {11,12};  // Use PWM-capable GPIO pins on ESP32

void setup() {
  Serial.begin(115200);  // Start serial communication
  for (int i = 0; i < num_rods; i++) {
    pinMode(em_pins[i], OUTPUT);  // Initialize PWM pins
    ledcSetup(i, 5000, 8);      // Set up PWM channel (channel, frequency, resolution)
    ledcAttachPin(em_pins[i], i); // Attach PWM channel to GPIO pin
        Serial.printf("PWM channel %d attached to pin %d\n", i, em_pins[i]);

  }
  
}

void loop() {
 

  if (Serial.available() > 0) {
    String data_str = Serial.readStringUntil('\n');
    float amplitudes[num_rods];
    parseData(data_str, amplitudes);

    // Convert amplitudes to PWM values 
    for (int i = 0; i < num_rods; i++) {
      int pwm = (int)(amplitudes[i] * 255);  // Scale 0.0-1.0 to 0-255
      ledcWrite(i, pwm);  // Set PWM output using LEDC
    }
  }
}

// Existing parseData function remains unchanged
void parseData(String data_str, float* amplitudes) {
  int index = 0;
  int start = 0;
  int end = data_str.indexOf(',');

  while (end != -1 && index < num_rods) {
    String value_str = data_str.substring(start, end);
    amplitudes[index] = value_str.toFloat();
    start = end + 1;
    end = data_str.indexOf(',', start);
    index++;
  }
  
  if (index < num_rods) {
    String value_str = data_str.substring(start);
    amplitudes[index] = value_str.toFloat();
  }
}