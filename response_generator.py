import ollama

MAX_HISTORY_LENGTH = 10

DATA_BUFFERS = {
    "textual": [],
    "audio": [],
    "visual": [],
    "physical": []
}
conversation_history = []

async def generate_response():
    print(f"Data buffer before response generation: {DATA_BUFFERS}", flush=True)

    # Append current message to history
    conversation_history.append({'role': 'user', 'content': ''.join(DATA_BUFFERS['textual'])})

    # 'System' message sent at start of conversation as a way to specify how the agent should respond
    messages = [
        {'role': 'system', 'content': "You are an AI-powered research assistant. \
                                        Your task is to provide precise, factual, and well-researched responses. \
                                        Always answer in a clear and concise manner, \
                                        providing only accurate information."}
    ]

    # Append conversation history to the messages
    messages.extend(conversation_history)

    # Generate response
    response = ollama.chat(
        model='llama3.2',
        messages = messages
        #temperature = 0,
        #max_tokens = 150
    )

    # Add the model's response to the conversation history
    # If more than max limit, pop first 
    conversation_history.append({'role': 'assistant', 'content': response['message']['content']})
    if len(conversation_history) > MAX_HISTORY_LENGTH:
        conversation_history.pop(0)

    # Clear data buffers
    DATA_BUFFERS['textual'].clear()
    print(f"Data buffer after response generation: {DATA_BUFFERS}", flush=True)
    print(f"Conversation history: {conversation_history}", flush=True)

    return response['message']['content']


async def wav_generation_test_response(data):
    messages = [
        {'role': 'system', 'content': "You are an AI-powered research assistant. \
                                        Your task is to provide precise, factual, and well-researched responses. \
                                        Always answer in a clear and concise manner, \
                                        providing only accurate information."},
        {'role': 'user', 'content': data}
    ]
    response = ollama.chat(
        model='llama3.2',
        messages=messages
    )

    return response['message']['content']
        