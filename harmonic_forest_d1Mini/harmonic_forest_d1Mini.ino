const int num_rods = 6;  // Number of electromagnets
int em_pins[num_rods] = {D1, D2, D5, D6, D7, D8};  // PWM-capable GPIO pins

void setup() {
  Serial.begin(115200 );  // ESP8266 typically uses faster baud rate
  for (int i = 0; i < num_rods; i++) {
    pinMode(em_pins[i], OUTPUT);  // Initialize PWM pins
  }
}

void loop() {
  if (Serial.available() > 0) {
    String data_str = Serial.readStringUntil('\n');
    float amplitudes[num_rods];
    parseData(data_str, amplitudes);

    // Convert amplitudes to PWM values (0-1023 for ESP8266's 10-bit resolution)
    for (int i = 0; i < num_rods; i++) {
      int pwm = (int)(amplitudes[i] * 1023);  // Scale 0.0-1.0 to 0-1023
      analogWrite(em_pins[i], pwm);  // Set PWM output
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