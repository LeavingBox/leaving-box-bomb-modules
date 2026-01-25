#!/usr/bin/env bash
PORT="${1:-rfc2217://localhost:4000}"; MPREMOTE="${MPREMOTE:-mpremote}"; command -v mpremote >/dev/null 2>&1 || MPREMOTE="python -m mpremote"
$MPREMOTE connect "port:$PORT" fs cp ../main.py :main.py
$MPREMOTE connect "port:$PORT" fs cp ../config.json :config.json
$MPREMOTE connect "port:$PORT" fs cp -r ../bomb_device :
# $MPREMOTE connect "port:$PORT" fs cp -r ../modules : 
