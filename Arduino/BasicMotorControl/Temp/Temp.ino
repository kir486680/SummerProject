int pinTemp = A1;   //This is where our Output data goes

void setup() {
  Serial.begin(9600);     
}
void loop() {
  int temp = analogRead(pinTemp);    //Read the analog pin
  temp = temp * 0.48828125;   // convert output (mv) to readable celcius
  Serial.print("Temperature: ");
  Serial.print(temp);
  Serial.println("C");  //print the temperature status
  delay(1000);  
}
