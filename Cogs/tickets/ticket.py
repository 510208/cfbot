import asyncio
import logging
import discord
from discord.ext import commands
import yaml

with open('cfg.yml', "r", encoding="utf-8") as file:
    config = yaml.safe_load(file)["tickets"]
    message = config["messages"]
    multiline_msg = config["multiline_messages"]
    button_texts = config["button_texts"]
    embed_txt = config["embed_text"]

logger = logging.getLogger(__name__)

COG_INTRO = {
    "name": "客服單系統",
    "description": "為伺服器新增客服單功能，由夜間部設計"
}

class MainMenu(discord.ui.View):
    def __init__(self, timeout = None):
        super().__init__(timeout = timeout)
    
    @discord.ui.button(
        label = button_texts["new_ticket"],
        style = discord.ButtonStyle.primary,
        custom_id = "ticket-on:on_button"
    )
    async def on_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        """建立一個以'ticket-{username}'為名的新頻道"""
        # 設定相關常數
        TICKET_CATEGORY = config["category_id"]   # 客服單分類的 ID
        GUILD = interaction.guild
        AUTHOR = interaction.user
        STAFF_ROLE_ID: list[int] = config["staff_role_id"]
        # 檢查是否已經有相同名稱的頻道
        for channel in GUILD.text_channels:
            if channel.name == f"ticket-{AUTHOR.name}":
                await interaction.response.send_message(
                    message["ticket_exists"],
                    ephemeral = True
                )
                return
        
        try:
            # 建立新頻道
            overwrites = {
                GUILD.default_role: discord.PermissionOverwrite(read_messages=False),  # 禁止所有人查看
                interaction.user: discord.PermissionOverwrite(read_messages=True, send_messages=True),  # 允許用戶查看
                GUILD.me: discord.PermissionOverwrite(read_messages=True, send_messages=True),  # 允許機器人查看
            }
            # 遍覽所有客服人員的 ID，並將其加入到 overwrites 中
            for role_id in STAFF_ROLE_ID:
                role = GUILD.get_role(role_id)
                overwrites[role] = discord.PermissionOverwrite(read_messages=True, send_messages=True)
            
            CHANNEL = await GUILD.create_text_channel(
                f"ticket-{AUTHOR.name}",
                category = GUILD.get_channel(TICKET_CATEGORY),
                overwrites = overwrites
            )

            # 發送歡迎訊息
            await channel.send(
                multiline_msg["welcome_ticket"].format(
                    user = AUTHOR.name,
                    user_mention = AUTHOR.mention,
                    user_id = AUTHOR.id,
                    channel = CHANNEL.name,
                    channel_mention = CHANNEL.mention,
                    channel_id = CHANNEL.id,
                    staff_mention = ", ".join([role.mention for role in STAFF_ROLE_ID])
                )
            )
        except Exception as e:
            logger.error(f"建立客服單時發生錯誤：{e}")
            await interaction.response.send_message(
                message["error"],
                ephemeral = True
            )

class ViewsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

async def setup(bot):
    if not config["enabled"]:
        logger.info("載入客服單系統失敗，原因：在配置文件中停用了此模組")
        return
    await bot.add_cog(ViewsCog(bot))
    logger.info(f"{COG_INTRO['name']} 已經註冊")