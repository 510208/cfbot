# 公告頻道防多餘訊息擴充功能

import discord
from discord.ext import commands
from discord import app_commands
import logging
import yaml

logger = logging.getLogger(__name__)

COG_INTRO = {
    "name": "自動刪除",
    "description": "自動刪除指定頻道的多餘訊息（非本機器人與白名單的訊息）",
    "author": "SamHacker",
    "countributors": ["SamHacker"],
}

class Remove_Message(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = self.bot.config
        logger.info("Remove Message cog 已經載入")

    # 事件
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        # 從 self.config 中取得 'auto_delete' 區塊的設定
        # 使用 .get() 方法可以安全地取得設定，如果鍵不存在則回傳 None 或指定的預設值
        auto_delete_settings = self.config.get('auto_delete')

        if not auto_delete_settings:
            # 如果 cfg.yml 中沒有 'auto_delete' 區塊，則不執行任何操作
            # 您也可以在此處記錄一個警告
            # logger.warning("設定檔中缺少 'auto_delete' 區塊，自動刪除功能可能無法正常運作。")
            return

        # 檢查功能是否啟用、是否在指定頻道、且訊息發送者不在白名單中
        if auto_delete_settings.get('enabled', False) and \
           message.channel.id in auto_delete_settings.get('channel_id', []) and \
           message.author.id not in auto_delete_settings.get('whitelist', []):

            # 如果設定要私訊通知，且訊息不是由機器人自己發出的
            if auto_delete_settings.get('dm', False) and message.author != self.bot.user:
                dm_content_template = auto_delete_settings.get('dm_content', "您在 {guild} 發送的訊息已被自動刪除。")
                try:
                    msg = dm_content_template.format(
                        member=message.author.mention,
                        member_name=message.author.name,
                        guild=message.guild.name,
                        message=message.content
                    )
                    await message.author.send(msg)
                    logger.info(f"已私訊 {message.author.name} 關於在 {message.guild.name} 的訊息被自動刪除。")
                except discord.Forbidden:
                    logger.warning(f"無法私訊 {message.author.name} (ID: {message.author.id})，可能對方關閉了私訊。")
                except KeyError as e:
                    logger.error(f"私訊內容模板格式錯誤，缺少鍵：{e}。模板：'{dm_content_template}'")
                except Exception as e:
                    logger.error(f"私訊 {message.author.name} 時發生未預期錯誤: {e}")
            try:
                await message.delete()
                logger.info(f"已自動刪除 {message.author.name} 在 {message.guild.name} 的頻道 {message.channel.name} 中的訊息。")
            except discord.Forbidden:
                logger.error(f"無法刪除訊息於頻道 {message.channel.name} (ID: {message.channel.id})。機器人可能缺乏 '管理訊息' 權限。")
            except discord.NotFound:
                logger.warning(f"嘗試刪除訊息 (ID: {message.id}) 時未找到該訊息，可能已被手動刪除。")
            except Exception as e:
                logger.error(f"刪除訊息時發生未預期錯誤: {e}")

async def setup(bot):
    if not bot.config.get("auto_delete", {}).get("enable", False):
        logger.info(f"跳過載入 {COG_INTRO['name']}，因為它被禁用。")
        return
    await bot.add_cog(Remove_Message(bot))
    logger.info(f"{COG_INTRO['name']} 已經註冊")