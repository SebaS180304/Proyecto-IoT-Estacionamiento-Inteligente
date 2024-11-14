#include <ESP8266WiFi.h>
#include <PubSubClient.h>

#include "config.h"  
#include "MQTT.hpp"
#include "ESP8266_Utils.hpp"
#include "ESP8266_Utils_MQTT.hpp"

#define PhotoR A0
#define RLED D0
#define GLED D1
#define BLED D2

int maxValue = 32;
int minValue = 13;

void setup(void){
	Serial.begin(9600);
  pinMode(RLED, OUTPUT);
  pinMode(GLED, OUTPUT);
  pinMode(BLED, OUTPUT);
	SPIFFS.begin();
	ConnectWiFi_STA(false);
	InitMqtt();
}


void loop(){
	HandleMqtt();
  //--------------------------------------------------------------------------------------
  int value = analogRead(PhotoR);
  if (value < minValue){ value = 13; }
  Serial.print("Luz disponible: ");
  Serial.println(value);
  int light = map(value, minValue, maxValue, 255, 0);
  Serial.print("Luz ejecutada: ");
  Serial.println(light);
  analogWrite(RLED, light);
  analogWrite(GLED, light);
  analogWrite(BLED, light);
  //--------------------------------------------------------------------------------------
	PublisMqtt(value);
	delay(1000);
}


