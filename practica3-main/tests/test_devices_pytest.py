import pytest
import json
import os
from controller.controller import add_device, remove_device, save_devices, load_devices, device_data

@pytest.fixture(autouse=True)
def reset_device_data():
    """Restaura el estado base antes de cada test."""
    device_data.clear()
    device_data.update({"device_last_id": 1, "devices": {"1": "sensor"}})

def test_add_device_updates_structure():
    """Verifica que añadir un switch crea el dispositivo correctamente."""
    result = add_device("switch")
    assert result is True
    assert "2" in device_data["devices"]
    assert device_data["devices"]["2"] == "switch"

def test_remove_device_deletes_entry():
    """Verifica que eliminar un dispositivo borra su ID."""
    add_device("watch")
    remove_device("2")
    assert "2" not in device_data["devices"]

def test_save_devices_creates_file(tmp_path):
    """Verifica que save_devices guarda en data/devices.json."""
    # Asegurar carpeta data existe
    os.makedirs("data", exist_ok=True)
    save_devices()
    path = "data/devices.json"
    assert os.path.exists(path)
    with open(path, "r") as f:
        data = json.load(f)
        assert data["devices"]["1"] == "sensor"

def test_load_devices_reads_file(tmp_path):
    """Verifica que load_devices carga correctamente desde data/devices.json."""
    os.makedirs("data", exist_ok=True)
    fake_data = {"device_last_id": 3, "devices": {"3": "watch"}}
    with open("data/devices.json", "w") as f:
        json.dump(fake_data, f)

    device_data.clear()  #LIMPIAR antes de cargar
    load_devices()
    assert "3" in device_data["devices"]
    assert device_data["devices"]["3"] == "watch"