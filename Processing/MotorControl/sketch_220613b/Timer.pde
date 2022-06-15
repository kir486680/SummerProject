class Timer{
 float Time;
 float prevTime;
 Timer(float set){
  Time = set; 
 }
 float getTime(){
  return(Time); 
 }
 float getPrevTime(){
   return(prevTime);
 }
 void setTime(float set){
  Time = set; 
 }
 void countUp(){
  float temp = Time;
  prevTime = temp;
  Time += 1/frameRate; 
 }
 void countDown(){
  Time -=1/frameRate; 
 }
}
