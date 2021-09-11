import discord
from discord.ext import commands
from core.classes import Cog_Extension
import json, asyncio, datetime

class Task(Cog_Extension):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        self.counter = 0
        self.taskcounter = 0
    #    async def interval():
    #       await self.bot.wait_until_ready()
    #        self.channel = self.bot.get_channel(872049328989020170)
    #        while not self.bot.is_closed():
    #            await self.channel.send("Hi i'm running!")
    #            await asyncio.sleep(5)

    #    self.bg_task = self.bot.loop.create_task(interval())

        async def time_task():
            await self.bot.wait_until_ready()
            self.channel = self.bot.get_channel(872049328989020170)
            while not self.bot.is_closed():
                now_time = datetime.datetime.now().strftime('%H%M')
                with open('setting.json','r',encoding='utf8') as jfile:
                    jdata = json.load(jfile)
                if self.taskcounter == 1:
                    time_task.cancel()
                else:
                    pass

                if now_time == jdata['time'] and self.counter == 0:
                    await self.channel.send('Task Working!')
                    self.counter = 1
                    await asyncio.sleep(1)
                else:
                    await asyncio.sleep(1)
                    pass

        self.bg_task = self.bot.loop.create_task(time_task())

    @commands.command()
    async def set_channel(self, ctx, ch: int):
        self.channel = self.bot.get_channel(ch)
        await ctx.send(f"Set channel: {self.channel.mention}")

    @commands.command()
    async def set_time(self, ctx, time):
        self.counter = 0
        with open('setting.json','r',encoding='utf8') as jfile:
            jdata = json.load(jfile)
        jdata['time'] = time
        with open('setting.json','w',encoding='utf8') as jfile:
            json.dump(jdata, jfile, indent=4)#indent = 縮排  = 4 = tab
    
    @commands.command()
    async def task_cancel(self, ctx):
        self.taskcounter = 1
        await ctx.send(f"close task!")
    
    @commands.command()
    async def task_continue(self, ctx):
        self.taskcounter = 0
        await ctx.send(f"continue task!")


def setup(bot):
    bot.add_cog(Task(bot))