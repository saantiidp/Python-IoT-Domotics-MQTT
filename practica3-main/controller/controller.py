import argparse
import discord
import json
import sys
import signal
import paho.mqtt.client as mqtt

# Variables globales
device_data = {"device_last_id": 3, "devices": {"1": "sensor", "2": "switch", "3": "watch"}}
latest_message = None
message_flag = 0
DEVICES_FILE = "data/devices.json"  # Ruta al archivo de persistencia

# Función para obtener el TOKEN de un archivo

def get_token_from_file(filepath="config/bot_info.txt"):
    """
    Lee un archivo de configuración y obtiene el token de autenticación del bot de Discord.

    Args:
        filepath (str): Ruta relativa o absoluta del archivo que contiene el token. 
                        'config/bot_info.txt'.

    Returns:
        str: El token de autenticación del bot.

    Raises:
        FileNotFoundError: Si el archivo especificado no existe.
        ValueError: Si no se encuentra el token en el archivo.
    """
    with open(filepath, "r") as f:
        for line in f:
            if line.startswith("token:"):
                return f.readline().strip()

# Manejo de interrupciones

def signal_handler(sig, frame):
    """
    Maneja la señal de interrupción (SIGINT) para cerrar el programa de forma controlada.

    Cuando se detecta Ctrl+C, guarda el estado actual de los dispositivos
    y termina la ejecución del programa de forma segura.

    Args:
        sig (int): Número de la señal recibida.
        frame (frame object): Frame actual en el momento de la señal (pila de llamadas).

    Returns:
        None
    """
    print("Finalizando... Ctrl+C detectado")
    save_devices()
    sys.exit(0)

# Enviar mensaje al canal de Discord

async def respond_discord(message, response):
    """
    Envía una respuesta al mismo canal de Discord donde se recibió el mensaje del usuario.

    Args:
        message (discord.Message): El mensaje original recibido por el bot.
        response (str): El contenido de texto que se desea enviar como respuesta.

    Returns:
        None

    Exceptions:
        Captura cualquier excepción que ocurra al intentar enviar el mensaje
        y la imprime por consola.
    """
    try:
        await message.channel.send(response)
    except Exception as e:
        print("Error enviando mensaje Discord:", e)

# MQTT: Conexión

def on_connect(client, userdata, flags, rc):
    """
    Callback que se ejecuta cuando el cliente MQTT se conecta exitosamente al broker.

    Suscribe automáticamente al cliente a los topics relevantes del sistema domótico
    (sensores, switches y reloj). Muestra por consola si la conexión fue exitosa o fallida.

    Args:
        client (paho.mqtt.client.Client): Instancia del cliente MQTT conectado.
        userdata (any): Datos definidos por el usuario (no utilizados aquí).
        flags (dict): Flags de respuesta del broker MQTT.
        rc (int): Código de resultado de la conexión (0 indica éxito).

    Returns:
        None
    """
    if rc == 0:
        print("Conexión exitosa al broker MQTT.")
        topics = ["sensor_2", "switch_2", "watch_2"]
        for topic in topics:
            full_topic = f"redes2/2312/1/{topic}"
            client.subscribe(full_topic)
            print(f"Suscrito al topic: {full_topic}")
    else:
        print(f"Error de conexión al broker MQTT. Código de error: {rc}")


# MQTT: Mensaje recibido

def on_mqtt_message(client, userdata, msg):
    """
    Callback que se ejecuta cuando el cliente MQTT recibe un mensaje en un topic suscrito.

    Decodifica el mensaje recibido, lo almacena en una variable global para ser procesado
    posteriormente y activa una bandera que indica que se ha recibido un nuevo mensaje.

    Args:
        client (paho.mqtt.client.Client): Instancia del cliente MQTT que recibió el mensaje.
        userdata (any): Datos definidos por el usuario (no utilizados aquí).
        msg (paho.mqtt.client.MQTTMessage): Mensaje MQTT recibido, que incluye topic y payload.

    Returns:
        None
    """
    global latest_message, message_flag
    latest_message = msg.payload.decode("utf-8")
    print(f"Mensaje recibido:\n\tTopic: {msg.topic}\n\tContenido: {latest_message}")
    message_flag = 1

    if "sensor" in msg.topic:
        process_sensor_message(msg.topic, latest_message)

# Gestionar dispositivos

def save_devices():
    """
    Guarda el estado actual de los dispositivos en un archivo JSON.

    Serializa el diccionario global `device_data` y lo almacena en el archivo 'devices.json',
    permitiendo persistencia de datos entre ejecuciones del programa.

    Args:
        None

    Returns:
        None

    Exceptions:
        Captura cualquier excepción ocurrida durante la escritura del archivo
        y muestra un mensaje de error por consola.
    """
    try:
        with open("data/devices.json", "w") as f:
            json.dump(device_data, f, indent=4)
        print("Estado de dispositivos guardado correctamente en 'data/devices.json'.")
    except Exception as e:
        print("Error guardando dispositivos:", e)


def load_devices():
    """
    Carga el estado de los dispositivos desde un archivo JSON.

    Lee el archivo 'devices.json' y actualiza el diccionario global `device_data`
    con los datos almacenados. Si el archivo no existe o contiene errores,
    se imprime un mensaje de advertencia y se mantiene el estado por defecto.

    Args:
        None

    Returns:
        None

    Exceptions:
        Captura cualquier excepción durante la lectura o parseo del archivo
        y continúa la ejecución utilizando los valores iniciales por defecto.
    """
    global device_data
    try:
        with open("data/devices.json", "r") as f:
            new_data = json.load(f)
            device_data.clear()
            device_data.update(new_data)
        print("Dispositivos cargados correctamente desde 'data/devices.json'.")
    except Exception as e:
        print(f"No se pudo cargar 'devices.json'. Usando datos por defecto. Error: {e}")

def add_device(tipo):
    """
    Añade un nuevo dispositivo al sistema domótico.

    Incrementa el contador global de IDs, agrega un nuevo dispositivo del tipo especificado
    al diccionario `device_data`, y guarda el estado actualizado en el archivo 'devices.json'.

    Args:
        tipo (str): El tipo de dispositivo a añadir (por ejemplo, 'sensor', 'switch', 'watch').

    Returns:
        bool: True si el dispositivo añadido es de tipo 'switch', False en otro caso.
    """
    device_data["device_last_id"] += 1
    device_data["devices"][str(device_data["device_last_id"])] = tipo
    save_devices()
    return tipo == "switch"


def remove_device(device_id):
    """
    Elimina un dispositivo del sistema domótico según su ID.

    Busca y elimina el dispositivo correspondiente en el diccionario `device_data`
    usando el identificador proporcionado. Posteriormente guarda el estado actualizado
    en el archivo 'devices.json'. Si el ID no existe, no realiza ninguna acción.

    Args:
        device_id (str): ID del dispositivo que se desea eliminar.

    Returns:
        None
    """
    device_data["devices"].pop(device_id, None)
    save_devices()

def process_sensor_message(message):
    """
    Procesa el mensaje de un sensor para decidir si desencadena una acción.

    Args:
        message (str): Mensaje recibido del sensor (por ejemplo, una temperatura).

    Returns:
        str or None: Acción a realizar (por ejemplo, 'TOGGLE') o None si no aplica.
    """
    try:
        temp = float(message)
        if temp > 25:
            return "TOGGLE"
    except ValueError:
        pass
    return None


def publish_action(action, mqtt_client):
    """
    Publica una acción a realizar por un switch en el topic correspondiente.

    Args:
        action (str): Acción a realizar (por ejemplo, 'TOGGLE').
        mqtt_client (mqtt.Client): Cliente MQTT para enviar el mensaje.

    Returns:
        None
    """
    # Publicar a todos los switches
    for device_id, tipo in device_data["devices"].items():
        if tipo == "switch":
            mqtt_client.publish(f"redes2/2312/1/switch_{device_id}", action)

# Bot principal

def launch_bot(host, port):
    """
    Inicializa y lanza el bot de Discord y el cliente MQTT para el sistema domótico.

    Establece la conexión al broker MQTT y configura los eventos principales
    del bot de Discord para gestionar comandos de usuario relacionados con sensores,
    switches y dispositivos de reloj.

    Args:
        host (str): Dirección del broker MQTT.
        port (int): Puerto del broker MQTT.

    Funcionalidad:
        - Conexión al broker MQTT y suscripción a topics relevantes.
        - Carga y gestión del estado de los dispositivos (add, delete, list).
        - Interacción con usuarios vía comandos de Discord:
            * !sensor
            * !switch <id>
            * !watch
            * !add_device <tipo>
            * !del_device <id>
            * !devices
            * !help
        - Manejo seguro de interrupciones (Ctrl+C) para guardar estado antes de salir.

    Returns:
        None
    """
    # Obtener el token del bot de Discord desde el archivo de configuración
    TOKEN = get_token_from_file()

    # Crear los permisos necesarios para el bot (necesitamos leer mensajes)
    intents = discord.Intents.default()
    intents.message_content = True

    # Crear una instancia del bot de Discord con esos permisos
    bot = discord.Client(intents=intents)

    # Manejar Ctrl+C para guardar el estado antes de cerrar
    signal.signal(signal.SIGINT, signal_handler)
    
    # Cargar dispositivos previamente guardados desde devices.json
    load_devices()

    # Crear cliente MQTT para conectarse al broker
    mqtt_client = mqtt.Client()

    # Definir funciones callback para conexión y recepción de mensajes
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_mqtt_message
    # Conectarse al broker MQTT
    mqtt_client.connect(host, port, 60)
    # Empezar el bucle de escucha de MQTT en un hilo separado
    mqtt_client.loop_start()

    # Evento: cuando el bot de Discord está listo y conectado
    @bot.event
    async def on_ready():
        print(f"{bot.user} conectado a Discord")

    # Evento: cuando se recibe un mensaje en Discord
    @bot.event
    async def on_message(message):
        # Ignorar mensajes enviados por el propio bot
        if message.author == bot.user:
            return

        # Variables globales para manejar el mensaje recibido
        global latest_message, message_flag

        # Limpiar el mensaje recibido (eliminar espacios)
        content = message.content.strip()
        
        # Solo procesar mensajes que comienzan con '!'
        if not content.startswith("!"):
            return

        # Eliminar el primer carácter ('!') para procesar el comando
        command = content[1:]

        # Comando: mostrar dispositivos actuales
        if command == "devices":
            response = f"Dispositivos: {device_data['devices']}"
            #await: envislo al canal de Discord pero no quedar esperando
            await respond_discord(message, response)
        
        # Comando: añadir un nuevo dispositivo
        elif command.startswith("add_device"):
            try:
                _, tipo = command.split()
                if tipo in ("sensor", "switch", "watch"):
                    if add_device(tipo) and tipo == "switch":
                        mqtt_client.publish("redes2/2312/1/add_device", tipo)
                    await respond_discord(message, f"Dispositivo '{tipo}' añadido")
                else:
                    await respond_discord(message, "Tipo de dispositivo no válido")
            except:
                await respond_discord(message, "Uso: !add_device <tipo>")

        # Comando: eliminar un dispositivo por ID
        elif command.startswith("del_device"):
            try:
                _, device_id = command.split()
                if device_id in device_data["devices"]:
                    remove_device(device_id)
                    await respond_discord(message, f"Dispositivo {device_id} eliminado")
                else:
                    await respond_discord(message, "ID de dispositivo no válido")
            except:
                await respond_discord(message, "Uso: !del_device <id>")

        # Comando: activar/desactivar un switch por ID
        # por ejemplo !switch 2
        elif command.startswith("switch"):
            try:
                _, device_id = command.split()
                if device_id in device_data["devices"] and device_data["devices"][device_id] == "switch":
                    mqtt_client.publish(f"redes2/2312/1/switch_{device_id}", "TOGGLE")
                    while not message_flag:
                        pass
                    message_flag = 0
                    await respond_discord(message, latest_message)
                else:
                    await respond_discord(message, "ID de switch no válido.")
            except:
                await respond_discord(message, "Uso: !switch <id>")
                # Comando: pedir la temperatura de sensores
        elif command == "sensor":
            for device_id, device_type in device_data["devices"].items():
                if device_type == "sensor":
                    mqtt_client.publish(f"redes2/2312/1/sensor_{device_id}")
                    while not message_flag:
                        pass
                    message_flag = 0
                    await respond_discord(message, f"Sensor {device_id}: {latest_message}")
        # Comando: pedir la hora actual al reloj
        elif command == "watch":
            for device_id, device_type in device_data["devices"].items():
                if device_type == "watch":
                    mqtt_client.publish(f"redes2/2312/1/watch_{device_id}")
                    while not message_flag:
                        pass
                    message_flag = 0
                    await respond_discord(message, f"Reloj {device_id}: {latest_message}")
        # Comando: mostrar ayuda
        elif command == "help":
            help_msg = """```Comandos disponibles:
!sensor - Mostrar temperatura
!switch <id> - Activar switch
!watch - Mostrar hora
!add_device <tipo> - Añadir dispositivo (sensor/switch/watch)
!del_device <id> - Eliminar dispositivo
!devices - Listar dispositivos
!help - Mostrar ayuda```"""
            await respond_discord(message, help_msg)
        # Si el comando no se reconoce
        else:
            await respond_discord(message, "Comando no reconocido. Usa !help")
    # Arrancar el bot de Discord con el token
    bot.run(TOKEN)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Controlador Domótico")
    parser.add_argument('--host', default="redes2.ii.uam.es")
    parser.add_argument('--port', type=int, default=1883)
    args = parser.parse_args()
    launch_bot(args.host, args.port)