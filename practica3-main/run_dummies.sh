#!/bin/bash
export PYTHONWARNINGS="ignore::DeprecationWarning"

export PYTHONPATH=$(pwd)

#!/bin/bash

echo "Lanzando dummy devices en segundo plano..."

# PARA PRUEBAS EN LOCAL:
HOST="localhost"
PORT=1883

# PARA ENTREGA FINAL (usar esto en lugar de localhost):
# HOST="redes2.ii.uam.es"
# PORT=1883

# Dummy Sensor
python3 dummy_devices/dummy_sensor.py --host $HOST --port $PORT &
PID_SENSOR=$!
echo "dummy_sensor.py lanzado (PID: $PID_SENSOR)"

# Dummy Switch
python dummy_devices/dummy_switch.py --host localhost --port 1883 --probability 0.0 1 &

PID_SWITCH=$!
echo "dummy_switch.py lanzado (PID: $PID_SWITCH)"

# Dummy Clock
python3 dummy_devices/dummy_clock.py --host $HOST --port $PORT --time 12:00:00 --frequency 1 --rate 1 &
PID_CLOCK=$!
echo "dummy_clock.py lanzado (PID: $PID_CLOCK)"

echo ""
echo "Usa 'kill $PID_SENSOR $PID_SWITCH $PID_CLOCK' para detenerlos si lo necesitas."
