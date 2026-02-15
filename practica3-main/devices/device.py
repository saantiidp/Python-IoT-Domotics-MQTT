import abc
import uuid

class Device(abc.ABC):
    """
    Clase abstracta base para representar un dispositivo del sistema domótico.

    Cada dispositivo tiene un identificador único y debe implementar su propia
    lógica de manejo de mensajes MQTT.
    """

    def __init__(self, device_id):
        """
        Inicializa un nuevo dispositivo con el identificador proporcionado.

        Args:
            device_id (str): Identificador único del dispositivo.
        """
        self.device_id = device_id

    @abc.abstractmethod
    def handle_message(self, client, msg):
        """
        Método abstracto que debe ser implementado por las subclases.

        Define cómo el dispositivo debe procesar un mensaje MQTT recibido.

        Args:
            client (paho.mqtt.client.Client): Instancia del cliente MQTT.
            msg (paho.mqtt.client.MQTTMessage): Mensaje recibido.

        Returns:
            None
        """
        pass
