#!/bin/bash
set -e

# Read configuration
CONFIG_PATH=/data/options.json
CALIBRE_LIBRARY_PATH=$(jq -r '.calibre_library_path' "$CONFIG_PATH")
BOOK_INGEST_PATH=$(jq -r '.book_ingest_path' "$CONFIG_PATH")

# Create required directories
mkdir -p "$CALIBRE_LIBRARY_PATH"
mkdir -p "$BOOK_INGEST_PATH"

echo "Calibre library path: $CALIBRE_LIBRARY_PATH"
echo "Book ingest path: $BOOK_INGEST_PATH"

# Set environment variables for the container
export PUID=1000
export PGID=1000
export TZ=Europe/Amsterdam

# The Docker image has its own entrypoint, so we don't need to start anything manually
# Just let the container run as intended
echo "Starting Calibre Web Automated..."
exec "$@"
