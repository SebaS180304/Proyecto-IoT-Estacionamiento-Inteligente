import sys
import threading
import paho.mqtt.client as paho
import time
import mysql.connector
from mysql.connector import errorcode

# Credenciales de MySQL
host = "localhost"
user = "root"
password = "Rosas05!"

# Nombre de la base de datos y las tablas
database_name = "ParkingLot"
table_name1 = "cajon"
table_name2 = "estacionamiento"

# Configuración inicial de MySQL
try:
    cnx = mysql.connector.connect(
        host=host,
        user=user,
        password=password
    )
    cursor = cnx.cursor()

    # Crear la base de datos si no existe
    try:
        cursor.execute(f"CREATE DATABASE {database_name}")
        print(f"Base de datos '{database_name}' creada.")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_DB_CREATE_EXISTS:
            print(f"La base de datos '{database_name}' ya existe.")
        else:
            print(err.msg)

    # Conectar a la base de datos
    cnx.database = database_name

    # Crear las tablas si no existen
    table_cajon_query = (
        f"CREATE TABLE IF NOT EXISTS {table_name1} ("
        "id INT AUTO_INCREMENT PRIMARY KEY, "
        "DistanciaH INT NOT NULL, "
        "DistanciaL INT NOT NULL, "
        "timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP)"
    )
    table_estacionamiento_query = (
        f"CREATE TABLE IF NOT EXISTS {table_name2} ("
        "id INT AUTO_INCREMENT PRIMARY KEY, "
        "Temperatura INT NOT NULL, "
        "Iluminacion INT NOT NULL, "
        "Movimiento INT NOT NULL, "
        "timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP)"
    )
    cursor.execute(table_cajon_query)
    cursor.execute(table_estacionamiento_query)
    print(f"Tablas '{table_name1}' y '{table_name2}' creadas o ya existen.")

except mysql.connector.Error as err:
    print(f"Error en la configuración inicial de MySQL: {err}")
    sys.exit(1)
finally:
    cursor.close()
    cnx.close()

# Clientes MQTT
client1 = paho.Client()
client2 = paho.Client()
client3 = paho.Client()
client4 = paho.Client()
client5 = paho.Client()

# Diccionarios para almacenar datos
estacionamiento_data = {"Temperatura": None, "Iluminacion": None, "Movimiento": None}
cajon_data = {"DistanciaH": None, "DistanciaL": None}

def insert_data(table_name, data):
    """Inserta datos en la base de datos."""
    try:
        cnx = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database_name
        )
        cursor = cnx.cursor()

        if table_name == table_name1:  # Tabla cajon
            query = f"INSERT INTO {table_name} (DistanciaH, DistanciaL) VALUES (%s, %s)"
            cursor.execute(query, (data["DistanciaH"], data["DistanciaL"]))
        elif table_name == table_name2:  # Tabla estacionamiento
            query = f"INSERT INTO {table_name} (Temperatura, Iluminacion, Movimiento) VALUES (%s, %s, %s)"
            cursor.execute(query, (data["Temperatura"], data["Iluminacion"], data["Movimiento"]))

        cnx.commit()
        print(f"Datos insertados en {table_name}: {data}")
    except mysql.connector.Error as err:
        print(f"Error al insertar datos: {err}")
    finally:
        cursor.close()
        cnx.close()
        
def insert_or_update_cajon_data():
    """Inserta o actualiza los datos relacionados con la tabla 'cajon', incluyendo el estado."""
    if cajon_data["DistanciaH"] is not None and cajon_data["DistanciaL"] is not None:
        try:
            # Calcular estado
            estado = "No disponible" if cajon_data["DistanciaH"] < 7 else "Disponible"

            # Conectar a la base de datos
            cnx = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database_name
            )
            cursor = cnx.cursor()

            # Insertar datos con estado
            query = f"""
                INSERT INTO {table_name1} (DistanciaH, DistanciaL, estado)
                VALUES (%s, %s, %s)
            """
            cursor.execute(query, (cajon_data["DistanciaH"], cajon_data["DistanciaL"], estado))
            cnx.commit()
            print(f"Datos insertados en '{table_name1}': {cajon_data}, estado: {estado}")
        except mysql.connector.Error as err:
            print(f"Error al insertar datos en 'cajon': {err}")
        finally:
            cursor.close()
            cnx.close()

        # Limpiar el diccionario después de insertar
        for key in cajon_data:
            cajon_data[key] = None

def message_handling_1(client, userdata, msg):
    estacionamiento_data["Temperatura"] = int(msg.payload.decode())
    if all(estacionamiento_data.values()):
        insert_data(table_name2, estacionamiento_data)
        for key in estacionamiento_data:
            estacionamiento_data[key] = None

def message_handling_2(client, userdata, msg):
    estacionamiento_data["Iluminacion"] = int(msg.payload.decode())
    if all(estacionamiento_data.values()):
        insert_data(table_name2, estacionamiento_data)
        for key in estacionamiento_data:
            estacionamiento_data[key] = None

def message_handling_3(client, userdata, msg):
    estacionamiento_data["Movimiento"] = int(msg.payload.decode())
    if all(estacionamiento_data.values()):
        insert_data(table_name2, estacionamiento_data)
        for key in estacionamiento_data:
            estacionamiento_data[key] = None

def message_handling_4(client, userdata, msg):
    cajon_data["DistanciaH"] = int(msg.payload.decode())
    insert_or_update_cajon_data()

def message_handling_5(client, userdata, msg):
    cajon_data["DistanciaL"] = int(msg.payload.decode())
    insert_or_update_cajon_data()

# Asignar callbacks a los clientes
client1.on_message = message_handling_1
client2.on_message = message_handling_2
client3.on_message = message_handling_3
client4.on_message = message_handling_4
client5.on_message = message_handling_5

if __name__ == "__main__":
    try:
        print("Presiona CTRL+C para salir...")

        # Conectar los clientes MQTT
        for client in [client1, client2, client3, client4, client5]:
            client.connect("localhost", 1883, 60)

        # Suscribirse a los temas
        client1.subscribe("arduino_1/hello_node1clima")
        client2.subscribe("arduino_1/hello_node2luz")
        client3.subscribe("arduino_1/hello_node3peaton")
        client4.subscribe("arduino_1/hello_node4dist1")
        client5.subscribe("arduino_1/hello_node5dist2")

        # Ejecutar los clientes en hilos
        threads = [threading.Thread(target=client.loop_forever) for client in [client1, client2, client3, client4, client5]]
        for thread in threads:
            thread.start()

        while True:
            time.sleep(0.5)

    except KeyboardInterrupt:
        print("Desconectando...")
        for client in [client1, client2, client3, client4, client5]:
            client.disconnect()
        print("Programa terminado.")
