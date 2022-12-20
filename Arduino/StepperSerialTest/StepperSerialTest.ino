/*
O. Devauchelle, P. Delorme, A. Abramian, E. Lajeunesse & F. Metivier
GNU General Public License v3.0, 2022
*/

void setup() {

  Serial.begin(9600);
  
  while (Serial.available() > 0) { // empty the input buffer
    Serial.read();
  }

}

void serialEvent() {
  
  String UserCommand = Serial.readStringUntil('\n');
  
  if ( UserCommand == "id" ){
    Serial.println( "Stepper" );
  }
  
  else{
    Serial.println("???");
  }
}


void loop() {
  delay(10);

}
