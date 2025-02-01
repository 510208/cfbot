import logging
import discord
from discord.ext import commands
import yaml

logger = logging.getLogger(__name__)

COG_INTRO = {
    "name": "取得身分組",
    "description": "使用反應身分組、配置視圖等方式讓使用者取得身分組。",
    "author": "SamHacker",
    "countributors": ["SamHacker"],
}

with open('cfg.yml', "r", encoding="utf-8") as file:
    config = yaml.safe_load(file).get("reaction_roles", {})
    reactions: list = config.get("reactions", [])

class ReactionRules(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logger.info(f"{COG_INTRO["name"]} 已加載！")
        # 檢查目標訊息是否有設定的Emoji，若沒有就加上
        message = await self.bot.get_channel(config.get("channel_id")).fetch_message(config.get("message_id"))
        # 取得訊息中所有的Emoji
        reactions = [reaction.emoji for reaction in message.reactions]
        # 將reactions中所有項目的emoji鍵值取出
        reactions = [reaction.get("emoji") for reaction in reactions]
        # 檢查是否有缺少的Emoji
        for emoji in config.get("roles").keys():
            if emoji not in reactions:
                await message.add_reaction(emoji)
                logger.info(f"已新增 {emoji} Emoji 到訊息中。")

    # 反應身分組
    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        # 檢查是否為機器人自己的反應
        if user.bot:
            return
        # 檢查是否為指定的訊息
        if reaction.message.id != config.get("role_message_id"):
            return
        # 檢查是否為指定的Emoji
        if reaction.emoji not in config.get("roles").keys():
            return
        # 取得身分組
        role = reaction.message.guild.get_role(config.get("roles")[reaction.emoji])
        # 給予身分組
        await user.add_roles(role)
        logger.info(f"{user} 取得了 {role} 身分組。")

    # 在使用者移除反應時移除身分組
    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction, user):
        # 檢查是否為機器人自己的反應
        if user.bot:
            return
        # 檢查是否為指定的訊息
        if reaction.message.id != config.get("role_message_id"):
            return
        # 檢查是否為指定的Emoji
        if reaction.emoji not in config.get("roles").keys():
            return
        # 檢查配置檔是否啟用此項功能
        if not config.get("remove_role_on_reaction_remove", False):
            return
        # 取得身分組
        role = reaction.message.guild.get_role(config.get("roles")[reaction.emoji])
        # 移除身分組
        await user.remove_roles(role)
        logger.info(f"{user} 移除了 {role} 身分組。")

async def setup(bot):
    if not config.get("enabled", True):
        logger.info(f"跳過載入 {COG_INTRO["name"]}，因為它被禁用。")
        return
    await bot.add_cog(ReactionRules(bot))