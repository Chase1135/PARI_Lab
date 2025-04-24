#!/bin/bash
set -euo pipefail

# Pull the model from model_params.json
config_file = "LLM/model_params.json"
model = $(
  python3 - <<EOF
import json
print(json.load(open("$config_file"))["model"])
EOF
)

# Start the Ollama server in the background
ollama serve &

sleep 3

# Check if the model already exists
if ! ollama list | grep -q "$model"; then
  # Pull the model if it doesn't exist
  ollama pull "$model"

  if [ $? -ne 0 ]; then
    echo "Error pulling the model"
    exit 1
  fi
else
  echo "Model $model already exists, skipping pull."
fi

# Start servers
uvicorn server:app --host 0.0.0.0 --port 5000 --ws-ping-interval 20 --ws-ping-timeout 40
