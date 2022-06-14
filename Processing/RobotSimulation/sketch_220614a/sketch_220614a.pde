

int x1 = 120;
int y1 = 20;
int x2 = 420;
int y2 = 20;

int finalY = 480;

Robot robot;

void setup() {
  size(500, 500);
  background(#818B95);
  frameRate(30);

}

void draw() {  
  //refresh background
  background(#818B95); 

  print("-");
  
  strokeWeight(10);
 
  robot = new Robot();
  

  line(120, 20, 120, 480); //left rail 
  line(420, 20, 420, 480); //raight rail 
  line(x1,y1,x2,y2); // rail across 
  line(120,480,420,480); // bottom rail across 
  delay(100);
}

void moveToVertical(){
    if(y1 < finalY){
   y1+=5; 
   y2+=5; 
  }
}
