# 公告頻道防多餘訊息擴充功能

import discord
from discord.ext import commands
from discord import app_commands
import logging
import yaml

with open('cfg.yml', "r", encoding="utf-8") as file:
    config = yaml.safe_load(file)

logger = logging.getLogger(__name__)

COG_INTRO = {
    "name": "自動刪除",
    "description": "自動刪除指定頻道的多餘訊息（非本機器人與白名單的訊息）"
}

class Remove_Message(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        logger.info("Remove Message cog 已經載入")

    # 事件
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.channel.id in config['auto_delete']['channel_id'] and \
            message.author.id not in config['auto_delete']['whitelist'] and \
                config['auto_delete']['enabled']:
            if config['auto_delete']['dm'] and message.author != self.bot.user:
                msg = config['auto_delete']['dm_content'].format(
                    member=message.author.mention,
                    member_name=message.author.name,
                    guild=message.guild.name,
                    message=message.content
                )
                await message.author.send(msg)
                logger.info(f"已經私訊 {message.author.name} 關於在 {message.guild.name} 的訊息")
            await message.delete()
            logger.info(f"已經刪除 {message.author.name} 在 {message.guild.name} 的訊息")

async def setup(bot):
    await bot.add_cog(Remove_Message(bot))
    logger.info(f"{COG_INTRO['name']} 已經註冊")