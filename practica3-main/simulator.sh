#!/bin/bash

echo "=== Lanzando simulador de integración ==="

# Ejecutables y configuración
CONTROLLER_CMD="python controller/controller.py --host localhost --port 1883"
DUMMY_SENSOR_CMD="python dummy_devices/dummy_sensor.py --host localhost --port 1883 --min 20 --max 30 --increment 1 --interval 1 1"
DUMMY_SWITCH_CMD="python dummy_devices/dummy_switch.py --host localhost --port 1883 --probability 0.0 1"
DUMMY_CLOCK_CMD="python dummy_devices/dummy_clock.py --host localhost --port 1883 --time 09:00:00 --increment 60 --rate 1 1"

# Lanzar controller
echo "Lanzando controller..."
$CONTROLLER_CMD &
CONTROLLER_PID=$!
sleep 2

# Lanzar dummies
echo "Lanzando sensor dummy..."
$DUMMY_SENSOR_CMD &
SENSOR_PID=$!

echo "Lanzando switch dummy..."
$DUMMY_SWITCH_CMD &
SWITCH_PID=$!

echo "Lanzando clock dummy..."
$DUMMY_CLOCK_CMD &
CLOCK_PID=$!

# Espera y test de interacción
sleep 5
echo "Simulando publicación MQTT al switch..."
mosquitto_pub -h localhost -p 1883 -t "redes2/2312/1/switch_1" -m "accion"

# Esperar a que se vean resultados
sleep 10

# Finalizar procesos
echo "Finalizando procesos..."
kill $SENSOR_PID $SWITCH_PID $CLOCK_PID $CONTROLLER_PID 2>/dev/null

echo "Simulación completada. Todos los procesos terminados."
