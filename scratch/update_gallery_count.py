# -*- coding: utf-8 -*-
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TPL_PATH = os.path.join(BASE_DIR, "templates", "index.html")
APP_JS_PATH = os.path.join(BASE_DIR, "static", "js", "app.js")

# 1. Update templates/index.html
with open(TPL_PATH, "r", encoding="utf-8") as f:
    html = f.read()

old_snippet = """              <div style="font-size:12px; color:#64748b; margin-top:2px;">
                共收錄 <span id="gallery-total-count" style="font-weight:700; color:#2563eb;">0</span> 件實作專案
              </div>
            </div>
            <!-- Category Filter Buttons -->
            <div class="gallery-filter-bar">
              <button type="button" class="gallery-filter-btn active" data-filter="all" onclick="filterWorks('all', this)">全部展示</button>
              <button type="button" class="gallery-filter-btn" data-filter="期中報告" onclick="filterWorks('期中報告', this)">📌 期中報告</button>
              <button type="button" class="gallery-filter-btn" data-filter="期末成果" onclick="filterWorks('期末成果', this)">🏆 期末成果</button>
              <button type="button" class="gallery-filter-btn" data-filter="自主練習" onclick="filterWorks('自主練習', this)">💡 自主練習</button>
              <button type="button" class="gallery-filter-btn" data-filter="mine" onclick="filterWorks('mine', this)">👤 我的作品</button>
            </div>"""

new_snippet = """              <div style="font-size:12px; color:#64748b; margin-top:2px;">
                <span id="gallery-category-label" style="font-weight:700; color:#1e293b;"></span>共收錄 <span id="gallery-total-count" style="font-weight:700; color:#2563eb;">0</span> 件實作專案 <span style="font-size:11px; color:#94a3b8;">(已排除教師示範)</span>
              </div>
            </div>
            <!-- Category Filter Buttons -->
            <div class="gallery-filter-bar">
              <button type="button" class="gallery-filter-btn active" data-filter="all" onclick="filterWorks('all', this)">全部展示 <span class="badge-count">(0)</span></button>
              <button type="button" class="gallery-filter-btn" data-filter="期中報告" onclick="filterWorks('期中報告', this)">📌 期中報告 <span class="badge-count">(0)</span></button>
              <button type="button" class="gallery-filter-btn" data-filter="期末成果" onclick="filterWorks('期末成果', this)">🏆 期末成果 <span class="badge-count">(0)</span></button>
              <button type="button" class="gallery-filter-btn" data-filter="自主練習" onclick="filterWorks('自主練習', this)">💡 自主練習 <span class="badge-count">(0)</span></button>
              <button type="button" class="gallery-filter-btn" data-filter="mine" onclick="filterWorks('mine', this)">👤 我的作品 <span class="badge-count">(0)</span></button>
            </div>"""

if old_snippet in html:
    html = html.replace(old_snippet, new_snippet)
    with open(TPL_PATH, "w", encoding="utf-8") as f:
        f.write(html)
    print("SUCCESS: Updated templates/index.html")
else:
    print("WARNING: old_snippet not found in templates/index.html")
