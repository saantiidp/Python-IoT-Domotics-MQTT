from unittest.mock import patch, MagicMock
import sys
import subprocess

def test_connects_to_broker():
    result = subprocess.run(
        [sys.executable, "dummy_devices/dummy_sensor.py", "--host", "localhost", "--test-once", "99"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=5
    )
    assert result.returncode == 0

def test_connection_failure():
    result = subprocess.run(
        [sys.executable, "dummy_devices/dummy_sensor.py", "--host", "invalid_broker", "99"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=5
    )
    assert result.returncode != 0

def test_trigger_rules_on_sensor_message():
    import controller.controller as ctrl

    ctrl.device_data["4"] = "sensor"

    with patch("controller.controller.process_sensor_message") as mock:
        msg = MagicMock()
        msg.topic = "redes2/2312/1/sensor_4"
        msg.payload = b"25"
        ctrl.on_mqtt_message(None, None, msg)
        mock.assert_called_once_with("redes2/2312/1/sensor_4", "25")

def test_perform_action_on_rule_result():
    import controller.controller as ctrl
    ctrl.mqtt_client = MagicMock()
    ctrl.device_data["1"] = "switch"
    ctrl.publish_action("ON", ctrl.mqtt_client)
    ctrl.mqtt_client.publish.assert_called_once_with("redes2/2312/1/switch_2", "ON")


def test_loads_devices_from_json(tmp_path):
    import controller.controller as ctrl
    fake_json = tmp_path / "devices.json"
    fake_json.write_text('{"device_last_id": 1, "devices": {"1": "sensor"}}')
    ctrl.device_data.clear()

    with patch("controller.controller.DEVICES_FILE", str(fake_json)):
        ctrl.load_devices()
    assert ctrl.device_data["devices"]["1"] == "sensor"
