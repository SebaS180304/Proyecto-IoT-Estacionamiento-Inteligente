#include <ESP8266WiFi.h>
#include <PubSubClient.h>

#include "config.h"  // Sustituir con datos de vuestra red
#include "MQTT.hpp"
#include "ESP8266_Utils.hpp"
#include "ESP8266_Utils_MQTT.hpp"

#define LED D7
#define pirPin D0


void setup(void){
	Serial.begin(9600);
  pinMode(LED, OUTPUT);
  pinMode(pirPin, INPUT);
	SPIFFS.begin();
	ConnectWiFi_STA(false);
	InitMqtt();
}


void loop(){
	HandleMqtt();
  //--------------------------------------------------------------------------------------
  int motion = digitalRead(pirPin);
  if (motion == HIGH){
    Serial.println("Peaton detectado!!!");
  } else {
    Serial.println("No se detecta movimiento");
  }
  digitalWrite(LED, motion);
  //--------------------------------------------------------------------------------------
	if (motion == HIGH){ PublisMqtt(motion); }
	delay(1000);
}


