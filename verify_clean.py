# -*- coding: utf-8 -*-
import os, sys
sys.stdout.reconfigure(encoding='utf-8')
forbidden = ['連鎖餐飲', '死穴', '慘劇', '扣總分', '扣分', '隨堂測驗']
files = ['slides_data.js', 'index.html', '商業軟體應用.html', '平台首頁(單機離線直接點開).html', 'data/curriculum.json', 'downloads/Week02_Vibe_Coding_實作操作手冊.md']
clean = True
for fname in files:
    if os.path.exists(fname):
        with open(fname, 'r', encoding='utf-8') as f:
            c = f.read()
        for w in forbidden:
            if w in c:
                print(f'FAIL: {fname} contains {w}')
                clean = False
if clean:
    print('SUCCESS: 100% CLEAN OF ALL FORBIDDEN TERMS!')
