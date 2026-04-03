#!/bin/bash

set -e

# Create directories for persistent volumes
mkdir -p ./volumes/ollama-data
mkdir -p ./apptainerdata/psyche

# Convert docker images to SIF files (if not already done)
echo "Pulling and converting Docker images to SIF..."

# Disable cache explicitly for each build
echo "Building Ollama image..."
SINGULARITY_DISABLE_CACHE=True apptainer build --force ollama.sif docker://ollama/ollama

echo "Building psyche image..."
SINGULARITY_DISABLE_CACHE=True apptainer build --force psyche.sif docker://adijida/psyche:latest