import openai
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY
async def generate_response(conversation, model="gpt-4"):
    messages = conversation["messages"]
    if conversation.get('temperature', None) is None:
        temperature = 0.5
    else:
        temperature = float(conversation["temperature"])
    system_prompt = conversation.get("system prompt", "You are a helpful discord bot")
    messages[0]= create_message("system", system_prompt)
    # print(messages)
    response = await openai.ChatCompletion.acreate(
        model=model,
        messages=messages,
        temperature=temperature,
    )
    reply = response.choices[0].message["content"]
    # print(reply)
    return reply

def create_message(role, content):
    return {
        "role": role,
        "content": content
    }
