#!/bin/bash

# Start the Ollama server in the background
ollama serve &

#sleep 3

# Check if the model already exists
if ! ollama list | grep -q "llama3.2"; then
  # Pull the model if it doesn't exist
  ollama pull llama3.2

  if [ $? -ne 0 ]; then
    echo "Error pulling the model"
    exit 1
  fi
else
  echo "Model llama3.2 already exists, skipping pull."
fi

# Start servers
uvicorn server:app --host 0.0.0.0 --port 5000 --ws-ping-interval 20 --ws-ping-timeout 40
