# Discord 資料查詢模組

import logging
import sqlite3
from pydactyl import PterodactylClient
import aiohttp
# 解析 Base64 的模組
import base64
import json
import time
import asyncio

logger = logging.getLogger(__name__)

# 用 Discord ID 查詢玩家的 Minecraft 資訊的類別
class dcSearcher:
    def __init__(self, pt_url: str, pt_key: str, db_path: str):
        self.api = PterodactylClient(pt_url, pt_key)
        self.db_path = db_path

    def __getServerStat(self):
        try:
            ct_response_item = self.api.client.servers.files.get_file_contents("bea94db6", "/plugins/DiscordSRV/accounts.aof")
            ct = ct_response_item.text
            # 若取得資料為空，則引起錯誤
            if ct == "":
                raise GetDiscordSRVDataFailed("取得 DiscordSRV 資料失敗：資料為空")
            # print(f"取得 DiscordSRV 資料成功，內容：\n{ct}")
            ct = ct.split("\n")
            # 格式：980016361906524181 ecfedf45-e28a-4533-9d62-597fd8abbff5
            # 這裡的字典格式為 {Discord ID: Minecraft UUID}
            d = {}
            for i in ct:
                if i == "":
                    continue
                i = i.split(" ")
                ins = {i[0]: i[1]}
                d.update(ins)
            return d
        except Exception as e:
            logger.error(f"取得 DiscordSRV 資料失敗：{e}")
            raise GetDiscordSRVDataFailed(f"取得 DiscordSRV 資料失敗：{e}")

    async def syncDcsrv(self):
        """同步 DiscordSRV 資料到資料庫"""

        # 開啟sqlite3資料庫
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # 調用getServerStat並將字典記錄到map變數中
        map = self.__getServerStat()

        # 取得資料庫中現有的資料
        cursor.execute("SELECT dc_id, mc_uuid FROM player_discord_mapping")
        existing_data = cursor.fetchall()

        # 將資料庫中的資料轉換成字典以便處理
        db_map = {mc_uuid: dc_id for dc_id, mc_uuid in existing_data}

        # 刪除資料庫中 map 中沒有的紀錄
        for mc_uuid in db_map:
            if mc_uuid not in map.values():
                cursor.execute("DELETE FROM player_discord_mapping WHERE mc_uuid = ?", (mc_uuid,))

        # 新增 map 中有但資料庫中沒有的紀錄，或是更新不一致的紀錄
        for dc_id, mc_uuid in map.items():
            if mc_uuid not in db_map:
                cursor.execute("INSERT INTO player_discord_mapping (dc_id, mc_uuid) VALUES (?, ?)", (dc_id, mc_uuid))
            elif db_map[mc_uuid] != dc_id:
                cursor.execute("UPDATE player_discord_mapping SET dc_id = ? WHERE mc_uuid = ?", (dc_id, mc_uuid))

        # 提交變更並關閉資料庫連接
        conn.commit()
        conn.close()

    # 調用 syncDcsrv 函數進行同步
    # syncDcsrv()

    # print(getServerStat())
    # 查詢函式
    # 藉由 Minecraft UUID 取得對應的 Discord ID
    def getDiscordID(self, mc_uuid: str):
        """調用 syncDcsrv 函數進行同步
        
        Parameters
        -----------
        mc_uuid: str
            要查詢的 Minecraft UUID
        """
        conn = sqlite3.connect('databases/playermapping.db')
        cursor = conn.cursor()
        cursor.execute("SELECT dc_id FROM player_discord_mapping WHERE mc_uuid = ?", (mc_uuid,))
        dc_id = cursor.fetchone()
        conn.close()
        if dc_id == None:
            return dc_id
        return dc_id[0]
    
    # 藉由 Discord ID 取得對應的 Minecraft UUID
    def getMinecraftUUID(self, dc_id: str):
        conn = sqlite3.connect('databases/playermapping.db')
        cursor = conn.cursor()
        cursor.execute("SELECT mc_uuid FROM player_discord_mapping WHERE dc_id = ?", (dc_id,))
        mc_uuid = cursor.fetchone()
        conn.close()
        if mc_uuid == None:
            return mc_uuid
        return mc_uuid[0]
    
    # 主函式
    def getBindInfo(self, mc_uuid = None, dc_id = None):
        """藉由 Minecraft UUID 或 Discord ID 取得玩家的帳號綁定資料
        
        Parameters
        -----------
        mc_uuid: str
            要查詢的 Minecraft UUID
        dc_id: str
            要查詢的 Discord ID
        """
        if mc_uuid == None and dc_id == None:
            raise IDNotFound(f"所提供的 Minecraft UUID 或 Discord ID 不能為空。，但函式接收到：\nmc_uuid = {mc_uuid}，dc_id = {dc_id}")
        elif mc_uuid != None:
            d = {
                "dc_id": self.getDiscordID(mc_uuid),
                "mc_class": playerInfo(playerUUID = mc_uuid)
            }
            return d
        elif dc_id != None:
            puuid = self.getMinecraftUUID(dc_id)
            if puuid == None:
                return {"dc_id": dc_id, "mc_class": None}
            
            d = {
                "dc_id": dc_id,
                "mc_class": playerInfo(playerUUID = puuid)
            }
            return d

    def excuteDbCmd(self, cmd: str):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        r = cursor.execute(cmd)
        conn.commit()
        conn.close()
        return r.fetchall()

    # 自訂錯誤：找不到 Discord ID 或 Minecraft UUID

# 用 UUID 查詢玩家的 Minecraft 資訊的類別
class playerInfo:
    def __init__(self, playerUUID: str, playerTimeStamps: int = None):
        self.playerUUID = playerUUID
        self.playerTimeStamps = playerTimeStamps
        self.playerName = "NotSearched"
        self.__playerProperties = None
        self.__lastUpdateNameStamp = None
        self.lastUpdateName = None
        
        self.skinUrl = None
        self.avatarUrl = None
        self.isometricHeadUrl = None
        self.bodyUrl = None
        self.isometricAvatarUrl = None
    
    async def __getInfo(self):
        async with aiohttp.ClientSession() as session:
            base_url = "https://sessionserver.mojang.com/session/minecraft/profile/"
            if self.playerTimeStamps != None:
                args = f"?at={self.playerTimeStamps}"
            else:
                args = ""
            async with session.get(f"{base_url}{self.playerUUID}{args}") as response:
                return await response.json()
            
    def __getPlayerProperties(self, basedText: str):
        # 將 base64 解碼
        # print(basedText)
        if not isinstance(basedText, str):
            return basedText
        decoded = base64.b64decode(basedText)
        # 將解碼後的資料轉換成字串
        decodedStr = decoded.decode("utf-8")
        # 將字串轉換成字典
        decodedDict = eval(decodedStr)
        return decodedDict

    async def get(self):
        """取得玩家資訊"""
        try:
            info = await self.__getInfo()
            self.playerName = info["name"]
            self.__playerProperties = info["properties"]
            for i in self.__playerProperties:
                if i["name"] == "textures":
                    self.__playerProperties = i
                    break
            self.__playerProperties = self.__getPlayerProperties(self.__playerProperties["value"])
            self.lastUpdateName = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.__playerProperties["timestamp"]/1000))
            # Skin URL
            self.skinUrl = self.__playerProperties["textures"]["SKIN"]["url"]
            # 純頭顱 正面
            self.avatarUrl = f"https://mc-heads.net/avatar/{self.playerUUID}"
            # 純頭顱 3D
            self.isometricHeadUrl = f"https://mc-heads.net/head/{self.playerUUID}"
            # 全身 正面
            self.bodyUrl = f"https://mc-heads.net/player/{self.playerUUID}"
            # 全身 3D
            self.isometricAvatarUrl = f"https://mc-heads.net/body/{self.playerUUID}"
        # 若找不到玩家資訊，則將玩家名稱設為 NotSearched，連結設定為黑白 Steve
        except Exception as e:
            self.playerName = "NotFound"
            self.avatarUrl = "https://mc-heads.net/avatar/Steve"
            self.isometricHeadUrl = "https://mc-heads.net/head/Steve"
            self.bodyUrl = "https://mc-heads.net/player/Steve"
            self.isometricAvatarUrl = "https://mc-heads.net/body/Steve"
            logger.error(f"取得玩家資訊失敗：{e}")
            return

# 自訂錯誤：找不到 Discord ID 或 Minecraft UUID
class IDNotFound(Exception):
    def __init__(self, message):
        self.message = message

# 自訂錯誤：取得 DiscordSRV 資料失敗
class GetDiscordSRVDataFailed(Exception):
    def __init__(self, message):
        self.message = message