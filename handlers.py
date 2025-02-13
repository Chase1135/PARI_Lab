from response_generator import DATA_BUFFERS

# DEFAULT MODALITY HANDLERS
def handle_textual(data):
    print("DEFAULT TEXTUAL HANDLER TRIGGERED")
    print(f"Data received: {data}", flush=True)
    DATA_BUFFERS["textual"].append(data)
    pass

def handle_audio(data):
    print("DEFAULT AUDIO HANDLER TRIGGERED")
    print(f"Data received: {data}", flush=True)
    DATA_BUFFERS["audio"].append(data)
    pass

def handle_visual(data):
    print("DEFAULT VISUAL HANDLER TRIGGERED")
    print(f"Data received: {data}", flush=True)
    DATA_BUFFERS["visual"].append(data)
    pass

def handle_physical(data):
    print("DEFAULT PHYSICAL HANDLER TRIGGERED")
    print(f"Data received: {data}", flush=True)
    DATA_BUFFERS["physical"].append(data)
    pass

DEFAULT_INPUTS = [
    {"name": "text_input", "modality": "textual", "chunked": False},
    {"name": "user_speech", "modality": "audio", "chunked": True},
    {"name": "eyes", "modality": "visual", "chunked": True},
    {"name": "touch", "modality": "physical", "chunked": True}
]

DEFAULT_HANDLERS = {
    "textual": handle_textual,
    "audio": handle_audio,
    "visual": handle_visual,
    "physical": handle_physical
}