# Pterodactyl 玩家資訊查詢功能

import discord
from discord.ext import commands
from discord import app_commands
import logging
import yaml
from pydactyl import PterodactylClient
from plugins.discordcore import *
import re
from discord.ext import tasks

with open('cfg.yml', "r", encoding="utf-8") as file:
    config = yaml.safe_load(file)["ptersearch"]
    taskCfg = config["upd_task"]

logger = logging.getLogger(__name__)

COG_INTRO = {
    "name": "玩家綁定搜尋",
    "description": "搜尋經 DiscordSRV 插件綁定的玩家資訊，並以本地 SQLite 資料庫座快取"
}

api = PterodactylClient(config["api_url"], config["api_key"], debug=True)

class PteroSearch(commands.Cog):
    s = app_commands.Group(
        name = "search",
        description = "查詢玩家資訊"
    )

    @s.command(
        name = "自對端抓取帳號設定",
        description = "前往 Pterdactyl 伺服器下載並同步玩家資訊"
    )
    async def sync(self, interaction: discord.Interaction):
        """前往 Pterdactyl 伺服器下載並同步玩家資訊"""
        dcs = dcSearcher(config["api_url"], config["api_key"], config["db_path"])
        try:
            await dcs.syncDcsrv()
            await interaction.response.send_message("<a:INFO:1193029532739960943> | 同步完成")
        except Exception as e:
            logger.error(f"同步失敗：{e}")
            await interaction.response.send_message("<a:ERROR:1193029541301860353> | 同步失敗，請查看日誌\n```\n"+str(e)+"\n```")

    @s.command(
        name = "藉discord查詢",
        description = "使用 Discord ID 查詢玩家資訊"
    )
    async def connectInfoByMC(self, interaction: discord.Interaction, dc_member: discord.Member):
        """使用 Discord ID 查詢玩家 Minecraft 資訊

        Parameters
        -----------
        member: discord.Member
            要查詢的玩家 Discord 帳號
        """
        dcs = dcSearcher(config["api_url"], config["api_key"], config["db_path"])
        try:
            b = dcs.getBindInfo(
                dc_id = dc_member.id
            )
        except Exception as e:
            logger.error(f"查詢失敗：{e}")
            await interaction.response.send_message("<a:ERROR:1193029541301860353> | 查詢失敗，請查看日誌\n\n```\n"+str(e)+"\n```")
            return
        
        # 檢查傳回值是否為字典
        if not(isinstance(b, dict)):
            await interaction.response.send_message("<a:ERROR:1193029541301860353> | 傳回值格式錯誤：\n預期格式為 DICT，但傳回以下結果：\n\n```\n"+b+"\n```")
            return
        
        # 檢查是否有找到玩家
        if b["mc_class"] == None or not isinstance(b["mc_class"], playerInfo):
            await interaction.response.send_message(f"<a:ERROR:1193029541301860353> | 找不到玩家或傳回值格式錯誤，\n若您確定有此名玩家，請檢查日誌\n收到的查詢：{str(dc_member.id)}\n收到的參數：\n```\n"+str(b)+"\n```")
            return
        
        player: playerInfo = b["mc_class"]
        await player.get()
        embed = discord.Embed(title=f"玩家資訊查詢結果：{dc_member.name}", description="以下是您的請求結果", color=0x718e73)
        embed.set_author(name=player.playerName, icon_url=player.avatarUrl)
        embed.set_thumbnail(url=player.bodyUrl)
        embed.add_field(name="玩家 Minecraft 名稱", value=player.playerName, inline=False)
        embed.add_field(name="玩家 Minecraft UUID", value=player.playerUUID, inline=False)
        embed.add_field(name="玩家 Discord ID", value=dc_member.mention, inline=False)
        embed.set_image(url=player.isometricAvatarUrl)
        await interaction.response.send_message(embed=embed)

    async def getPlayerUUID(self, playerName: str):
        """取得玩家 UUID

        Parameters
        -----------
        playerName: str
            玩家名稱
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://api.mojang.com/users/profiles/minecraft/{playerName}") as response:
                return await response.json()["id"]

    @s.command(
        name = "藉minecraft查詢",
        description = "使用麥塊帳號查詢玩家資訊"
    )
    async def connectInfoByMC(self, interaction: discord.Interaction, mc_info: str):
        """使用 Minecraft UUID 查詢玩家 Minecraft 綁定資訊

        Parameters
        -----------
        mc_info: discord.Member
            要查詢的玩家 Minecraft UUID 或名稱（建議輸入 UUID）
        """
        playerUUID = None
        # 檢查使用者輸入的是 UUID 還是名稱
        if not re.match(r"/([0-9a-f]{8})(?:-|)([0-9a-f]{4})(?:-|)(4[0-9a-f]{3})(?:-|)([89ab][0-9a-f]{3})(?:-|)([0-9a-f]{12})/", mc_info.lower()):
            # 使用的是名稱
            # 取得玩家 UUID
            playerUUID = await self.getPlayerUUID(mc_info)
            playerUUID = f"{playerUUID[:8]}-{playerUUID[8:12]}-{playerUUID[12:16]}-{playerUUID[16:20]}-{playerUUID[20:]}"
        else:
            # 使用的是 UUID
            # 檢查 UUID 有無減號
            if "-" in mc_info:
                playerUUID = mc_info
            else:
                playerUUID = f"{mc_info[:8]}-{mc_info[8:12]}-{mc_info[12:16]}-{mc_info[16:20]}-{mc_info[20:]}"
            
        dcs = dcSearcher(config["api_url"], config["api_key"], config["db_path"])
        b = await dcs.getBindInfo(
            mc_uuid = playerUUID
        )
        # 檢查傳回值是否為字典
        if not(isinstance(b, dict)):
            await interaction.response.send_message("<a:ERROR:1193029541301860353> | 傳回值格式錯誤：\n預期格式為 DICT，但傳回以下結果：\n\n```\n"+b+"\n```")
            return
        
        # 檢查是否有找到玩家
        if b["mc_class"] == None or not isinstance(b["mc_class"], playerInfo):
            await interaction.response.send_message(f"<a:ERROR:1193029541301860353> | 找不到玩家或傳回值格式錯誤，\n若您確定有此名玩家，請檢查日誌\n收到的查詢：{mc_info}\n收到的參數：\n```\n"+str(b)+"\n```")
            return
        
        player: playerInfo = b["mc_class"]
        playerDcId = b["dc_id"]
        playerDc: discord.Member = await interaction.guild.fetch_member(playerDcId)
        await player.get()
        embed = discord.Embed(title=f"玩家資訊查詢結果：{player.playerName}", description="以下是您的請求結果", color=0x718e73)
        embed.set_author(name=player.playerName, icon_url=player.avatarUrl)
        embed.set_thumbnail(url=player.bodyUrl)
        embed.add_field(name="玩家 Discord ID", value=playerDc.mention, inline=False)
        embed.add_field(name="玩家 Minecraft 名稱", value=player.playerName, inline=True)
        embed.add_field(name="玩家 Minecraft UUID", value=player.playerUUID, inline=True)
        embed.set_image(url=playerDc.avatar.url)
        await interaction.response.send_message(embed=embed)

    # 定義排程
    @tasks.loop(
        hours = taskCfg["interval"]["hours"],
        minutes = taskCfg["interval"]["minutes"],
        seconds = taskCfg["interval"]["seconds"]
    )
    async def syncDcSrv(self):
        if not taskCfg["enabled"]:
            logger.info("PterSearch 模組排程同步功能已禁用，不執行同步任務")
            return
        logger.info("PterSearch 模組排程同步功能已啟用，正在執行同步任務")
        dcs = dcSearcher(config["api_url"], config["api_key"], config["db_path"])
        await dcs.syncDcsrv()
        logger.info("PterSearch 模組排程同步功能已完成同步任務")

async def setup(bot):
    if not(config["enabled"]):
        logger.info("載入 PterSearch 模組失敗，原因：在配置文件中停用了此模組")
        return
    await bot.add_cog(PteroSearch(bot))
    if taskCfg["enabled"]:
        logger.warning("PterSearch 模組附加功能：排程同步 已啟用")
        logger.warning(f"排程同步設定：每 {taskCfg['hours']} 小時 {taskCfg['minutes']} 分鐘 {taskCfg['seconds']} 秒")
        logger.warning("請確保您面板端的伺服器已啟用 API 功能，並且此設定不會逾越 API 限制，否則系統將可能崩潰！")
    logger.info(f"{COG_INTRO['name']} 已經註冊")