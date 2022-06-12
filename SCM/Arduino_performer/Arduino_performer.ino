//#include <SoftwareSerial.h>
#define PIN 2



void setup() {
  // put your setup code here, to run once:
  pinMode(PIN,OUTPUT);
  Serial.begin(9600);
  
}

// 传入角度，舵机转动指定角度
// 周期是20ms，控制范围0.5ms-2.5ms
void rotate_angle(float angle){
  long temp_time = millis();
  while(millis() - temp_time < 1000){
    int us = (int)(angle / 180. * 2000. + 500.);
    digitalWrite(PIN, HIGH);
    delayMicroseconds(us);
    digitalWrite(PIN, LOW);
    delayMicroseconds(20000 - us);
    }
  }

void loop() {
  while(Serial.available()){
    char c = Serial.read();
//    Serial.write(c);
    switch(c){
          case '1':
            rotate_angle(0);
            break;
          case '2':
            rotate_angle(45);
            break;
          case '3':
            rotate_angle(90);
            break;
          case '4':
            rotate_angle(135);
            break;
          case '5':
            rotate_angle(180);
            break;
      }
    }
}
