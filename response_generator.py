import ollama

async def generate_response(data):
    # Define an asynchronous generator to yield the streamed tokens
    async def async_generate():
        messages = [
            {'role': 'system', 'content': "You are an AI-powered research assistant. \
                                         Your task is to provide precise, factual, and well-researched responses. \
                                         Always answer in a clear and concise manner, \
                                         providing only accurate information."},
            {'role': 'user', 'content': data}
        ]
        response = ollama.chat(
            model='llama3.2',
            messages = messages,
            stream=True,
            temperature = 0,
            max_tokens = 150
        )
        async for token in response:  # Streaming the tokens as they are received
            print(f"Generated token: {token['message']['content']}", flush=True)
            yield token['message']['content']  # Yield the token as it is generated

    # Call the async generator and yield the tokens to the caller
    async for token in async_generate():
        yield token