#!/usr/bin/env python3
import os, requests
from datetime import datetime

TAVILY_KEY = os.environ.get("TAVILY_API_KEY", "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")
MINIMAX_KEY = os.environ.get("MINIMAX_API_KEY", "sk-api-B4li9vGe0fH2_8fpTu1VmZ1I6-cmSnmkLFmWJ9GCKZCJ1l-jzpqwcE8CPJnSMBq8xv8nop-T9zrcK7vSkZRcil05c9TcADK07n94zG3v7Gk5fp3R2bW_DWo")
MINIMAX_GROUP = os.environ.get("MINIMAX_GROUP_ID", "2030928714635682370")

def log(m): print(f"[{datetime.now().strftime('%H:%M:%S')}] {m}")

def search(q):
    log(f"搜索: {q}")
    try:
        r = requests.post("https://api.tavily.com/search", json={"api_key": TAVILY_KEY, "query": q, "max_results": 5}, timeout=30)
        items = [(i.get("title",""), i.get("url","")) for i in r.json().get("results",[])]
        log(f"  找到 {len(items)} 条")
        return items
    except Exception as e: log(f"  错误: {e}"); return []

def fmt(items):
    if not items: return '<div style="padding:10px;color:#888">暂无</div>'
    html = ''
    for t, u in items:
        if t and u: html += f'<div style="padding:12px 0;border-bottom:1px solid rgba(255,255,255,0.05)"><div>{t}</div><a href="{u}" target="_blank" style="color:#f093fb;font-size:0.85rem;margin-top:5px">🔗 原文</a></div>'
    return html

def html(date, d):
    return f'''<!DOCTYPE html><html><head><meta charset="UTF-8"><title>日报-{date}</title><style>body{{font-family:sans-serif;background:linear-gradient(#1a1a2e,#16213e);color:#fff;padding:40px}}h1{{background:-webkit-linear-gradient(#f093fb,#f5576c)}}section{{background:rgba(255,255,255,0.05);padding:25px;margin:20px 0;border-radius:16px}}h2{{color:#f093fb}}</style></head><body><h1>📰 {date}</h1><section><h2>🔧 OpenClaw</h2>{d.get('o','')}</section><section><h2>⚡ 电力</h2>{d.get('p','')}</section><section><h2>📊 售电</h2>{d.get('e','')}</section><section><h2>💹 财经</h2>{d.get('f','')}</section><section><h2>📢 综合</h2>{d.get('n','')}</section></body></html>'''

log("开始...")
d = datetime.now().strftime("%Y年%m月%d日")
q = {"o":"OpenClaw AI","p":"中国电力 青海竞价","e":"青海售电","f":"财经","n":"综合"}
c = {k:fmt(search(v)) for k,v in q.items()}
with open("index.html","w",encoding="utf-8") as f: f.write(html(d,c))
log("完成!")
