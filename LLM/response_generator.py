import ollama
import json
from buffers import INBOUND_BUFFERS
from utils import Benchmark

# Load model parameters from JSON file
with open("LLM/model_params.json", "r") as model_params:
    config = json.load(model_params)

@Benchmark.time_execution
async def generate_response(**kwargs):
    # System prompt sent at start of conversation as a way to specify how the agent should respond
    system_message = config["messages"][0]["content"].format(**kwargs)

    # Append conversation history to the messages
    user_input = ''.join(INBOUND_BUFFERS['textual'])

    # Compose messages
    messages = [
        {'role': 'system', 'content': system_message},
        {'role': 'user', 'content': user_input}
    ]

    # Generate response
    response = ollama.chat(
        model=config["model"],
        messages=messages,
        options=config.get("options", {})
    )

    # Clear data buffers
    INBOUND_BUFFERS['textual'].clear()
    print(f"Prompt sent to model: {messages}", flush=True)

    return response['message']['content']
        