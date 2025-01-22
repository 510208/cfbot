<p align="center"><img src="https://github.com/user-attachments/assets/debe6451-5a5a-4867-a4ba-979eb924eb1e" width="400px"></p>

<h1 align="center"><strong>
CfBot
</strong></h1>

<p align="center">
   <a href="https://discord.gg/CWCjhRGJ2e">
      <img src="https://github.com/user-attachments/assets/b98f0cdb-b224-4cea-a12f-f1a72ecc5260" width="150px">
   </a>
   <a href="https://github.com/510208">
      <img src="https://github.com/user-attachments/assets/f4c073e0-0bde-4d1e-91e9-0b384fc2ca54" width="150px">
   </a>
   <a href="https://discordpy.readthedocs.io/">
      <img src="https://github.com/user-attachments/assets/21ac2c4d-3ad9-44fe-a2ff-40914c3d2e30" width="150px">
   </a>
   <a href="https://github.com/510208/cfbot">
      <img src="https://github.com/user-attachments/assets/5ef90eeb-5127-435f-89ab-e4e1fe46e2ac" width="150px">
   </a>
</p>

> 原 `雲羽機器人`、`CloudFeather Announcement Bot` 等名稱，因為名稱太亂，就整理一下了

[![Stand With Ukraine](https://raw.githubusercontent.com/vshymanskyy/StandWithUkraine/main/banner2-direct.svg)](https://stand-with-ukraine.pp.ua)

> [!IMPORTANT]  
> 本機器人為 [510208](https://github.com/510208) 為雲羽生存服開發的機器人，專案所有權仍為 510208 所有，因此即使雲羽生存服關閉，你也仍然可以使用它！

這是一個提供給 [🪶Minecraft 雲羽伺服器](https://discord.gg/CfGvx3NQWZ) 的 Discord Bot，由服主 SamHacker 編寫。為了幫助更多人而不限於我們伺服器內部，我將此專案開源出來給大家使用

## 💻 如何部署？

你可以使用虛擬環境或直接搭建，以下分析兩種方式的優缺點：

| | [**📦 虛擬環境**](#-虛擬環境) | [**⏰ 直接搭建**](#-直接搭建) |
|:---|:---|:---|
| **原理** | 在電腦上建立一個虛擬的、與本機隔離的獨立 Python 環境，<br>並在那之中運行機器人，就像沙箱一樣！ | 使用原本就安裝在電腦上的 Python 原生環境直接運行機器人，<br>這種方法你可以打少少的指令完成一個部署，期待嗎？
| **優點** | <li>無須擔心為了機器人妨礙到其他 Python 軟體的執行<li>可提供更佳的彈性 | <li>部署較為簡單<li>耗用儲存空間較少 |
| **缺點** | <li>部署較為麻煩<li>每次執行前需要先切換進虛擬環境中 | <li>容易造成環境衝突<li>後期糾錯較為麻煩 |

### 📦 虛擬環境

搭建在 Python 虛擬環境中是個不錯的主意！如此一來，你可以比較不需要擔心插件衝突的問題，並且它提供了你未來擴充機器人的彈性。想像一下，未來你的機器人可以幫你管整個 Minecraft 伺服器，聽起來是不是很心動？

心動不如馬上行動，我們開始吧！

1. 先前往 [Python官網](https://www.python.org/) 下載並安裝 Python
> 喔對了！我使用的是 Python 3.10.6，我可以保證這個版本下的程式可以正常運作！
> 
> 請記得，安裝時必須要勾選 `Add Python 3.x to PATH`，否則待會的操作會很麻煩喔...
2. 安裝完成後，你可以在網頁最上面有綠色`<> Code`按紐，按下它之後點選"Download ZIP"（在最下方），下載後解壓縮
   （Zip格式可以用Windows 10以上的系統解壓），或是使用以下兩個按鈕下載發行版與開發中版本


<a href="https://github.com/510208/cfbot/releases/latest">
   <img src="https://github.com/user-attachments/assets/9b0f058e-e3c6-4451-8de8-b19f947291d0" width="150px">
</a>
<a href="https://github.com/510208/cfbot">
   <img src="https://github.com/user-attachments/assets/5d6ab893-d9ab-48f2-bb73-55be590412b4" width="150px">
</a>

3. 按住Shift鍵並在資料夾中右鍵，選擇"使用PowerShell開啟"
4. 會跳出一個看起來很複雜的視窗，不用怕，直接貼上下面這段就好，記得一行一行貼：
```shell
$ python -m venv
$ cd .venv/Scripts
$ activate
$ pip install -r requirements.txt
```
> 請記得，前面的錢號不用打進去，那代表你要自己輸入的意思
5. 現在你搭建好了！恭喜你！！

### ⏰ 直接搭建

很簡單，首先先照上方虛擬方式的方法執行，但你只需要打這些指令即可：

```shell
$ pip install -r requirements.txt
```
（是的沒錯就這麼少）

### 🔒 建立機器人

如果你看到了這裡，恭喜你已經完成了一半！再來你需要去建立一個 Discord 機器人，請照以下教學處理：

1. 前往 [https://discord.com/developers/applications](https://discord.com/developers/applications) 網站並登入自己的 Discord 帳號
2. 單按右上紫色的 "New Applaction"，它會幫你建立一個新的機器人。然後會跳出一個如圖的訊息，輸入你希望機器人的名字，然後打勾勾按 Create 建立機器人：

![image](https://github.com/510208/yunyubot-dc-annou/assets/107909497/f5363ebd-c448-4ca8-a0e6-9ef448949aab)

3. 切換到左列的 Bot，將底下三個 "Privileged Gateway Intents" 的勾都勾上：

![image](https://github.com/510208/yunyubot-dc-annou/assets/107909497/44ceb53d-4776-404c-b6b6-e2a6900fa8b3)

4. 滑到上方，單按 Token 下大大的 "Reset Token"。點下去，如果你有雙步驟驗證請打一下驗證碼：

![image](https://github.com/510208/yunyubot-dc-annou/assets/107909497/27994e32-8374-457f-8ebe-023263df4489)

5. 看到一組亂碼，存下來千萬別告訴別人。打開軟體的資料夾找到 `token.txt` ，將剛剛的亂碼貼進這個文件中
> 這組亂碼跟你的密碼是一樣的，因此千萬要小心不要分享給人。只要別人擁有這組亂碼，他就可以在你的 Discord 群組中為所欲為！

### ▶ 機器人，啟動！！

恭喜你進度條到了99%，剩下最後一件事就是雙按 `main.py` 啟動機器人。

如果看到類似以下的訊息，代表你已經可以去找機器人...了嗎？
```log
228: [2024-06-29 21:16:46,384][INFO] - [main] 載入annou_stat.py中...
30: [2024-06-29 21:16:46,412][INFO] - [annou_stat] AnnouStat cog 已經載入
230: [2024-06-29 21:16:46,415][INFO] - [main] 載入annou_stat.py成功
237: [2024-06-29 21:16:46,416][INFO] - [main] 跳過nlfile.py, 原因：採用nl方式跳過載入
239: [2024-06-29 21:16:46,416][INFO] - [main] 跳過__pycache__
603: [2024-06-29 21:16:46,417][INFO] - [client] logging in using static token
561: [2024-06-29 21:16:48,248][INFO] - [gateway] Shard ID None has connected to Gateway (Session ID: 6989b35e31230ee56a079ae50220d5a3).
28: [2024-06-29 21:16:50,347][INFO] - [main] Logged in as (機器人名稱)#(機器人編號) (ID: 機器人ID)
```

### 🤝 邀請機器人

對，現在機器人啟動了。但你有沒有發現一件事情：

> 我的伺服器裡還是沒這隻機器人啊！！！！

因此讓我們邀請機器人吧！

1. 切換到 [https://discord.com/developers/applications](https://discord.com/developers/applications)，點擊你剛剛建立好的機器人之後切換到左列 OAuth 中：

![image](https://github.com/510208/yunyubot-dc-annou/assets/107909497/a3acf2ee-2295-4a9a-b495-be47ff2cc9c9)

2. 拉到下方 `OAuth2 URL Generator`，勾選bot，然後勾選"Adminstrator"給機器人管理權限
3. `GENERATED URL`即為邀機器人進服的方法！

## ⛏ 編輯配置

> [!CAUTION]
> 編輯完配置後記得要使用Reload指令以加載新版本

請參考 [`cfg.yml`](cfg.yml) 中的設定資訊來做執行

## 🆖 協助開發

首先，我個人也不是什麼太厲害的人，對於這邊的貢獻流程如果有建議歡迎提Issue補充！總之非常感謝你願意看到這一步，如果你也想為這個專案做貢獻，請照以下說明操作：

### ❗ 常見錯誤

#### 特權網關意圖錯誤

```
discord.errors.PrivilegedIntentsRequired: Shard ID None is requesting privileged intents that have not been explicitly enabled in the developer portal. It is recommended to go to https://discord.com/developers/applications/ and explicitly enable the privileged intents within your application's page. If this is not possible, then consider disabling the privileged intents instead.
```

以上是特權網關意圖錯誤，如果你的錯誤碼類似這樣，請前往 [Discord Developer Portal](https://discord.com/developers/applications)，進入機器人選項後在Bots底下的"Privileged Gateway Intents"全部勾選後Save並且重啟即可排除

#### Token錯誤

```
discord.errors.LoginFailure: Improper token has been passed.
```

類似以上訊息，可能是你的 Token 錯誤。請照上方教學重新前往開發者面板並取得新的 Token 後 再次嘗試，仍然錯誤再前來詢問


> [!CAUTION]
> 如果 Token 被你誤發到 Github 等平台，Discord 也會自動重置該組 Token 以防止意外發生

### ❓ 遇到問題

如果你遇到以下情況，請照這個章節的說明操作：

- 遇到Traceback錯誤以致無法執行或啟動
- 執行或啟動過程中遇到Traceback錯誤，但仍能繼續走流程
- 或其他問題適合提Issue

請在 [Issues](https://github.com/510208/yunyubot-dc-annou/issues) 中提出問題，並提供以下必須資訊（如果不提供或找不到，我們有權利不做受理）：

- Python版本與機器人版本（可以透過Git檢視Commit的編號）
- 錯誤內容
- 如何啟動這個錯誤
- 發現時間
- 是否已經確定不是自己問題

有部分錯誤已知解決方法並列在常見錯誤區段中，請自行先做檢查後再提 Issue，否則我們有權不受理

### ❤ 協助開發

非常謝謝你願意協助這個機器人的完善，未來我會考慮更換一下這個機器人的名稱。順帶一提，本機器人應該不會是 [Nether Bot](https://github.com/510208/nether) 的繼承人（至少現在不會）

如果你要協助開發，請參考[CONTRIBUTING.md](CONTRIBUTING.md)的描述，謝謝您

### 💗 贊助專案

> [!IMPORTANT]
> 我們目前不接受任何格式的贊助，非常遺憾

## 🙏 備註與謝誌

非常感謝 @510208 的開發，與以下用戶的協助：

| **用戶或團體** | **內容** |
|:---|:---|
| [雲羽生存服](https://discord.gg/CfGvx3NQWZ) | 提供Discord群組做為測試之用 |
| [Asteroid Bot Hosting](https://discord.gg/DuJEFKqckm) | 提供機器人24小時託管 |
| LunarKdeo3147 | 協助測試專案與提供建議 |
| !夜間部（ @woodypegasus382 ） | 提供 [ticket.py](https://github.com/510208/cfbot/blob/main/Cogs/tickets/ticket.py) 開發協助 |

與你的使用！
