#!/usr/bin/env python3
import requests
from datetime import datetime

TAVILY_KEY = "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"
MINIMAX_KEY = "sk-api-B4li9vGe0fH2_8fpTu1VmZ1I6-cmSnmkLFmWJ9GCKZCJ1l-jzpqwcE8CPJnSMBq8xv8nop-T9zrcK7vSkZRcil05c9TcADK07n94zG3v7Gk5fp3R2bW_DWo"
MINIMAX_GROUP = "2030928714635682370"

def search(query):
    url = "https://api.tavily.com/search"
    try:
        r = requests.post(url, json={"api_key": TAVILY_KEY, "query": query, "max_results": 5}, timeout=30)
        return [(i.get("title",""), i.get("url","")) for i in r.json().get("results",[])]
    except: return []

def call(prompt):
    url = "https://api.minimax.chat/v1/text/chatcompletion_v2"
    headers = {"Authorization": f"Bearer {MINIMAX_KEY}", "Content-Type": "application/json"}
    data = {"model": "abab6.5s-chat", "messages": [{"role":"system","content":"编辑"},{"role":"user","content":prompt}], "max_tokens": 400, "group_id": MINIMAX_GROUP}
    try:
        r = requests.post(url, headers=headers, json=data, timeout=120)
        result = r.json()
        if "error" in result: return str(result['error'])
        choices = result.get("choices", [])
        if choices: return choices[0].get("message",{}).get("content","")
    except: return "错误"

def fmt(items):
    if not items: return '<div>暂无</div>'
    html = ''
    for title, url in items:
        if title: html += f'<div style="padding:12px 0;border-bottom:1px solid rgba(255,255,255,0.05)"><div>{title}</div><a href="{url}" target="_blank" style="color:#f093fb;font-size:0.85rem;margin-top:5px">🔗 查看原文</a></div>'
    return html

def html(date, d):
    return f'''<!DOCTYPE html><html><head><meta charset="UTF-8"><title>日报-{date}</title><style>body{{font-family:sans-serif;background:linear-gradient(#1a1a2e,#16213e);color:#fff;padding:40px}}h1{{background:-webkit-linear-gradient(#f093fb,#f5576c);-webkit-background-clip:text}}section{{background:rgba(255,255,255,0.05);padding:25px;margin:20px 0;border-radius:16px}}h2{{color:#f093fb}}a{{text-decoration:none}}</style></head><body><h1>📰 {date}</h1><section><h2>🔧 OpenClaw</h2>{d.get('o','')}</section><section><h2>⚡ 电力</h2>{d.get('p','')}</section><section><h2>📊 售电</h2>{d.get('e','')}</section><section><h2>💹 财经</h2>{d.get('f','')}</section><section><h2>📢 综合</h2>{d.get('n','')}</section></body></html>'''

d = datetime.now().strftime("%Y年%m月%d日")
c = {"o":fmt(call("搜索OpenClaw及AI自动化工具的最新消息，5条重要新闻，每条用一句话概括标题"))}
c["p"] = fmt(call("搜索中国电力市场：青海省竞价上网、国网电网竞价上网最新政策、新能源发电，水电站发电电竞价消息，5条"))
c["e"] = fmt(call("搜索青海省售电公司动态：注册量变化、业务量前10排名等，5条"))
c["f"] = fmt(call("今天最重要的10条财经新闻"))
c["n"] = fmt(call("今天最重要的10条综合新闻"))
with open("index.html","w") as f: f.write(html(d,c))
print("完成")
