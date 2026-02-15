"""
dummy_switch.py

Simula un interruptor (switch) que cambia su estado ON/OFF al recibir una acción por MQTT.

Argumentos:
  --host         Host del broker MQTT (por defecto: redes2.ii.uam.es)
  --port, -p     Puerto del broker MQTT (por defecto: 1883)
  --probability, -P  Probabilidad de fallo al recibir una acción (por defecto: 0.3)
  id             ID del switch (entero, obligatorio)

Ejemplo:
  python dummy_switch.py --host localhost --port 1883 --probability 0.4 1
"""
import paho.mqtt.client as mqtt
import json
import random
import argparse
import signal
import sys
import os

# Variables globales
switch_data = {}
switch_id = None
broker_host = None
broker_port = None
probability = 0.3
client = None

def handle_action(device_id):
    """
    Cambia el estado del switch manualmente (para test).
    """
    state = switch_data.get(str(device_id), False)
    switch_data[str(device_id)] = not state
    return "ON" if not state else "OFF"
# Funciones para guardar y cargar estado de switches
def save_switches():
    """
    Guarda el estado actual de los switches en switches.json.
    """    
    os.makedirs("data", exist_ok=True)
    with open("data/switches.json", "w") as f:
        json.dump(switch_data, f)
    print("Estado de switches guardado.")

def load_switches():
    """
    Carga el estado de los switches desde switches.json.
    Si el archivo no existe o está vacío/corrupto, se usa un diccionario vacío.
    """
    global switch_data
    try:
        with open("data/switches.json", "r") as f:
            switch_data = json.load(f)
        print("Switches cargados correctamente de switches.json")
    except (FileNotFoundError, json.JSONDecodeError):
        switch_data = {}
        print("No se pudo cargar switches.json. Se usará configuración por defecto.")


# Función al recibir señal SIGINT (Ctrl+C)
def handle_sigint(sig, frame):
    """
    Maneja la señal SIGINT (Ctrl+C) para salir limpiamente.
    Guarda el estado y sale del programa.
    """
    print("\nSaliendo por Ctrl+C...")
    save_switches()
    sys.exit(0)

# Callback al conectar con el broker
def on_connect(client, userdata, flags, rc):
    """
    Callback que se ejecuta al conectar al broker.
    Se suscribe al topic del switch correspondiente.

    Args:
        client: Instancia del cliente MQTT.
        userdata: Datos definidos por el usuario.
        flags: Banderas de conexión.
        rc (int): Código de resultado de la conexión.
    """
    print(f"Switch conectado al broker {broker_host}:{broker_port} con resultado {rc}")
    topic_request = f"redes2/2312/1/switch_{switch_id}"
    client.subscribe(topic_request)
    print(f"Suscrito al topic {topic_request}")

# Callback al recibir un mensaje
def on_message(client, userdata, msg):
    """
    Callback que se ejecuta al recibir un mensaje.
    Cambia el estado del switch si no hay fallo simulado.

    Args:
        client: Instancia del cliente MQTT.
        userdata: Datos definidos por el usuario.
        msg: Mensaje MQTT recibido.
    """
    global switch_data
    message = msg.payload.decode()
    print(f"Mensaje recibido en {msg.topic}: {message}")
    
    if random.random() < probability:
        print("Simulando fallo. No se realizará acción.")
        return

    state = switch_data.get(str(switch_id), False)
    switch_data[str(switch_id)] = not state
    print(f"Nuevo estado de switch {switch_id}: {'ON' if not state else 'OFF'}")
    
    topic_response = f"redes2/2312/1/switch_{switch_id+1}"
    response = "ON" if not state else "OFF"
    client.publish(topic_response, response)
    print(f"Respuesta publicada en {topic_response}: {response}")

def main():
    """
    Analiza los argumentos de línea de comandos y lanza la simulación del switch.
    """
    global switch_id, broker_host, broker_port, probability, client

    parser = argparse.ArgumentParser(description="Dummy switch device")
    parser.add_argument("--host", default="redes2.ii.uam.es", help="Broker host")
    parser.add_argument("-p", "--port", type=int, default=1883, help="Broker port")
    parser.add_argument("-P", "--probability", type=float, default=0.3, help="Failure probability")
    parser.add_argument("id", type=int, help="Switch device ID")
    args = parser.parse_args()

    broker_host = args.host
    broker_port = args.port
    probability = args.probability
    switch_id = args.id

    signal.signal(signal.SIGINT, handle_sigint)

    load_switches()

    client = mqtt.Client(protocol=mqtt.MQTTv311)





    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(broker_host, broker_port, 60)
    client.loop_forever()

if __name__ == "__main__":
    main()