#include <stdio.h>
#include <limits.h>
#include <math.h>

int motor1pin1 = 2;
int motor1pin2 = 3;
int motor2pin1 = 4;
int motor2pin2 = 5;

int x;
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
 Serial.begin(115200);
 Serial.setTimeout(1);
}
void loop() {
 while (!Serial.available());
 x = Serial.readString().toInt();

 int digit = numPlaces(x);
 float power = pow(10,digit-1);
 
 int pumpAmount = x % (int)power;
 int motorNum = (x / (int)power); 
 Serial.print(motorNum);
 
 
}

void pumpMotor(int motorNum, int pumpAmount){
  if(motorNum == 1){
    digitalWrite(motor1pin1, HIGH);
    digitalWrite(motor1pin2, LOW);
    delay(1000);
    digitalWrite(motor1pin1, LOW);
    digitalWrite(motor1pin2, LOW);
  }
  else if(motorNum == 2){
    digitalWrite(motor2pin1, HIGH);
    digitalWrite(motor2pin2, LOW);
    delay(1000);
    digitalWrite(motor2pin1, LOW);
    digitalWrite(motor2pin2, LOW);
  }
}
