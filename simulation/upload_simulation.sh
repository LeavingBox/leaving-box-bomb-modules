#!/usr/bin/env bash
echo "Make sure the simulator is fresh & reset..."
echo "Installing required packages..."
mpremote mip install aioble

echo "Uploading updated files..."
PORT="${1:-rfc2217://localhost:4000}"; MPREMOTE="${MPREMOTE:-mpremote}"; command -v mpremote >/dev/null 2>&1 || MPREMOTE="python -m mpremote"
$MPREMOTE connect "port:COM4" fs cp ../main.py :main.py
$MPREMOTE connect "port:COM4" fs cp ../config.json :config.json
$MPREMOTE connect "port:COM4" fs cp -r ../bomb_device :
# $MPREMOTE connect "port:$PORT" fs cp -r ../modules : 
