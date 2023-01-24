#pip install discord.py
#pip install openai

import discord
from discord.ext import commands
import itertools
import requests
import openai
import json
import requests
import wave

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=["!",""],intents=intents)
bot.remove_command("help")


@bot.command()
async def help(message):
    if message.author.bot:
        return
    else:
        embed=discord.Embed(title="ヘルプ機能", description="コマンドの説明。", color=0xff9300)
        embed.add_field(name="!ctx", value="OpenAIと会話できます 例文:非国民め", inline=False)
        await message.channel.send(embed=embed)

        
#ChatGPT
def GPT(stext):

    openai.api_key = API_KEY
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=stext,
            max_tokens=40,
            temperature=0.1,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
    )
    content = response.choices[0].text.split('.')
    return response.choices[0].text
    
@bot.command()
async def ctx(ctx, *, msg):
    query = msg.split(" ")
    response = GPT(query)
    print(response)
    await ctx.send(response)
    
#VOICEVOX

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

@bot.command()
async def voivo(ctx, *, msg):
    if __name__ == '__main__':
        text = msg
        generate_wav(text)
        await ctx.channel.send(file=discord.File("./audio.mp3"))

#Deepl
        
@bot.command()
async def trans(ctx, *, msg):
    trans_now = await ctx.send("日本語から英語に翻訳中アルよ\n")
    api_key = Deepl_API
    params = {
                "auth_key": api_key,
                "text": str(msg),
                "source_lang": "JA",
                "target_lang": "EN"
            }

    request = requests.post("https://api-free.deepl.com/v2/translate", data=params) #無料コース
    result = request.json()
    await trans_now.edit(content=result["translations"][0]["text"])
 
bot.run("") #TOKEN
API_KEY = "" #OpenAI's APIKEY
Deepl_API = "" #Deepl API
