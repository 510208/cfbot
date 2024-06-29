# @client.tree.context_menu(name='Show Join Date')

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
with open("cfg.yaml", "r", encoding="utf-8") as file:
    cfg = yaml.safe_load(file)

class AnnouStat(commands.Cog):
    @app_commands.context_menu(name='將維修狀態更新為還未開始')
    async def stat_to_wait(interaction: discord.Interaction, message: discord.Message):
        logging.info('維修狀態更新為還未開始')
        logging.info(f'請求發起人：{interaction.user}')
                # 檢查訊息是否為機器人發送
        if message.author.id != interaction.application_id:
            await interaction.send('此訊息不是由機器人發送')
            return
        # 檢查使用者是否為機器人管理員
        if interaction.author.id not in BOT_ADMIN:
            await interaction.send('你沒有權限使用此機器人')
            return
        # 將選取的訊息分片成陣列
        msg = message.content.split('\n')
        # 找出"### 維修狀態"的行數
        linenum = 0
        for i in range(len(msg)):
            if msg[i].startswith("### 維修狀態"):
                linenum = i
                break
        # 將"還未排定"換成"還未開始"
        msg[linenum + 1] = "<:dangerous:1254019093900558397> 還未開始"
        # 將訊息重新組合成字串
        newmsg = '\n'.join(msg)
        # 更新訊息
        await message.edit(content=newmsg)
        await interaction.send('維修狀態已更新為還未開始')
        return
    
    @app_commands.context_menu(name='將維修狀態更新為維修中')
    async def stat_to_doing(interaction: discord.Interaction, message: discord.Message):
        logging.info('維修狀態更新為維修中')
        logging.info(f'請求發起人：{interaction.user}')
                # 檢查訊息是否為機器人發送
        if message.author.id != interaction.application_id:
            await interaction.send('此訊息不是由機器人發送')
            return
        # 檢查使用者是否為機器人管理員
        if interaction.author.id not in BOT_ADMIN:
            await interaction.send('你沒有權限使用此機器人')
            return
        # 將選取的訊息分片成陣列
        msg = message.content.split('\n')
        # 找出"### 維修狀態"的行數
        linenum = 0
        for i in range(len(msg)):
            if msg[i].startswith("### 維修狀態"):
                linenum = i
                break
        # 將"還未排定"換成"維修中"
        msg[linenum + 1] = "<:loading:1254016316420128841> 維修中"
        # 將訊息重新組合成字串
        newmsg = '\n'.join(msg)
        # 更新訊息
        await message.edit(content=newmsg)
        await interaction.send('維修狀態已更新為維修中')
        return
    
    @app_commands.context_menu(name='將維修狀態更新為擱置中')
    async def stat_to_pause(interaction: discord.Interaction, message: discord.Message):
        logging.info('維修狀態更新為擱置中')
        logging.info(f'請求發起人：{interaction.user}')
                # 檢查訊息是否為機器人發送
        if message.author.id != interaction.application_id:
            await interaction.send('此訊息不是由機器人發送')
            return
        # 檢查使用者是否為機器人管理員
        if interaction.author.id not in BOT_ADMIN:
            await interaction.send('你沒有權限使用此機器人')
            return
        # 將選取的訊息分片成陣列
        msg = message.content.split('\n')
        # 找出"### 維修狀態"的行數
        linenum = 0
        for i in range(len(msg)):
            if msg[i].startswith("### 維修狀態"):
                linenum = i
                break
        # 將"還未排定"換成"擱置中"
        msg[linenum + 1] = "<:more:1254016318521217034> 擱置中"
        # 將訊息重新組合成字串
        newmsg = '\n'.join(msg)
        # 更新訊息
        await message.edit(content=newmsg)
        await interaction.send('維修狀態已更新為擱置中')
        return
    
    @app_commands.context_menu(name='將維修狀態更新為已完成')
    async def stat_to_done(interaction: discord.Interaction, message: discord.Message):
        logging.info('維修狀態更新為已完成')
        logging.info(f'請求發起人：{interaction.user}')
        # 檢查訊息是否為機器人發送
        if message.author.id != interaction.application_id:
            await interaction.send('此訊息不是由機器人發送')
            return
        # 檢查使用者是否為機器人管理員
        if interaction.author.id not in BOT_ADMIN:
            await interaction.send('你沒有權限使用此機器人')
            return
        # 將選取的訊息分片成陣列
        msg = message.content.split('\n')
        # 找出"### 維修狀態"的行數
        linenum = 0
        for i in range(len(msg)):
            if msg[i].startswith("### 維修狀態"):
                linenum = i
                break
        # 將"還未排定"換成"已完成"
        msg[linenum + 1] = "<:check:1254019091371397130> 維修完成"
        # 將訊息重新組合成字串
        newmsg = '\n'.join(msg)
        # 找出裡面有"結束"的行數
        for i in range(len(msg)):
            if msg[i].startswith("結束"):
                linenum = i
                break
        # 時間設為當前時間
        msg[linenum + 1] = f"- **<:stop:1254016323013443584> 結束**：{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        # 更新訊息
        await message.edit(content=newmsg)
        await interaction.send('維修狀態已更新為已完成')
        return