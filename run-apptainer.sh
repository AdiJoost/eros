#!/bin/bash

HOST_IP=$(ip route get 1 | awk '{print $7; exit}')

export OLLAMA_HOST="http://${HOST_IP}:11434"
export OPEN_AI_HOST="http://${HOST_IP}:11434/v1"

echo "Detected host IP: $HOST_IP"
echo "Using OLLAMA_HOST=$OLLAMA_HOST"
echo "Using OPEN_AI_HOST=$OPEN_AI_HOST"

set -e

# Create directories for persistent volumes
mkdir -p ./volumes/ollama-data
mkdir -p ./apptainerdata/psyche

sleep 5

echo "Starting Ollama..."
apptainer exec \
  --bind "$(pwd)/volumes/ollama-data:/root/.ollama" \
  --env OLLAMA_MODELS=/root/.ollama/models \
  --nv \
  ollama.sif \
  ollama serve > /dev/null &

OLLAMA_PID=$!

sleep 5

# Get absolute path to the Psyche directory (where this script is)
PSYCHE_DIR="$(cd "$(dirname "$0")"; pwd)"

echo "Starting Psyche..."
apptainer exec \
  --env ollama_host=$OLLAMA_HOST \
  --env open_ai_host=$OPEN_AI_HOST \
  --env-file "$PSYCHE_DIR/.env" \
  --bind "$PSYCHE_DIR:/psyche" \
  --pwd /psyche \
  psyche.sif \
  python run.py

echo "Shutting down Ollama..."
kill $OLLAMA_PID

wait $OLLAMA_PID 2>/dev/null || true

echo "Cleanup complete"