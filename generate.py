#!/usr/bin/env python3
import os, requests
from datetime import datetime

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")

def call_openai(prompt):
    if not OPENAI_API_KEY:
        return "API Key未配置"
    url = "https://api.openai.com/v1/chat/completions"
    headers = {"Authorization": f"Bearer {OPENAI_API_KEY}", "Content-Type": "application/json"}
    data = {"model": "gpt-4o-mini", "messages": [{"role": "system", "content": "你是专业编辑"}, {"role": "user", "content": prompt}], "max_tokens": 500}
    try:
        r = requests.post(url, headers=headers, json=data, timeout=60)
        return r.json().get("choices", [{}])[0].get("message", {}).get("content", "获取失败")
    except: return "获取失败"

def generate_html(date, content):
    return f'''<!DOCTYPE html><html lang="zh-CN"><head><meta charset="UTF-8"><title>每日AI简报 - {date}</title><style>*{{margin:0;padding:0;box-sizing:border-box}}body{{font-family:-apple-system,sans-serif;background:linear-gradient(135deg,#1a1a2e,#16213e);min-height:100vh;color:#fff;padding:40px 20px}}.container{{max-width:900px;margin:0 auto}}header{{text-align:center;margin-bottom:40px}}h1{{font-size:2.5rem;background:linear-gradient(90deg,#f093fb,#f5576c);-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:10px}}.date{{color:#888;font-size:1.1rem}}.section{{background:rgba(255,255,255,0.05);border-radius:16px;padding:25px;margin-bottom:20px}}.section h2{{color:#f093fb;font-size:1.4rem;margin-bottom:15px}}.summary{{color:#ccc;line-height:1.8;white-space:pre-line}}footer{{text-align:center;padding:40px;color:#666}}</style></head><body><div class="container"><header><h1>📰 每日AI简报</h1><p class="date">{date}</p></header><div class="section"><h2>🔧 OpenClaw技术动态</h2><div class="summary">{content.get('openclaw','')}</div></div><div class="section"><h2>⚡ 电力交易信息</h2><div class="summary">{content.get('power','')}</div></div><div class="section"><h2>📊 售电公司动态</h2><div class="summary">{content.get('electricity','')}</div></div><div class="section"><h2>💹 财经新闻</h2><div class="summary">{content.get('finance','')}</div></div><div class="section"><h2>📢 综合新闻</h2><div class="summary">{content.get('news','')}</div></div><footer><p>🤖 由 AI 自动生成</p></footer></div></body></html>'''

def main():
    date = datetime.now().strftime("%Y年%m月%d日")
    prompts = {"openclaw":"搜索最近24小时OpenClaw及AI自动化工具最新消息，3条","power":"搜索最近24小时中国电力市场消息，3条","electricity":"搜索最近24小时青海售电公司动态，3条","finance":"今天最重要的3条财经新闻","news":"今天最重要的3条综合新闻"}
    content = {k:call_openai(v) for k,v in prompts.items()}
    with open("index.html","w",encoding="utf-8") as f: f.write(generate_html(date,content))
    print("完成!")

if __name__ == "__main__": main()
