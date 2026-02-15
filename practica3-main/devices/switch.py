from .device import Device
import json

class Switch(Device):
    """
    Clase Switch que representa un interruptor (on/off),
    heredando de la clase abstracta Device.
    """

    def __init__(self, device_id):
        """
        Inicializa un interruptor con su identificador único y estado inicial apagado.

        Args:
            device_id (str): Identificador único del switch.
        """
        super().__init__(device_id)
        self.state = False  # El switch empieza apagado (False)

    def get_data(self):
        """
        Método placeholder para futura extensión,
        como obtener el estado automáticamente.

        Returns:
            None
        """
        pass

    def handle_message(self, client, msg):
        """
        Procesa un mensaje MQTT para cambiar el estado del switch.

        Actualmente no implementado (se implementaría en el dummy_switch).

        Args:
            client (paho.mqtt.client.Client): Cliente MQTT.
            msg (paho.mqtt.client.MQTTMessage): Mensaje recibido.

        Returns:
            None
        """
        pass

    def get_device_id(self) -> str:
        """
        Obtiene el identificador del switch.

        Returns:
            str: Identificador único del switch.
        """
        return self.device_id

    def get_state(self) -> bool:
        """
        Obtiene el estado actual del switch (encendido/apagado).

        Returns:
            bool: Estado del switch (True para encendido, False para apagado).
        """
        return self.state
