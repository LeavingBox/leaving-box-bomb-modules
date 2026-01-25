# leaving-box-bomb-modules

## Virtual env
It's recommended to use a virtual environment to manage dependencies.
Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

## Run the main.py bridge

From the repository root:

```bash
python main.py
```

## ESP32 helpers

See `bomb_device/README.md` for MicroPython provisioning (HTTP or BLE) and the
ESP-NOW main controller loop.


## Simulation
See `simulation/README.md` for running the simulation environment using Wokwi.
