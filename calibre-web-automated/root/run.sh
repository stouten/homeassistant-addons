#!/bin/bash

# Read Home Assistant add-on configuration options from /data/options.json
OPTIONS_FILE=/data/options.json
CALIBRE_LIBRARY_PATH=$(jq -r '.calibre_library_path' "$OPTIONS_FILE")

# Ensure the Calibre library path exists
mkdir -p "$CALIBRE_LIBRARY_PATH"
echo "Using Calibre library path: $CALIBRE_LIBRARY_PATH"

# CWA needs these environment variables
export PUID=1000
export PGID=1000
export TZ=UTC

# Create required directories
mkdir -p /config/calibre-web
mkdir -p /config/processed_books
mkdir -p /config/cwa-book-ingest

# Set the library path for CWA
export CALIBRE_LIBRARY_PATH="$CALIBRE_LIBRARY_PATH"

# Start Calibre Web Automated using its own startup script
cd /app/calibre-web-automated || { echo "Error: CWA directory not found!"; exit 1; }

# Execute the original CWA startup
exec /app/calibre-web-automated/startup.sh
