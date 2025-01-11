# 歡迎訊息擴充功能

import discord
from discord.ext import commands
from discord import app_commands
import logging
import yaml

with open('cfg.yml', "r", encoding="utf-8") as file:
    config = yaml.safe_load(file)

logger = logging.getLogger(__name__)

COG_INTRO = {
    "name": "歡迎訊息",
    "description": "歡迎新使用者加入 Discord 伺服器的訊息"
}

class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        logger.info("Welcome cog 已經載入")

    # 事件
    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        logger.info(f'{member} 加入了伺服器')
        channel_id = config['welcome_channel_id']
        # 取得頻道
        channel = member.guild.get_channel(channel_id)
        # 傳送訊息
        fmt = config['welcome_message'].format(
            member = member.mention,
            member_name = member.name,
            guild = member.guild.name,
            member_count = len(member.guild.members),
            member_id = member.id,
            member_created_at = member.created_at,
            member_joined_at = member.joined_at,
            member_avatar = member.avatar.url
        )
        embed = discord.Embed(
            title = config['welcome_title'],
            description = fmt,
            color = discord.Color.green()
        )
        embed.set_thumbnail(url=member.avatar.url)
        await channel.send(embed=embed)
    
    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        logger.info(f'{member} 離開了伺服器')
        channel_id = config['leave_channel_id']
        # 取得頻道
        channel = member.guild.get_channel(channel_id)
        # 傳送訊息
        fmt = config['leave_message'].format(
            member = member.mention,
            member_name = member.name,
            guild = member.guild.name,
            member_count = len(member.guild.members),
            member_id = member.id,
            member_created_at = member.created_at,
            member_joined_at = member.joined_at,
            member_avatar = member.avatar.url
        )
        embed = discord.Embed(
            title = config["leave_title"],
            description = fmt,
            color = discord.Color.red()
        )
        embed.set_thumbnail(url=member.avatar.url)
        await channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Welcome(bot))
    logger.info(f"{COG_INTRO['name']} 已經註冊")