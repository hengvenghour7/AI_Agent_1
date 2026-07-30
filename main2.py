import ollama

response = ollama.chat(
    model="gemma4:latest",
    messages=[
        {
            "role": "user",
            "content": "Hi"
        }
    ],
    # options={
    #     "num_predict": 100
    # }
)

print(response["message"]["content"])