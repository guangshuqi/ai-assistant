import openai
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY
async def generate_response(messages, model="gpt-4", temperature=0):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature,
    )
    return response.choices[0].message["content"]

def create_message(role, content):
    return {
        "role": role,
        "content": content
    }
