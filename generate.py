#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import requests
from datetime import datetime

TAVILY_KEY = "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"
MINIMAX_KEY = "sk-api-B4li9vGe0fH2_8fpTu1VmZ1I6-cmSnmkLFmWJ9GCKZCJ1l-jzpqwcE8CPJnSMBq8xv8nop-T9zrcK7vSkZRcil05c9TcADK07n94zG3v7Gk5fp3R2bW_DWo"
MINIMAX_GROUP = "2030928714635682370"

def log(msg):
    print("[%s] %s" % (datetime.now().strftime("%H:%M:%S"), msg))

def search(query):
    log("Searching: " + query)
    try:
        url = "https://api.tavily.com/search"
        data = {"api_key": TAVILY_KEY, "query": query, "max_results": 5}
        r = requests.post(url, json=data, timeout=30)
        results = r.json().get("results", [])
        items = [(i.get("title", ""), i.get("url", "")) for i in results[:5]]
        log("Found: " + str(len(items)))
        return items
    except Exception as e:
        log("Error: " + str(e))
        return []

def format_items(items):
    if not items:
        return '<div style="padding:10px;color:#888">No data</div>'
    html = ""
    for title, url in items:
        if title and url:
            html += '<div style="padding:12px 0;border-bottom:1px solid rgba(255,255,255,0.05)">'
            html += '<div>' + title + '</div>'
            html += '<a href="' + url + '" target="_blank" style="color:#f093fb;font-size:0.85rem;margin-top:5px">Original</a>'
            html += '</div>'
    return html

def generate_html(date, news):
    html = '''<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Daily Report - ''' + date + '''</title>
<style>
body{font-family:sans-serif;background:linear-gradient(#1a1a2e,#16213e);color:#fff;padding:40px}
h1{background:-webkit-linear-gradient(#f093fb,#f5576c)}
section{background:rgba(255,255,255,0.05);padding:25px;margin:20px 0;border-radius:16px}
h2{color:#f093fb}
</style>
</head>
<body>
<h1>Daily Report ''' + date + '''</h1>
<section><h2>OpenClaw</h2>''' + news.get('o','') + '''</section>
<section><h2>Power</h2>''' + news.get('p','') + '''</section>
<section><h2>Electricity</h2>''' + news.get('e','') + '''</section>
<section><h2>Finance</h2>''' + news.get('f','') + '''</section>
<section><h2>News</h2>''' + news.get('n','') + '''</section>
</body>
</html>'''
    return html

log("Starting...")
date = datetime.now().strftime("%Y-%m-%d")

queries = {
    "o": "OpenClaw AI news",
    "p": "China power market Qinghai",
    "e": "Qinghai electricity company",
    "f": "Finance news China",
    "n": "China news"
}

news = {}
for key, query in queries.items():
    news[key] = format_items(search(query))

html_content = generate_html(date, news)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_content)

log("Done!")
