#!/usr/bin/env python3
# mirror_board.py
# 每次运行会抓取内网榜单，并推送到 GitHub 仓库供外网访问（支持 GitHub Pages）

import os
import subprocess
import requests
from datetime import datetime

# === 配置区（改这里） ===
OJ_URL = "http://contest.gdutacm.org/public"   # 你的内网榜单地址（确保能访问）
GIT_REMOTE = "github"      # 你在本地 git 设置的 GitHub 远程名
GIT_BRANCH = "master"      # GitHub 默认分支
GIT_COMMIT_MSG = "Update leaderboard at {}"
INDEX_FILE = "index.html"  # 保存的 HTML 文件名
# ======================

def fetch_page():
    """抓取内网榜单页面"""
    try:
        r = requests.get(OJ_URL, timeout=15)
        r.raise_for_status()
        return r.text
    except Exception as e:
        print("抓取榜单失败：", e)
        return None

def save_html(html):
    """保存 HTML 到本地文件"""
    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        f.write(html)

def git_commit_push():
    """提交并推送到 GitHub"""
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    msg = GIT_COMMIT_MSG.format(ts)

    cmds = [
        ["git", "add", INDEX_FILE],
        ["git", "commit", "-m", msg],
        ["git", "push", GIT_REMOTE, GIT_BRANCH]
    ]

    for c in cmds:
        proc = subprocess.run(c, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if proc.returncode != 0:
            # 如果是 git commit 没有改动，可以忽略
            if "nothing to commit" in proc.stderr.lower():
                continue
            print("Git 命令失败:", " ".join(c))
            print(proc.stderr)
            return False
    return True

def main():
    html = fetch_page()
    if html:
        save_html(html)
        print("已抓取榜单并保存到", INDEX_FILE)
        ok = git_commit_push()
        if ok:
            print("已推送到 GitHub。")
        else:
            print("推送失败，请检查 GitHub 登录状态或网络。")
    else:
        print("没有抓到榜单，不进行提交。")

if __name__ == "__main__":
    main()
