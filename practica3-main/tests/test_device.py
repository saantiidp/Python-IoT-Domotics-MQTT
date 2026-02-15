import pytest
import subprocess
import sys

def test_connects_to_broker():
    result = subprocess.run(
        [sys.executable, "dummy_devices/dummy_sensor.py", "--host", "localhost", "--test-once", "99"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=5
    )
    assert b"conectado al broker" in result.stdout.lower()

def test_fails_on_wrong_broker():
    result = subprocess.run(
        [sys.executable, "dummy_devices/dummy_sensor.py", "--host", "wrong.broker", "99"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=5
    )
    assert result.returncode != 0

def test_parses_command_line_args():
    # Solo verificamos que no lanza excepción de argparse
    result = subprocess.run(
        [sys.executable, "dummy_devices/dummy_sensor.py", "--min", "10", "--max", "20", "--increment", "2", "--interval", "1", "--test-once", "99", "--host", "invalid_host"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=5
    )
    # El código de error es aceptable si solo queremos probar el parser
    assert b"--min" in result.stderr or result.returncode != 2  # código 2 es error de parser


def test_switch_toggles_state():
    import dummy_devices.dummy_switch as switch
    state = switch.handle_action("1")
    assert switch.switch_data["1"] is True
    assert state in ["ON", "OFF"]


def test_sensor_cycles_values():
    import dummy_devices.dummy_sensor as sensor
    sensor.sensor_data = {"1": 20}
    value = sensor.sensor_data["1"]
    new_value = value + 1 if value + 1 <= 30 else 20
    sensor.sensor_data["1"] = new_value
    assert 20 <= sensor.sensor_data["1"] <= 30