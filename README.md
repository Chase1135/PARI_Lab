# AI Metahuman Research Toolset

This repository contains the source code and tools for an AI-powered Metahuman research system. The system provides a modular, plug-and-play infrastructure enabling researchers to explore human-like cognitive functionalities within a realistic virtual human environment powered by Unreal Engine 5.

## Project Overview

The core of this project is a Docker-hosted Python backend system integrated with Unreal Engine 5's Metahuman model. Users interact with the virtual human via textual or voice inputs, and the system processes these interactions using:

- **Large Language Model (LLM)**: Ollama LLM generates realistic, contextually relevant textual responses.
- **Text-to-Speech (TTS)**: Responses are converted into audio for realistic Metahuman speech interactions.

## Key Features

- **Modularity**: Easily extensible to integrate additional cognitive mechanisms or processing pipelines.
- **Real-time Interaction**: Realistic interaction facilitated through communication between frontend and backend.
- **Data Capture**: Records textual, audio, visual, and physical inputs from interactions for extensive research possibilities.

## Project Structure

- **`server.py`**: Core FastAPI server managing REST and WebSocket communication between the frontend (Unreal Engine) and backend.
- **`processors.py`**: Defines default and custom data processing classes for different data modalities (textual, audio, visual, physical).
- **`response_generator.py`**: Manages interactions with Ollama LLM to generate textual responses.
- **`model_params.json`**: Configuration parameters for the LLM.
- **`PlayHT.py`**: Implements Text-to-Speech capabilities using PlayHT API.
- **`buffers.py`**: Provides data buffers for inbound and outbound communication.
- **`mongodb.py`**: Example MongoDB integration for logging interaction data.
- **`start_servers.sh`**: Script to launch backend services, including the Ollama server and FastAPI server.

## Requirements
To install the necessary dependencies:
```bash
pip install -r requirements.txt
```

## Example Interaction
- **Textual Input**: Users submit prompts through the frontend interface in Unreal Engine 5.
- **Backend Processing**: The backend generates LLM-based textual responses and converts them into audio.
- **Metahuman Output**: Audio is streamed back to the frontend, where the virtual Metahuman speaks the generated responses.

## Future Integrations
- Integration of cognitive modules to give the Metahuman "consciousness".

## HOW TO RUN WITHIN DOCKER DESKTOP:
1. Open Docker terminal
2. Pull Docker image ('docker pull chasea1135/pari_lab_server:latest')
3. Run container ('docker run -p 5000:5000 chasea1135/pari_lab_server:latest') OR click run on downloaded image
4. If run from images tab, enter port # (5000)

RUNNING LOCALLY:
1. Clone repository, install necessary dependencies (pydantic, fastapi, uvicorn, websockets, ollama)
2. Open docker terminal, navigate to project folder
3. Type 'docker-compose up --build' in terminal

TO TEST:
1. Run test_connection.py (type exit to close connection)
