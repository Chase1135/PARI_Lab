#!/bin/bash
set -euo pipefail

# Load env variables
if [ -f .env ]; then
  export $(cat .env | xargs)
fi

echo "SERVER_HOST=$SERVER_HOST"
echo "SERVER_PORT=$SERVER_PORT"

# Start the Ollama server in the background
export OLLAMA_HOST=0.0.0.0:11434
ollama serve &

while ! nc -z 127.0.0.1 11434; do
  sleep 1
done

# Pull the model from model_params.json
config_file="llm/model_params.json"
model=$(python3 -c "import json; print(json.load(open('$config_file'))['model'])")

# Check if the model already exists
if ! ollama list | grep -q "$model"; then
  # Pull the model if it doesn't exist
  echo "Pulling model $model..."
  ollama pull "$model" || { echo "Error pulling model"; exit 1; }
else
  echo "Model $model already exists, skipping pull."
fi

# Start servers
uvicorn server:app --host 0.0.0.0 --port $SERVER_PORT