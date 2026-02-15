import paho.mqtt.client as mqtt
import time

received_messages = []

def on_message(client, userdata, msg):
    decoded = msg.payload.decode()
    print(f"Mensaje recibido en {msg.topic}: {decoded}")
    received_messages.append(decoded)

def test_dummy_switch_response():
    """
    Verifica que dummy_switch responde con 'ON' o 'OFF' tras recibir un mensaje en switch_1.
    """
    broker = "localhost"
    topic_trigger = "redes2/2312/1/switch_1"
    topic_response = "redes2/2312/1/switch_2"

    client = mqtt.Client()
    client.on_message = on_message
    client.connect(broker, 1883, 60)
    client.subscribe(topic_response)
    client.loop_start()

    client.publish(topic_trigger, "1")  # Enviamos acción

    start_time = time.time()
    while time.time() - start_time < 5:
        if any(msg in ["ON", "OFF"] for msg in received_messages):
            break
        time.sleep(0.1)

    client.loop_stop()
    client.disconnect()

    assert any(msg in ["ON", "OFF"] for msg in received_messages), "No se recibió respuesta del dummy switch."