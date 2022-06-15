import controlP5.*; //library
import processing.serial.*; //library

Serial port; //do not change
ControlP5 cp5; //create ControlP5 object
int motor = 0; // motor speed variable

boolean button = false;
boolean saved = true;

int x = 25;
int y = 100;
int w = 50;
int h = 50;

int time;
int wait = 1000;
int lastRecordingTime = 0;
int lastIdleTime = 0;
int totalRunningTime = 0;

boolean tick;


JSONArray json;
int jsonLen;

void setup() {
  size(480, 270); 
  time = millis();//store the current time
  smooth();
  strokeWeight(3);

  //save json array
  json = loadJSONArray("data.json");
  jsonLen = checkJsonLength();
  
//setting up port communication
port = new Serial(this, "COM3", 9600); //connected arduino port
cp5 = new ControlP5(this); //do not change

//setting up a slider 
Slider slider = cp5.addSlider("motor")
.setPosition(125, 20) //x and y upper left corner
.setSize(50, 250) //(width, height)
.setRange(0, 255) //slider range low,high
.setValue(125) //start val
.setColorBackground(color(0, 0, 255)) //top of slider color r,g,b
.setColorForeground(color(0, 255, 0)) //botom of slider color r,g,b
.setColorValue(color(255, 255, 255)) //vall color r,g,b
.setColorActive(color(255, 0, 0)) //mouse over color
;
}

void draw() {
  if (button) {
    saved = false;
    background(255);
    stroke(0);
  //check the difference between now and the previously stored time is greater than the wait interval
  if(millis() - time >= wait){
    tick = !tick;//if it is, do something
    time = millis();//also update the stored time
  }
  line(50,10,tick ? 10 : 90,90);
  lastRecordingTime = millis();
  totalRunningTime = MsConversion(lastRecordingTime - lastIdleTime);
  } else {
    
    background(0);
    stroke(255);
    if(totalRunningTime > 0 && saved == false){
      print("Need To save");
      saveJson(2,2,2);
      saved = true;

    }
    lastIdleTime = millis();
    
  }
  if(saved){
    textSize(30);
    text("saved", 200, 200); 
  
  }
  fill(175);
  rect(x,y,w,h);

}

int MsConversion(int MS)
{
int totalSec = (MS / 1000);
int seconds = (MS / 1000) % 60;
int minutes = (MS / (1000*60)) % 60;
int hours = ((MS/(1000*60*60)) % 24);                      

String HumanTime= (hours+": " +minutes+ ": "+ seconds);
println (HumanTime);
return seconds;
}


// When the mouse is pressed, the state of the button is toggled.   
// Try moving this code to draw() like in the rollover example.  What goes wrong?
void mousePressed() {
  if (mouseX > x && mouseX < x+w && mouseY > y && mouseY < y+h) {
    button = !button;
  }  
}


void saveJson(int pwm, int sec, int ml){
  JSONObject data = new JSONObject();
  data.setInt("pwm", pwm);
  data.setInt("sec", sec);
  data.setInt("ml", ml);
  json.setJSONObject(jsonLen, data);
  saveJSONArray(json, "data.json");
  jsonLen++;
}

int checkJsonLength(){
  int i = 0;
  while(true){
    try{
    json.getJSONObject(i); 
    }catch(Exception e){
      return i;
    }
    i++;
  }

}
