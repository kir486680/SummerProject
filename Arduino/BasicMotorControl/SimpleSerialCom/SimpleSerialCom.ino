#define enA 9
#define in1 8
#define in2 7
#define button 4

int rotDirection = 0;
int pressed = false;

void setup() {
  pinMode(enA, OUTPUT);
  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);
  pinMode(button, INPUT);
  // Set initial rotation direction
  digitalWrite(in1, HIGH);
  digitalWrite(in2, LOW);
  Serial.begin(9600);
}

void loop() {
  if(Serial.available()){
    int val = Serial.read();
    if(val !=0){
      analogWrite(enA, val); // Send PWM signal to L298N Enable pin
      digitalWrite(in1, HIGH);
      digitalWrite(in2, LOW);
    }else{
      digitalWrite(in1, LOW);
      digitalWrite(in2, LOW);
    }

  }
}

/*
255 - 21s - 30ml
200-26.48- 30ml
150 - 34 - 30ml
*/
