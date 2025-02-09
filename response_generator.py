import ollama

async def generate_response(data):

    messages = [
        {'role': 'system', 'content': "You are an AI-powered research assistant. \
                                        Your task is to provide precise, factual, and well-researched responses. \
                                        Always answer in a clear and concise manner, \
                                        providing only accurate information."},
        {'role': 'user', 'content': data}
    ]
    response = ollama.chat(
        model='llama3.2',
        messages = messages
        #temperature = 0,
        #max_tokens = 150
    )

    return response['message']['content']

    