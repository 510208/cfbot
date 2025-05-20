# ❤️ 協助開發

感謝你願意為 **CFBot** 貢獻力量！這份指南將幫助你順利參與開發，確保專案的品質與一致性。

---

---

## 🍽️ 建立分支

請在進行開發時，為你的變更建立 **獨立的分支**，避免直接提交到 `main` 分支。

### **✅ 良好分支命名範例**

- `feature-add_yaml_configure`：新增 YAML 配置功能。
- `feature-randomgames`：新增與隨機小遊戲相關的功能。

### **❌ 不建議的分支名稱**

- `feature-master`：容易與主分支混淆。
- `feature-add-some-game-for-some-players`：過長且不夠直觀。
- `randomgames`：前面建議註明`feature`或`fix`等，說明這個分支的意義

🔹 **請在 PR 提交時，請求合併到 `develop` 分支，而非 `main` 分支。**

> ⚠️ **請勿直接對 `main` 提交變更！** `main` 分支僅用於正式發布，所有變更應先提交至 `develop` 進行審核。

---

## 🏗️ 修改內部組件的規則

若你要修改 核心組件，請遵守以下規範：

- 確保變更有正當理由，例如修正錯誤、優化效能或增加通用性。
- 對所有影響的區塊進行全面測試，避免破壞現有功能。
- 避免破壞性變更（Breaking Changes），若無法避免，請提供遷移指南。
- 遵循現有架構與風格指南，保持代碼一致性。
- 提供詳細的變更紀錄，在 PR 中清楚描述修改內容。
- 更新對應的文件與設定檔，確保其他開發者能理解你的改動。
- 確保修改不影響現有的 CI/CD 流程，並通過所有測試。

## 🧩 擴充功能開發指南

### **📦 初始化開發環境**

本專案使用 **Discord.py** 進行開發，並採用 **Cogs 架構** 來確保模組化與穩定性。

1. 安裝 **PDM** 來管理依賴：

   ```bash
   pip install pdm
   ```

2. 複製專案程式碼：

   ```bash
   git clone https://github.com/510208/cfbot
   cd cfbot
   ```

3. 安裝依賴：

   ```bash
   pdm install
   ```

🔹 **現在你就可以開始開發了！**

---

### **📂 建立你的 Cog**

1. **在 `cogs` 目錄下建立一個資料夾**，命名為你的功能名稱，例如 `my-awesome-project`。
2. **在該資料夾內新增 `.py` 檔案**（與資料夾名稱相同），例如 `my-awesome-project.py`。
3. **使用以下模板進行開發**：

   ```python
   # 匯入模組，請將模組統一於此匯入
   import logging
   import discord
   from discord.ext import commands
   import yaml

   # 記錄檔系統，需要的除錯紀錄等請用logging模組輸出
   logger = logging.getLogger(__name__)

   # 齒輪說明，為你開發的Cog寫說明文件
   COG_INTRO = {
       "name": "歡迎訊息",
       "description": "歡迎新使用者加入 Discord 伺服器的訊息"
   }

   # 主齒輪
   class MyAwesomeCog(commands.Cog):
       def __init__(self, bot):
           # 初始化機器人，config改從self.config取得
           self.bot = bot
           self.config = bot.config.get("my_awesome_cog", {})

       @commands.Cog.listener()
       async def on_ready(self):
           # 在擴充功能準備好時跳通知
           logger.info(f"{COG_INTRO["name"]} 已加載！")

   async def setup(bot):
       # 檢查這項擴充功能是否被啟動
       if not bot.config.get("my_awesome_cog", {}).get("enabled", True):
           logger.info(f"跳過載入 {COG_INTRO["name"]}，因為它被禁用。")
           return
       await bot.add_cog(MyAwesomeCog(bot))
   ```

4. **在 `cfg.yml` 中新增相應的設定項目**：

   ```yaml
   # ================================
   #  ○ MyAwesomeCog 設定
   #  齒輪：tickets/...
   # ================================
   my_awesome_cog:
     enabled: true # 是否啟用此擴充功能
     # 其他配置設定，請在鍵後面加上說明，最好採用繁體中文撰寫
     key: value
     key2: value2
   ```

5. **最佳開發實踐**：
   - 使用可讀性高的變數名稱，避免無意義名稱（如 `a`, `b`, `test123`）。
   - 儘可能讓使用者可自訂功能設定。
   - 避免硬編碼（Hardcoding），使用變數或設定檔管理常數。
   - 需要額外的函式庫時，請更新 `pyproject.toml` 並在 PR 中註明。

---

## 📜 撰寫擴充功能文件

請確保你的擴充功能有清晰的文件，讓其他人能夠輕鬆使用它。

### **📖 `README.md` 範本**

將以下內容放入你的 **擴充功能資料夾** 中：

````markdown
# 📦 MyAwesomeCog

## 🔍 功能簡介

- **作者**：SamHacker
- **授權條款**：GNU/GPL v3

## ⚙️ 設定方式

\```yaml
my_awesome_cog:
enabled: true # 啟用此功能

# ...

\```

- `enabled`：是否啟用此擴充功能。

## 🛠 指令列表

- `!example`：示範指令。
````

### **📌 其他文件注意事項**

- 若你的功能 **預設不啟用**，請將 `enabled` 設為 `false`。
- 若你的功能 **不適合內建啟用**，請將檔案名稱前綴為 `nl_`（例如 `nl_my_feature.py`）。

---

## 🏋️ Pull Request 規則

當你準備提交 PR 時，請確保符合以下標準：

✅ **Pull Request 提交前檢查清單**：

- [ ] **確認程式碼通過基本測試**，確保無錯誤。
- [ ] **遵循 Python PEP8 規範**，確保程式碼格式清晰。
- [ ] **提供清楚的 PR 標題與描述**。
- [ ] **若修改現有功能，請提供相應的變更紀錄（Changelog）**。
- [ ] **若有 Issue，請在 PR 中標註（例如 `Closes #123`）**。

🔹 **提交 PR**：[GitHub Pull Requests](https://github.com/510208/cfbot/pulls)

感謝你的貢獻！🚀
