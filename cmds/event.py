from typing import Text

from discord.channel import TextChannel
from discord.ext.commands.errors import ChannelNotFound
from core.classes import Cog_Extension
import discord
from discord.ext import commands
from cmds.main import Main #從cmd資料夾的main檔案import Cog的class-->Main
import json
import mysql.connector
from mysql.connector import Error




with open('setting.json','r',encoding='utf8') as jFile:
    jdata = json.load(jFile)

class Event(Cog_Extension):
    @commands.Cog.listener()
    async def on_member_join(self, member):
        count = 0
        for tc in member.guild.text_channels:
            if str(tc.name) == 'welcome':
                count += 1
        if count == 0:
            await member.guild.create_text_channel(name = 'welcome')
        for tc in member.guild.text_channels:
            if str(tc.name) == 'welcome':
                channel = self.bot.get_channel(tc.id)

        await channel.send(f"歡迎 {member} 加入 {member.guild.name}! :joy: ")
        

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        count = 0
        for tc in member.guild.text_channels:
            if str(tc.name) == 'leave':
                count += 1
        if count == 0:
            await member.guild.create_text_channel(name = 'leave')
        for tc in member.guild.text_channels:
            if str(tc.name) == 'leave':
                channel = self.bot.get_channel(tc.id)
        
        await channel.send(f"{member} 離開了群組... :sob: ")
        
        
        
#####################################################################################

    #  #處理指令發生的錯誤 error handler
    # @commands.Cog.listener()
    # async def on_command_error(self, ctx, error):
    #    #檢查指令是否有自己的error handler
    #     if hasattr(ctx.command, 'on_error'):
    #         return 
    #     if isinstance(error,commands.errors.MissingRequiredArgument):
    #         await ctx.send("遺失參數")
    #     elif isinstance(error,commands.errors.CommandNotFound):
    #         await ctx.send("無效指令")
    #     elif isinstance(error,commands.errors.CommandInvokeError):
    #         await ctx.send("權限不足")
    #     else:
    #         await ctx.send("發生錯誤", error)
            
        


#commands.errors.CommandInvokeError:
# 😆
####################################################################################

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, data):
        sever_id = data.guild_id
        msg_id = data.message_id#int
        try:
            # 連接 MySQL/MariaDB 資料庫
            connection = mysql.connector.connect(
            host='140.136.151.98',          # 主機名稱
            database='123', # 資料庫名稱
            user='b14',        # 帳號
            password='b140311')  # 密碼
            # 查詢資料庫
            cursor = connection.cursor()
            cursor.execute(f"SELECT msg_id FROM roles WHERE sever_id={sever_id}")
            # 取回全部的資料
            records = cursor.fetchall()
            for record in records:
                if str(msg_id) == str(record[0]):
                    cursor.execute(f"SELECT emoji1,role1,emoji2,role2 FROM roles WHERE sever_id={sever_id} AND msg_id={msg_id}")
                    rec = cursor.fetchall()
                    for (e1,r1,e2,r2) in rec:
                        emoji1 = e1
                        role1 = r1
                        emoji2 = e2
                        role2 = r2
                    guild = self.bot.get_guild(sever_id)#取得當前所在伺服器
                    user = guild.get_member(data.user_id)
                    if str(data.emoji) == str(emoji1):
                        rolx = guild.get_role(int(role1))
                        await user.add_roles(rolx)
                        await user.send(f"您已獲得了 **{rolx}** 身分組!")
                    elif str(data.emoji) == str(emoji2):
                        roly = guild.get_role(int(role2))
                        await user.add_roles(roly)
                        await user.send(f"您已獲得了 **{roly}** 身分組!")

                    break


        except Error as e:
            print("資料庫連接失敗：", e)
        finally:
            if (connection.is_connected()):
                cursor.close()
                connection.close()


    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, data):
        sever_id = data.guild_id
        msg_id = data.message_id#int
        try:
            # 連接 MySQL/MariaDB 資料庫
            connection = mysql.connector.connect(
            host='140.136.151.98',          # 主機名稱
            database='123', # 資料庫名稱
            user='b14',        # 帳號
            password='b140311')  # 密碼
            # 查詢資料庫
            cursor = connection.cursor()
            cursor.execute(f"SELECT msg_id FROM roles WHERE sever_id={sever_id}")
            # 取回全部的資料
            records = cursor.fetchall()
            for record in records:
                if str(msg_id) == str(record[0]):
                    print("in")
                    cursor.execute(f"SELECT emoji1,role1,emoji2,role2 FROM roles WHERE sever_id={sever_id} AND msg_id={msg_id}")
                    rec = cursor.fetchall()
                    for (e1,r1,e2,r2) in rec:
                        emoji1 = e1
                        role1 = r1
                        emoji2 = e2
                        role2 = r2
                    guild = self.bot.get_guild(sever_id)#取得當前所在伺服器
                    user = guild.get_member(data.user_id)

                    if str(data.emoji) == str(emoji1):
                        rolx = guild.get_role(int(role1))
                        await user.remove_roles(rolx)
                        await user.send(f"您已失去 **{rolx}** 身分組!")
                    elif str(data.emoji) == str(emoji2):
                        roly = guild.get_role(int(role2))
                        await user.remove_roles(roly)
                        await user.send(f"您已失去 **{roly}** 身分組!")

                    break


        except Error as e:
            print("資料庫連接失敗：", e)
        finally:
            if (connection.is_connected()):
                cursor.close()
                connection.close()

    #delete_count = 0
    #last_audit_log_id = 0
#--------------------------------------------------------------------------------------------------    
    #抓取被刪除的訊息
    @commands.Cog.listener()
    async def on_message_delete(self, msg):
        sever_id = msg.guild.id
        #msg.author = name
        user_name = msg.author.name
        m = []
        for i in msg.content:
            m.append(i)
            break
        if str(m[0]) == '[':
            pass
        else:
            try:
                # 連接 MySQL/MariaDB 資料庫
                connection = mysql.connector.connect(
                host='140.136.151.98',          # 主機名稱
                database='123', # 資料庫名稱
                user='b14',        # 帳號
                password='b140311')  # 密碼
                # 查詢資料庫
                cursor = connection.cursor()
                cursor.execute(f"SELECT word FROM dw WHERE sever_id={sever_id}")

                # 取回全部的資料
                records = cursor.fetchall()
                c=0
                # 列出查詢的資料
                for dw in records:
                    if dw[0] in msg.content:
                        c += 1
                #如果是髒話字眼就不進行抓取並記錄該名使用者
                
                pass###############


                if c > 0:
                    ##############################################################################################
                    # 查詢資料庫是否有該用戶資料，沒有就建立新資料，有就更新資料
                    for member in msg.guild.members:
                        if member.name == user_name:
                            user_id = member.id
                            break
                    #尋找資料
                    cursor = connection.cursor()
                    cursor.execute(f"SELECT count FROM user_dw_count WHERE sever_id={sever_id} AND user_id={user_id}")
                    # 取回全部的資料
                    records = cursor.fetchall()

                    if len(records) == 0:
                        SQL = "INSERT INTO user_dw_count(sever_id,user_id,count) VALUES( %s, %s, 1)"
                        cursor.execute(SQL,(sever_id,user_id))
                        connection.commit()
                    else:
                        L = list(records[0])
                        count = int(L[0])
                        count += 1
                        if count >10:
                            if count%5==0:
                                guild = self.bot.get_guild(sever_id)
                                owner = guild.owner#伺服器擁有者 職階最高
                                user = self.bot.get_user(user_id)
                                await owner.send(f"{user.name} 在{guild.name}伺服器中已經違反規則{count}次了!")
                             
                        
                        SQL = "UPDATE user_dw_count SET count = %s WHERE sever_id = %s AND user_id = %s"
                        cursor.execute(SQL,(count,sever_id,user_id))
                        connection.commit()
                        pass
                        
                    #更新count資料(count++)
                    
                        
                    ##############################################################################################
                    pass
                else:
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
                        #await msg.channel.send(f"{deleter} has deleted {msg.author} message!")
                        try:
                            await msg.channel.send(f"**{msg.author}** 被刪除的訊息 : {msg.content} ")
                            break
                        except:
                            await msg.channel.send(f"存取訊息失敗")
                            break      
            except Error as e:
                print("資料庫連接失敗：", e)

            finally:
                if (connection.is_connected()):
                    cursor.close()
                    connection.close()
            
#-------------------------------------------------------------------------------------------------------            
    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.author==self.bot.user :
            if '表情獲取身分組' in str(msg.content):
                sever_id = msg.guild.id
                s = str(msg.content).split('~')
                r = s[1].split(',')
                emoji1 = (r[0].split(':')[0]).strip()
                r1 = (r[0].split(':')[1]).strip()
                emoji2 = (r[1].split(':')[0]).strip()
                r2 = (r[1].split(':')[1]).strip()
                f = 0 # 用來判斷是否存入所有身分組
                for Role in msg.guild.roles:
                    if Role.name == r1:
                        r1 = Role.id
                        f+=1
                    elif Role.name == r2:
                        r2 = Role.id
                        f+=1
                    if f>1:
                        break
                msg_id = msg.id
                role1 = r1
                role2 = r2
                try:
                    # 連接 MySQL/MariaDB 資料庫
                    connection = mysql.connector.connect(
                    host='140.136.151.98',          # 主機名稱
                    database='123', # 資料庫名稱
                    user='b14',        # 帳號
                    password='b140311')  # 密碼
                    # 查詢資料庫
                    cursor = connection.cursor()
                    
                    SQL = f"INSERT INTO roles(sever_id,msg_id,emoji1,role1,emoji2,role2) value(%s,%s,%s,%s,%s,%s);"
                    cursor.execute(SQL,(sever_id,msg_id,emoji1,role1,emoji2,role2))
                    connection.commit()
                    print("GOOD")
                            
                except Error as e:
                    print("資料庫連接失敗：", e)
                finally:
                    if (connection.is_connected()):
                        cursor.close()
                        connection.close()

            else:
                pass
        else:
            sever_id = msg.guild.id
            m = []
            for i in msg.content:
                m.append(i)
                break
            if str(m[0]) == '[':
                   pass
            else:   #若不是指令則做學習功能的偵測、髒話的偵測等動作
                try:
                    # 連接 MySQL/MariaDB 資料庫
                    connection = mysql.connector.connect(
                    host='140.136.151.98',          # 主機名稱
                    database='123', # 資料庫名稱
                    user='b14',        # 帳號
                    password='b140311')  # 密碼
                    # 查詢資料庫
                    cursor = connection.cursor()
                    cursor.execute(f"SELECT word FROM dw WHERE sever_id={sever_id}")
                    # 取回全部的資料
                    records = cursor.fetchall()
                    # 列出查詢的資料
                    for dw in records:
                        if dw[0] in msg.content and msg.author != self.bot.user:
                            await msg.delete()
                            break

                    connection = mysql.connector.connect(
                    host='140.136.151.98',          # 主機名稱
                    database='123', # 資料庫名稱
                    user='b14',        # 帳號
                    password='b140311')  # 密碼
                    cursor = connection.cursor()
                    cursor.execute(f"SELECT keyword,reply FROM cat WHERE sever_id={sever_id}")
                    
                    record = cursor.fetchall()

                    for (keyword, reply) in record:
                        if(str(keyword) == str(msg.content)):
                            await msg.channel.send(reply)

                                    
                except Error as e:
                    print("資料庫連接失敗：", e)
                finally:
                    if (connection.is_connected()):
                        cursor.close()
                        connection.close()






def setup(bot):
    bot.add_cog(Event(bot))