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
    reactions = config.get("reactions", {})

class ReactionRules(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logger.info(f"{COG_INTRO["name"]} 已加載！")
        # 檢查目標訊息是否有設定的Emoji，若沒有就加上
        message = await self.bot.get_channel(config.get("channel_id")).fetch_message(config.get("message_id"))
        

    # 反應身分組
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if not config.get("enabled", True):
            return
        if payload.message_id == config.get("message_id"):
            guild = self.bot.get_guild(payload.guild_id)
            member = guild.get_member(payload.user_id)
            if member.bot:
                return
            role = discord.utils.get(guild.roles, name=config.get("roles").get(str(payload.emoji)))
            await member.add_roles(role)

async def setup(bot):
    if not config.get("enabled", True):
        logger.info(f"跳過載入 {COG_INTRO["name"]}，因為它被禁用。")
        return
    await bot.add_cog(ReactionRules(bot))