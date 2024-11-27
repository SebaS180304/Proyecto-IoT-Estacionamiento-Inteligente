#include <ESP8266WiFi.h>
#include <PubSubClient.h>

#include "config.h"
#include "MQTT.hpp"
#include "ESP8266_Utils.hpp"
#include "ESP8266_Utils_MQTT.hpp"
#include "DHT.h"

#define DHTPIN D7
#define DHTTYPE DHT11
#define fanPin D1

DHT dht(DHTPIN, DHTTYPE);
float prevTemp = 0;


void setup(void){
	Serial.begin(9600);
  dht.begin();
	SPIFFS.begin();
  pinMode(fanPin, OUTPUT);
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
  
  if (temperature >= 27){
    pinMode(fanPin, INPUT);
    Serial.println("Encendido");
  } else {
    pinMode(fanPin, OUTPUT);
    digitalWrite(fanPin, 0);
    Serial.println("Apagado");
  }
  Serial.print("Humedad: ");
  Serial.print(humidity);
  Serial.print(" %\t");
  Serial.print("Temperatura: ");
  Serial.print(temperature);
  Serial.println(" °C\t");
  //--------------------------------------------------------------------------------------
  //if(prevTemp != temperature && temperature >= 30){ PublisMqtt(temperature); }
  PublisMqtt(temperature);
  prevTemp = temperature;
	delay(1000);
}


