import discord
from discord.channel import VoiceChannel
from discord.ext import commands
from core.classes import Cog_Extension
import datetime
import random
import requests
import re
import mysql.connector
from mysql.connector import Error



class Main(Cog_Extension):
    

    @commands.command()
    async def sayd(self, ctx,*,msg):
        await ctx.message.delete()
        await ctx.send(msg)


    @commands.command()
    async def clean(self,ctx, num:int):
        await ctx.channel.purge(limit=num+1)

    #ban成員指令
    @commands.command()
    async def ban(self, ctx, name):
        sever_id = ctx.guild.id
        await ctx.message.delete()
        User_id = ''.join([x for x in name if x.isdigit()])           
        for member in ctx.guild.members:
            if str(member.id) == User_id:
                user_id = member.id
                user_m = member
                user_n = member.name
        print("1")
        try:
            # 連接 MySQL/MariaDB 資料庫
            connection = mysql.connector.connect(
            host='140.136.151.98',          # 主機名稱
            database='123', # 資料庫名稱
            user='b14',        # 帳號
            password='b140311')  # 密碼
            # 查詢資料庫
            cursor = connection.cursor()
            cursor.execute(f"SELECT user_id FROM ban WHERE sever_id={sever_id}")

            # 取回全部的資料
            records = cursor.fetchall()
            f = 0
            for record in records:
                if record[0] == user_id:
                    f += 1
                    break
            if f == 0:
                SQL = f"INSERT INTO ban(sever_id,user_id) value(%s,%s);"
                cursor = connection.cursor()
                cursor.execute(SQL,(sever_id,user_id))
                connection.commit()
                await ctx.guild.ban(user_m)
                await ctx.send(f":white_check_mark: Ban {user_n}!")
            else:
                pass
        except Error as e:
            print("資料庫連接失敗：", e)

        finally:
            if (connection.is_connected()):
                cursor.close()
                connection.close()
        
                


    #解ban成員指令
    @commands.command()
    async def unban(self, ctx, name):
        sever_id = ctx.guild.id
        await ctx.message.delete()
        bans = await ctx.guild.bans()
        print("1")
        try:
            # 連接 MySQL/MariaDB 資料庫
            connection = mysql.connector.connect(
            host='140.136.151.98',          # 主機名稱
            database='123', # 資料庫名稱
            user='b14',        # 帳號
            password='b140311')  # 密碼
            # 查詢資料庫
            cursor = connection.cursor()
            cursor.execute(f"SELECT user_id FROM ban WHERE sever_id={sever_id}")

            # 取回全部的資料
            records = cursor.fetchall()
            print("2")
            for banentry in bans:
                if banentry.user.name == name:
                    user_id = banentry.user.id
                    user = banentry.user

            for record in records:
                if int(record[0]) == user_id:
                    SQL = "DELETE FROM ban WHERE sever_id=%s AND user_id=%s"
                    cursor = connection.cursor()
                    cursor.execute(SQL,(sever_id,user_id))
                    connection.commit()

                    await ctx.guild.unban(user)
                    await ctx.send(f":white_check_mark: Unban {name}!")
                    break
            
        except Error as e:
            print("資料庫連接失敗：", e)

        finally:
            if (connection.is_connected()):
                cursor.close()
                connection.close()
        

    #--------------------------------------------------------------------------------------
    #投票功能
    @commands.command()
    async def vote(self, ctx,*,msg):
        await ctx.message.delete()
        choose = re.findall(r'\S+',msg)
        # for i in list(msg):
        #     if i != ' ':
        #         choose.append(i)
        embed=discord.Embed(title=choose[0], color=0xd400ff,timestamp = datetime.datetime.now(datetime.timezone.utc))
        embed.set_author(name="📊投票📊")
        embedlist = ['1️⃣','2️⃣','3️⃣','4️⃣','5️⃣','6️⃣','7️⃣','8️⃣','9️⃣','🔟']#❌ #⭕ 
        count = 0
        choose.pop(0)
        if len(choose)> 1:
            for i in choose:
                embed.add_field(name=embedlist[count], value=i, inline=False)
                count += 1
            m = await ctx.send(embed=embed)
            count = 0
            for i in choose:
                await m.add_reaction(embedlist[count])
                count += 1
        else:
            m = await ctx.send(embed=embed)
            await m.add_reaction('❌')
            await m.add_reaction('⭕')

        
        
    #-----------------------------------------------------------------------------------------------
    #kick 成員
    @commands.command()
    async def kick(self, ctx, name):
        await ctx.message.delete()
        user_id = ''.join([x for x in name if x.isdigit()])
        for member in ctx.guild.members:
            if str(member.id) == user_id:
                await ctx.guild.kick(member)
                await ctx.send(f":white_check_mark: 已將 **{member.name}** 從伺服器中踢除!")

    #-----------------------------------------------------------------------------------------------
    #成員禁音指令
    @commands.command()
    async def mute(self,ctx, user):
        await ctx.message.delete()
        user_id = ''.join([x for x in user if x.isdigit()])
        for member in ctx.guild.members:
            if str(member.id) == user_id:
                await member.edit(mute = True)
                await ctx.send(f":white_check_mark: **{member.name}** 已被禁音!")
    
    @commands.command()
    async def unmute(self,ctx, user):
        await ctx.message.delete()
        user_id = ''.join([x for x in user if x.isdigit()])
        for member in ctx.guild.members:
            if str(member.id) == user_id:
                await member.edit(mute = False)
                await ctx.send(f":white_check_mark: **{member.name}** 已被取消禁音!")

    #-----------------------------------------------------------------------------------------------
    #移動成員指令
    @commands.command()
    async def move(self,ctx, name, vc):
        await ctx.message.delete()
        user_id = ''.join([x for x in name if x.isdigit()])
        #print(user_id)
        guild = self.bot.get_guild(ctx.guild.id)
        #print(type(ctx.author))
        member = guild.get_member(int(user_id))

        #print(type(member))
        #print(member.name)
        for v in ctx.guild.voice_channels:
            if str(v.name) == vc:
                #print(type(v))
                await member.move_to(v)
                await ctx.send(f"已將 **{member.name}** 移到 **{v.name}** 頻道!")
                break
        #if 
        



    #-----------------------------------------------------------------------------------------------
    @commands.command()
    async def create_tch(self, ctx, Name):
        await ctx.message.delete()
        guild = self.bot.get_guild(ctx.guild.id)
        await guild.create_text_channel(name = Name)
        await ctx.send(f"以創建 {Name} 文字頻道!")
    #-----------------------------------------------------------------------------------------------
    @commands.command()
    async def sever(self, ctx):
        await ctx.message.delete()
        counto = 0
        count = 0
        countb = 0
        for member in ctx.guild.members:
            if member.bot == False:
                count += 1
                if str(member.status) == 'online':
                    counto += 1
            else:
                countb += 1
        await ctx.send(f"伺服器總人數 : {count}")
        await ctx.send(f"伺服器機器人數 : {countb}")
        await ctx.send(f"目前在線人數 : {counto}")

    @commands.command()
    async def role(self,ctx,Name):
        await ctx.message.delete()
        user_id = ''.join([x for x in Name if x.isdigit()])
        member = ctx.guild.get_member(int(user_id))
        for i in member.roles:
            if str(i) == str("@everyone"):
                pass
            else:
                await ctx.send(i)

#---------------------------------------------------------------------------------------------------------------
    @commands.group()
    async def 髒話(self,ctx):
        pass
    @髒話.command()
    async def add(ctx,dirtyword):
        sever_id = ctx.guild.id
        f = 0
        #print(type(dirtyword))
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
                if dw[0] == dirtyword:
                    f = 1
            
            if f == 1:
                pass
            else :
                sql = "INSERT INTO dw (sever_id,word) VALUES (%s, %s);"
                newdata = (sever_id,dirtyword)
                cursor = connection.cursor()
                cursor.execute(sql, newdata)
                connection.commit()
                await ctx.send(':white_check_mark:新增成功!')

            
        except Error as e:
            print("資料庫連接失敗：", e)

        finally:
            if (connection.is_connected()):
                cursor.close()
                connection.close()
            
        #將輸入的字分開
        #若資料庫中沒有則加入至資料庫
        #pass
    @髒話.command()
    async def list(self,ctx):
        await ctx.message.delete()
        sever_id = ctx.guild.id
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
            if len(records) == 0 :
                await ctx.send("本伺服器目前沒有設定不雅字眼~ :sweat_smile: ")
                pass
            # 列出查詢的資料
            for i in records:
                await ctx.send('`'+i[0]+'`')    
            
        except Error as e:
            print("資料庫連接失敗：", e)

        finally:
            if (connection.is_connected()):
                cursor.close()
                connection.close()
    @髒話.command()
    async def delete(ctx, msg):
        sever_id = ctx.guild.id
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
                if dw[0] == msg:
                    sql = f"DELETE FROM dw WHERE word=%s AND sever_id=%s"
                    cursor = connection.cursor()
                    cursor.execute(sql,(msg,sever_id))      
                    connection.commit()   
                    await ctx.send(f'已經將 "{msg}" 刪除! :blush:') 

                    break          

        except Error as e:
            print("資料庫連接失敗：", e)

        finally:
            if (connection.is_connected()):
                cursor.close()
                connection.close()
#-------------------------------------------------------------------------------------------------------
    #學習功能
    @commands.group()
    async def skyler(self,ctx):
        pass

    @skyler.command()
    async def add(self,ctx,msg,msg2):
        sever_id = ctx.guild.id
        f = 0#flag
        try:
            # 連接 MySQL/MariaDB 資料庫
            connection = mysql.connector.connect(
            host='140.136.151.98',          # 主機名稱
            database='123', # 資料庫名稱
            user='b14',        # 帳號
            password='b140311')  # 密碼
            # 查詢資料庫
            cursor = connection.cursor()
            cursor.execute(f"SELECT keyword FROM cat WHERE sever_id={sever_id}")

            # 取回全部的資料
            records = cursor.fetchall()

            for kw in records:
                if kw[0] == msg:
                    f += 1

            if f>0:
                sql = "UPDATE cat SET reply = %s WHERE sever_id = %s AND keyword = %s"
                cursor = connection.cursor()
                cursor.execute(sql, (msg2,sever_id,msg))
                await ctx.send(':white_check_mark:新增成功!')

                # 確認資料有存入資料庫
                connection.commit()
            else:
                sql = "INSERT INTO cat (sever_id,keyword,reply) VALUES (%s, %s,%s)"
                cursor.execute(sql,(sever_id,msg,msg2))
                connection.commit()
                await ctx.send(':white_check_mark:新增成功!')

        except Error as e:
            print("資料庫連接失敗：", e)

        finally:
            if (connection.is_connected()):
                cursor.close()
                connection.close()
    @skyler.command()
    async def delete(self, ctx,msg):
        sever_id = ctx.guild.id
        try:
            # 連接 MySQL/MariaDB 資料庫
            connection = mysql.connector.connect(
            host='140.136.151.98',          # 主機名稱
            database='123', # 資料庫名稱
            user='b14',        # 帳號
            password='b140311')  # 密碼
            # 查詢資料庫
            cursor = connection.cursor()
            cursor.execute(f"SELECT keyword FROM cat WHERE sever_id={sever_id}")

            # 取回全部的資料
            records = cursor.fetchall()
            # 列出查詢的資料
            for dw in records:
                if dw[0] == msg:
                    sql = f"DELETE FROM cat WHERE keyword=%s AND sever_id=%s"
                    cursor = connection.cursor()
                    cursor.execute(sql,(msg,sever_id))      
                    connection.commit()              
            await ctx.send(f'已經將 "{msg}" 刪除! :blush:')
        except Error as e:
            print("資料庫連接失敗：", e)

        finally:
            if (connection.is_connected()):
                cursor.close()
                connection.close()
    #####
    #####
                

def setup(bot):
    bot.add_cog(Main(bot))