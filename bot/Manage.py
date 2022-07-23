import discord
from discord.ext import commands
import random
import datetime
import requests
import json

# 임배드 함수
def embed(title, description, color=random.randint(0x000000, 0xFFFFFF)):
    return discord.Embed(title=title, description=description, color=color)

async def timeout_user(bot, *, user_id: int, guild_id: int, until):
    headers = {"Authorization": f"Bot {bot.http.token}"}
    url = f"https://discord.com/api/v9/guilds/{guild_id}/members/{user_id}"
    timeout = (datetime.datetime.utcnow() + datetime.timedelta(minutes=until)).isoformat()
    json = {'communication_disabled_until': timeout}
    session = requests.patch(url, json=json, headers=headers)
    if session.status_code in range(200, 299):
        return session.json()

async def remove_timeout_user(bot, *, user_id: int, guild_id: int):
    headers = {"Authorization": f"Bot {bot.http.token}"}
    url = f"https://discord.com/api/v9/guilds/{guild_id}/members/{user_id}"
    json = {'communication_disabled_until': None}
    session = requests.patch(url, json=json, headers=headers)
    if session.status_code in range(200, 299):
        return session.json()

class Manage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.command()
    async def clear(self, ctx, *, amount=999999999999999999999):
        if ctx.author.guild_permissions.manage_messages:
            try:
                amount += 1
                await ctx.channel.purge(limit=amount)
            except:
                await ctx.reply(embed=embed("삭제 실패","메시지 관리 권한과 함께 초대해주세요",discord.Color.red()))
            if amount == 1000000000000000000000:
                await ctx.send(embed=embed("삭제 완료","이 채널에 있는 모든 메시지 (매우 오래된 메시지 제외)가 삭제되었습니다",discord.Color.green()))
            else:
                await ctx.send(embed=embed("삭제 완료",f"{amount}개의 메시지가 삭제되었습니다",discord.Color.green()))
        else:
            await ctx.reply(embed=embed("삭제 실패",'메시지 관리권한이 없습니다',discord.Color.red()))
    @commands.command()
    async def timeout(self, ctx, user:discord.Member, min:int):
        if not ctx.author.guild_permissions.ban_members:
            return await ctx.reply(embed=embed("타임아웃 실패","필수 요구사항인 **멤버 밴**권한이 없습니다",discord.Color.red()))
        handshake = await timeout_user(bot=self.bot, user_id=user.id, guild_id=ctx.guild.id, until=min)
        if handshake:
             return await ctx.reply(embed=embed("타임아웃 완료",f"{user}님을 {min}분동안 타임아웃 시켰습니다",discord.Color.green()))
    @commands.command()
    async def removetimeout(self, ctx, user:discord.Member):
        if not ctx.author.guild_permissions.ban_members:
            return await ctx.reply(embed=embed("타임아웃 해제 실패","필수 요구사항인 **멤버 밴**권한이 없습니다",discord.Color.red()))
        handshake = await remove_timeout_user(bot=self.bot, user_id=user.id, guild_id=ctx.guild.id)
        if handshake:
             return await ctx.reply(embed=embed("타임아웃 해제 완료",f"{user}님의 타임아웃을 해제시켰습니다",discord.Color.green()))
    @commands.command()
    async def kick(self, ctx, user:discord.Member, *, text=None):
        if ctx.author.guild_permissions.kick_members:
            await ctx.guild.kick(user, reason=text)
            await ctx.reply(embed=embed("킥 성공",f"{user}님을 킥 했어요 \n킥 사유:{text}",discord.Color.green()))
        else:
            await ctx.reply(embed=embed("킥 실패","필수 요구사항인 **멤버 추방**권한이 없습니다",discord.Color.red()))
    @commands.command()
    async def ban(self, ctx, user:discord.Member, *, text=None):
        if ctx.author.guild_permissions.ban_members:
            await ctx.guild.ban(user, reason=text)
            await ctx.reply(embed=embed("밴 성공",f"{user}님을 밴 했어요 \n밴 사유:{text}",discord.Color.green()))
        else:
            await ctx.reply(embed=embed("밴 실패","필수 요구사항인 **멤버 밴**권한이 없습니다",discord.Color.red()))
    @commands.command()
    async def unban(self, ctx, user:discord.User):
        if ctx.author.guild_permissions.ban_members:
            await ctx.guild.unban(user)
            await ctx.reply(embed=embed("언밴 성공",f"{user}님을 언밴 했어요",discord.Color.green()))
        else:
            await ctx.reply(embed=embed("언밴 실패","필수 요구사항인 **멤버 밴**권한이 없습니다",discord.Color.red()))
    @commands.command()
    async def warn(self,ctx,user:discord.Member,number:int=1,*,reason='None'):
        if not ctx.author.guild_permissions.ban_members:
            return
        jstring = open("warn.json", "r", encoding='utf-8-sig').read()
        warn = json.loads(jstring)
        jstring = open("warnlimit.json", "r", encoding='utf-8-sig').read()
        warnlimit = json.loads(jstring)
        try:
            warn[str(user.id)] += number
            with open(f"warn.json", "w+", encoding='utf-8-sig') as f:
                json_string = json.dump(warn, f, indent=2, ensure_ascii=False)
        except:
            warn[str(user.id)] = int(number)
            with open(f"warn.json", "w+", encoding='utf-8-sig') as f:
                json_string = json.dump(warn, f, indent=2, ensure_ascii=False)
        if warn[str(user.id)] >= int(warnlimit):
            try:
                await user.send(embed=discord.Embed(title="경고,밴 안내",description=f'당신은 경고 갯수가 {warnlimit}이상이 되어 이 봇에 의해 밴당했어요\n경고 사유 : {reason}',color=discord.Color.red()))
            except:
                pass
            del warn[str(user.id)]
            await ctx.guild.ban(user,reason=f'경고 한도 초과. 마지막 경고 {reason}')
            c = await ctx.send(f'{str(user)}님이 경고한도 {warnlimit}({warn[str(user.id)]}/{warnlimit})를 초과하여 밴됬습니다')
            await c.add_reaction('<a:yes:993087382586929183>')
        else:
            try:
                await user.send(embed=discord.Embed(title="경고 안내",description=f'당신은 경고 {number}개를 받아 경고 갯수가 {warn[str(user.id)]}/{warnlimit}가 되었어요\n경고 사유 : {reason}',color=discord.Color.red()))
            except:
                pass
            await ctx.message.add_reaction('<a:yes:993087382586929183>')
    @commands.command()
    async def warnlimit(self,ctx,limit:int):
        global warnlimit
        if not ctx.author.guild_permissions.ban_members:
            return
        with open(f"warnlimit.json", "w+", encoding='utf-8-sig') as f:
            json_string = json.dump(limit, f, indent=2, ensure_ascii=False)
        await ctx.message.add_reaction('<a:yes:993087382586929183>')
    @commands.command()
    async def checkwarn(self,ctx,user:discord.Member=None):
        if user == None:
            user = ctx.author
        jstring = open("warn.json", "r", encoding='utf-8-sig').read()
        warn = json.loads(jstring)
        jstring = open("warnlimit.json", "r", encoding='utf-8-sig').read()
        warnlimit = json.loads(jstring)
        try:
            await ctx.send(embed=embed("경고 확인",f'{str(user.name)}님의 경고는 {str(warn[str(user.id)])}/{str(warnlimit)}개입니다'))
        except:
            await ctx.send(embed=embed("경고 확인 불가",f'{str(user)}님은 경고를 받지 않았어요',discord.Color.red()))
    @commands.command()
    async def resetwarn(self,ctx,user:discord.Member):
        if not ctx.author.guild_permissions.ban_members:
            return
        jstring = open("warn.json", "r", encoding='utf-8-sig').read()
        warn = json.loads(jstring)
        del warn[str(user.id)]
        with open(f"warn.json", "w+", encoding='utf-8-sig') as f:
            json_string = json.dump(warn, f, indent=2, ensure_ascii=False)
        await ctx.message.add_reaction('<a:yes:993087382586929183>')
    @commands.command()
    async def removewarn(self,ctx,user:discord.Member,limit:int):
        if not ctx.author.guild_permissions.ban_members:
            return
        jstring = open("warn.json", "r", encoding='utf-8-sig').read()
        warn = json.loads(jstring)
        try:
            warn[str(user.id)] -= limit
            if warn[str(user.id)] < limit:
                await ctx.send(f'{str(user)}님 경고가 {limit}개 이하여서 경고를 삭제하지 못했어요')
                warn[str(user.id)] += limit
                with open(f"warn.json", "w+", encoding='utf-8-sig') as f:
                    json_string = json.dump(warn, f, indent=2, ensure_ascii=False)
                return
        except:
            await ctx.send(embed=embed("경고삭제 실패",f'{str(user)}님은 경고를 받지 않았어요'))
            return
        with open(f"warn.json", "w+", encoding='utf-8-sig') as f:
            json_string = json.dump(warn, f, indent=2, ensure_ascii=False)
        await ctx.message.add_reaction('<a:yes:993087382586929183>')
    #@commands.Cog.listener()
    async def on_message(self , message):
        if message.guild.id == 978533527928844328:
            if not self.bot.user.id == message.author.id:
                await message.guild.get_channel(994542973125664778).send(embed=embed(f"메시지 전송 로그",f"<@{message.author.id}> : {message.content}\n\n<#{message.channel.id}>에서 전송된 메시지",discord.Color.green()))
    #@commands.Cog.listener()
    async def on_message_delete(self , message):
        if message.guild.id == 978533527928844328:
            if not self.bot.user.id == message.author.id:
                await message.guild.get_channel(994542973125664778).send(embed=embed(f"메시지 삭제 로그",f"<@{message.author.id}> : {message.content}\n\n<#{message.channel.id}>에서 전송된 메시지",discord.Color.red()))
    #@commands.Cog.listener()
    async def on_message_edit(self , before, after):
        if before.guild.id == 978533527928844328:
            if not self.bot.user.id == before.author.id:
                await before.guild.get_channel(994542973125664778).send(embed=embed(f"메시지 수정 로그",f"<@{before.author.id}> : {before.content}\n==>\n<@{before.author.id}> : {after.content}\n\n<#{before.channel.id}>에서 전송된 메시지",discord.Color.orange()))
async def setup(bot):
    await bot.add_cog(Manage(bot))