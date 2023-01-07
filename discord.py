#py -m pip install discord.py
#py -m pip install openai

import discord
from discord.ext import commands
import itertools
import requests
import openai

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

AI_API_KEY = "" #OpenAI's APIKEY

def gpt3(stext):
    openai.api_key = AI_API_KEY

    response = openai.Completion.create(
        engine='text-davinci-001',
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

@bot.command()
async def ctx(ctx, *, msg):
    query = msg.split(" ")
    response = gpt3(query)
    print(response)
    await ctx.send(response)

bot.run("") #TOKEN

#8=========D ← My big cock.You need to describe this to get it to work