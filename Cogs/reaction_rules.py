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
    config = yaml.safe_load(file).get("my_awesome_cog", {})

class MyAwesomeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logger.info("MyAwesomeCog 已加載！")

async def setup(bot):
    if not config.get("enabled", True):
        logger.info("跳過載入 MyAwesomeCog，因為它被禁用。")
        return
    await bot.add_cog(MyAwesomeCog(bot))