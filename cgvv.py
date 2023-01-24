import discord
from discord.ext import commands
import itertools
import requests
import openai
import json
import requests
import wave
import pytz

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=["!",""],intents=intents)
bot.remove_command("help")

def GPT(stext):
    openai.api_key = API_KEY

    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=stext,
            max_tokens=320,#number of characters
            temperature=0.1,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
    )
    content = response.choices[0].text.split('.')
    print(content)
    return response.choices[0].text

def generate_wav(text, speaker=1, filepath='./audio.mp3'):
    host = 'localhost'
    port = 50021
    params = (
        ('text', text),
        ('speaker', speaker),
    )
    response1 = requests.post(
        f'http://{host}:{port}/audio_query',
        params=params
    )
    headers = {'Content-Type': 'application/json',}
    response2 = requests.post(
        f'http://{host}:{port}/synthesis',
        headers=headers,
        params=params,
        data=json.dumps(response1.json())
    )

    wf = wave.open(filepath, 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(24000)
    wf.writeframes(response2.content)
    wf.close()

@bot.event
async def on_message(message):
    if message.guild:
            return
        if not message.guild:

            if message.author.bot:
                return
            else:
                print(message.content)
                async with message.channel.typing():
                    query = message.content
                    response = GPT(query)
                    await message.author.send(response)
                    generate_wav(response)
                    await message.channel.send(file=discord.File("./audio.mp3"))
                    

bot.run("") #TOKEN
API_KEY = "" #OpenAI's APIKEY
