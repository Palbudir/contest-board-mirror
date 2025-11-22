#!/usr/bin/env python3
# mirror_board.py
# 每次运行会抓取内网榜单，并推送到 Gitee 仓库供外网访问

import os
import subprocess
import requests
from datetime import datetime

# === 配置区（改这里） ===
OJ_URL = "http://contest.gdutacm.org/public"   # 你的内网榜单地址（确保能访问）
GIT_BRANCH = "master"    # Gitee 默认是 master
GIT_COMMIT_MSG = "Update leaderboard at {}"
# ======================

def fetch_page():
    r = requests.get(OJ_URL, timeout=15)
    r.raise_for_status()
    return r.text

def save_html(html):
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)

def git_commit_push():
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    msg = GIT_COMMIT_MSG.format(ts)

    cmds = [
        ["git", "add", "index.html"],
        ["git", "commit", "-m", msg],
        ["git", "push", "origin", GIT_BRANCH]
    ]

    for c in cmds:
        proc = subprocess.run(c, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if proc.returncode != 0:
            print("Git command failed:", c)
            print(proc.stderr)
            return False
    return True

def main():
    try:
        html = fetch_page()
        save_html(html)
        print("已抓取榜单。")
        ok = git_commit_push()
        if ok:
            print("已推送到 Gitee。")
        else:
            print("推送失败，请检查 Gitee 登录状态。")
    except Exception as e:
        print("发生错误：", e)

if __name__ == "__main__":
    main()
