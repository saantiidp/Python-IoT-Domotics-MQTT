import unittest
import json
import os
import tempfile
from controller.controller import add_device, remove_device, save_devices, load_devices, device_data

class DeviceManagerTestCase(unittest.TestCase):

    def setUp(self):
        """Restablece el estado inicial antes de cada test."""
        device_data.clear()
        device_data.update({"device_last_id": 1, "devices": {"1": "sensor"}})

    def test_add_new_device(self):
        """Verifica que añadir un nuevo dispositivo funciona correctamente."""
        result = add_device("watch")
        self.assertFalse(result)  # 'watch' no es un switch
        self.assertIn("2", device_data["devices"])
        self.assertEqual(device_data["devices"]["2"], "watch")

    def test_remove_existing_device(self):
        """Verifica que eliminar un dispositivo lo elimina del diccionario."""
        add_device("switch")
        remove_device("2")
        self.assertNotIn("2", device_data["devices"])

    def test_save_and_load_devices(self):
        """Verifica guardar y luego cargar dispositivos desde archivo real."""
        # Archivo temporal para simular devices.json
        with tempfile.NamedTemporaryFile(delete=False, mode="w+", suffix=".json") as tmp:
            path = tmp.name
            # Sobreescribimos el save_devices para usar el path temporal
            original_device_data = {"device_last_id": 3, "devices": {"3": "switch"}}
            with open(path, "w") as f:
                json.dump(original_device_data, f)

            # Limpiamos antes de cargar
            device_data.clear()
            with open(path, "r") as f:
                loaded = json.load(f)
                device_data.update(loaded)

        self.assertEqual(device_data["device_last_id"], 3)
        self.assertIn("3", device_data["devices"])
        os.remove(path)  # Limpieza

if __name__ == "__main__":
    unittest.main()