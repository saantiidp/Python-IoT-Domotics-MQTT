[](url)## MEMORIA PRÁCTICA 3 REDES 2
## Santiago de Prada Lorenzo
## 3º Ingeniería Informática, Redes y Comunicaciones 2 UAM

### Índice
* [Introducción](#introducción)
* [Desarrollo de Diseño](#desarrollo-de-diseño)
* [Desarrollo Técnico](#desarrollo-técnico)
* [Arquitectura](#arquitectura)
* [Diseño Distribuido](#diseño-distribuido)
* [Uso](#uso)
* [Configuración](#configuración)
* [Compilación y Ejecución](#compilación-y-ejecución)
* [Conclusiones](#conclusiones)
* [Comandos para crearte entorno virtual python3](#comandos-para-crearte-entorno-virtual-python3)

### Introducción
El objetivo de la práctica es diseñar e implementar un sistema domótico distribuido que permita simular y gestionar dispositivos IoT a través del protocolo MQTT. Aunque se trata de una solución simplificada, el sistema debe ser completamente funcional, manejando adecuadamente tanto la recepción como el envío de mensajes entre los distintos componentes. Para ello, se han desarrollado simuladores de sensores, relojes e interruptores que publican y responden a eventos en tiempo real, así como un controlador central encargado de aplicar reglas y coordinar las acciones. Al finalizar la práctica, el sistema debe ser capaz de ejecutarse de forma automática mediante scripts de prueba y simulación, y demostrar su correcto funcionamiento mediante pruebas unitarias y de integración.

Un sistema domótico distribuido con MQTT es una arquitectura que permite conectar y coordinar distintos dispositivos inteligentes en el hogar, como sensores, interruptores o relojes, mediante un canal de mensajería ligero y asíncrono. Usando el protocolo MQTT, los dispositivos pueden comunicar eventos y recibir órdenes de forma eficiente, lo que permite automatizar acciones según reglas definidas por el usuario.

En este documento se describe el diseño e implementación de un sistema domótico simulado en Python, compuesto por un conjunto de dispositivos dummy, un controlador central y una lógica de reglas. Se detallan las clases y scripts desarrollados, la comunicación mediante topics MQTT, el manejo de persistencia y la ejecución de pruebas automáticas. Además, se presentan los desafíos encontrados durante el desarrollo, las decisiones tomadas en el diseño, y los resultados obtenidos con los scripts de simulación e integración.

### Desarrollo de Diseño
Para el desarrollo del sistema domótico hemos trabajado sobre un entorno Linux Ubuntu, utilizando como editor principal Visual Studio Code, aprovechando extensiones como Live Share para trabajo colaborativo. El proyecto ha sido implementado en Python 3.11, utilizando el entorno virtual venv para gestionar dependencias como paho-mqtt y pytest.

El sistema se compone de múltiples módulos que simulan dispositivos IoT (interruptores, sensores y relojes), un controlador central (controller.py) encargado de recibir los mensajes MQTT, persistir el estado de los dispositivos y gestionar las reglas definidas, y un conjunto de scripts de simulación (run_all.sh y simulator.sh) que permiten lanzar todos los componentes y validar el comportamiento global.

Durante el desarrollo:

Hemos estructurado el proyecto separando claramente los dispositivos simulados (en dummy_devices/) de las clases base (device.py) y sus especializaciones (switch.py, sensor.py, watch.py).

Los dummies implementan una simulación autónoma del comportamiento de dispositivos reales: se conectan a un broker MQTT, publican o reaccionan a eventos, y permiten comprobar si el sistema funciona sin hardware real.

Los devices representan la estructura lógica interna del sistema: clases orientadas a objetos que definen cómo un Switch, Sensor o Clock debe comportarse en el controlador.

La persistencia se realiza en ficheros JSON (data/*.json) para mantener el estado entre ejecuciones.

Se ha añadido soporte para ejecutar pruebas automáticas con pytest y unittest, incluidas en tests/, abarcando tanto la conectividad, como el procesamiento de eventos y reglas.

Se han gestionado correctamente las señales de interrupción (SIGINT) para garantizar que el estado de los dispositivos simulados se guarda al finalizar el sistema.

En los scripts de ejecución se han definido opciones para facilitar el despliegue y pruebas integradas del sistema, incluyendo ejecución paralela de dispositivos simulados y pruebas automatizadas.

Esta arquitectura modular nos ha permitido desarrollar, probar y validar cada componente de manera independiente y luego integrarlos en un entorno controlado y reproducible.

### Desarrollo Técnico
### Arquitectura
Para la realización de esta práctica hemos desarrollado un sistema domótico distribuido basado en dispositivos IoT simulados que se comunican mediante el protocolo MQTT. El sistema está compuesto por tres tipos de dispositivos: interruptores (switches), sensores y relojes (clocks), todos implementados como procesos independientes. Cada uno de estos dispositivos publica o responde a eventos en topics específicos del broker Mosquitto, siguiendo la estructura definida por la práctica (redes2/GRUPO/PAREJA/ID).

El núcleo del sistema es el controller, que suscribe los topics correspondientes, escucha los eventos publicados y decide las acciones a realizar. Este controlador es también el encargado de invocar al motor de reglas, comprobar si se deben disparar acciones y persistir el estado de los dispositivos en ficheros JSON.

Además, para facilitar las pruebas y el desarrollo, se ha desarrollado un conjunto de dummies (simuladores) que emulan el comportamiento de los dispositivos reales. Estos se pueden lanzar fácilmente mediante scripts de shell como run_all.sh o simulator.sh, y permiten verificar el comportamiento completo del sistema sin necesidad de hardware real.

### Diseño Distribuido
El sistema ha sido diseñado como un conjunto de procesos independientes que se comunican mediante MQTT de forma asíncrona. Esta arquitectura permite ejecutar cada componente por separado y facilita el desarrollo modular.

Cada dispositivo dummy es autónomo y mantiene su propio estado en ficheros (switches.json, sensors.json, etc.). El controller puede ejecutarse con distintos ficheros de configuración y reglas, lo que facilita la extensibilidad y el testing.

La persistencia de dispositivos se ha gestionado usando ficheros JSON y clases Device, Switch, Sensor y Watch, lo que permite cargar la configuración al iniciar el sistema y actualizarla dinámicamente.

Se ha implementado control de interrupciones (SIGINT) para que los dispositivos puedan guardar su estado al finalizar, garantizando que el entorno sea reproducible en sucesivas ejecuciones.

### Uso
El sistema puede lanzarse mediante los siguientes scripts:

run_all.sh: ejecuta los dummies (interruptores, sensores, relojes) y luego corre los tests de integración.

simulator.sh: lanza el entorno completo (controller y dispositivos) y simula publicaciones MQTT para comprobar el sistema en funcionamiento.

Los dispositivos pueden también lanzarse individualmente con los siguientes comandos:

# Interruptor
python dummy_devices/dummy_switch.py --host localhost --port 1883 --probability 0.3 1

# Sensor
python dummy_devices/dummy_sensor.py --host localhost --port 1883 --min 20 --max 30 --increment 1 --interval 1 2

# Reloj
python dummy_devices/dummy_clock.py --host localhost --port 1883 --time 09:00:00 --increment 60 --rate 1 3

### Configuración
Los dispositivos leen y escriben su estado en ficheros bajo el directorio data/, lo que les permite recuperar su estado entre ejecuciones. Ejemplos:

data/switches.json

data/sensors.json

data/clocks.json

data/devices.json (gestión global por el controller)

Los topics MQTT utilizados por los dispositivos siguen el patrón:

redes2/2312/1/switch_1
redes2/2312/1/sensor_1
redes2/2312/1/watch_1

### Compilación y Ejecución
No es necesaria compilación, ya que todo el sistema está implementado en Python. Para ejecutar el sistema completo con pruebas:

./run_all.sh

Para simular el sistema en entorno real con el controller y observar su comportamiento en tiempo real:

./simulator.sh

Los tests incluidos validan tanto la funcionalidad de los dispositivos individuales como el comportamiento global del sistema al recibir eventos y aplicar reglas.

### Conclusiones
En este documento se ha descrito el diseño e implementación de un sistema domótico distribuido basado en dispositivos IoT simulados y comunicación mediante el protocolo MQTT. Aunque los dispositivos desarrollados (sensores, interruptores y relojes) son simulaciones (dummies), su funcionamiento reproduce fielmente el comportamiento de dispositivos reales conectados en un entorno domótico.

El sistema ha sido desarrollado íntegramente en Python y ejecutado sobre Linux Ubuntu, lo que ha facilitado la depuración y automatización de pruebas con herramientas como pytest y unittest. Para la persistencia de estados, se han utilizado ficheros JSON, y la estructura modular del sistema ha permitido extenderlo y probarlo fácilmente.

A nivel de arquitectura, el uso de MQTT ha permitido una comunicación asíncrona y desacoplada entre los componentes del sistema. En este esquema:

Los devices son clientes MQTT que se suscriben a su propio topic (una especie de cola).

El controller actúa como coordinador, escuchando eventos, procesando reglas y tomando decisiones sobre los dispositivos.

Los dispositivos se modelan como clases que heredan de una clase abstracta Device, permitiendo un diseño extensible y reutilizable.

La lógica del Rule Engine se encuentra embebida en el controller, lo que simplifica la arquitectura para esta práctica sin necesidad de dividir procesos adicionales. Las reglas del tipo "si temperatura > 25, enciende ventilador" pueden ser configuradas y se ejecutan automáticamente en respuesta a eventos.

En cuanto al desarrollo, se ha trabajado con scripts de automatización (run_all.sh, simulator.sh) que permiten lanzar todos los actores del sistema de forma controlada. Asimismo, se han implementado tests exhaustivos que cubren tanto el comportamiento individual de los dispositivos como la interacción entre ellos a través del broker.

Desde el punto de vista del aprendizaje, la práctica ha sido una excelente introducción a los sistemas distribuidos, a la comunicación asíncrona basada en publicación/suscripción, y a la organización modular del código. También ha servido para consolidar habilidades en pruebas, depuración y documentación de sistemas complejos.

En resumen, este proyecto ha permitido simular un entorno IoT completo y funcional, entendiendo los principios de diseño detrás de una red domótica moderna. Hemos podido experimentar con conceptos clave como la persistencia ligera, el uso de topics MQTT, la simulación de eventos y el procesamiento de reglas. Esto ha facilitado una comprensión práctica de cómo se construyen sistemas IoT reales con una arquitectura modular, reactiva y mantenible.

### Comandos para crearte entorno virtual python3
1. Crear entorno virtual
   ```bash
   python3 -m venv redesp3

2. Activar entorno virtual (Dentro del directorio donde has creado el entorno)
   ```bash
   source redesp3/bin/activate

3. Instalar requirements.txt
   ```bash
   cd practica3
   pip install -r requirements.txt

4. Desactivar entorno virtual
   ```bash
   deactivate
