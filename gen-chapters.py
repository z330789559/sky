#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
扫描当前目录下的章节文件（形如 NNN-章名-章题.md），生成 chapters.json。
以后新增/改名章节后，运行一次即可，无需手改 index.html：

    python3 gen-chapters.py

分幕规则（按章号）：000–009 = 第一幕，010–023 = 第二幕，024 及以后 = 第三幕。
如需调整幕的分界，改下面 act() 里的两个边界即可。
"""
import os, re, json

ROOT = os.path.dirname(os.path.abspath(__file__))

def act(num: str) -> int:
    p = num[:3]
    if p < '010':
        return 1
    if p < '024':
        return 2
    return 3

def title_of(fname: str) -> str:
    parts = fname[:-3].split('-')          # 去掉 .md 再按 - 切
    if len(parts) >= 3:
        return parts[1] + ' · ' + '-'.join(parts[2:])
    return '-'.join(parts[1:])

def main():
    files = sorted(f for f in os.listdir(ROOT)
                   if re.match(r'^\d', f) and f.endswith('.md'))
    data = [{
        'file':  f,
        'num':   f.split('-')[0],
        'title': title_of(f),
        'act':   act(f.split('-')[0]),
    } for f in files]
    out = os.path.join(ROOT, 'chapters.json')
    with open(out, 'w', encoding='utf-8') as w:
        json.dump(data, w, ensure_ascii=False, indent=1)
        w.write('\n')
    print(f'✓ chapters.json 已更新：{len(data)} 篇')

if __name__ == '__main__':
    main()
