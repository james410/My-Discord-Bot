import discord
from discord.ext import commands
from core.classes import Cog_Extension
import datetime
import random
import requests

class Main(Cog_Extension):
    

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'{round(self.bot.latency*1000)} (ms)')

    @commands.command()
    async def hi(self, ctx):
        await ctx.send('axxxxq')

    @commands.command()
    async def em(self, ctx):
        embed=discord.Embed(title="About", url="https://www.artstation.com/search?sort_by=relevance", description="About the bot", color=0xff00c8,
        timestamp = datetime.datetime.now(datetime.timezone.utc))
        embed.set_author(name="james", url="https://www.artstation.com/search?sort_by=relevance", icon_url="https://cdn.discordapp.com/attachments/835499797033123850/876753106128494653/5b5747a0dbb24ea2.gif")
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/835499797033123850/876753106128494653/5b5747a0dbb24ea2.gif")
        embed.add_field(name="1", value="11", inline=False)
        embed.add_field(name="2", value="22", inline=True)
        embed.add_field(name="3", value="33", inline=True)
        embed.add_field(name="4", value="44", inline=False)
        embed.set_footer(text="123")
        await ctx.send(embed=embed)

    @commands.command()
    async def sayd(self, ctx,*,msg):
        await ctx.message.delete()
        await ctx.send(msg)

    @commands.command()
    async def clean(self,ctx, num:int):
        await ctx.channel.purge(limit=num+1)

    @commands.command()
    async def rand_squad(self, ctx):
        online = []
        for member in ctx.guild.members:
            if str(member.status) == 'online' and member.bot == False:
                online.append(member.name)
        
        random_online = random.sample(online, k=4)
        
        for squad in range(2):
            a = (random.sample(random_online, k=2))
            await ctx.send(f"第{squad+1}組: " + str(a))
            for name in a:
                random_online.remove(name)  
        
    @commands.group()
    async def codetest(self, ctx):
        pass

    @codetest.command()
    async def python(self, ctx):
        await ctx.send("Python")

    @codetest.command()
    async def javascript(self, ctx):
        await ctx.send("javascript")

    @codetest.command()
    async def cpp(self, ctx):
        await ctx.send("C++")

    @commands.command()
    async def cmdA(self, ctx, num):
        await ctx.send(num)

    @commands.command()
    async def cmdB(self, ctx, num):
        await ctx.send(num)


    #指令個別專用的錯誤處理
    @cmdB.error    #直接指定該類別下的指令
    async def cmdB_error(self, ctx, error):
        if isinstance(error,commands.errors.MissingRequiredArgument):
            await ctx.send("請輸入參數")

    @commands.command()
    async def test(self,ctx):
        response = requests.get('https://jsonstorage.net/api/items/',{
            "id": "3311696a-67f6-41ec-b1c1-a48f91dac7a6"
        })
        #取得原來資料
        data = response.json()
        
        #新增一筆資料到原來資料裡
        data['new'] = "This is a new data"

        update = requests.put('https://jsonstorage.net/api/items/',
            params = {"id": "3311696a-67f6-41ec-b1c1-a48f91dac7a6"},
            json = data
        )
        print(update)


def setup(bot):
    bot.add_cog(Main(bot))