#!/usr/bin/env python3
import os, requests
from datetime import datetime

KEY = "sk-api-B4li9vGe0fH2_8fpTu1VmZ1I6-cmSnmkLFmWJ9GCKZCJ1l-jzpqwcE8CPJnSMBq8xv8nop-T9zrcK7vSkZRcil05c9TcADK07n94zG3v7Gk5fp3R2bW_DWo"

def call(p):
    r = requests.post("https://api.minimax.chat/v1/text/chatcompletion_v2", 
        headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"},
        json={"model": "abab6.5s-chat", "messages": [{"role":"system","content":"你是编辑"}, {"role":"user","content":p}], "max_tokens": 500}, timeout=60)
    return r.json().get("choices",[{}])[0].get("message",{}).get("content","获取失败")

def html(date, c):
    return f'''<!DOCTYPE html><html><head><meta charset="UTF-8"><title>AI日报-{date}</title><style>body{{font-family:sans-serif;background:linear-gradient(#1a1a2e,#16213e);color:#fff;padding:40px}}h1{{background:-webkit-linear-gradient(#f093fb,#f5576c)}}section{{background:rgba(255,255,255,0.05);padding:20px;margin:15px 0;border-radius:10px}}h2{{color:#f093fb}}</style></head><body><h1>📰 AI日报 {date}</h1><section><h2>🔧 OpenClaw</h2><p>{c.get('o','')}</p></section><section><h2>⚡ 电力</h2><p>{c.get('p','')}</p></section><section><h2>📊 售电</h2><p>{c.get('e','')}</p></section><section><h2>💹 财经</h2><p>{c.get('f','')}</p></section><section><h2>📢 综合</h2><p>{c.get('n','')}</p></section><footer>🤖 AI生成</footer></body></html>'''

d = datetime.now().strftime("%Y年%m月%d日")
c = {"o":call("OpenClaw最新消息，3条"),"p":call("电力市场消息，3条"),"e":call("售电公司消息，3条"),"f":call("财经新闻，3条"),"n":call("综合新闻，3条")}
with open("index.html","w",utf-8) as f: f.write(html(d,c))
print("完成")
