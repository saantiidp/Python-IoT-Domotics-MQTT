"""
dummy_clock.py

Simula un reloj que publica la hora cada cierto intervalo en un topic MQTT.

Argumentos:
  --host         Host del broker MQTT (por defecto: redes2.ii.uam.es)
  --port, -p     Puerto del broker MQTT (por defecto: 1883)
  --time         Hora de inicio en formato HH:MM:SS (por defecto: hora actual)
  --increment    Incremento en segundos entre publicaciones (por defecto: 1)
  --rate         Frecuencia de publicación (en segundos) (por defecto: 1)
  id             ID del reloj (entero, obligatorio)

Ejemplo:
  python dummy_clock.py --host localhost --port 1883 --time 09:00:00 --increment 60 --rate 1 1
"""
import argparse
import time
import json
import signal
import os
from datetime import datetime, timedelta
import paho.mqtt.client as mqtt

clocks_file = "data/clocks.json"
clock_data = {}
client = None

def load_clocks():
    """"
    Carga el estado de los relojes desde clocks.json.
    Si el archivo no existe o está vacío/corrupto, se usa un diccionario vacío.
    """
    global clock_data
    if os.path.exists(clocks_file):
        try:
            with open(clocks_file, "r") as f:
                clock_data = json.load(f)
                print("Relojes cargados correctamente de clocks.json")
        except json.JSONDecodeError:
            print("clocks.json vacío o corrupto. Se inicializa estado vacío.")
            clock_data = {}
    else:
        print("No se encontró clocks.json. Se usará configuración por defecto.")
        clock_data = {}

def save_clocks():
    """
    Guarda el estado actual de los relojes en clocks.json.
    """
    with open(clocks_file, "w") as f:
        json.dump(clock_data, f, indent=2)
        print("Estado de relojes guardado.")

def handle_sigint(sig, frame):
    """
    Maneja la señal SIGINT (Ctrl+C) para salir limpiamente.
    Guarda el estado y desconecta del broker.
    """
    print("\nSaliendo por Ctrl+C...")
    save_clocks()
    if client:
        client.disconnect()
    exit(0)

def run(host, port, clock_id, start_time, increment, rate):
    """
    Ejecuta la lógica principal del reloj simulado.
    Publica una hora en incremento definido a una frecuencia fija.

    Args:
        host (str): Host del broker MQTT.
        port (int): Puerto del broker MQTT.
        clock_id (int): ID del reloj.
        start_time (str): Hora inicial en formato HH:MM:SS.
        increment (int): Incremento en segundos por cada publicación.
        rate (float): Intervalo entre publicaciones (frecuencia).
    """    
    global client
    topic_response = f"redes2/2312/1/watch_{clock_id}"

    if topic_response not in clock_data:
        clock_data[topic_response] = start_time

    current_time = datetime.strptime(clock_data[topic_response], "%H:%M:%S")
    delta = timedelta(seconds=increment)

    client = mqtt.Client(protocol=mqtt.MQTTv311)


    client.connect(host, port, 60)
    print(f"Clock conectado al broker {host}:{port} con resultado {client.connect(host, port)}")
    print(f"Publicando en topic {topic_response}")

    signal.signal(signal.SIGINT, handle_sigint)

    while True:
        clock_str = current_time.strftime("%H:%M:%S")
        client.publish(topic_response, clock_str)
        clock_data[topic_response] = clock_str
        current_time += delta
        time.sleep(rate)

def main():
    """
    Analiza los argumentos de línea de comandos y lanza la simulación del reloj.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="redes2.ii.uam.es")
    parser.add_argument("--port", "-p", type=int, default=1883)
    parser.add_argument("--time", default=None, help="Hora de inicio (HH:MM:SS)")
    parser.add_argument("--increment", type=int, default=1, help="Incremento en segundos")
    parser.add_argument("--rate", type=float, default=1.0, help="Frecuencia de envío en segundos")
    parser.add_argument("id", type=int, help="ID del reloj")

    args = parser.parse_args()
    if args.time:
        start_time = args.time
    else:
        start_time = datetime.now().strftime("%H:%M:%S")

    load_clocks()
    run(args.host, args.port, args.id, start_time, args.increment, args.rate)

if __name__ == "__main__":
    main()
