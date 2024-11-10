import paho.mqtt.client as mqtt
import mysql.connector
from mysql.connector import errorcode
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)


# Configuración de la base de datos
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Rosas05!',
    'database': 'ParkingLot'
}

# Configuración MQTT
mqtt_broker = "localhost"  # Cambiar si el broker MQTT está en otro host
mqtt_port = 1883
mqtt_topic = "esp8266/temperature"

# Función para conectar a la base de datos e insertar temperatura
def insert_temperature(temperature):
    try:
        # Conectarse a la base de datos MySQL
        cnx = mysql.connector.connect(**db_config)
        cursor = cnx.cursor()

        # Consulta de inserción para la tabla estacionamiento
        insert_query = "INSERT INTO estacionamiento (Temperatura) VALUES (%s)"
        cursor.execute(insert_query, (temperature,))
        
        cnx.commit()
        print(f"Temperatura {temperature} insertada en la base de datos.")

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Error en las credenciales de la base de datos.")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("La base de datos no existe.")
        else:
            print(err)
    finally:
        cursor.close()
        cnx.close()

# Callback para el mensaje MQTT recibido
def on_message(client, userdata, msg):
    try:
        temperature = float(msg.payload.decode())
        print(f"Temperatura recibida: {temperature}")
        
        # Llamar a la función para insertar en la base de datos
        insert_temperature(temperature)

    except ValueError:
        print("Error: La temperatura recibida no es un número válido.")

# Configuración y conexión MQTT
client = mqtt.Client()

client.on_message = on_message

try:
    client.connect(mqtt_broker, mqtt_port, 60)
    print("Conectado al broker MQTT.")
except Exception as e:
    print(f"No se pudo conectar al broker MQTT: {e}")
    exit(1)

# Suscribirse al topic donde el ESP8266 publica la temperatura
client.subscribe(mqtt_topic)

# Bucle principal de MQTT
try:
    client.loop_forever()
except KeyboardInterrupt:
    print("Desconectando del broker MQTT.")
    client.disconnect()