class Robot{
  float horizontalX;
  float horizontalY;
  float verticalX;
  float verticalY;
  float horizontalLen;
  float verticalLen;
  float verticalGearD;
  float horizontalGearD;
  float gearSpeed;
  
  
  Robot(float x1, float y1, float x2, float y2,float verticalGearD, float horizontalGearD, float gearSpeed){
   this.horizontalX = x1;
   this.horizontalY = y1;
   this.verticalX = x2;
   this.verticalY = y2;
   this.verticalGearD = verticalGearD;
   this.verticalGearD = horizontalGearD;
   this.gearSpeed = gearSpeed;
  }
  
  void moveVerticalRot(int rotations){
    float distance = 2 * PI * (this.verticalGearD/2); 

    for(int i =0;i<abs(rotations);i++){
      if(rotations > 0){
        this.verticalY += distance;
      }else{
        this.verticalY -= distance;
      }
    }

  }
  void moveHorizontalRot(int rotations){
    float distance = 2 * PI * (this.horizontalGearD/2); 

    for(int i =0;i<abs(rotations);i++){
      if(rotations > 0){
        this.horizontalX += distance;
      }else{
        this.horizontalY -= distance;
      }
    }

  }
  void moveTo(float x, float y){
    float dx = x - this.x;
    float dy = y - this.y;
    
    int horizontalRot = int(dx/ 2 * PI * (this.horizontalGearD/2));
    int verticalRot = int(dy/ 2 * PI * (this.verticalGearD/2));
    
    moveHorizontalRot(horizontalRot);
    moveVerticalRot(verticalRot);
    
    
  }
  
}
