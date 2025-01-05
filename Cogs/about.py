# 關於

import discord
from discord.ext import commands
from discord import app_commands
import discord.ui as ui
import yaml
import logging
from main import BOT_ADMIN
from nltemplates import *
import re
import datetime
import plugins.const_codes as const_codes

logger = logging.getLogger(__name__)

COG_INTRO = {
    "name": "關於",
    "description": "關於專案（不能移除）"
}

# 讀取設定檔
with open("cfg.yml", "r", encoding="utf-8") as file:
    cfg = yaml.safe_load(file)

class About(commands.Cog):
    @app_commands.command(name='關於')
    async def about(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title = "關於",
            description = "一款開放原始碼的 Discord 機器人，透過 Python 搭建，並使用 [GNU v3.0 License](https://github.com/510208/yunyubot-dc-annou/blob/0cd1caf148e00f15ce42c84b79013b84e4dfd30e/LICENSE) 授權\n由插件師兼伺服器工程師SamHacker搭建",
            color = 0x00ff00
        )
        embed.add_field(
            name = "作者",
            value = "SamHacker"
        )
        embed.add_field(
            name = "版本",
            value = cfg["version"]
        )
        embed.add_field(
            name = "授權條款",
            value = "GNONE GNU General Public License v3.0"
        )
        embed.add_field(
            name = "原始碼",
            value = f"[GitHub](https://github.com/510208/{const_codes.REPO_NAME})"
        )
        # 設定大頭貼
        embed.set_thumbnail(url="https://gravatar.com/avatar/f7598bd8d4aba38d7219341f81a162fc842376b3b556b1995cbb97271d9e2915?s=256")
        # 設定頁尾
        embed.set_footer(text="© 2021 SamHacker")
        # 附加一張圖片，位置在main.py的同一層目錄下resources資料夾中
        file = discord.File("resources/cover.png", filename="cover.png")
        embed.set_image(url="attachment://cover.png")
        await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(About(bot))
    logger.info(f"{COG_INTRO['name']} 已經註冊")