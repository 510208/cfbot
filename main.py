import discord
import logging
from discord.ext import commands
from discord.ext.commands import CommandNotFound, NoEntryPointError
import os
import yaml
import asyncio
import platform
import json
# from Cogs.tickets.ticket import SELF_PATH
import plugins.const_codes as const_codes
import re

# Project Version
VERSION = '1.0.4'

# Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(lineno)d: [%(asctime)s][%(levelname)s] - [%(module)s] %(message)s'
)

logging.getLogger('discord').setLevel(logging.WARNING)
logging.getLogger('logging').setLevel(logging.WARNING)
logging.getLogger('plugins.const_codes').setLevel(logging.WARNING)
logging.getLogger('asyncio').setLevel(logging.WARNING)
logging.getLogger('json').setLevel(logging.WARNING)
logging.getLogger('yaml').setLevel(logging.WARNING)

with open('cfg.yml', 'r', encoding='utf-8') as f:
    cfg = yaml.load(f, Loader=yaml.FullLoader)
    logging.info('讀取cfg.yml成功！')

if cfg['debug']:
    logging.getLogger().setLevel(logging.DEBUG)
    logging.getLogger('discord').setLevel(logging.DEBUG)
    logging.getLogger('logging').setLevel(logging.DEBUG)
    logging.getLogger('plugins.const_codes').setLevel(logging.DEBUG)
    logging.getLogger('asyncio').setLevel(logging.DEBUG)
    logging.getLogger('json').setLevel(logging.DEBUG)
    logging.getLogger('yaml').setLevel(logging.DEBUG)
    WARNING_MSG = """
____!___!___!___!___!___!___!___!___!____

    W A R N I N G ! ! !

  您已啟用除錯模式，可能會看到更多詳細資訊
  本模式給予開發人員更大的彈性，但也可能
  會對您的隱私造成風險，請注意！

  您可以在cfg.yml中關閉除錯模式
  請注意，除錯模式可能會對機器人造成影響，
  請僅在開發環境中或需要除厝時啟動除錯模式，
  如果你不知道除錯模式的風險，請勿啟動除錯模式  

  請勿將除錯模式開啟於正式環境
____!___!___!___!___!___!___!___!___!____
"""
    for line in WARNING_MSG.split('\n'):
        logging.warning(line)

# 檢查錯誤狀態
if cfg is None:
    logging.error('cfg.yml為空！')
    exit()

# 可以使用指令的使用者ID
BOT_ADMIN = cfg["admin_id"]

# Bot
bot = commands.Bot(command_prefix='sh!', intents=discord.Intents.all())

# 寫入已同步的指令
async def write_slash_synced(slash: discord.app_commands.AppCommand):
    SELF_PATH = os.path.dirname(os.path.abspath(__file__))
    FILE_NAME = 'slash.json'
    FILE_PATH = os.path.join(SELF_PATH, FILE_NAME)
    with open(FILE_PATH, 'w') as f:
        # 取得所有指令與其說明，並存入陣列中
        logging.info('寫入指令同步資料')
        slash = []
        for command in bot.tree.walk_commands():
            logging.debug(f'指令名稱：{command.name}，指令說明：{command.description}')
            slash.append({
                'name': command.name,
                'description': command.description
            })
        
        logging.debug(f'指令同步資料：{slash}')
        json.dump(slash, f, indent = 4)
        logging.info('指令同步資料寫入成功')

# Cogs Slash Command
@bot.event
async def on_ready():
    # 輸出歡迎訊息
    ASCII_CODE = rf"""
____________________________________________________

         ┌--- ┌---
         |    ├---     Logged in as {bot.user}
         |    |        Bot ID: {bot.user.id}
         └--- ┴
____________________________________________________

  OS: {platform.system()} {platform.release()}
  Python Version: {platform.python_version()}
  Discord.py Version: {discord.__version__}
  CFBot Version: {cfg["version"]}
  Development by 510208, Thanks for using!

            Open Source with GNU 3.0 and pleasure!
                       Developed with ❤️ by 510208

"""
    DEBG_CODE = rf"""
____________________________________________________

         ┌--- ┌---
         |    ├---     Logged in as {bot.user}
         |    |        Bot ID: {bot.user.id}
         └--- ┴  d     Working in Debug Mode!!
____________________________________________________

  OS: {platform.system()} {platform.release()}
  Python Version: {platform.python_version()}
  Discord.py Version: {discord.__version__}
  CFBot Version: {cfg["version"]}
  Development by 510208, Thanks for using!

            Open Source with GNU 3.0 and pleasure!
                       Developed with ❤️ by 510208

"""
    if cfg['debug']:
        for line in DEBG_CODE.split('\n'):
            logging.info(line)
    else:
        for line in ASCII_CODE.split('\n'):
            logging.info(line)
    logging.info('------')
    for guild in bot.guilds:
        logging.info(f'{guild.name} (ID: {guild.id})')
    logging.info('------')
    await bot.change_presence(activity=discord.Game(name='正在雲羽生存服搞事...'))
    # 檢查配置檔案版本
    logging.info('檢查配置檔案版本...')
    if cfg['version'] != VERSION:
        # 判斷是否為新版本
        if cfg['version'] < VERSION:
            logging.warning('配置檔案版本過舊，可能會導致錯誤，請更新配置檔案！')
        else:
            logging.warning('配置檔案版本過新，可能會導致錯誤，請更新機器人！')
        logging.warning(f'配置檔案版本：{cfg["version"]}，機器人版本：{VERSION}')
        logging.warning('如因配置版本不同引起的錯誤，請勿提出 Issue')
    else:
        logging.info('配置檔案版本正確，繼續啟動')
        logging.info(f'配置檔案版本：{cfg["version"]}，機器人版本：{VERSION}')
    # 檢查更新
    if cfg['check_update']:
        logging.info('檢查更新中...')
        try:
            version = await const_codes.check_version()
            if version['latest'] != VERSION:
                logging.warning('檢查到新版本！')
                logging.warning(f'最新版本：{version["latest"]}')
                logging.warning(f'請前往 {version["zip"]} 下載最新版本')
            else:
                logging.info('已是最新版本')
        except Exception as e:
            logging.error(f'檢查更新失敗：{e}')
    else:
        logging.info('已關閉檢查更新，繼續啟動')
    # 同步指令
    logging.info('同步指令中...')
    slash = await bot.tree.sync()
    if slash:
        logging.info(f'指令同步完成：{slash}')
        await write_slash_synced(slash)
    else:
        logging.error('指令同步失敗')

# Error Handler
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        ctx.send('欸欸指令不存在', ephemeral=True)
        return
    raise error

# Cog List Command
@bot.tree.command(
    name='齒輪列表',
    description='列出所有Cogs資料夾中的Cogs'
)
async def cog_list(ctx):
    if ctx.user.id not in BOT_ADMIN:
        await ctx.response.send_message('你沒有權限使用此機器人', ephemeral=True)
        return
    # 遍覽Cogs資料夾，並取出所有可用Cogs，然後逐一檢查是否被啟用
    logging.info('取得Cogs列表')
    logging.info(f'請求發起人：{ctx.user}')
    # cogs = []
    # for filename in os.listdir('./cogs'):
    #     if filename.endswith('.py'):
    #         cogs.append(filename[:-3])
        
    # 取出已啟用的Cogs
    # enabled_cogs = []
    # for cog in cogs:
    #     if cog in bot.cogs:
    #         enabled_cogs.append(cog)
    
    # 回傳Embed訊息
    embed = discord.Embed(
        title='Cogs列表',
        description='以下為所有Cogs列表',
        color=discord.Color.blue()
    )
    logging.info(f'已啟用的Cogs：{bot.cogs}')
    for cog in bot.cogs:
        embed.add_field(
            name=cog,
            value='<:check:1254019091371397130> 已啟用',
            inline=False
        )
    # 取得bot.cogs的所有鍵名（bot.cogs是一個字典）
    all_cogs = bot.cogs.keys()
    # 將all_cogs全部變小寫
    all_cogs = [cog.lower() for cog in all_cogs]
    for cog in os.listdir('./Cogs'):
        if cog.endswith('.py'):
            if cog[:-3] not in all_cogs:
                embed.add_field(
                    name=cog[:-3],
                    value='<:dangerous:1254019093900558397> 未啟用',
                    inline=False
                )
    embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/thumb/7/7e/Engranajesreductores.JPG/240px-Engranajesreductores.JPG")
    await ctx.response.send_message(embed=embed)

# Enable Cog Command
@bot.tree.command(
    name='啟用齒輪',
    description='啟用指定的Cog'
)
async def enable_cog(ctx, cog: str):
    logging.info('啟用Cogs')
    logging.info(f'請求發起人：{ctx.user}, 參數： cog={cog}')
    if ctx.user.id not in BOT_ADMIN:
        await ctx.response.send_message('你沒有權限使用此機器人', ephemeral=True)
        return
    # if cog == '*':
    #     # 先卸載全部Cog
    #     for cog in bot.cogs:
    #         await bot.unload_extension(f'Cogs.{cog}')
    #     # 啟用全部Cog
    #     await load_extensions()
    try:
        # 檢查是否有該Cog
        if os.path.isfile(f'./Cogs/{cog}.py') == False:
            await ctx.response.send_message('找不到該Cog')
            return
        # 啟用Cog
        await bot.load_extension(f'Cogs.{cog}')
        await ctx.response.send_message(f'已啟用{cog}')
    except Exception as e:
        logging.error(f'發生錯誤：{e}')
        await ctx.response.send_message(f'發生錯誤：{e}')

# Disable Cog Command
@bot.tree.command(
    name='停用齒輪',
    description='停用指定的Cog'
)
async def disable_cog(ctx, cog: str):
    logging.info('停用Cogs')
    logging.info(f'請求發起人：{ctx.user}, 參數： cog={cog}')
    if ctx.user.id not in BOT_ADMIN:
        await ctx.response.send_message('你沒有權限使用此機器人', ephemeral=True)
        return
    try:
        # 檢查是否有該Cog
        if os.path.isfile(f'./Cogs/{cog}.py') == False:
            await ctx.response.send_message('找不到該Cog')
            return
        
        # 停用Cog
        await bot.unload_extension(f'Cogs.{cog}')
        await ctx.response.send_message(f'已停用{cog}')
    except Exception as e:
        logging.error(f'發生錯誤：{e}')
        await ctx.response.send_message(f'發生錯誤：{e}')

# Reload Cog Command
@bot.tree.command(
    name='重新載入齒輪',
    description='重新載入指定的Cog'
)
async def reload_cog(ctx, cog: str):
    logging.info('熱重載Cogs')
    logging.info(f'請求發起人：{ctx.user}, 參數： cog={cog}')
    if ctx.user.id not in BOT_ADMIN:
        await ctx.response.send_message('你沒有權限使用此機器人', ephemeral=True)
        return
    try:
        # 檢查是否有該Cog
        # 取得檔案絕對路徑
        SELF_PATH = os.path.dirname(os.path.abspath(__file__))
        logging.debug(f'檔案絕對路徑：{SELF_PATH}')
        # 檢查使用者請求的Cog是否為子資料夾（如tickets/ticket）
        if '/' in cog:
            logging.debug('使用者請求的Cog為子資料夾')
            # 取得子資料夾名稱
            sub_cog = cog.split('/')[0]
            logging.debug(f'子資料夾名稱：{sub_cog}')
            # 檢查是否有該子資料夾
            if os.path.isdir(f'./Cogs/{sub_cog}') == False:
                await ctx.response.send_message('找不到該Cog')
                return
        # 檢查是否有該Cog
        if not os.path.isfile(f'./Cogs/{cog}.py'):
            logging.debug('使用者請求的Cog為子資料夾')
            await ctx.response.send_message('找不到該Cog')
            return
        
        # 重新載入Cog
        await bot.reload_extension(f'Cogs.{cog}')
        await ctx.response.send_message(f'已重新載入{cog}')
    except Exception as e:
        logging.error(f'發生錯誤：{e}')
        if ctx.response.is_done():
            await ctx.followup.send(f'發生錯誤：{e}')
        else:
            await ctx.response.send_message(f'發生錯誤：{e}')

# Reload Admin Command
@bot.tree.command(
    name='重新載入管理員',
    description='重新載入管理員指令'
)
async def reload_admin(ctx):
    logging.info('熱重載管理員')
    logging.info(f'請求發起人：{ctx.user}')
    # 重新讀取配置檔案
    with open('cfg.yml', 'r', encoding='utf-8') as f:
        cfg = yaml.load(f, Loader=yaml.FullLoader)
        logging.info('讀取cfg.yml成功！')
    # 重新讀取管理員ID
    NEW_ADMIN = cfg["admin_id"]
    if ctx.user.id not in BOT_ADMIN and ctx.user.id not in NEW_ADMIN:
        await ctx.response.send_message('你沒有權限使用此機器人', ephemeral=True)
        return
    # 尋找哪些管理員是新增的、哪些被移除了
    new_admin = []
    removed_admin = []
    for admin in NEW_ADMIN:
        if admin not in BOT_ADMIN:
            new_admin.append(admin)
        if admin not in NEW_ADMIN:
            removed_admin.append(admin)
    # 更新管理員ID
    BOT_ADMIN = NEW_ADMIN
    logging.info(f'新增的管理員：{new_admin}')
    logging.info(f'被移除的管理員：{removed_admin}')
    # 把更新與移除的管理員合併，並透過+與-號分別顯示，存成一個多行字串
    new_admin_str = '\n'.join([f'+ {admin}' for admin in new_admin])
    removed_admin_str = '\n'.join([f'- {admin}' for admin in removed_admin])
    admin_str = new_admin_str + '\n' + removed_admin_str
    try:
        # 重新載入管理員指令
        await bot.reload_extension('admin')
        await ctx.response.send_message(f'已重新載入管理員，以下為更新的管理員：\n{admin_str}')
    except Exception as e:
        logging.error(f'發生錯誤：{e}')
        await ctx.response.send_message(f'發生錯誤：{e}')

# Help Command
@bot.tree.command(
    name='說明',
    description='取得機器人指令的說明'
)
async def help(ctx):
    logging.info('取得指令說明')
    logging.info(f'請求發起人：{ctx.user}')
    embed = discord.Embed(
        title='指令說明',
        description='以下為機器人指令的說明',
        color=discord.Color.green()
    )
    for command in bot.tree.walk_commands():
        embed.add_field(
            name=command.name,
            value=command.description,
            inline=False
        )
    await ctx.response.send_message(embed=embed)

# Sync Slash Command
@bot.command(
    name='sync',
    description='同步指令'
)
async def sync(ctx):
    logging.info('同步指令中...')
    if ctx.author.id not in BOT_ADMIN:
        await ctx.send('你沒有權限使用此機器人')
        return
    mes = await ctx.send('同步指令中...')
    slash = await bot.tree.sync()
    if not slash:
        await ctx.send('指令同步失敗')
        return
    embed = discord.Embed(
        title='指令同步',
        description='指令同步完成',
        color=discord.Color.green()
    )
    for slash_sl in slash:
        name = slash_sl.name
        description = slash_sl.description
        embed.add_field(
            name=name,
            value=description,
            inline=False
        )
    embed.set_thumbnail(url="https://gravatar.com/avatar/f7598bd8d4aba38d7219341f81a162fc842376b3b556b1995cbb97271d9e2915?s=256")
    # 正確的調用方式
    await mes.edit(content="完成同步！", embed=embed)

# 一開始bot開機需載入全部程式檔案，並且跳過nl開頭的檔案。
# 載入範圍包含Cogs資料夾與其子資料夾，但不包含子資料夾中的子資料夾。
async def load_extensions(bot):
    """Loads cogs from the 'Cogs' directory and its subdirectories, skipping files starting with 'nl'."""
    for root, _, files in os.walk("./Cogs"):
        for filename in files:
            if filename.endswith(".py") and not filename.startswith("nl"):
                relative_path = os.path.relpath(os.path.join(root, filename), "./")  # Get the path relative to the root directory.
                module_name = relative_path.replace(os.sep, '.')[:-3]  # Convert to module path, and remove ".py".
                try:
                    logging.info(f"載入 {relative_path} 中...")
                    await bot.load_extension(module_name)
                    logging.info(f"載入 {relative_path} 成功")
                    logging.getLogger(module_name).setLevel(logging.INFO)
                except NoEntryPointError as e:
                    logging.error(f"載入 {relative_path} 失敗，原因：無子程式加載切入點")
                    continue
                except Exception as e:
                    logging.error(f"載入 {relative_path} 失敗：{e}")
                    continue
            else:
                if filename.startswith("nl"):
                    logging.info(f"跳過 {filename}，原因：採用nl方式跳過載入")
                else:
                    logging.info(f"跳過 {filename}")

# Start Bot
try:
    with open('TOKEN.txt', 'r') as f:
        TOKEN = f.readline()
        logging.info('讀取TOKEN成功！')
        # logging.info(TOKEN)
except FileNotFoundError:
    logging.error('找不到 TOKEN.txt！請照 README.md 的步驟取得 TOKEN 並建立該文件')
    exit(1)
# TOKEN = cfg['TOKEN']
# if TOKEN == '' or TOKEN == 'yourTOKEN.pastethere':
#     logging.error('TOKEN 錯誤！')
#     exit()
# if re.match(r'^([MN][\w-]{23,25})\.([\w-]{6})\.([\w-]{27,39})$', TOKEN) is None:
#     logging.warning('機器人自我檢查系統偵測到：您提供的 TOKEN 格式錯誤')
#     logging.warning('這可能導致機器人運作崩潰或出現異常，請確保您提供的 TOKEN 是正確的')
#     logging.warning('機器人不會因此而強制退出，但請注意機器人的運作狀況，以免發生異常！')

async def main():
    async with bot:
        await load_extensions(bot)
        try:
            await bot.start(TOKEN)
        except KeyboardInterrupt:
            await bot.close()
            logging.info('Bot已關閉，謝謝使用！')
            exit(0)
        except discord.LoginFailure as e:
            logging.error('登入失敗，可能是TOKEN錯誤')
            logging.error('請前往 https://github.com/510208/yunyubot-dc-annou/?tab=readme-ov-file#TOKEN%E9%8C%AF%E8%AA%A4 了解更多')
            logging.error(f'錯誤訊息：{e}')
        except discord.errors.RateLimited as e:
            logging.error('登入失敗，可能是登入次數過多')
            logging.error('請稍後再試')
            logging.error(f'錯誤訊息：{e}')
        except discord.errors.PrivilegedIntentsRequired as e:
            logging.error('登入失敗，可能是未開啟Privileged Gateway Intents')
            logging.error('請前往 https://github.com/510208/yunyubot-dc-annou/?tab=readme-ov-file#%E7%89%B9%E6%AC%8A%E7%B6%B2%E9%97%9C%E6%84%8F%E5%9C%96%E9%8C%AF%E8%AA%A4 了解更多')
            logging.error(f'錯誤訊息：{e}')
        except Exception as e:
            logging.error(f'Bot發生錯誤：{e}')
            logging.error('請前往 https://github.com/510208/yunyubot-dc-annou/?tab=readme-ov-file#-%E9%81%87%E5%88%B0%E5%95%8F%E9%A1%8C 回報錯誤')

# 確定執行此py檔才會執行
async def close_bot():
    # 卸載全部Cog
    logging.info('卸載全部Cogs')
    for cog in bot.cogs:
        logging.info(f'卸載{cog}中...')
        try:
            bot.unload_extension(f'Cogs.{cog}')
            logging.info(f'卸載{cog}成功')
        except Exception as e:
            logging.error(f'卸載{cog}失敗：{e}')
    logging.info('Bot關閉中...')
    await bot.close()
    logging.info('Bot已關閉，謝謝使用！')

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        asyncio.run(close_bot())
        exit(0)
else:
    logging.error(f'請直接執行此 {__name__}.py 檔')
    # exit(1)