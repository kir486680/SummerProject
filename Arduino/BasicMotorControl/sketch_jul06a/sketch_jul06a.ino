#include <stdio.h>
#include <limits.h>
#include <math.h>

int motor1pin1 = 8;
int motor1pin2 = 7;
int motor2pin1 = 5;
int motor2pin2 = 4;

int enA = 9;
int enB = 3;

int x;
int x1;
int x2;
int *motorNum;
int *amountPump;
int *motorSpeed;

int numPlaces (int n) {
    if (n < 0) return numPlaces ((n == INT_MIN) ? INT_MAX: -n);
    if (n < 10) return 1;
    return 1 + numPlaces (n / 10);
}
void setup() {
 pinMode(motor1pin1, OUTPUT);
 pinMode(motor1pin2, OUTPUT);
 pinMode(motor2pin1, OUTPUT);
  pinMode(motor2pin2, OUTPUT);
  digitalWrite(motor1pin1, LOW);
  digitalWrite(motor1pin2, LOW);
  digitalWrite(motor2pin1, LOW);
  digitalWrite(motor2pin2, LOW);
 Serial.begin(115200);
 Serial.setTimeout(1);
}
void loop() {
  
 while (!Serial.available());
 x = Serial.readString().toInt();
 x1 = Serial.readString().toInt();
 x2 = Serial.readString().toInt();
 //parseSerial(x); 
 
 Serial.print(x);
 Serial.print(x1);
 Serial.print(x2);
 //pumpMotor(*motorNum, *amountPump);
 
}

void parseSerial(String str){
    int n = str.length();
 
    // declaring character array
    char char_array[n + 1];
    strcpy(char_array, str.c_str());
 
    char *token = strtok(char_array, "-");
   
    int cnt = 1;
    while (token != NULL)
    {
       Serial.print(*motorNum);
       Serial.print(*amountPump);
       Serial.print(*motorSpeed);
       Serial.print("----");
        printf("%s\n", token);
        int tokens = atoi(token);
        //(true) ? (/*run if true*/) : (/*run if false*/);
        if(cnt == 1)
            motorNum = &tokens;
        if(cnt == 2)
            amountPump = &tokens;
        if(cnt == 3)
            motorSpeed = &tokens;
        cnt++;
        token = strtok(NULL, "-");
    }
}

void pumpMotor(int motorNum, int pumpAmount){
  
  if(motorNum == 1){
    analogWrite(enA, 255);
    digitalWrite(motor1pin1, HIGH);
    digitalWrite(motor1pin2, LOW);
    delay(2000);
    digitalWrite(motor1pin1, LOW);
    digitalWrite(motor1pin2, LOW);
  }
  else if(motorNum == 2){
    analogWrite(enB, 255);
    digitalWrite(motor2pin1, HIGH);
    digitalWrite(motor2pin2, LOW);
    delay(2000);
    digitalWrite(motor2pin1, LOW);
    digitalWrite(motor2pin2, LOW);
  }
}
