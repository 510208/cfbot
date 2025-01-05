# 群組紀錄擴充功能

import discord
from discord.ext import commands
from discord import app_commands
import logging
import yaml

with open('cfg.yml', "r", encoding="utf-8") as file:
    config = yaml.safe_load(file)["dc_logging"]

logger = logging.getLogger(__name__)

COG_INTRO = {
    "name": "Discord 群組紀錄",
    "description": "紀錄 Discord 群組的變更"
}

class DcLogging(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        logger.info("DcLogging cog 已經載入")

    # 發送訊息事件
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        embed = discord.Embed(
            title="訊息紀錄",
            description="發送訊息",
            color=0xececff
        )
        if config["enabled"] == False or config["log_events"]["msg_send"] == False:
            return
        if message.author.bot and config["enabled_for_bot"] == False:
            return
        if message.author == self.bot.user:
            return
        embed.add_field(name="發送者", value=message.author.mention)
        embed.add_field(name="頻道", value=message.channel.mention)
        embed.add_field(name="訊息", value=message.content)
        embed.set_footer(text=f"訊息ID: {message.id}")
        if message.attachments:
            embed.add_field(name="附件", value="\n".join([attachment.url for attachment in message.attachments]))
        
        if config["console"] == True:
            logger.info(f"事件：發送訊息\n發送者：{message.author.mention}\n頻道：{message.channel.mention}\n訊息：{message.content}")
        
        await self.bot.get_channel(config["channel_id"]).send(embed=embed)

    # 刪除訊息事件
    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        embed = discord.Embed(
            title="訊息紀錄",
            description="刪除訊息",
            color=0xffecf0
        )
        if config["enabled"] == False or config["log_events"]["msg_delete"] == False:
            return
        if message.author.bot and config["enabled_for_bot"] == False:
            return
        if message.author == self.bot.user:
            return
        embed.add_field(name="發送者", value=message.author.mention)
        embed.add_field(name="頻道", value=message.channel.mention)
        embed.add_field(name="訊息", value=message.content)
        embed.set_footer(text=f"訊息ID: {message.id}")
        if message.attachments:
            embed.add_field(name="附件", value="\n".join([attachment.url for attachment in message.attachments]))
        
        if config["console"] == True:
            logger.info(f"事件：刪除訊息\n發送者：{message.author.mention}\n頻道：{message.channel.mention}\n訊息：{message.content}")
        
        await self.bot.get_channel(config["channel_id"]).send(embed=embed)
    
    # 編輯訊息事件
    @commands.Cog.listener()
    async def on_message_edit(self, before: discord.Message, after: discord.Message):
        embed = discord.Embed(
            title="訊息紀錄",
            description="編輯訊息",
            color=0xffe4ec
        )
        if config["enabled"] == False or config["log_events"]["msg_edit"] == False:
            return
        if before.author.bot and config["enabled_for_bot"] == False:
            return
        if before.author == self.bot.user:
            return
        embed.add_field(name="發送者", value=before.author.mention)
        embed.add_field(name="頻道", value=before.channel.mention)
        embed.add_field(name="舊訊息", value=before.content)
        embed.add_field(name="新訊息", value=after.content)
        embed.set_footer(text=f"訊息ID: {before.id}")
        if before.attachments:
            embed.add_field(name="附件", value="\n".join([attachment.url for attachment in before.attachments]))
        
        if config["console"] == True:
            logger.info(f"事件：編輯訊息\n發送者：{before.author.mention}\n頻道：{before.channel.mention}\n舊訊息：{before.content}\n新訊息：{after.content}")
        
        await self.bot.get_channel(config["channel_id"]).send(embed=embed)
    
    # 加入伺服器事件
    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        embed = discord.Embed(
            title="成員紀錄",
            description="加入伺服器",
            color=0xececff
        )
        if config["enabled"] == False or config["log_events"]["member_join"] == False:
            return
        embed.add_field(name="成員", value=member.mention)
        embed.add_field(name="加入時間", value=member.joined_at.strftime("%Y-%m-%d %H:%M:%S"))

        if config["console"] == True:
            logger.info(f"事件：加入伺服器\n成員：{member.mention}\n加入時間：{member.joined_at.strftime('%Y-%m-%d %H:%M:%S')}")
        
        await self.bot.get_channel(config["channel_id"]).send(embed=embed)
    
    # 離開伺服器事件
    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        embed = discord.Embed(
            title="成員紀錄",
            description="離開伺服器",
            color=0xffecf0
        )
        if config["enabled"] == False or config["log_events"]["member_leave"] == False:
            return
        embed.add_field(name="成員", value=member.mention)
        embed.add_field(name="離開時間", value=member.joined_at.strftime("%Y-%m-%d %H:%M:%S"))
        await self.bot.get_channel(config["channel_id"]).send(embed=embed)

    # 禁止成員事件
    @commands.Cog.listener()
    async def on_member_ban(self, guild: discord.Guild, user: discord.User):
        embed = discord.Embed(
            title="成員紀錄",
            description="禁止成員",
            color=0xffe4ec
        )
        if config["enabled"] == False or config["log_events"]["member_banned"] == False:
            return
        if user.bot and config["enabled_for_bot"] == False:
            return
        embed.add_field(name="成員", value=user.mention)
        embed.add_field(name="執行者", value=guild.me.mention)

        if config["console"] == True:
            logger.info(f"事件：禁止成員\n成員：{user.mention}\n執行者：{guild.me.mention}")
        
        await self.bot.get_channel(config["channel_id"]).send(embed=embed)

    # 解除禁止成員事件
    @commands.Cog.listener()
    async def on_member_unban(self, guild: discord.Guild, user: discord.User):
        embed = discord.Embed(
            title="成員紀錄",
            description="解除禁止成員",
            color=0xececff
        )
        if config["enabled"] == False or config["log_events"]["member_unbanned"] == False:
            return
        if user.bot and config["enabled_for_bot"] == False:
            return
        embed.add_field(name="成員", value=user.mention)
        embed.add_field(name="執行者", value=guild.me.mention)

        if config["console"] == True:
            logger.info(f"事件：解除禁止成員\n成員：{user.mention}\n執行者：{guild.me.mention}")
        
        await self.bot.get_channel(config["channel_id"]).send(embed=embed)

    # 靜音成員事件
    @commands.Cog.listener()
    async def on_member_update(self, before: discord.Member, after: discord.Member):
        embed = discord.Embed(
            title="成員紀錄",
            description="靜音成員",
            color=0xffecf0
        )
        if config["enabled"] == False or config["log_events"]["member_muted"] == False:
            return
        if before.guild_permissions.mute_members == after.guild_permissions.mute_members:
            return
        embed.add_field(name="成員", value=before.mention)
        embed.add_field(name="執行者", value=before.guild.me.mention)
        
        if config["console"] == True:
            logger.info(f"事件：靜音成員\n成員：{before.mention}\n執行者：{before.guild.me.mention}")

        await self.bot.get_channel(config["channel_id"]).send(embed=embed)
    
    # 解除靜音成員事件
    @commands.Cog.listener()
    async def on_member_update(self, before: discord.Member, after: discord.Member):
        embed = discord.Embed(
            title="成員紀錄",
            description="解除靜音成員",
            color=0xececff
        )
        if config["enabled"] == False or config["log_events"]["member_unmuted"] == False:
            return
        if before.guild_permissions.mute_members == after.guild_permissions.mute_members:
            return
        embed.add_field(name="成員", value=before.mention)
        embed.add_field(name="執行者", value=before.guild.me.mention)

        if config["console"] == True:
            logger.info(f"事件：解除靜音成員\n成員：{before.mention}\n執行者：{before.guild.me.mention}")
        
        await self.bot.get_channel(config["channel_id"]).send(embed=embed)
    
    # 加入角色事件
    @commands.Cog.listener()
    async def on_member_update(self, before: discord.Member, after: discord.Member):
        embed = discord.Embed(
            title="成員紀錄",
            description="加入角色",
            color=0xececff
        )
        if config["enabled"] == False or config["log_events"]["member_role_add"] == False:
            return
        if before.roles == after.roles:
            return
        embed.add_field(name="成員", value=before.mention)
        embed.add_field(name="加入角色", value=", ".join([role.mention for role in after.roles if role not in before.roles]))
        # embed.add_field(name="執行者", value=before.guild.me.mention)

        if config["console"] == True:
            logger.info(f"事件：加入角色\n成員：{before.mention}\n加入角色：{', '.join([role.mention for role in after.roles if role not in before.roles])}")
        
        await self.bot.get_channel(config["channel_id"]).send(embed=embed)

    # 移除角色事件
    @commands.Cog.listener()
    async def on_member_update(self, before: discord.Member, after: discord.Member):
        embed = discord.Embed(
            title="成員紀錄",
            description="移除角色",
            color=0xffecf0
        )
        if config["enabled"] == False or config["log_events"]["member_role_remove"] == False:
            return
        if before.roles == after.roles:
            return
        embed.add_field(name="成員", value=before.mention)
        embed.add_field(name="移除角色", value=", ".join([role.mention for role in before.roles if role not in after.roles]))
        # embed.add_field(name="執行者", value=before.guild.me.mention)

        if config["console"] == True:
            logger.info(f"事件：移除角色\n成員：{before.mention}\n移除角色：{', '.join([role.mention for role in before.roles if role not in after.roles])}")
        
        await self.bot.get_channel(config["channel_id"]).send(embed=embed)
    
    # 語音頻道相關事件
    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        embed = discord.Embed(
            title="成員紀錄",
            description="語音頻道相關事件",
            color=0xececff
        )
        if before.channel is None and after.channel and config["log_events"]["vc_join"] == True:
            embed.add_field(name="成員", value=member.mention)
            embed.add_field(name="加入語音頻道", value=after.channel.mention)

            if after.self_mute:
                muted = "是"
            else:
                muted = "否"
            
            embed.add_field(name="靜音", value=muted)
            
            if config["console"] == True:
                logger.info(f"事件：加入語音頻道\n成員：{member.mention}\n加入語音頻道：{after.channel.mention}\n靜音：{muted}")
            
        elif before.channel and after.channel is None and config["log_events"]["vc_leave"] == True:
            embed.add_field(name="成員", value=member.mention)
            embed.add_field(name="離開語音頻道", value=before.channel.mention)

            if before.self_mute:
                muted = "是"
            else:
                muted = "否"

            embed.add_field(name="靜音", value=muted)
            
            if config["console"] == True:
                logger.info(f"事件：離開語音頻道\n成員：{member.mention}\n離開語音頻道：{before.channel.mention}\n靜音：{muted}")
            
        elif before.channel != after.channel and config["log_events"]["vc_move"] == True:
            embed.add_field(name="成員", value=member.mention)
            embed.add_field(name="移動：從", value=before.channel.mention)
            embed.add_field(name="移動：到", value=after.channel.mention)
            
            if before.self_mute:
                muted = "是"
            else:
                muted = "否"

            embed.add_field(name="靜音", value=muted)

            if config["console"] == True:
                logger.info(f"事件：移動語音頻道\n成員：{member.mention}\n移動：從：{before.channel.mention}\n移動：到：{after.channel.mention}\n靜音：{muted}")
        
        await self.bot.get_channel(config["channel_id"]).send(embed=embed)

async def setup(bot):
    await bot.add_cog(DcLogging(bot))
    logger.info(f"{COG_INTRO['name']} 已經註冊")