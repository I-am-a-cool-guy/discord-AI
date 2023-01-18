import discord
from discord.ext import commands
import itertools
import requests
import openai

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=["!",""],intents=intents)
bot.remove_command("help")

AI_API_KEY = "" #OpenAI's APIKEY

def gpt3(stext):
    openai.api_key = AI_API_KEY

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

@bot.event
async def on_message(message):
    if message.guild:
        return
    if not message.guild:
        query = message.content
        response = gpt3(query)
        await message.author.send(response)
        print(response)

bot.run("") #TOKEN
