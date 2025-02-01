import logging
import discord
from discord.ext import commands
import yaml
import os
import inspect
from typing import Union

logger = logging.getLogger(__name__)

# 切換工作目錄至父目錄
# 獲取引入此檔案的檔案（通常是 main.py）
caller_file = inspect.stack()[-1].filename  # 最底層的調用者
caller_dir = os.path.dirname(os.path.abspath(caller_file))  # 取得 main.py 所在的資料夾

# 設定工作目錄為 main.py 所在的資料夾
os.chdir(caller_dir)

COG_INTRO = {
    "name": "取得身分組",
    "description": "使用反應身分組、配置視圖等方式讓使用者取得身分組。",
    "author": "SamHacker",
    "countributors": ["SamHacker"],
}

with open('cfg.yml', "r", encoding="utf-8") as file:
    config = yaml.safe_load(file).get("reaction_roles", {})
    logger.info(f"載入 {COG_INTRO['name']} 設定：{config}")
    reactions: list = config.get("reactions", [])
    logger.info(f"載入 {COG_INTRO['name']} 設定：{reactions}")

class ReactionRules(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logger.info(f"{COG_INTRO['name']} 已加載！")
        # 檢查目標訊息是否有設定的Emoji，若沒有就加上
        message = await self.bot.get_channel(config.get("role_channel_id")).fetch_message(config.get("role_message_id"))
        # 取得訊息中所有的Emoji
        msg_emoji = [reaction.emoji for reaction in message.reactions]
        logger.info(f"訊息中的 Emoji：{msg_emoji}")
        # 將reactions中所有項目的emoji鍵值取出
        reaction_emojis = [entry["emoji"] for entry in reactions]
        logger.info(f"設定中的 Emoji：{reaction_emojis}")
        # 檢查設定的Emoji是否不存在
        # 檢查是否有缺少的Emoji
        for emoji in reaction_emojis:
            if emoji not in msg_emoji:
                await message.add_reaction(emoji)
                logger.info(f"訊息中沒有的 Emoji：{emoji}")
        # # 檢查是否有多餘的Emoji
        # for emoji in msg_emoji:
        #     if emoji not in reaction_emojis:
        #         await message.clear_reaction(emoji)
        #         logger.info(f"訊息中多餘的 Emoji：{emoji}")

    # 反應身分組
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        logger.info(f"{payload.user_id} 反應了 {payload.emoji}。")
        # 檢查是否為機器人自己的反應
        if payload.user_id == self.bot.user.id:
            return
        # 檢查是否為指定的訊息
        if payload.message_id != config.get("role_message_id"):
            return
        # 檢查是否為指定的Emoji
        for reaction in reactions:
            if str(payload.emoji) == reaction["emoji"]:
                # 取得身分組
                guild = self.bot.get_guild(payload.guild_id)
                role = guild.get_role(reaction["role_id"])
                member = guild.get_member(payload.user_id)
                # 給予身分組
                await member.add_roles(role)
                logger.info(f"{member} 取得了 {role} 身分組。")
                break

    # 在使用者移除反應時移除身分組
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
        logger.info(f"{payload.user_id} 移除了 {payload.emoji}。")
        # 檢查是否為機器人自己的反應
        if payload.user_id == self.bot.user.id:
            return
        # 檢查是否為指定的訊息
        if payload.message_id != config.get("role_message_id"):
            return
        # 檢查是否為指定的Emoji
        for reaction in reactions:
            if str(payload.emoji) == reaction["emoji"]:
                # 檢查配置檔是否啟用此項功能
                if not config.get("remove_role_on_reaction_remove", False):
                    return
                # 取得身分組
                guild = self.bot.get_guild(payload.guild_id)
                role = guild.get_role(reaction["role_id"])
                member = guild.get_member(payload.user_id)
                # 移除身分組
                await member.remove_roles(role)
                logger.info(f"{member} 移除了 {role} 身分組。")
                break

async def setup(bot):
    if not config.get("enabled", True):
        logger.info(f"跳過載入 {COG_INTRO['name']}，因為它被禁用。")
        return
    # logger.info(f"目前工作目錄：{os.getcwd()}")
    await bot.add_cog(ReactionRules(bot))