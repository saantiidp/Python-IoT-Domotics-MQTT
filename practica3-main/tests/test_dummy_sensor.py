import paho.mqtt.client as mqtt
import time

received_messages = []

def on_message(client, userdata, msg):
    decoded = msg.payload.decode()
    print(f"Mensaje recibido en {msg.topic}: {decoded}")
    received_messages.append(decoded)

def test_dummy_sensor_response():
    """
    Verifica que dummy_sensor publica al menos un mensaje en sensor_1.
    """
    broker = "localhost"
    topic_response = "redes2/2312/1/sensor_1"


    client = mqtt.Client()
    client.on_message = on_message
    client.connect(broker, 1883, 60)
    client.subscribe(topic_response)
    client.loop_start()

    timeout = 5  # segundos
    start_time = time.time()

    while time.time() - start_time < timeout:
        if received_messages:  
            break
        time.sleep(0.1)

    client.loop_stop()
    client.disconnect()

    print(f"Mensajes recibidos: {received_messages}")
    assert received_messages, "No se recibió ningún mensaje del dummy sensor."