"""
dummy_sensor.py

Simula un sensor que publica una temperatura variable en un topic MQTT.

Argumentos:
  --host         Host del broker MQTT (por defecto: redes2.ii.uam.es)
  --port, -p     Puerto del broker MQTT (por defecto: 1883)
  --min, -m      Valor mínimo de temperatura (por defecto: 20)
  --max, -M      Valor máximo de temperatura (por defecto: 30)
  --increment    Incremento entre valores (por defecto: 1)
  --interval, -i Intervalo de publicación en segundos (por defecto: 1)
  id             ID del sensor (entero, obligatorio)

Ejemplo:
  python dummy_sensor.py --host localhost --port 1883 --min 20 --max 30 --increment 1 --interval 1 2
"""
import argparse
import time
import json
import signal
import os
import paho.mqtt.client as mqtt



sensors_file = "data/sensors.json"
sensor_data = {}
client = None

def load_sensors():
    """
    Carga el estado de los sensores desde sensors.json.
    Si el archivo no existe o está vacío/corrupto, se usa un diccionario vacío.
    """
    global sensor_data
    if os.path.exists(sensors_file):
        try:
            with open(sensors_file, "r") as f:
                sensor_data = json.load(f)
                print("Sensores cargados correctamente de sensors.json")
        except json.JSONDecodeError:
            print("sensors.json vacío o corrupto. Se inicializa estado vacío.")
            sensor_data = {}
    else:
        print("No se encontró sensors.json. Se usará configuración por defecto.")
        sensor_data = {}

def save_sensors():
    """
    Guarda el estado actual de los sensores en sensors.json.
    """
    with open(sensors_file, "w") as f:
        json.dump(sensor_data, f, indent=2)
        print("Estado de sensores guardado.")

def handle_sigint(sig, frame):
    """
    Maneja la señal SIGINT (Ctrl+C) para salir limpiamente.
    Guarda el estado y desconecta del broker.
    """
    print("\nSaliendo por Ctrl+C...")
    save_sensors()
    if client:
        client.disconnect()
    exit(0)

def run(host, port, sensor_id, min_val, max_val, increment, interval,test_once=False):
    """
    Ejecuta la lógica principal del sensor simulado.
    Publica temperaturas simuladas en un topic a intervalos regulares.

    Args:
        host (str): Host del broker MQTT.
        port (int): Puerto del broker MQTT.
        sensor_id (int): ID del sensor.
        min_val (int): Valor mínimo de temperatura.
        max_val (int): Valor máximo de temperatura.
        increment (int): Paso de incremento entre valores.
        interval (float): Tiempo entre publicaciones en segundos.
    """
    global client
    topic_response = f"redes2/2312/1/sensor_{sensor_id}"

    if topic_response not in sensor_data:
        sensor_data[topic_response] = min_val

    client = mqtt.Client(protocol=mqtt.MQTTv311)

    rc = client.connect(host, port, 60)
    print(f"Sensor conectado al broker {host}:{port} con resultado {rc}", flush=True)

    print(f"Publicando en topic {topic_response}")

    signal.signal(signal.SIGINT, handle_sigint)

    current = sensor_data[topic_response]
    while True:
        client.publish(topic_response, f"Temperature: {current} °C")
        current += increment
        if current > max_val:
            current = min_val
        sensor_data[topic_response] = current
        if test_once:
            time.sleep(0.1)
            break  # solo una vez para pruebas
        time.sleep(interval)

def main():
    """
    Analiza los argumentos de línea de comandos y lanza la simulación del sensor.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="redes2.ii.uam.es")
    parser.add_argument("--port", "-p", type=int, default=1883)
    parser.add_argument("--min", "-m", type=int, default=20)
    parser.add_argument("--max", "-M", type=int, default=30)
    parser.add_argument("--increment", type=int, default=1)
    parser.add_argument("--interval", "-i", type=float, default=1)
    parser.add_argument("id", type=int, help="ID del sensor")
    parser.add_argument("--test-once", action="store_true")
    args = parser.parse_args()
    load_sensors()
    run(args.host, args.port, args.id, args.min, args.max, args.increment, args.interval, args.test_once)

if __name__ == "__main__":
    main()