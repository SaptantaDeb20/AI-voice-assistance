from deepseek import DeepSeekAPI

client = DeepSeekAPI(
    api_key="sk-8a85d4a0191640fc97aa9e2da4ad1684"
)

response = client.chat.completions.create(
    model="deepseek-gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {
            "role": "user",
            "content": "hello"
        }
    ]
)

print(response.choices[0].message)