#include <ESP8266WiFi.h>
#include <PubSubClient.h>

#include "config.h"  // Sustituir con datos de vuestra red
#include "MQTT.hpp"
#include "ESP8266_Utils.hpp"
#include "ESP8266_Utils_MQTT.hpp"

#define LEDV D3
#define LEDY D2
#define pirPin D0


void setup(void){
	Serial.begin(9600);
  pinMode(LEDV, OUTPUT);
  pinMode(LEDY, OUTPUT);
  pinMode(pirPin, INPUT);
	SPIFFS.begin();
	ConnectWiFi_STA(false);
	InitMqtt();
}


unsigned long lastMotionTime = 0;

void loop(){
  HandleMqtt();
  
  int motion = digitalRead(pirPin);
  
  if (motion == HIGH) {
    Serial.println("Peaton detectado!!!");
    digitalWrite(LEDV, LOW);
    digitalWrite(LEDY, HIGH);
    lastMotionTime = millis();  // Store the time motion was detected
  }
  else {
    Serial.println("No se detecta movimiento");
    digitalWrite(LEDV, HIGH);
    digitalWrite(LEDY, LOW);
  }
  
  //if (motion == HIGH) { 
  //  PublisMqtt(motion); 
  //}
  PublisMqtt(motion);
  
  delay(1000);  // Brief delay to allow for stable sensor reading
}