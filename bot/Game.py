import discord
from discord.ext import commands
import os
import asyncio
import random
def embed(title, description, color=random.randint(0x000000, 0xFFFFFF)):
    return discord.Embed(title=title, description=description, color=color)
class Game(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def 업다운(self,ctx):
        rn = random.randint(1,100)
        
        count = 0
        await ctx.reply(embed=embed("업다운게임","봇이 1부터 100까지의 숫자를 정했습니다! 정해진 기회는 7번이고 그중 봇이 정한 숫자를 맞춰주세요!\n[제한시간 15초]"))
        for i in range(7):
            try:
                msg = await self.bot.wait_for('message', check=lambda message: message.author == ctx.author,timeout=15)
            except asyncio.TimeoutError:
                return await ctx.reply(embed=embed("게임 실패",f"<@{ctx.author.id}>님, 제안시간안에 게임을 성공하지 못했습니다...",discord.Color.red()))
            await msg.delete()
            try:
                test = int(msg.content)
            except:
                await ctx.reply(embed=embed("경고","숫자로 입력하세요.",discord.Color.gold()))
            try:
                if int(msg.content) == rn:
                    return await ctx.reply(embed=embed("게임 성공",f"<@{ctx.author.id}>님, 적중했어요! 봇이 선택한 숫자는 {rn}였습니다!\n[{count}번만에 맞추셨어요]",discord.Color.green()))
                elif int(msg.content) > rn:
                    i = 7 - count - 1
                    if i == 0:
                        return await ctx.reply(embed=embed("게임 실패",f"<@{ctx.author.id}>님, 7번 안에 숫자를 맞추지 못했어요.",discord.Color.red()))
                    await ctx.reply(embed = embed("다운!",f"기회가 {i}번 남음.\n[입력한 수 : {msg.content}]"),delete_after=10)
                elif int(msg.content) < rn:
                    i = 7 - count - 1
                    if i == 0:
                        return await ctx.reply(embed=embed("게임 실패",f"<@{ctx.author.id}>님, 7번 안에 숫자를 맞추지 못했어요.",discord.Color.red()))
                    await ctx.reply(embed = embed("업!",f"기회가 {i}번 남음.\n[입력한 수 : {msg.content}]"),delete_after=10)
                count += 1
            except:
                pass

async def setup(bot):
    await bot.add_cog(Game(bot))