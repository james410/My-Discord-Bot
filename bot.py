import discord
from discord.ext import commands
import json
import random
import os

with open('setting.json','r',encoding='utf8') as jFile:
    jdata = json.load(jFile)

intents = discord.Intents.all()#預設是default
intents.members = True

bot = commands.Bot(command_prefix='[',intents = intents)

@bot.event
async def on_ready():
    print(">> bot is online <<")


#load function
@bot.command()
async def load(ctx, extension):
    bot.load_extension(f'cmds.{extension}')
    await ctx.send(f'Loaded {extension} done.')
    print(f"load {extension}")
#unload function
@bot.command()
async def unload(ctx, extension):
    bot.unload_extension(f'cmds.{extension}')
    await ctx.send(f'Un - Loaded {extension} done.')
    print(f"unload {extension}")
#reload function
@bot.command()
async def reload(ctx, extension):
    bot.reload_extension(f'cmds.{extension}')
    await ctx.send(f'Re - Loaded {extension} done.')
    print(f"reload {extension}")


for filename in os.listdir('./cmds'):
    if filename.endswith('.py'):
        bot.load_extension(f'cmds.{filename[:-3]}')


if __name__ == "__main__":
    bot.run(jdata['TOKEN'])