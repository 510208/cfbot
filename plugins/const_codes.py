# 常數代碼

import requests

# 專案常數
REPO_NAME = 'yunyubot-dc-annou'

# 定義代碼
# 開啟 async 檢查專案最新版本
async def check_version():
    """檢查專案最新版本"""
    url = f"https://api.github.com/repos/510208/{REPO_NAME}/tags"
    response = requests.get(url)
    tags = response.json()
    latest_tag = tags[0]['name']
    zip_url = tags[0]['zipball_url']
    tar_url = tags[0]['tarball_url']
    return {'latest': latest_tag, 'zip': zip_url, 'tar': tar_url}