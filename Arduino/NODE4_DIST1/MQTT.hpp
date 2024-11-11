
const char* MQTT_BROKER_ADRESS = "172.20.10.2";
const uint16_t MQTT_PORT = 1883;
const char* MQTT_CLIENT_NAME = "NODE4_DIST1";

WiFiClient espClient;
PubSubClient mqttClient(espClient);

void SuscribeMqtt()
{
	mqttClient.subscribe("arduino_1/hello_node4dist1");
}

String payload;
void PublisMqtt(unsigned long data)
{
	payload = "";
	payload = String(data);
	mqttClient.publish("arduino_1/hello_node4dist1", (char*)payload.c_str());
}

String content = "";
void OnMqttReceived(char* topic, byte* payload, unsigned int length) 
{
	Serial.print("Received on ");
	Serial.print(topic);
	Serial.print(": ");

	content = "";	
	for (size_t i = 0; i < length; i++) {
		content.concat((char)payload[i]);
	}
	Serial.print(content);
	Serial.println();
}