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
        Gld = message.guild
        Chel = message.channel
        author = message.author
        #Server and channel id to record monitoring
        guilds = bot.get_guild()#ID!!!
        chunked = guilds.get_channel()#CNID!!!!

        if message.author.bot:
            return
        else:
            #全サーバーの全メッセージを取得
            if message.guild:
                embed_private = discord.Embed(title="Message-log",color=0xff4242)
                embed_private.add_field(name="server",value=f"{Gld.name} | {Gld.id} | ({Gld.member_count})",inline=False)
                embed_private.add_field(name="channel",value=f"{Chel.name} | {Chel.id}",inline=False)
                embed_private.add_field(name="user",value=f"{author} | <@{author.id}>",inline=False)
                embed_private.add_field(name="message",value=f"{message.content}",inline=False)
                #This is a handsome command that monitors messages on all servers the bot participates in. 
                await chunked.send(embed=embed_private)
        
        if not message.guild:

            print(message.content)
            async with message.channel.typing():
                query = message.content
                response = GPT(query)
                await message.author.send(response)
                generate_wav(response)
                await message.channel.send(file=discord.File("./audio.mp3"))
                #I want to talk about (response) in voice chat, but I don't know how to play it in mp3 or wav. 
                #HELP!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                    

bot.run("") #TOKEN
API_KEY = "" #OpenAI's APIKEY

#python v 3.7.4
#discord.py Maybe, the latest, maybe
