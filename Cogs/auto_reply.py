# 自動回覆擴充功能

import discord
from discord.ext import commands
from discord import app_commands
import logging
import yaml
import re

# with open('cfg.yml', "r", encoding="utf-8") as file:
#     config = yaml.safe_load(file)["auto_reply"]
#     ignore = config['ignore_rules']
#     rules = config['rules']

logger = logging.getLogger(__name__)

COG_INTRO = {
    "name": "自動回覆",
    "description": "自動回覆指定關鍵字的訊息",
    "author": "SamHacker",
    "countributors": ["SamHacker"],
}

class Auto_Reply(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = self.bot.config.get("auto_reply", {})
        self.ignore = self.config.get("ignore_rules", {})
        self.rules = self.config.get("rules", [])
        logger.info("Auto Reply cog 已經載入")

    def _format_response(self, rule_response, message):
        """格式化自動回覆的訊息內容。

        此方法會取用一個包含預留位置的回覆樣板字串 (`rule_response`)
        以及觸發此回覆的 Discord 訊息物件 (`message`)，
        並將樣板中的預留位置替換為從訊息物件中提取的實際資訊。

        Args:
            rule_response (str): 回覆訊息的樣板字串，包含以下預留位置：
                - `{message}`: 觸發訊息的內容。
                - `{author}`: 訊息發送者的名稱。
                - `{author_mention}`: 提及訊息發送者 (例如 @使用者)。
                - `{author_id}`: 訊息發送者的 Discord ID。
                - `{channel}`: 訊息所在頻道的名稱。
                - `{channel_mention}`: 提及訊息所在的頻道 (例如 #頻道)。
                - `{channel_id}`: 訊息所在頻道的 ID。
                - `{guild}`: 訊息所在伺服器的名稱。
                - `{guild_id}`: 訊息所在伺服器的 ID。
            message (discord.Message): 觸發自動回覆的 Discord 訊息物件。

        Returns:
            str: 經過格式化處理，已將預留位置替換為實際內容的回覆字串。
        """
        return rule_response.format(
            message=message.content,  # 訊息內容
            author=message.author.name,  # 訊息發送者
            author_mention=message.author.mention,  # 訊息發送者
            author_id=message.author.id,  # 訊息發送者ID
            channel=message.channel.name,  # 訊息發送頻道
            channel_mention=message.channel.mention,  # 訊息發送頻道
            channel_id=message.channel.id,  # 訊息發送頻道ID
            guild=message.guild.name,  # 訊息發送伺服器
            guild_id=message.guild.id  # 訊息發送伺服器ID
        )

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        # 檢查ignore_rules
        # 是否為機器人發出
        if message.author.bot and self.ignore['ignore_bots']:
            return
        # 是否是自己發出的
        if message.author.id == self.bot.user.id and self.ignore['ignore_self']:
            return
        # 是否為指定頻道
        if message.channel.id in self.ignore['ignore_channels']:
            return
        # 是否為指定成員，或在指定身分組中
        # 取得訊息發送者的所有身分組ID
        roles = [role.id for role in message.author.roles]
        if message.author.id in self.ignore['ignore_users'] or \
        any(role in self.ignore['ignore_roles'] for role in roles):
            return
        
        # 檢查rules
        for rule in self.rules:
            # 檢查是否符合規則
            # 先檢查是否啟用正規表示式匹配
            logger.debug(f"正在檢查規則：{rule}，是否啟用正規表示式匹配：{rule['match_regex']}")
            if rule['match_regex']:
                logger.debug(f"正在使用正規表示式匹配，匹配結果：{re.search(rule['trigger'], message.content)}")
                if not re.search(rule['trigger'], message.content):
                    continue
                if rule['no_reply']:
                    # 照ephemeral中的布林值指定是否為私人訊息
                    m = await message.channel.send(self._format_response(rule['response'], message))
                    logger.info(f"自動回覆: {message.author.name} 在 {message.guild.name} 的 {message.channel.name} 頻道中觸發了自動回覆")
                    return
                else:
                    await message.reply(self._format_response(rule['response'], message))
                    logger.info(f"自動回覆: {message.author.name} 在 {message.guild.name} 的 {message.channel.name} 頻道中觸發了自動回覆")
                    return
            else:
                logger.debug(f"正在使用一般模式匹配，匹配結果：{re.search(rule['trigger'], message.content)}")
                if not rule['trigger'] in message.content:
                    continue
                if rule['no_reply']:
                    await message.channel.send(self._format_response(rule['response'], message))
                    logger.info(f"自動回覆: {message.author.name} 在 {message.guild.name} 的 {message.channel.name} 頻道中觸發了自動回覆")
                    return
                else:
                    await message.reply(self._format_response(rule['response'], message))
                    logger.info(f"自動回覆: {message.author.name} 在 {message.guild.name} 的 {message.channel.name} 頻道中觸發了自動回覆")
                    return

async def setup(bot):
    if not bot.config.get("auto_reply", {}).get("enable", False):
        logger.info(f"{COG_INTRO['name']} 未啟用，跳過註冊")
        return
    await bot.add_cog(Auto_Reply(bot))
    logger.info(f"{COG_INTRO['name']} 已經註冊")