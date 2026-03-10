#!/usr/bin/env python3
import requests
from datetime import datetime

KEY = "sk-api-B4li9vGe0fH2_8fpTu1VmZ1I6-cmSnmkLFmWJ9GCKZCJ1l-jzpqwcE8CPJnSMBq8xv8nop-T9zrcK7vSkZRcil05c9TcADK07n94zG3v7Gk5fp3R2bW_DWo"
GROUP = "2030928714635682370"

def call(prompt):
    url = "https://api.minimax.chat/v1/text/chatcompletion_v2"
    headers = {"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"}
    data = {"model": "abab6.5s-chat", "messages": [{"role":"system","content":"你是专业财经编辑，擅长写新闻摘要"},{"role":"user","content":prompt}], "max_tokens": 600, "group_id": GROUP}
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
    if not items or "⚠️" in items: return f'<div style="padding:10px">{items}</div>'
    lines = [l.strip() for l in items.strip().split('\n') if l.strip()]
    html = ''
    for line in lines[:5]:
        title = line.lstrip('0123456789.、) ').strip()
        if title: html += f'<div style="padding:10px 0;border-bottom:1px solid rgba(255,255,255,0.05)">{title}</div>'
    return html or f'<div>{items}</div>'

def html(date, d):
    return f'''<!DOCTYPE html><html><head><meta charset="UTF-8"><title>日报-{date}</title><style>body{{font-family:-apple-system,sans-serif;background:linear-gradient(#1a1a2e,#16213e);color:#fff;padding:40px}}h1{{background:-webkit-linear-gradient(#f093fb,#f5576c);-webkit-background-clip:text}}section{{background:rgba(255,255,255,0.05);padding:25px;margin:20px 0;border-radius:16px}}h2{{color:#f093fb;font-size:1.4rem;margin-bottom:15px;border-bottom:1px solid rgba(255,255,255,0.1);padding-bottom:10px}}</style></head><body><h1>📰 每日AI简报 {date}</h1><section><h2>🔧 OpenClaw技术动态</h2>{d.get('o','')}</section><section><h2>⚡ 电力交易</h2>{d.get('p','')}</section><section><h2>📊 售电公司</h2>{d.get('e','')}</section><section><h2>💹 财经新闻</h2>{d.get('f','')}</section><section><h2>📢 综合新闻</h2>{d.get('n','')}</section></body></html>'''

d = datetime.now().strftime("%Y年%m月%d日")
c = {"o":fmt(call("搜索OpenClaw及AI自动化工具的最新消息，5条重要新闻，每条用一句话概括标题"))}
c["p"] = fmt(call("搜索中国电力市场：青海省竞价上网、国网电网竞价上网最新政策、新能源发电、水电站发电电竞价消息，5条"))
c["e"] = fmt(call("搜索青海省售电公司动态：注册量变化、业务量前10排名等，5条"))
c["f"] = fmt(call("今天最重要的10条财经新闻"))
c["n"] = fmt(call("今天最重要的10条综合新闻"))
with open("index.html","w",encoding="utf-8") as f: f.write(html(d,c))
print("完成")
