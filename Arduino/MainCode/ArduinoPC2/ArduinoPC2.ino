//define motors
int motor1pin1 = 8;
int motor1pin2 = 7;
int motor2pin1 = 5;
int motor2pin2 = 4;

int enA = 9;
int enB = 3;

int motorNum;
float amountPump;
int motorSpeed;
boolean done = false;

const byte numLEDs = 2;
byte ledPin[numLEDs] = {12, 13};
unsigned long LEDinterval[numLEDs] = {200, 400};
unsigned long prevLEDmillis[numLEDs] = {0, 0};

const byte buffSize = 40;
char inputBuffer[buffSize];
const char startMarker = '<';
const char endMarker = '>';
byte bytesRecvd = 0;
boolean readInProgress = false;
boolean newDataFromPC = false;



char messageFromPC[buffSize] = {0};
int newFlashInterval = 0;
float servoFraction = 0.0; // fraction of servo range to move


unsigned long curMillis;

unsigned long prevReplyToPCmillis = 0;
unsigned long replyToPCinterval = 1000;

//=============

void setup() {
  Serial.begin(9600);
  
    // flash LEDs so we know we are alive
  for (byte n = 0; n < numLEDs; n++) {
     pinMode(ledPin[n], OUTPUT);
     digitalWrite(ledPin[n], HIGH);
  }
  delay(500); // delay() is OK in setup as it only happens once
  
  for (byte n = 0; n < numLEDs; n++) {
     digitalWrite(ledPin[n], LOW);
  }
  

  
    // tell the PC we are ready
  Serial.println("<Arduino is ready>");
}

//=============

void loop() {
  curMillis = millis();
  getDataFromPC();
  //updateFlashInterval();
  replyToPC();
  //
  flashLEDs();

  if(done == false && motorNum != NULL ){
    motorNum = 2;
    amountPump = 30;
    pumpMotor();
    Serial.println("First Motor Done");
    //amountPump = 0;
    motorNum = 1;
    pumpMotor();
    done = true;
  }

  Serial.println("ENd of the loop ");
}

//=============

void getDataFromPC() {

    // receive data from PC and save it into inputBuffer
    
  if(Serial.available() > 0) {

    char x = Serial.read();

      // the order of these IF clauses is significant
      
    if (x == endMarker) {
      readInProgress = false;
      newDataFromPC = true;
      inputBuffer[bytesRecvd] = 0;
      parseData();
    }
    
    if(readInProgress) {
      inputBuffer[bytesRecvd] = x;
      bytesRecvd ++;
      if (bytesRecvd == buffSize) {
        bytesRecvd = buffSize - 1;
      }
    }

    if (x == startMarker) { 
      bytesRecvd = 0; 
      readInProgress = true;
    }
  }
}

//=============
 
void parseData() {

    // split the data into its parts
    
  char * strtokIndx; // this is used by strtok() as an index
  
  strtokIndx = strtok(inputBuffer,",");      // get the first part - the string
  motorNum = atoi(strtokIndx); // copy it to messageFromPC
  
  strtokIndx = strtok(NULL, ","); // this continues where the previous call left off
  amountPump = atoi(strtokIndx);     // convert this part to an integer
  
  strtokIndx = strtok(NULL, ","); 
  motorSpeed = atoi(strtokIndx);     // convert this part to a float

}

//=============

void replyToPC() {

  if (newDataFromPC) {
    newDataFromPC = false;
    Serial.print("<Msg ");
    Serial.print(messageFromPC);
    Serial.print(" MotrorNum ");
    Serial.print(motorNum);
    Serial.print(" Amount Pump ");
    Serial.print(amountPump);
    Serial.print(" Motor Speed  ");
    Serial.print(motorSpeed);
    Serial.print(" Time ");
    Serial.print(curMillis >> 9); // divide by 512 is approx = half-seconds
    Serial.println(">");
  }
}

//============

void updateFlashInterval() {

   // this illustrates using different inputs to call different functions
  if (strcmp(messageFromPC, "LED1") == 0) {
     updateLED1();
  }
  
  if (strcmp(messageFromPC, "LED2") == 0) {
     updateLED2();
  }
}

//=============

void updateLED1() {

  if (newFlashInterval > 100) {
    LEDinterval[0] = newFlashInterval;
  }
}

//=============

void updateLED2() {

  if (newFlashInterval > 100) {
    LEDinterval[1] = newFlashInterval;
  }
}

//=============

void flashLEDs() {

  for (byte n = 0; n < numLEDs; n++) {
    if (curMillis - prevLEDmillis[n] >= LEDinterval[n]) {
       prevLEDmillis[n] += LEDinterval[n];
       digitalWrite( ledPin[n], ! digitalRead( ledPin[n]) );
    }
  }
}



//=============

void pumpMotor(){

  if(motorNum == 1){
    analogWrite(enA, 255);
    digitalWrite(motor1pin1, HIGH);
    digitalWrite(motor1pin2, LOW);

    delay((amountPump*0.8-8)*1000);
    digitalWrite(motor1pin1, LOW);
    digitalWrite(motor1pin2, LOW);
  }
  else if(motorNum == 2){
    analogWrite(enB, 255);
    digitalWrite(motor2pin1, HIGH);
    digitalWrite(motor2pin2, LOW);
    delay((amountPump*0.8-8)*1000);
    digitalWrite(motor2pin1, LOW);
    digitalWrite(motor2pin2, LOW);
  }
}
