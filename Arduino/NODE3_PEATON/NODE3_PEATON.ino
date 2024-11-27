#include <ESP8266WiFi.h>
#include <PubSubClient.h>

#include "config.h"  // Sustituir con datos de vuestra red
#include "MQTT.hpp"
#include "ESP8266_Utils.hpp"
#include "ESP8266_Utils_MQTT.hpp"

#define LEDV D7
#define LEDY D6
#define LEDR D5
#define pirPin D0


void setup(void){
	Serial.begin(9600);
  pinMode(LEDV, OUTPUT);
  pinMode(LEDY, OUTPUT);
  pinMode(LEDR, OUTPUT);
  pinMode(pirPin, INPUT);
	SPIFFS.begin();
	ConnectWiFi_STA(false);
	InitMqtt();
}


unsigned long lastMotionTime = 0;
bool motionDetected = false;

void loop(){
  HandleMqtt();
  
  int motion = digitalRead(pirPin);
  
  if (motion == HIGH && !motionDetected) {
    Serial.println("Peaton detectado!!!");
    digitalWrite(LEDV, LOW);
    digitalWrite(LEDY, HIGH);
    lastMotionTime = millis();  // Store the time motion was detected
    motionDetected = true;  // Prevent repeat detection until reset
  }
  
  if (motionDetected) {
    if (millis() - lastMotionTime > 3000 && millis() - lastMotionTime <= 8000) {
      digitalWrite(LEDY, LOW);
      digitalWrite(LEDR, HIGH);
    }
    if (millis() - lastMotionTime > 8000) {
      digitalWrite(LEDR, LOW);
      motionDetected = false;  // Reset motion state after the cycle
    }
  } else {
    Serial.println("No se detecta movimiento");
    digitalWrite(LEDV, HIGH);
  }
  
  //if (motion == HIGH) { 
  //  PublisMqtt(motion); 
  //}
  PublisMqtt(motion);
  
  delay(1000);  // Brief delay to allow for stable sensor reading
}