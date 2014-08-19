/* Simple Serial ECHO script : Written by ScottC 03/07/2012 */
#include<stdlib.h>
/* Use a variable called byteRead to temporarily store
   the data coming from the computer */
byte byteRead;
int analogPin = 0;
int readVal = 0;
int pumpPin = 2;
float avegValue = 0.0;
char holder[7];

void setup() {                
// Turn the Serial Protocol ON
  Serial.begin(9600);
  pinMode(pumpPin,OUTPUT);
}

void loop() {

  if (Serial.available()) {
    /* read the most recent byte */
    byteRead = Serial.read();
    /*ECHO the value that was read, back to the serial port. */
    processInput((char)byteRead);
  }
}

void processInput(char Input) {
  
  // do something different depending on the 
  switch (Input) {
  case 'p': 
    pump()  ;
    returnValue("\"Done\"",false);
    break;
  case 'r':   
    returnValue(getSensorReading(),false);
    break;
  default:    
    returnValue("\"unknownCommand\"",true);
    break;
  } 
}

String getSensorReading(){
     /*  check if data has been sent from the computer: */
     avegValue = 0;
     for (int i=0; i<10;i++) {
         avegValue += analogRead(analogPin);
     }
     avegValue = avegValue/10.0;
         // read the input pin
     String g= (String)dtostrf( avegValue, 7, 3,holder);
     return g;
}

void returnValue(String value, boolean error){
  String Error = "null";
  if (error) {
    Error = "1";
  };
  String g= "{\"value\" :"+value+",\"error\":"+Error+"}";  
  Serial.println(g);
}

void pump() {
  digitalWrite(pumpPin, HIGH);
  delay(2000);
  digitalWrite(pumpPin,LOW); 
}
