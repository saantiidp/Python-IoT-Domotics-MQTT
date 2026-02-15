# Python-IoT-Domotics-MQTT

Sistema **domótico distribuido en Python** basado en **MQTT**, con dispositivos simulados (sensores, interruptores y relojes), un controlador central, motor de reglas, persistencia en JSON y pruebas automáticas.

> Proyecto académico de Redes y Comunicaciones II (UAM). Para la explicación técnica completa, consulta `memoria.md`.

---

## 🚀 Descripción general

Este proyecto implementa un **sistema de automatización del hogar** usando el modelo **publicación/suscripción** con MQTT.  
Todos los dispositivos son **simulados (dummies)**, lo que permite probar el sistema completo **sin hardware real**.

El sistema incluye:

- 🧠 Un **controlador central** que:
  - Se suscribe a los topics de los dispositivos
  - Aplica reglas
  - Persiste el estado en ficheros JSON
- 🔌 **Dispositivos simulados**:
  - Interruptores (switches)
  - Sensores
  - Relojes (clocks/watches)
- 📡 Comunicación mediante **MQTT (broker Mosquitto)**
- 💾 **Persistencia** en JSON
- 🧪 **Tests unitarios e integración** con `pytest` / `unittest`
- ⚙️ Scripts de shell para lanzar simulaciones y pruebas automáticamente

---

## 🏗️ Arquitectura (alto nivel)

- Cada dispositivo se ejecuta como un **proceso independiente** y se conecta al broker MQTT.
- Los dispositivos **publican eventos** y **se suscriben a comandos** en sus propios topics.
- El **controller**:
  - Escucha los eventos de todos los dispositivos
  - Evalúa reglas
  - Envía comandos de vuelta
  - Guarda y restaura el estado desde disco
- La comunicación es **asíncrona y desacoplada** gracias a MQTT.

Para una explicación detallada del diseño y las decisiones de implementación, consulta **`memoria.md`**.

---

## 📁 Estructura del proyecto (simplificada)

```
.
├── controller.py
├── device.py
├── switch.py
├── sensor.py
├── watch.py
├── dummy_devices/
│   ├── dummy_switch.py
│   ├── dummy_sensor.py
│   └── dummy_clock.py
├── data/
│   ├── switches.json
│   ├── sensors.json
│   ├── clocks.json
│   └── devices.json
├── tests/
├── run_all.sh
├── simulator.sh
├── requirements.txt
├── README.md
└── memoria.md
```

---

## ▶️ Cómo ejecutar

### 1️⃣ Crear y activar entorno virtual

```bash
python3 -m venv redesp3
source redesp3/bin/activate
```

### 2️⃣ Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3️⃣ Ejecutar simulación completa + tests

```bash
./run_all.sh
```

### 4️⃣ Ejecutar simulación interactiva

```bash
./simulator.sh
```

---

## 🔧 Ejecutar dispositivos manualmente

Ejemplos:

```bash
# Interruptor
python dummy_devices/dummy_switch.py --host localhost --port 1883 --probability 0.3 1

# Sensor
python dummy_devices/dummy_sensor.py --host localhost --port 1883 --min 20 --max 30 --increment 1 --interval 1 2

# Reloj
python dummy_devices/dummy_clock.py --host localhost --port 1883 --time 09:00:00 --increment 60 --rate 1 3
```

---

## 📄 Documentación

- 📘 **Memoria técnica completa:** ver `memoria.md`
- Incluye:
  - Diseño detallado
  - Arquitectura
  - Modelo distribuido
  - Persistencia
  - Motor de reglas
  - Estrategia de pruebas
  - Conclusiones

---

## 🛠️ Tecnologías

- Python 3
- MQTT (Mosquitto)
- paho-mqtt
- pytest / unittest
- Persistencia en JSON
- Bash

---

## 👤 Autor

**Santiago de Prada Lorenzo**  
Universidad Autónoma de Madrid — Redes y Comunicaciones II

---

## 📜 Licencia

MIT (o la licencia académica que prefieras)
