echo "Resetting the device..."
mpremote reset

sleep 2  # Wait for the device to reset
mpremote run ./cleanup.py

echo "Installing required packages..."
mpremote mip install aioble

echo "Uploading updated files..."
mpremote fs cp ./main.py :main.py
mpremote fs cp ./config.json :config.json
mpremote fs cp -r ./bomb_device :

echo "Files after upload:"
mpremote ls

echo "Connecting to device shell..."
mpremote
# mpremote fs cp -r ./modules : 