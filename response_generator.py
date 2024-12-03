import ollama
import asyncio

async def generate_response(data):
    def sync_generate():
        response = ollama.chat(
            model='llama3.2',
            messages=[{'role': 'user', 'content': data}],
            stream=True
        )
        for token in response:
            print(f"Generated token: {token}", flush=True)
            yield token

    # Wrap synchronous generator into asynchronous one
    for token in await asyncio.to_thread(list, sync_generate()):
        yield token
