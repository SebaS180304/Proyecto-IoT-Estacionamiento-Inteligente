import sys
import threading
import paho.mqtt.client as paho
import time
import signal


import mysql.connector
from mysql.connector import errorcode

# Configuración de la base de datos
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Rosas05!',
    'database': 'ParkingLot'
}

# Nombre de la tabla
table_name = "test_datatable"

client1 = paho.Client()
client2 = paho.Client()

data1 = None
data2 = None

apprun = True

# Función para conectar a la base de datos e insertar datos
def insert_into_db(data):
    try:
        # Conectarse a la base de datos MySQL
        cnx = mysql.connector.connect(**db_config)
        cursor = cnx.cursor()

        # Insertar el payload recibido en la tabla
        insertion_query = f"INSERT INTO {table_name} (value) VALUES (%s)"
        cursor.execute(insertion_query, (data,))
        cnx.commit()
        print(f"Valor {data} insertado en la tabla '{table_name}'.")

    except mysql.connector.Error as err:
        print(f"Error de base de datos: {err}")
    finally:
        cursor.close()
        cnx.close()

def message_handling_1(client, userdata, msg):
    global data1
    data1 = msg.payload.decode()
    insert_into_db(data1)

def message_handling_2(client, userdata, msg):
    global data2
    data2 = msg.payload.decode()
    insert_into_db(data2)

def loop_1(num):
    global client1
    client1.loop_forever()

def loop_2(num):
    global client2
    client2.loop_forever()

def signal_handler(sig, frame):
    global client1
    global client2
    print('You pressed Ctrl+C!')
    client1.disconnect()
    client2.disconnect()
    print("Quit")
    exit(0)

signal.signal(signal.SIGINT, signal_handler)

if client1.connect("localhost", 1883, 60) != 0:
    print("No se pudo conectar al broker MQTT")
    exit(1)
    
if client2.connect("localhost", 1883, 60) != 0:
    print("No se pudo conectar al broker MQTT")
    exit(1)

client1.subscribe("arduino_1/hello_esp8266")
client2.subscribe("arduino_2/hello_esp8266")

try:
    print("Presiona CTRL+C para salir...")
    t1 = threading.Thread(target=loop_1, args=(0,))
    t2 = threading.Thread(target=loop_2, args=(0,))
    
    t1.start()
    t2.start()
    
    while True:
        try:
            time.sleep(0.5)
            print("data1:" + str(data1))
            print("data2:" + str(data2))
            print("----")
        except KeyboardInterrupt:
            print("Desconectando")
            client1.disconnect()
            client2.disconnect()
            time.sleep(1)
            break
    
    t1.join()
    t2.join()
    
except Exception:
    print("Se detecto una excepción, algo salio mal...")
