#!/bin/bash

echo "Ejecutando entorno completo: Dummies + Tests..."

# 1. Lanzar los dummy devices con argumentos correctos
python3 dummy_devices/dummy_sensor.py --host localhost --port 1883 --min 20 --max 30 --increment 1 --interval 1 1 &
python3 dummy_devices/dummy_switch.py --host localhost --port 1883 --probability 0.3 1 &
python3 dummy_devices/dummy_clock.py --host localhost --port 1883 --time 09:00:00 --increment 60 --rate 1 1 &
PID_DUMMIES=$!
echo "Dummies lanzados en segundo plano (PID del proceso del script: $PID_DUMMIES)"

# 2. Esperar unos segundos para que los dispositivos se conecten
echo "Esperando 3 segundos para que los dummies se conecten al broker..."
sleep 3

# 3. Ejecutar los tests completos
echo "Ejecutando tests unitarios y de integración..."
./run_tests.sh

# 4. Preguntar si quieres detener los dummies al terminar
echo ""
read -p "¿Quieres detener los dummies ahora? (s/n): " RESPUESTA

if [ "$RESPUESTA" = "s" ]; then
    echo "Deteniendo procesos de dummies..."
    pkill -f dummy_sensor.py
    pkill -f dummy_switch.py
    pkill -f dummy_clock.py
    echo "Dummies detenidos."
else
    echo "Dummies siguen ejecutándose. Recuerda que puedes matarlos manualmente con 'kill' si quieres."
fi

echo "Finalizado."
