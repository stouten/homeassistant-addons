#!/bin/bash

# Read Home Assistant add-on configuration options from /data/options.json
OPTIONS_FILE=/data/options.json
CALIBRE_LIBRARY_PATH=$(jq -r '.calibre_library_path' "$OPTIONS_FILE")

# Ensure the Calibre library path exists
mkdir -p "$CALIBRE_LIBRARY_PATH"
echo "Using Calibre library path: $CALIBRE_LIBRARY_PATH"

# --- Handle Ingress Configuration ---
# HASS_INGRESS_PORT and HASS_BASE_PATH are set by Home Assistant when Ingress is enabled
# Default values if Ingress is not detected
CALIBRE_WEB_PORT=8083
CALIBRE_WEB_URL_PREFIX="/"

if [ -n "$HASS_INGRESS_PORT" ]; then
    echo "Ingress detected. Setting Calibre-Web port to $HASS_INGRESS_PORT and URL prefix to $HASS_BASE_PATH."
    CALIBRE_WEB_PORT="$HASS_INGRESS_PORT"
    CALIBRE_WEB_URL_PREFIX="$HASS_BASE_PATH"
else
    echo "Ingress not detected. Using default Calibre-Web port $CALIBRE_WEB_PORT and URL prefix $CALIBRE_WEB_URL_PREFIX."
fi

# Ensure the Calibre-Web configuration directory exists and is writable.
# This directory is mapped to /config/calibre-web on the Home Assistant host for persistence.
CALIBRE_WEB_CONFIG_DIR="/config/calibre-web"
mkdir -p "$CALIBRE_WEB_CONFIG_DIR"

# Also ensure the log file path is writable
CALIBRE_WEB_LOG_FILE="$CALIBRE_WEB_CONFIG_DIR/calibre-web.log"

# Navigate to the directory where the original Docker image placed its application files.
# Based on the original Dockerfile of crocodilestick/calibre-web-automated,
# the Calibre-Web-Automated repository is cloned into /app.
# Within that, the 'calibre-web' application itself is in /app/calibre-web-automated/calibre-web.
cd /app/calibre-web-automated || { echo "Error: /app/calibre-web-automated directory not found!"; exit 1; }

# Execute the Calibre-Web application with dynamic arguments.
# We are explicitly calling calibreweb.py and overriding the arguments from their default startup.sh.
# 'exec' ensures that this process runs as PID 1, allowing Home Assistant to correctly manage it.
exec python3 calibre-web/calibreweb.py \
    --config "$CALIBRE_WEB_CONFIG_DIR/config.py" \
    --port "$CALIBRE_WEB_PORT" \
    --url_prefix "$CALIBRE_WEB_URL_PREFIX" \
    --library_path "$CALIBRE_LIBRARY_PATH" \
    --enable-local-users \
    --enable-registration \
    --enable-log-file "$CALIBRE_WEB_LOG_FILE"