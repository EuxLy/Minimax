#!/usr/bin/env python3
import requests
from datetime import datetime

KEY = "sk-api-B4li9vGe0fH2_8fpTu1VmZ1I6-cmSnmkLFmWJ9GCKZCJ1l-jzpqwcE8CPJnSMBq8xv8nop-T9zrcK7vSkZRcil05c9TcADK07n94zG3v7Gk5fp3R2bW_DWo"
GROUP = "2030928714635682370"

def call(prompt):
    url = "https://api.minimax.chat/v1/text/chatcompletion_v2"
    headers = {"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"}
    data = {"model": "abab6.5s-chat", "messages": [{"role":"system","content":"编辑"},{"role":"user","content":prompt}], "max_tokens": 600, "group_id": GROUP}
    try:
        r = requests.post(url, headers=headers, json=data, timeout=120)
        result = r.json()
        if "error" in result: return "⚠️ " + str(result['error'])
        choices = result.get("choices", [])
        if choices and len(choices) > 0:
            content = choices[0].get("message", {}).get("content")
            if content: return content
        return "⚠️ 无内容"
    except Exception as e: return "⚠️ " + str(e)

def fmt(items):
    if not items or "⚠️" in items: return f'<p>{items}</p>'
    lines = [l.strip() for l in items.strip().split('\n') if l.strip()]
    html = ''
    for i, line in enumerate(lines[:5]):
        title = line.lstrip('0123456789.、) ').strip()
        if title: html += f'<div style="padding:10px 0;border-bottom:1px solid rgba(255,255,255,0.05)">{title}</div>'
    return html or f'<p>{items}</p>'

def html(date, d):
    return f'''<!DOCTYPE html><html><head><meta charset="UTF-8"><title>日报-{date}</title><style>body{{font-family:-apple-system,sans-serif;background:linear-gradient(#1a1a2e,#16213e);color:#fff;padding:40px}}h1{{background:-webkit-linear-gradient(#f093fb,#f5576c);-webkit-background-clip:text}}section{{background:rgba(255,255,255,0.05);padding:25px;margin:20px 0;border-radius:16px}}h2{{color:#f093fb;font-size:1.4rem;margin-bottom:15px;border-bottom:1px solid rgba(255,255,255,0.1);padding-bottom:10px}}</style></head><body><h1>📰 每日AI简报 {date}</h1><section><h2>🔧 OpenClaw</h2>{d.get('o','')}</section><section><h2>⚡ 电力</h2>{d.get('p','')}</section><section><h2>📊 售电</h2>{d.get('e','')}</section><section><h2>💹 财经</h2>{d.get('f','')}</section><section><h2>📢 综合</h2>{d.get('n','')}</section></body></html>'''

d = datetime.now().strftime("%Y年%m月%d日")
c = {"o":fmt(call("O")),"p":fmt(call("P")),"e":fmt(call("E")),"f":fmt(call("F")),"n":fmt(call("N"))}
with open("index.html","w",encoding="utf-8") as f: f.write(html(d,c))
print("OK")
