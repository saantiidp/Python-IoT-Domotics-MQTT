import paho.mqtt.client as mqtt
import subprocess
import time
import os
import signal

received_messages = []

def on_message(client, userdata, msg):
    received_messages.append(msg.payload.decode())

def test_dummy_clock_response():
    broker = "localhost"
    topic_response = "redes2/2312/1/watch_2"

    # Lanzamos el dummy_clock en segundo plano
    process = subprocess.Popen([
        "python3", "dummy_devices/dummy_clock.py", 
        "--host", broker, "--port", "1883", "--time", "12:00:00", 
        "--increment", "1", "--rate", "1", "2"
    ])

    # Esperamos a que se conecte y publique
    time.sleep(2)

    client = mqtt.Client()
    client.on_message = on_message
    client.connect(broker, 1883, 60)
    client.subscribe(topic_response)
    client.loop_start()

    time.sleep(5)  # Esperar mensajes publicados

    client.loop_stop()
    client.disconnect()

    # Terminamos el dummy
    os.kill(process.pid, signal.SIGINT)

    # Validamos que se ha recibido al menos una hora
    assert any(":" in msg for msg in received_messages), "No se recibió hora del dummy reloj."
