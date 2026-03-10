#!/usr/bin/env python3
import os, requests
from datetime import datetime

KEY = "sk-api-B4li9vGe0fH2_8fpTu1VmZ1I6-cmSnmkLFmWJ9GCKZCJ1l-jzpqwcE8CPJnSMBq8xv8nop-T9zrcK7vSkZRcil05c9TcADK07n94zG3v7Gk5fp3R2bW_DWo"
GROUP = "2030928714635682370"

def call(p):
    url = "https://api.minimax.chat/v1/text/chatcompletion_v2"
    headers = {"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"}
    data = {"model": "abab6.5s-chat", "messages": [{"role":"system","content":"编辑"}, {"role":"user","content":p}], "max_tokens": 500, "group_id": GROUP}
    try:
        r = requests.post(url, headers=headers, json=data, timeout=90)
        result = r.json()
        if "choices" in result and len(result["choices"]) > 0:
            return result["choices"][0]["message"]["content"]
        return f"错误: {result}"
    except Exception as e:
        return f"错误: {str(e)}"

def html(date, c):
    return f'''<!DOCTYPE html><html><head><meta charset="UTF-8"><title>AI日报-{date}</title><style>body{{font-family:sans-serif;background:linear-gradient(#1a1a2e,#16213e);color:#fff;padding:40px}}section{{background:rgba(255,255,255,0.05);padding:20px;margin:15px 0;border-radius:10px}}h2{{color:#f093fb}}</style></head><body><h1>📰 AI日报 {date}</h1><section><h2>🔧 OpenClaw</h2><p>{c.get('o','')}</p></section><section><h2>⚡ 电力</h2><p>{c.get('p','')}</p></section><section><h2>📊 售电</h2><p>{c.get('e','')}</p></section><section><h2>💹 财经</h2><p>{c.get('f','')}</p></section><section><h2>📢 综合</h2><p>{c.get('n','')}</p></section></body></html>'''

d = datetime.now().strftime("%Y年%m月%d日")
c = {"o":call("OpenClaw消息3条"),"p":call("电力消息3条"),"e":call("售电消息3条"),"f":call("财经3条"),"n":call("综合3条")}
with open("index.html","w",encoding="utf-8") as f: f.write(html(d,c))
print("完成")
