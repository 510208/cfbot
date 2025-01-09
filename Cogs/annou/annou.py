# 公告擴充功能

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

logger = logging.getLogger(__name__)

COG_INTRO = {
    "name": "公告系統",
    "description": "用於公告設定的擴充功能"
}

# 讀取設定檔
with open("cfg.yml", "r", encoding="utf-8") as file:
    cfg = yaml.safe_load(file)

class UpdateModal(discord.ui.Modal, title = "發送更新公告"):
    # 導言
    intro = ui.TextInput(
        label = "公告引言 (0~200字內)",
        style = discord.TextStyle.paragraph,
        placeholder = "請輸入公告引言，留空行將採用預設值",
        min_length = 0,
        max_length = 200,
        required = False
    )

    # 更新內容
    content = ui.TextInput(
        label = "更新內容",
        style = discord.TextStyle.paragraph,
        placeholder = "請輸入更新詳細內容，一行一個項目",
        required = True,
        custom_id = "content"
    )

    async def on_submit(self, ctx: discord.Interaction):
        if ctx.user.id not in BOT_ADMIN:
            await ctx.response.send_message("你沒有權限使用此機器人", ephemeral = True)
            return
        if self.content.value == "":
            await ctx.response.send_message("更新內容不可為空", ephemeral = True)
            return
        if self.intro.value == "":
            self.intro_value = """
太棒了！我們伺服器又更新了~~
快來看看這次我們又更新了些啥吧，快點喔！
"""
        else:
            self.intro_value = self.intro.value
        upd = UpdateMsgGen(
            intro = self.intro_value,
            content = self.content.value.split("\n"),
            starter = ctx.user.id
        )
        await ctx.channel.guild.get_channel(cfg["annou_channel_id"]).send(upd.text)
        await ctx.response.send_message("公告已發布", ephemeral = True)

class FixModal(discord.ui.Modal, title = "發送修復公告"):
    # 導言
    intro = ui.TextInput(
        label = "公告引言 (0~200字內)",
        style = discord.TextStyle.paragraph,
        placeholder = "請輸入公告引言，留空行將採用預設值",
        min_length = 0,
        max_length = 200,
        required = False
    )

    # 修復內容
    content = ui.TextInput(
        label = "更新內容",
        style = discord.TextStyle.paragraph,
        placeholder = "請輸入更新詳細內容，一行一個項目",
        required = True,
        custom_id = "content"
    )

    # 修復原因
    reason = ui.TextInput(
        label = "修復原因",
        style = discord.TextStyle.paragraph,
        placeholder = "請輸入修復原因",
        required = True,
        custom_id = "reason"
    )

    # 開始時間
    begin_time = ui.TextInput(
        label = "開始時間",
        style = discord.TextStyle.paragraph,
        placeholder = "請輸入開始時間，格式為YYYY-MM-DD HH:MM",
        required = True,
        custom_id = "begin_time"
    )

    # 結束時間
    end_time = ui.TextInput(
        label = "結束時間",
        style = discord.TextStyle.paragraph,
        placeholder = "請輸入結束時間，格式為YYYY-MM-DD HH:MM",
        required = False,
        custom_id = "end_time"
    )

    async def on_submit(self, ctx: discord.Interaction):
        if ctx.user.id not in BOT_ADMIN:
            await ctx.response.send_message("你沒有權限使用此機器人", ephemeral = True)
            return
        if self.content.value == "":
            await ctx.response.send_message("更新內容不可為空", ephemeral = True)
            return
        if self.reason.value == "":
            self.reason_value = "未知原因"
        else:
            self.reason_value = self.reason.value
        if re.match(pattern = r"[0-9]*4-[0-9][1-9]-[0-9][1-9] [0-2][0-9]:[0-5][0-9]", string = self.begin_time.value):
            self.begin_time_value = self.begin_time.value + ":00"
            self.begin_time_unix = int(datetime.datetime.strptime(self.begin_time_value, "%Y-%m-%d %H:%M:%S").timestamp())
            self.begin_time_unix = f"<t:{self.begin_time_unix}:F>"
        else:
            logger.error("開始時間格式錯誤")
            await ctx.response.send_message("<:dangerous:1254019093900558397> 開始時間格式錯誤，請重新輸入", ephemeral = True)
            return
        if re.match(pattern = r"[0-9]*4-[0-9][1-9]-[0-9][1-9] [0-2][0-9]:[0-5][0-9]", string = self.end_time.value):
            self.end_time_value = self.end_time.value + ":00"
            self.end_time_unix = int(datetime.datetime.strptime(self.end_time_value, "%Y-%m-%d %H:%M:%S").timestamp())
            self.end_time_unix = f"<t:{self.end_time_unix}:F>"
        elif self.end_time.value == "":
            self.end_time_unix = "還未排定"
        else:
            logger.error("結束時間格式錯誤")
            await ctx.response.send_message("<:dangerous:1254019093900558397> 結束時間格式錯誤，請重新輸入", ephemeral = True)
            return
        if self.intro.value == "":
            self.intro_value = """
太棒了！我們伺服器又更新了~~
快來看看這次我們又更新了些啥吧，快點喔！
"""
        else:
            self.intro_value = self.intro.value
        upd = FixMsgGen(
            intro = self.intro_value,
            content = self.content.value.split("\n"),
            reason = self.reason_value,
            time = {
                "begin": self.begin_time_unix,
                "end": self.end_time_unix
            },
            starter = ctx.user.id
        )

        await ctx.channel.guild.get_channel(cfg["annou_channel_id"]).send(upd.text)
        await ctx.response.send_message("公告已發布", ephemeral = True)

class Annou(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        logger.info("Annou cog 已經載入")

    g_annou = app_commands.Group(
        name = "公告系統",
        description = "此群組包含了公告系統與其相關指令"
    )

    @g_annou.command(
        name = "更新公告",
        description = "發送一則更新公告至設定的頻道，採用表單模態框"
    )
    async def update_annou(self, ctx: discord.Interaction):
        logging.info('發布更新公告')
        logging.info(f'請求發起人：{ctx.user}')
        if ctx.user.id not in BOT_ADMIN:
            await ctx.response.send_message('你沒有權限使用此機器人', ephemeral=True)
            return
        await ctx.response.send_modal(UpdateModal())
    
    @g_annou.command(
        name = "修復公告",
        description = "發送一則修復公告至設定的頻道，採用表單模態框"
    )
    async def fix_annou(self, ctx: discord.Interaction):
        logging.info('發布修復公告')
        logging.info(f'請求發起人：{ctx.user}')
        if ctx.user.id not in BOT_ADMIN:
            await ctx.response.send_message('你沒有權限使用此機器人', ephemeral=True)
            return
        await ctx.response.send_modal(FixModal())

async def setup(bot):
    await bot.add_cog(Annou(bot))
    logger.info(f"{COG_INTRO['name']} 已經註冊")