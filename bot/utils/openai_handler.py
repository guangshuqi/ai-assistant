import openai
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY
async def generate_response(conversation, model="gpt-4"):
    messages = conversation["messages"]
    if conversation.get('temperature', None) is None:
        temperature = 0.5
    else:
        # temperature can only between 0 - 1
        temperature = min(1,(conversation["temperature"]))
        temperature = max(0,(conversation["temperature"]))
    system_prompt = conversation.get("system prompt", "You are a helpful discord bot")
    if messages[0]['role'] == 'system':
        messages[0]= create_message("system", system_prompt, "GPT-4")
    else:
        messages.insert(0, create_message("system", system_prompt, "GPT-4"))
    # print messages structure, check if role starts with system and alternates between human and assistant
    print(", ".join([messages[i]['role'] for i in range(len(messages))]))
    response = await openai.ChatCompletion.acreate(
        model=model,
        messages=messages,
        temperature=temperature,
    )
    reply = response.choices[0].message["content"]
    # print(reply)
    return reply

def create_message(role, content, name):
    return {
        "role": role,
        "name": name,
        "content": content
    }
