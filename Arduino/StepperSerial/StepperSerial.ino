/*
O. Devauchelle, P. Delorme, A. Abramian, E. Lajeunesse & F. Metivier
GNU General Public License v3.0, 2022
*/


const int dirA = 13;
const int dirB = 12;

const int motA = 11;
const int motB = 3;

const int brakeA = 8;
const int brakeB = 9;

float delayLength = -1; // negative value = stop
int nStep = -1; // negative = infinite number of steps
int RotDir = +1; // rotation direction 
String UserCommand = "?";
int CurrentStep = 0;

char* string2char(String command){
    if(command.length()!=0){
        char *p = const_cast<char*>(command.c_str());
        return p;
    }
}

void PrintParams(){    
      Serial.print("\"dt\":");
      Serial.print(delayLength);
      Serial.print(", \"N\":");
      Serial.print(nStep);
      Serial.print(", \"direction\":");
      Serial.print(RotDir);
      Serial.print(", \"currentN\":");
      Serial.println(CurrentStep);
}

void setup() {
  Serial.begin(9600);
  pinMode(dirA, OUTPUT);
  pinMode(dirB, OUTPUT);
  pinMode(brakeA, OUTPUT);
  pinMode(brakeB, OUTPUT);
  pinMode(motA, OUTPUT);
  pinMode(motB, OUTPUT);
}


void MotorStep(int iStep){
  
  if ( iStep == 0 ){
    digitalWrite(brakeA, HIGH);
    digitalWrite(brakeB, LOW);
    digitalWrite(dirB, LOW);
    digitalWrite(motB, HIGH);
  }
  
  else if ( iStep == 1 ){   
    digitalWrite(brakeA, LOW);
    digitalWrite(brakeB, HIGH);
    digitalWrite(dirA, LOW);
    digitalWrite(motA, HIGH);
  }
  
  else if ( iStep == 2 ){
    digitalWrite(brakeA, HIGH);
    digitalWrite(brakeB, LOW);
    digitalWrite(dirB, HIGH);
    digitalWrite(motB, HIGH);
  }
  
  else if ( iStep == 3 ){
    digitalWrite(brakeA, LOW);
    digitalWrite(brakeB, HIGH);
    digitalWrite(dirA, HIGH);
    digitalWrite(motA, HIGH);
  }
}


void loop() {

  if (Serial.available()> 0){
    
    UserCommand = Serial.readString();
    UserCommand.trim();

    if ( UserCommand == "s" ){
       Serial.println( "Stopping" );
       delayLength = -1;
    }

    else if ( UserCommand == "id" ){
       Serial.println( "Stepper" );
    }
    
    else if ( UserCommand == "?" ){
       PrintParams();
    }
    
    else {
      
      char * splitCommand = strtok ( string2char( UserCommand ), ">," );
      
      delayLength = atof( splitCommand );
    
      splitCommand = strtok ( NULL, "," );
      nStep = atoi( splitCommand );

      splitCommand = strtok ( NULL, "," );
      RotDir = atoi( splitCommand );
      
      CurrentStep = 0;
      
      PrintParams();
      
    }
    
  }

  if ( delayLength > 0 ){
    
    if ( CurrentStep < nStep ){
    
      if ( RotDir >= 0 ){
        for ( int iStep=0; iStep<=3; iStep++ ){
          MotorStep(iStep);
          delay(delayLength);
        }
      }
   
      else {
        for ( int iStep=3; iStep>=0; iStep-- ){
          MotorStep(iStep);
          delay(delayLength);
        }
      }
    }

    else {
      Serial.println( "Done" );
      delayLength = -1;
    }

    CurrentStep += 1;
  
  }

}
