from core.classes import Cog_Extension
import discord
from discord.ext import commands
from cmds.main import Main #從cmd資料夾的main檔案import Cog的class-->Main
import json

with open('setting.json','r',encoding='utf8') as jFile:
    jdata = json.load(jFile)

class Event(Cog_Extension):
    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = self.bot.get_channel(int(jdata['Welcome_channel']))
        await channel.send(f'{member} join!')

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = self.bot.get_channel(int(jdata['Leave_channel']))
        await channel.send(f'{member} leave!')

    @commands.Cog.listener()
    async def on_message(self, msg):
        keyword = ['apple','pen','pie','abc']
        if msg.content in keyword and msg.author != self.bot.user:
            await msg.channel.send('apple')
#####################################################################################

    # #處理指令發生的錯誤 error handler
    # @commands.Cog.listener()
    # async def on_command_error(self, ctx, error):
    #     #檢查指令是否有自己的error handler
    #     if hasattr(ctx.command, 'on_error'):
    #         return 

    #     if isinstance(error,commands.errors.MissingRequiredArgument):
    #         await ctx.send("遺失參數")
    #     elif isinstance(error,commands.errors.CommandNotFound):
    #        await ctx.send("沒這指令啦!")
    #     else:
    #         await ctx.send("發生錯誤")

####################################################################################

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, data):
        if data.message_id == 881500152685297724:
            if str(data.emoji) == '😂':
                guild = self.bot.get_guild(data.guild_id)#取得當前所在伺服器
                role = guild.get_role(881510385532928030)#取得伺服器內指定的身分組
                await data.member.add_roles(role)#給予該成員身分組
                await data.member.send(f"你取得了{role}身分組!")

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, data):
        if data.message_id == 881500152685297724:
            if str(data.emoji) == '😂':
                guild = self.bot.get_guild(data.guild_id)#取得當前所在伺服器
                user = guild.get_member(data.user_id)
                role = guild.get_role(881510385532928030)#取得伺服器內指定的身分組
                await user.remove_roles(role)#給予該成員身分組
                await user.send(f"你移除了{role}身分組!")

    #delete_count = 0
    #last_audit_log_id = 0

    @commands.Cog.listener()
    async def on_message_delete(self, msg):
        delete_count = 0
        last_audit_log_id = 0
        deleter = msg.author
        async for audilog in msg.guild.audit_logs(limit = 10,action=discord.AuditLogAction.message_delete):
            if (audilog.extra.count - delete_count) != 0 or audilog.id != last_audit_log_id:
                last_audit_log_id = audilog.id
                delete_count = audilog.extra.count
                deleter = audilog.user
            else:
                pass
            mc = audilog.extra.channel

        await msg.channel.send(f"{deleter} has deleted {msg.author} message!")    
            
    # @commands.Cog.listener()
    # async def on_message_delete(self, msg):
    #     counter = 1
    #     async for audilog in msg.guild.audit_logs(action=discord.AuditLogAction.message_delete):
    #         if counter == 1:
    #             await msg.channel.send(audilog.user.name)
    #             counter = 2


def setup(bot):
    bot.add_cog(Event(bot))