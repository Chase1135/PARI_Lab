import ollama
import json
import base64
from io import BytesIO
from PIL import Image
from data.buffers import INBOUND_BUFFERS
from utils.utils import Benchmark

# Load model parameters from JSON file
with open("llm/model_params.json", "r") as model_params:
    config = json.load(model_params)

@Benchmark.time_execution
async def generate_response(**kwargs):
    # System prompt sent at start of conversation as a way to specify how the agent should respond
    system_message = config["messages"][0]["content"].format(**kwargs)

    # Append conversation history to the messages
    user_input = ''.join(INBOUND_BUFFERS['textual'])

    image_bytes = None
    if INBOUND_BUFFERS['visual']:
        visual_data = INBOUND_BUFFERS['visual'][0]
        image = Image.fromarray(visual_data, mode="RGB")

        buffer = BytesIO()
        image.save(buffer, format="JPEG")
        image_bytes = buffer.getvalue()

    # Compose messages
    messages = [
        {'role': 'system', 'content': system_message},
        {
            'role': 'user',
            'content': user_input,
            'images': [image_bytes] if image_bytes else None
        }
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