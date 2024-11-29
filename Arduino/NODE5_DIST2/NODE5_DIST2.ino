#include <ESP8266WiFi.h>
#include <PubSubClient.h>

#include "config.h"
#include "MQTT.hpp"
#include "ESP8266_Utils.hpp"
#include "ESP8266_Utils_MQTT.hpp"

#define trigPin D2
#define echoPin D3
#define gLED D6
#define yLED D5
#define rLED D4
long prevDistance;


void setup(void){
	Serial.begin(9600);
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin,INPUT);
  pinMode(rLED, OUTPUT);
  pinMode(yLED, OUTPUT);
  pinMode(gLED, OUTPUT);
	SPIFFS.begin();
	ConnectWiFi_STA(false);
	InitMqtt();
}


void loop(){
	HandleMqtt();
  //--------------------------------------------------------------------------------------
  long time;
  long distance;
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  time = pulseIn(echoPin, HIGH);
  distance = time/59;
  int red = 0;
  int yellow = 0;
  int green = 0;
  if (distance < 5){
    yellow = 1;
  }
  Serial.print("Distancia: ");
  Serial.print(distance);
  Serial.println(" cm");
  digitalWrite(rLED, red);
  digitalWrite(yLED, yellow);
  digitalWrite(gLED, green);
  PublisMqtt(distance);
  //--------------------------------------------------------------------------------------
	delay(1000);
}


