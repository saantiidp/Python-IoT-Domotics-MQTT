from .device import Device
import random

class Sensor(Device):
    """
    Clase Sensor que representa un sensor de temperatura,
    heredando de la clase abstracta Device.
    """

    def __init__(self, device_id):
        """
        Inicializa un sensor con su identificador único.

        Args:
            device_id (str): Identificador del sensor.
        """
        super().__init__(device_id)

    def get_data(self):
        """
        Método placeholder que podría ser utilizado para obtener
        datos del sensor de forma manual o programada.

        Returns:
            None
        """
        pass

    def handle_message(self, client, msg):
        """
        Procesa un mensaje MQTT recibido y responde con un valor aleatorio simulado.

        Args:
            client (paho.mqtt.client.Client): Cliente MQTT conectado.
            msg (paho.mqtt.client.MQTTMessage): Mensaje recibido.

        Returns:
            None
        """
        print(f"Sensor recibió mensaje en topic '{msg.topic}': {msg.payload.decode('utf-8')}")
        # Simular una medida de temperatura aleatoria entre -20 y 50 grados
        sensor_value = random.uniform(-20, 50)
        # Publicar el valor generado en el mismo topic del sensor
        client.publish(self.topic, f"Sensor value: {sensor_value:.2f}")
