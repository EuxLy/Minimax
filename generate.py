#!/usr/bin/env python3
import requests
from datetime import datetime

KEY = "sk-api-B4li9vGe0fH2_8fpTu1VmZ1I6-cmSnmkLFmWJ9GCKZCJ1l-jzpqwcE8CPJnSMBq8xv8nop-T9zrcK7vSkZRcil05c9TcADK07n94zG3v7Gk5fp3R2bW_DWo"
GROUP = "2030928714635682370"

def call(prompt):
    url = "https://api.minimax.chat/v1/text/chatcompletion_v2"
    headers = {"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"}
    data = {"model": "abab6.5s-chat", "messages": [{"role":"system","content":"编辑"},{"role":"user","content":prompt}], "max_tokens": 300, "group_id": GROUP}
    try:
        r = requests.post(url, headers=headers, json=data, timeout=120)
        print(f"Status: {r.status_code}")
        result = r.json()
        if "error" in result: return f"错误: {result['error']}"
        choices = result.get("choices")
        if choices and len(choices) > 0:
            content = choices[0].get("message",{}).get("content")
            return content if content else "无内容"
        return f"结果: {result}"
    except Exception as e: return f"错误: {str(e)}"

def html(date, c):
    return f'''<!DOCTYPE html><html><head><meta charset="UTF-8"><title>日报-{date}</title><style>body{{font-family:sans-serif;background:linear-gradient(#1a1a2e,#16213e);color:#fff;padding:40px}}section{{background:rgba(255,255,255,0.05);padding:20px;margin:10px 0}}</style></head><body><h1>📰 {date}</h1><section><h2>🔧</h2><p>{c.get('o','')}</p></section><section><h2>⚡</h2><p>{c.get('p','')}</p></section><section><h2>📊</h2><p>{c.get('e','')}</p></section><section><h2>💹</h2><p>{c.get('f','')}</p></section><section><h2>📢</h2><p>{c.get('n','')}</p></section></body></html>'''

d = datetime.now().strftime("%Y年%m月%d日")
c = {"o":call("O"),"p":call("P"),"e":call("E"),"f":call("F"),"n":call("N")}
with open("index.html","w",encoding="utf-8") as f: f.write(html(d,c))
print("OK")
