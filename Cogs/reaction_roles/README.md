# 📦 Recation Roles（反應規則）

## 🔍 功能簡介
- **作者**：SamHacker
- **授權條款**：GNU/GPL v3

使用前要先在頻道中傳送一則訊息，訊息內容可以自訂，例如：

> 點擊emoji來取得正式成員身分組

然後在配置文件中設定，設定後新加入的用戶可以點擊下方的反應來取得指定的身分組

## ⚙️ 設定方式

### cfg.yml
```yaml
reaction_roles:
  enabled: true                  # 是否啟用反應身分組
  role_message_id: 0000000000000000000  # 身分組訊息ID
  role_channel_id: 0000000000000000000  # 身分組訊息頻道ID
  remove_role_on_reaction_remove: true    # 移除反應時是否移除身分組
  reactions:                     # 反應設定，使用清單模式來設定多個
  - emoji: "🎮"                  # 反應表情符號
    role_id: 0000000000000000000  # 身分組ID
```

- `enabled`：是否啟用此擴充功能。
- `role_message_id`：反應身分組的訊息ID，也就是上面說要傳送的訊息的ID
- `role_channel_id`：反應身分組的訊息所在頻道ID，也就是 `role_message_id` 所在的頻道
- `remove_role_on_reaction_remove`：
  - **設為true時**，使用者新增反應會取得身分組，移除反應時該身分組也會被移除，適用在可選身分組
  - **設為false時**，使用者新增反應一樣會獲得身分組，但移除反應時身分組也會存在，也就是除非管理員設定，否則身分組只能新增不能移除
- `reactions`：YAML清單，指定所有回應。清單中每個項目都包含以下兩個鍵值對：
  - `emoji`：所要使用的Emoji，建議使用預設擁有的Emoji，目前不支持伺服器專屬Emoji
  - `role_id`：所要新增的身分組ID，機器人的身分組權限必須在該身分組之上，否則無法新增該身分組

## 🛠 指令列表
- 本功能無指令
- 配置請在cfg.yml中完成