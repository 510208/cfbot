import logging
import discord
from discord.ext import tasks, commands

logger = logging.getLogger(__name__)

COG_INTRO = {
    "name": "伺服器狀態",
    "description": "在伺服器中的狀態類別建立多個頻道，並由機器人自動更新狀態，如人數、身分組數。",
    "author": "SamHacker",
    "countributors": ["SamHacker"],
}

class ServerStatus(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.config = bot.config.get("server_status", {})
        logger.info(f"載入 {COG_INTRO['name']} 設定：{self.config}")
        self.ct_config = self.config.get("counters", {})  # 取得所設定的計數器配置
        # 確保 interval 是一個有效的數字，預設為 60 秒
        interval = self.config.get("interval", 60)
        if not isinstance(interval, (int, float)) or interval <= 0:
            logger.warning(f"配置中的 interval ({interval}) 無效，將使用預設值 60 秒。")
            interval = 60
        self.update_status.change_interval(seconds=interval)  # 更新循環間隔

    # 將更新頻道的指令獨立成函式
    async def _update_channel_name(self, channel_id: int, channel_name_format: str, count: int, counter_name: str):
        """
        更新頻道名稱的函式
        :param channel_id: 頻道 ID
        :param channel_name_format: 頻道名稱的格式字串，例如 "成員數量：{count}"
        :param count: 要更新的計數
        :param counter_name: 計數器名稱，用於日誌記錄
        """
        channel = self.bot.get_channel(channel_id)
        if channel:
            try:
                new_name = channel_name_format.format(count=count)
                await channel.edit(name=new_name)
                logger.debug(f"更新頻道 {channel.name} ({channel_id}) [{counter_name}] 成員數量：{count}")
            except discord.Forbidden:
                logger.warning(f"無法更新頻道 {channel.name} ({channel_id}) [{counter_name}] 的名稱，權限不足。")
            except discord.HTTPException as e:
                logger.error(f"更新頻道 {channel.name} ({channel_id}) [{counter_name}] 時發生錯誤：{e}")

    
    # 定時更新狀態
    @tasks.loop(seconds=60)
    async def update_status(self):
        logger.info(f"開始更新伺服器狀態。")
        # 取得伺服器資訊
        guild = self.bot.get_guild(self.bot.guilds[0].id)

        # 取得與成員有關的統計配置
        member_config = self.ct_config.get("member", {})
        g_member = guild.members
        # 更新所有成員計數
        # （member下的all_members）
        all_members_config = member_config.get("all_members", {})
        if all_members_config.get("enable", False):
            count = len(g_member)
            channel_id = all_members_config.get("channel_id")
            await self._update_channel_name(
                channel_id,
                all_members_config.get("channel_name", "成員數量：{count}"),
                count,
                "all_members"
            )
                
            # 清理先前建立的變數，以減少記憶體使用量
            del all_members_channel
            del all_members_config
            del all_members

        # 更新線上成員計數
        # （member下的online_members）
        online_members_config = member_config.get("online_members", {})
        if online_members_config.get("enable", False):
            count = sum(1 for member in g_member if member.status == discord.Status.online)
            channel_id = online_members_config.get("channel_id")
            await self._update_channel_name(
                channel_id,
                online_members_config.get("channel_name", "線上成員數量：{count}"),
                count,
                "online_members"
            )

            # 清理先前建立的變數，以減少記憶體使用量
            del online_members_channel
            del online_members_config
            del online_members
        
        # 更新離線成員計數
        # （member下的offline_members）
        offline_members_config = member_config.get("offline_members", {})
        if offline_members_config.get("enable", False):
            count = sum(1 for member in g_member if member.status == discord.Status.offline)
            channel_id = offline_members_config.get("channel_id")
            await self._update_channel_name(
                channel_id,
                offline_members_config.get("channel_name", "離線成員數量：{count}"),
                count,
                "offline_members"
            )

            # 清理先前建立的變數，以減少記憶體使用量
            del offline_members_channel
            del offline_members_config
            del offline_members

        # 更新人數計數
        # （member下的humans）
        humans_config = member_config.get("humans", {})
        if humans_config.get("enable", False):
            count = sum(1 for member in g_member if not member.bot)
            channel_id = humans_config.get("channel_id")
            await self._update_channel_name(
                channel_id,
                humans_config.get("channel_name", "人數：{count}"),
                count,
                "humans"
            )

            # 清理先前建立的變數，以減少記憶體使用量
            del humans_channel
            del humans_config
            del humans
                
        # 更新機器人數量計數
        # （member下的bots）
        bots_config = member_config.get("bots", {})
        if bots_config.get("enable", False):
            count = sum(1 for member in g_member if member.bot)
            channel_id = bots_config.get("channel_id")
            await self._update_channel_name(
                channel_id,
                bots_config.get("channel_name", "機器人數：{count}"),
                count,
                "bots"
            )

            # 清理先前建立的變數，以減少記憶體使用量
            del bots_channel
            del bots_config
            del bots

        # 更新被封鎖（ban）的成員數量
        # （member下的banned_members）
        banned_members_config = member_config.get("member_banned", {})
        if banned_members_config.get("enable", False):
            count = len(await guild.bans())
            channel_id = banned_members_config.get("channel_id")
            await self._update_channel_name(
                channel_id,
                banned_members_config.get("channel_name", "被封鎖成員數量：{count}"),
                count,
                "member_banned"
            )

            # 清理先前建立的變數，以減少記憶體使用量
            del banned_members_channel
            del banned_members_config
            del banned_members

        # 更新無身分組成員數量
        # （role下的member_no_role）
        no_role_config = self.ct_config.get("member_no_role", {})
        if no_role_config.get("enable", False):
            count = sum(1 for member in g_member if not member.roles)
            channel_id = no_role_config.get("channel_id")
            await self._update_channel_name(
                channel_id,
                no_role_config.get("channel_name", "無身分組成員數量：{count}"),
                count,
                "member_no_role"
            )

            # 清理先前建立的變數，以減少記憶體使用量
            del no_role_channel
            del no_role_config
            del no_role_members
        
        # 更新擁有特定身分組的成員數量
        # （role下的member_with_role）
        role_config = self.ct_config.get("member_with_role", {})
        if role_config.get("enable", False):
            # 檢查role鍵（裡面是清單，
            # 例如：[
            #    {
            #       "role_id": 123456789012345678,
            #       "channel_id": 123456789012345678,
            #       "channel_name": "擁有身分組的成員數量：{count}"},
            #    ...
            # ]
            # 是否存在
            if isinstance(role_config.get("role"), list):
                for role in role_config.get("role"):
                    # 檢查role_id鍵是否存在
                    if role.get("role_id") and role.get("channel_id"):
                        # 取得身分組
                        role_obj = guild.get_role(role["role_id"])
                        if role_obj:
                            # 計算擁有該身分組的成員數量
                            count = sum(1 for member in g_member if role_obj in member.roles)
                            channel_id = role["channel_id"]
                            await self._update_channel_name(
                                channel_id,
                                role.get("channel_name", "擁有身分組的成員數量：{count}"),
                                count,
                                f"member_with_role:{role_obj.name}"
                            )
                            
                            # 清理先前建立的變數，以減少記憶體使用量
                            del channel
                            del members_with_role
                        else:
                            logger.warning(f"找不到身分組 {role['role_id']}。")
                    else:
                        logger.warning(f"角色配置不正確，缺少 role_id 或 channel_id。")

        # 取得與伺服器有關的統計配置
        guild_config = self.ct_config.get("guild", {})

        # 更新伺服器加成者數量
        # （guild下的guild_booster）
        booster_config = guild_config.get("guild_booster", {})
        if booster_config.get("enable", False):
            count = guild.premium_subscription_count
            channel_id = booster_config.get("channel_id")
            await self._update_channel_name(
                channel_id,
                booster_config.get("channel_name", "伺服器加成者數量：{count}"),
                count,
                "guild_booster"
            )

            # 清理先前建立的變數，以減少記憶體使用量
            del booster_channel
            del booster_config
            del booster

        # 更新伺服器成員數量
        # （guild下的guild_boost_level）
        boost_level_config = guild_config.get("guild_boost_level", {})
        if boost_level_config.get("enable", False):
            count = guild.premium_tier
            channel_id = boost_level_config.get("channel_id")
            await self._update_channel_name(
                channel_id,
                boost_level_config.get("channel_name", "伺服器加成者等級：{count}"),
                count,
                "guild_boost_level"
            )

            # 清理先前建立的變數，以減少記憶體使用量
            del boost_level_channel
            del boost_level_config
            del boost_level

        # 更新伺服器頻道數量
        # （guild下的channels）
        channels_config = guild_config.get("channels", {})
        if channels_config.get("enable", False):
            count = len(guild.channels)
            channel_id = channels_config.get("channel_id")
            await self._update_channel_name(
                channel_id,
                channels_config.get("channel_name", "伺服器頻道數量：{count}"),
                count,
                "channels"
            )

            # 清理先前建立的變數，以減少記憶體使用量
            del channels_channel
            del channels_config
            del channels

        # 更新伺服器文字頻道數量
        # （guild下的channels中的text_channels）
        text_channels_config = guild_config.get("channels", {}).get("text_channels", {})
        if text_channels_config.get("enable", False):
            count = len([channel for channel in guild.text_channels if not channel.is_news()])
            channel_id = text_channels_config.get("channel_id")
            await self._update_channel_name(
                channel_id,
                text_channels_config.get("channel_name", "伺服器文字頻道數量：{count}"),
                count,
                "text_channels"
            )

            # 清理先前建立的變數，以減少記憶體使用量
            del text_channels_channel
            del text_channels_config
            del text_channels
        
        # 更新伺服器公告頻道數量
        # （guild下的channels中的annou_channels）
        annou_channels_config = guild_config.get("channels", {}).get("annou_channels", {})
        if annou_channels_config.get("enable", False):
            # 獲取伺服器公告頻道數量，公告頻道由文字頻道中is_news()回傳True的頻道組成
            # 這裡的is_news()是discord.py中的一個方法，用於檢查頻道是否為公告頻道
            count = len([channel for channel in guild.text_channels if channel.is_news()])
            channel_id = annou_channels_config.get("channel_id")
            await self._update_channel_name(
                channel_id,
                annou_channels_config.get("channel_name", "伺服器公告頻道數量：{count}"),
                count,
                "annou_channels"
            )

            # 清理先前建立的變數，以減少記憶體使用量
            del annou_channels_channel
            del annou_channels_config
            del annou_channels

        # 更新伺服器語音頻道數量
        # （guild下的channels中的voice_channels）
        voice_channels_config = guild_config.get("channels", {}).get("voice_channels", {})
        if voice_channels_config.get("enable", False):
            count = len(guild.voice_channels)
            channel_id = voice_channels_config.get("channel_id")
            await self._update_channel_name(
                channel_id,
                voice_channels_config.get("channel_name", "伺服器語音頻道數量：{count}"),
                count,
                "voice_channels"
            )

            # 清理先前建立的變數，以減少記憶體使用量
            del voice_channels_channel
            del voice_channels_config
            del voice_channels

        # 更新伺服器論壇頻道數量
        # （guild下的channels中的forum_channels）
        forum_channels_config = guild_config.get("channels", {}).get("forum_channels", {})
        if forum_channels_config.get("enable", False):
            count = len(guild.voice_channels)
            channel_id = forum_channels_config.get("channel_id")
            await self._update_channel_name(
                channel_id,
                forum_channels_config.get("channel_name", "伺服器語音頻道數量：{count}"),
                count,
                "forum_channels"
            )

            # 清理先前建立的變數，以減少記憶體使用量
            del forum_channels_channel
            del forum_channels_config
            del forum_channels

        # 更新伺服器舞台頻道數量
        # （guild下的channels中的stage_channels）
        stage_channels_config = guild_config.get("channels", {}).get("stage_channels", {})
        if stage_channels_config.get("enable", False):
            count = len(guild.stage_channels)
            channel_id = stage_channels_config.get("channel_id")
            await self._update_channel_name(
                channel_id,
                stage_channels_config.get("channel_name", "伺服器舞台頻道數量：{count}"),
                count,
                "stage_channels"
            )

            # 清理先前建立的變數，以減少記憶體使用量
            del stage_channels_channel
            del stage_channels_config
            del stage_channels

        # 更新伺服器身分組數量
        # （guild下的roles）
        roles_config = guild_config.get("roles", {})
        if roles_config.get("enable", False):
            count = len(guild.roles)
            channel_id = roles_config.get("channel_id")
            await self._update_channel_name(
                channel_id,
                roles_config.get("channel_name", "伺服器身分組數量：{count}"),
                count,
                "roles"
            )

            # 清理先前建立的變數，以減少記憶體使用量
            del roles_channel
            del roles_config
            del roles

        # 更新伺服器擁有的表情符號數量
        # （guild下的emojis）
        emojis_config = guild_config.get("emojis", {})
        if emojis_config.get("enable", False):
            count = len(guild.emojis)
            channel_id = emojis_config.get("channel_id")
            await self._update_channel_name(
                channel_id,
                emojis_config.get("channel_name", "伺服器表情符號數量：{count}"),
                count,
                "emojis"
            )

            # 清理先前建立的變數，以減少記憶體使用量
            del emojis_channel
            del emojis_config
            del emojis

        # 更新伺服器貼圖數量
        # （guild下的stickers）
        stickers_config = guild_config.get("stickers", {})
        if stickers_config.get("enable", False):
            count = len(guild.stickers)
            channel_id = stickers_config.get("channel_id")
            await self._update_channel_name(
                channel_id,
                stickers_config.get("channel_name", "伺服器貼圖數量：{count}"),
                count,
                "stickers"
            )

            # 清理先前建立的變數，以減少記憶體使用量
            del stickers_channel
            del stickers_config
            del stickers

        logger.info(f"伺服器狀態更新完成。")

    @update_status.before_loop
    async def before_update_status(self):
        await self.bot.wait_until_ready()
        logger.info(f"準備開始計時更新伺服器狀態。")

async def setup(bot):
    if not bot.config.get("server_status", {}).get("enable", False):
        logger.info(f"跳過載入 {COG_INTRO['name']}，因為它被禁用。")
        return
    # logger.info(f"目前工作目錄：{os.getcwd()}")
    await bot.add_cog(ServerStatus(bot))