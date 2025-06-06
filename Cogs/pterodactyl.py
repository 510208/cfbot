# Pterodactyl 遊戲內輔助功能

import discord
from discord.ext import commands
from discord import app_commands
import logging
import yaml
from pydactyl import PterodactylClient
from mcsmapi import MCSMAPI

logging.getLogger('pydactyl').setLevel(logging.INFO)
logger = logging.getLogger(__name__)

COG_INTRO = {
    "name": "翼手龍面版輔助控制",
    "description": "控制採用翼手龍面版（Pterdactyl）的伺服器",
    "author": "SamHacker",
    "countributors": ["SamHacker"],
}

class PteroManager(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.config = bot.config.get("pterodactyl", {})
        if not self.config:
            logger.warning("Pterodactyl 模組未啟用，請在配置文件中啟用")
        elif not self.config.get("enabled", False):
            logger.info("載入 Pterodactyl 模組失敗，原因：在配置文件中停用了此模組")

        # 嘗試載入配置
        try:
            self.api = PterodactylClient(self.config["api_url"], self.config["api_key"])
        except KeyError as e:
            logger.error(f"找不到必要的配置項目：{e}")
            return
        logger.info("Pterodactyl 已經載入")

    pt = app_commands.Group(
        name = "pterodactyl",
        description = "Pterodactyl 遊戲內輔助功能"
    )

    # 定義電源選項相關
    pwr = app_commands.Group(
        name = "電源管理",
        description = "電源管理",
        parent=pt
    )
    @pwr.command(
        name = "開機",
        description = "開啟伺服器",
    )
    async def start(self, ctx: discord.Interaction):
        await ctx.response.send_message("<a:cpuerror:1193057058484924416> 正在開啟伺服器")
        server = self.api.client.servers.send_power_action(self.config["server_id"], "start")
        await ctx.channel.send("<a:INFO:1193029532739960943> 伺服器已經開啟")
        await ctx.channel.send(f"傳回值：\n```\n{server}\n```")

    @pwr.command(
        name = "關機",
        description = "關閉伺服器",
    )
    async def stop(self, ctx: discord.Interaction):
        await ctx.response.send_message("<a:cpuerror:1193057058484924416> 正在關閉伺服器")
        server = self.api.client.servers.send_power_action(self.config["server_id"], "stop")
        await ctx.channel.send("<a:INFO:1193029532739960943> 伺服器已經關閉")
        await ctx.channel.send(f"傳回值：\n```\n{server}\n```")
    
    @pwr.command(
        name = "重啟",
        description = "重啟伺服器",
    )
    async def restart(self, ctx: discord.Interaction):
        await ctx.response.send_message("<a:cpuerror:1193057058484924416> 正在重啟伺服器")
        server = self.api.client.servers.send_power_action(self.config["server_id"], "restart")
        await ctx.channel.send("<a:INFO:1193029532739960943> 伺服器已經重啟")
        await ctx.channel.send(f"傳回值：\n```\n{server}\n```")
    
    @pwr.command(
        name = "強制關機",
        description = "強制關閉伺服器",
    )
    async def kill(self, ctx: discord.Interaction):
        await ctx.response.send_message(":skull: 如果強制關閉伺服器，可能會導致數據丟失，確定要繼續嗎？(請在十秒以內回覆`確定`或`yes`以確認，否則操作將會取消)")
        def _check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel
        msg = await self.bot.wait_for('message', check=_check, timeout=10)
        if msg.content == "確定" or msg.content == "yes":
            await ctx.channel.send("<a:cpuerror:1193057058484924416> 正在強制關閉伺服器")
            server = self.api.client.servers.send_power_action(self.config["server_id"], "kill")
            await ctx.channel.send("<a:INFO:1193029532739960943> 伺服器已經強制關閉")
            await ctx.channel.send(f"傳回值：\n```\n{server}\n```")
        else:
            await ctx.channel.send("<a:cpuerror:1193057058484924416> 操作已經取消")

async def setup(bot):
    if not bot.config.get("pterodactyl", {}).get("enable", False):
        logger.info(f"跳過載入 {COG_INTRO['name']}，因為它被禁用。")
        return
    await bot.add_cog(PteroManager(bot))
    logger.info(f"{COG_INTRO['name']} 已經註冊")