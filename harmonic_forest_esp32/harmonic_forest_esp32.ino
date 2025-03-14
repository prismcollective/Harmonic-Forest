#include <math.h>
const int num_motors = 8;  // Number of steppers
int dir_pins[num_motors] = {13,11,9,3,18,16,7,5};  //starts odd GPIO
int step_pins[num_motors] = {14,12,10,46,8,17,15,6}; //starts on even GPIO
float motor_step_angles[num_motors] = {1.8,1.8,1.8,1.8,1.8,1.8,1.8,1.8};//each step corresponds to this amount of rotation;
float prev_angles[num_motors] = {};
int STEP_DELAYS[num_motors] = {};
const int STEP_DELAY = 500;
 //some motors can go faster, make sure to change that 

void setup() {
  Serial.begin(115200);  // Start serial communication
  
  for(int i = 0; i < num_motors; i++){
    prev_angles[i] = 0;//all cams should be at 0 to begin
    STEP_DELAYS[i] = 500;//minumum for certain motors we have
    pinMode(dir_pins[i],OUTPUT);
    pinMode(step_pins[i], OUTPUT);
    digitalWrite(dir_pins[i], LOW);
  }
  
}

void loop() {
  if (Serial.available() > 0) {
    String data_str = Serial.readStringUntil('\n');
    float new_angles[num_motors];//array storing the new ABSOLUTE angles 
    parseData(data_str, new_angles);
    float angle_differences[num_motors];//array storing the RELATIVE angle movement 
     
    for (int i = 0; i < num_motors; i++) {
      angle_differences[i] = new_angles[i] - prev_angles[i];//Anti-clockwise rotations are positive, frame of reference is the motor shaft pointed towards you
    }
    stepMotors(angle_differences);
    memcpy(prev_angles, new_angles, sizeof(prev_angles));
  }
}
float findMax(float arr[], int size) {
    if (size <= 0) return NAN; 
    
    float maxVal = arr[0]; 
    for (int i = 1; i < size; i++) {
        if (arr[i] > maxVal) {
            maxVal = arr[i]; 
        }
    }
    return maxVal;
}

// parse data
void parseData(String data_str, float* degrees_rotation) {
  int index = 0;
  int start = 0;
  int end = data_str.indexOf(',');
  
  while (end != -1 && index < num_motors) {
    String value_str = data_str.substring(start, end);
    degrees_rotation[index] = constrain(value_str.toFloat(), 0.0, 1.0) * 180
    degrees_rotation[index] *= 180;//convert to degrees
    start = end + 1;
    end = data_str.indexOf(',', start);
    index++;
  }
  
  if (index < num_motors) {
    String value_str = data_str.substring(start);
    degrees_rotation[index] = value_str.toFloat();
  }
}

void stepMotor(int motor_number,int angle) {
  digitalWrite(dir_pins[motor_number], (int)fabs(angle)/angle);//negative direction would be cw, positive would be ccw
  
  for(int step = 0; step < (int)abs(angle)/motor_step_angles[motor_number]; step++){
    digitalWrite(step_pins[motor_number], HIGH);
    delayMicroseconds(STEP_DELAYS[num_motors]);
  }

}

void stepMotors(float *angle_differences)
{
  float steps_required[num_motors];
  for (int i = 0; i < num_motors; i++) {
    steps_required[i] = round(fabs(angle_differences[i]) / motor_step_angles[i]);
  }
  int max_steps = (int)findMax(steps_required,num_motors);
  for (int step = 0; step < max_steps; step++)
  {
    for (int j = 0; j < num_motors; j++)
    {
      
      int direction = (angle_differences[j] > 0) ? HIGH : LOW;
      if (angle_differences[j] == 0) continue;
      int steps_required = round(abs(angle_differences[j]) / motor_step_angles[j]);
      if (step < steps_required)
      {
        
        digitalWrite(dir_pins[j], direction);
        digitalWrite(step_pins[j], HIGH);
      }
    }
    delayMicroseconds(STEP_DELAY);
    for (int j = 0; j < num_motors; j++)
    { 
      if (angle_differences[j] == 0) continue;     
      int steps_required = round(abs(angle_differences[j]) / motor_step_angles[j]);

      if (step < steps_required)
      {
        digitalWrite(step_pins[j], LOW);
      }
    }
    delayMicroseconds(STEP_DELAY);
  }
}