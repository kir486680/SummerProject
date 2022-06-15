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
float volume = 0;

float time;
int wait = 1000;
int lastRecordingTime = 0;
int firstRecordingTime = 0;
int lastIdleTime = 0;
int totalRunningTime = 0;

Timer startTimer;

boolean reset;

JSONArray json;
int jsonLen;

void setup() {
  size(480, 270); 
  startTimer = new Timer(0);
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
  textSize(10);
  if (button) {
    saved = false;
    background(255);
    stroke(0);
    
    volume = ((startTimer.getTime()) * 30)/20;
    startTimer.countUp();

    String myText = "Pumped volume: " + volume;
    text(myText, 200, 100);
    
  } else {
    background(0);
    stroke(255);
    if(startTimer.getTime() > 0 && saved == false){
      print("Need To save");
      saveJson(motor,startTimer.getTime(),30);
      saved = true;
      text("saved", 200, 200); 
    }
    startTimer.setTime(0);
  }
  fill(175);
  rect(x,y,w,h);

  //slider(motor);
}


void slider(int slider)
{
  port.write(slider);
}

// When the mouse is pressed, the state of the button is toggled.   
// Try moving this code to draw() like in the rollover example.  What goes wrong?
void mousePressed() {
  if (mouseX > x && mouseX < x+w && mouseY > y && mouseY < y+h) {
    button = !button;
  }  
}


void saveJson(int pwm, float sec, int ml){
  JSONObject data = new JSONObject();
  data.setInt("pwm", pwm);
  data.setFloat("sec", sec);
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
