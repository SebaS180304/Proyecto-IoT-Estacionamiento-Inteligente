#include <ESP8266WiFi.h>
#include <PubSubClient.h>

#include "config.h"  // Sustituir con datos de vuestra red
#include "MQTT.hpp"
#include "ESP8266_Utils.hpp"
#include "ESP8266_Utils_MQTT.hpp"

#define PhotoR A0
#define LED D1
int valorLDR = 0;
int umbralNum = 1000;


void setup(void){
	Serial.begin(9600);
  pinMode(LED, OUTPUT);
	SPIFFS.begin();
	ConnectWiFi_STA(false);
	InitMqtt();
}


void loop(){
	HandleMqtt();
  //--------------------------------------------------------------------------------------
  if (valorLDR = analogRead(PhotoR) >= umbralNum){
    digitalWrite(LED, HIGH);
  } else {
    digitalWrite(LED, LOW);
  }
  //--------------------------------------------------------------------------------------
	PublisMqtt(valorLDR);
	delay(1000);
}


