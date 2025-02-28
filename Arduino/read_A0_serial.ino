/*
  Analog Read Serial
  Reads an analog input on pin 0.
  prints  the result to the Serial Monitor.
  Attach the center pin of a potentiometer  to pin A0, and the outside pins to +5V and ground.
  from https://projecthub.arduino.cc/SBR/analog-read-serial-fff5fa
*/

const int NbMeasure = 100;

// the setup routine  runs once when you press reset:
void setup() {
  // initialize serial communication  at 9600 bits per second:
  Serial.begin(9600);
}

// the loop routine  runs over and over again forever:
void loop() {
  // read the input on analog  pin 0:
  int sensorValue = 0;
  for (int i=0; i < NbMeasure; i++) {
    sensorValue = sensorValue + analogRead(A0);
    delay(10);
    }
  sensorValue = sensorValue/NbMeasure;
  // print out the value you read:
  Serial.println(sensorValue);
}
