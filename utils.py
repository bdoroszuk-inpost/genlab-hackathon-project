import anthropic
import dotenv
import os
from openai import OpenAI
from elevenlabs.client import ElevenLabs
from elevenlabs import play

dotenv.load_dotenv()
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

anthropic_client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
openai_client = OpenAI(api_key=OPENAI_API_KEY)
elevenlabs_client = ElevenLabs(api_key=ELEVENLABS_API_KEY)

def set_up_clients():
    anthropic_client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    openai_client = OpenAI(api_key=OPENAI_API_KEY)
    elevenlabs_client = ElevenLabs(api_key=ELEVENLABS_API_KEY)

    return anthropic_client, openai_client, elevenlabs_client


def create_message(client, system, content_list, tools=None):
    """
    Schema of content_list:
    [{"role": "user", "content": [{"type": "text","text": "hi"}]}]
    """
    params = {
        "model": "claude-3-5-sonnet-20240620",
        "max_tokens": 1000,
        "temperature": 0,
        "system": system,
        "messages": content_list,
    }
    if tools:
        params["tools"] = tools
        # tool_choice = {"type": "tool", "name": "get_weather"}
        params["tool_choice"] = {"type": "tool", "name": tools[0]["name"]}
    message = client.messages.create(**params)

    # if tools return message.content[0].input, else message.content[0].text
    if tools:
        return message.content[0].input
    else:
        return message.content[0].text



def generate_image(client, prompt, size="1024x1024", quality="standard", n=1):
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size=size,
        quality=quality,
        n=n,
    )
    return response.data[0].url


def generate_and_play_audio(client, text, voice="Rachel", model="eleven_multilingual_v2"):
    audio = client.generate(
        text=text,
        voice=voice,
        model=model
    )
    play(audio)



tools = [
    {
        "name": "get_weather",
        "description": "Get the current weather in a given location",
        "input_schema": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The city and state, e.g. San Francisco, CA",
                }
            },
            "required": ["location"],
        },
    }
]

# response = create_message(anthropic_client, "weather", [ { "role": "user", "content": [ { "type": "text", "text": "What's the weather in San Francisco?" } ] } ], tools)
#
# print(response)
# # test text without function
# response2 = create_message(anthropic_client, "weather", [ { "role": "user", "content": [ { "type": "text", "text": "What's the weather in San Francisco?" } ] } ])
# print(response2)