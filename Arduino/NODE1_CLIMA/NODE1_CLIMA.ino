#include <ESP8266WiFi.h>
#include <PubSubClient.h>

#include "config.h"
#include "MQTT.hpp"
#include "ESP8266_Utils.hpp"
#include "ESP8266_Utils_MQTT.hpp"
#include "DHT.h"

#define DHTPIN D7
#define DHTTYPE DHT11
#define fanPin D8

DHT dht(DHTPIN, DHTTYPE);


void setup(void){
	Serial.begin(9600);
  dht.begin();
  pinMode(fanPin, OUTPUT);
	SPIFFS.begin();
	ConnectWiFi_STA(false);
	InitMqtt();
}


void loop(){
	HandleMqtt();
  //--------------------------------------------------------------------------------------
  float humidity = dht.readHumidity();
  float temperature = dht.readTemperature();
  if (isnan(humidity) || isnan(temperature)){
    Serial.println("Failed to read from DHT sensor!");
    delay(1000);
    return;
  } 
  int fan = 0;
  if (temperature >= 30){
    fan = 1;
  }
  digitalWrite(fanPin, fan);
  Serial.print("Humedad: ");
  Serial.print(humidity);
  Serial.print(" %\t");
  Serial.print("Temperatura: ");
  Serial.print(temperature);
  Serial.println(" °C\t");
  //--------------------------------------------------------------------------------------
	PublisMqtt(temperature);
	delay(1000);
}


