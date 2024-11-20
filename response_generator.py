import ollama

def generate_response(data):
    response = ollama.chat(
        model='llama3.2',
        messages=[{'role': 'user', 'content': data}]
    )

    return response['message']['content']

#print(generate_response('Hello ollama, I am chase.'))