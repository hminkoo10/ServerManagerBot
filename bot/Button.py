from discord.ui import Button
import discord
from discord import ButtonStyle
from discord.ext import commands
import random
import datetime
import requests
import json
import discord_components


# 임배드 함수
def embed(title, description, color=random.randint(0x000000, 0xFFFFFF)):
    return discord.Embed(title=title, description=description, color=color)


class Button(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def elevator(self, ctx):
        #이쪽 에러
        #label 오류
        b2 = discord.ui.Button(label="B2", style=discord.ButtonStyle.green, custom_id="B2")  # 라벨이 버튼 이름임
        b1 = discord.ui.Button(label="B1", style=discord.ButtonStyle.green, custom_id="B1")
        _1 = discord.ui.Button(label="1F", style=discord.ButtonStyle.green, custom_id="1F")
        _2 = discord.ui.Button(label="2F", style=discord.ButtonStyle.green, custom_id="2F")
        _3 = discord.ui.Button(label="3F", style=discord.ButtonStyle.green, custom_id="3F")
        _4 = discord.ui.Button(label="4F", style=discord.ButtonStyle.green, custom_id="4F")
        _5 = discord.ui.Button(label="5F", style=discord.ButtonStyle.green, custom_id="5F")
        ph = discord.ui.Button(label="PH", style=discord.ButtonStyle.green, custom_id="PH")
        await ctx.send(content="elevator",components=[[b1, b2, _1, _2, _3, _4, _5, ph]])


async def setup(bot):
    await bot.add_cog(Button(bot))
