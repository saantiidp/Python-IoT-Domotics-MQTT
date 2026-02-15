from .device import Device
from datetime import datetime, timedelta

class Watch(Device):
    """
    Clase Watch que representa un reloj configurable en el sistema domótico,
    heredando de la clase abstracta Device.
    """

    def __init__(self, device_id, start_time, frequency, rate):
        """
        Inicializa un reloj con hora inicial, frecuencia de actualización y velocidad de avance.

        Args:
            device_id (str): Identificador único del reloj.
            start_time (str or datetime): Hora de inicio en formato string '%H:%M:%S' o datetime.
            frequency (int): Frecuencia de actualización en segundos.
            rate (int): Velocidad de avance del reloj (por ejemplo, 2x más rápido que el tiempo real).
        """
        super().__init__(device_id)
        self.frequency = frequency
        self.rate = rate
        if isinstance(start_time, str):
            self.current_time = datetime.strptime(start_time, '%H:%M:%S')
        else:
            self.current_time = start_time

    def handle_message(self, client, msg):
        """
        Procesa un mensaje MQTT recibido solicitando la hora actual.

        Args:
            client (paho.mqtt.client.Client): Cliente MQTT conectado.
            msg (paho.mqtt.client.MQTTMessage): Mensaje recibido.

        Returns:
            None
        """
        print(f"🕒 Reloj recibió solicitud de hora en topic '{msg.topic}'")
        client.publish(self.topic, self.get_time())

    def get_time(self):
        """
        Obtiene la hora actual formateada como string.

        Returns:
            str: Hora actual del reloj en formato 'HH:MM:SS'.
        """
        return self.current_time.strftime('%H:%M:%S')

    def advance_time(self):
        """
        Avanza la hora del reloj según la frecuencia y la tasa de avance configuradas.

        Returns:
            None
        """
        self.current_time += timedelta(seconds=self.frequency * self.rate)
