# -*- coding: utf-8 -*-
"""
Generate professorial Google Docs Interactive Web Application for Midterm Manual:
- Google_Docs_期中報告操作手冊(以分頁劃分).html
Features:
- Native Google Docs Document Tabs (文件分頁) left sidebar navigation
- 6 Tabs:
  Tab 1: 📌 實務守則與期中目標說明 (重要規範)
  Tab 2: ⚙️ 第一部分：Google Antigravity 安裝與 GitHub 配置 (附截圖)
  Tab 3: 📊 第二部分：行銷企劃 SOP 五大階段流程與邊界解讀 (附流程圖)
  Tab 4: 💬 第三部分：七大核心商務 Prompt 指引與示範案例 (一鍵複製)
  Tab 5: 🔑 第四部分：GitHub API Token 生成與自動發布指引 (附截圖)
  Tab 6: 🌟 第五部分：【期中專案加分】產業數據分析視覺化專區 (含寵物經濟數據庫)
  Tab 7: ✅ 第六部分：期中專案 7 大成果檢核清單 (Checklist)
- Embedded high-res base64 screenshots
- Copyable CLEAR prompt buttons
- Direct Google Docs Cloud & Word download links
"""
import os
import base64

base_dir = r"g:\我的雲端硬碟\萬能科技大學\備課\11501課表\11501商業軟體應用"
assets_dir = os.path.join(base_dir, "assets", "midterm_ref_images")

imgs = [
    ('image9.png', 'fig1_1'),
    ('image14.png', 'fig1_2'),
    ('image10.png', 'fig1_3'),
    ('image11.png', 'fig2_1'),
    ('image2.png', 'fig3_1'),
    ('image5.png', 'fig3_2'),
    ('image17.png', 'fig3_3'),
    ('image6.png', 'fig3_4'),
    ('image15.png', 'fig3_5'),
    ('image8.png', 'fig3_6'),
    ('image12.png', 'fig4_1'),
    ('image16.png', 'fig4_2'),
    ('image13.png', 'fig4_3'),
    ('image7.png', 'fig4_4'),
]

b64 = {}
for src, key in imgs:
    path = os.path.join(assets_dir, src)
    if os.path.exists(path):
        with open(path, 'rb') as f:
            b64[key] = f"data:image/png;base64,{base64.b64encode(f.read()).decode('utf-8')}"
    else:
        b64[key] = ""

html_content = f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>萬能科技大學 - 商業軟體應用 期中報告操作手冊 (Google Docs 原生分頁版)</title>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.2/css/all.min.css">
  <style>
    :root {{
      --docs-blue: #1a73e8;
      --docs-hover: #f1f3f4;
      --docs-active: #e8f0fe;
      --docs-text: #202124;
      --docs-muted: #5f6368;
      --docs-border: #dadce0;
      --docs-bg: #f8f9fa;
      --docs-gold: #d97706;
      --docs-card-bg: #ffffff;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: 'Google Sans', Roboto, -apple-system, BlinkMacSystemFont, "微軟正黑體", sans-serif;
      background-color: var(--docs-bg);
      color: var(--docs-text);
      display: flex;
      flex-direction: column;
      height: 100vh;
      overflow: hidden;
    }}
    /* Top Header Bar */
    header.docs-header {{
      background: #ffffff;
      height: 64px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 16px;
      border-bottom: 1px solid var(--docs-border);
      flex-shrink: 0;
    }}
    .docs-brand {{
      display: flex;
      align-items: center;
      gap: 12px;
    }}
    .docs-logo {{
      width: 40px;
      height: 40px;
      background: #4285f4;
      border-radius: 8px;
      display: flex;
      align-items: center;
      justify-content: center;
      color: #ffffff;
      font-size: 20px;
      box-shadow: 0 2px 6px rgba(66, 133, 244, 0.3);
    }}
    .docs-title-block {{
      display: flex;
      flex-direction: column;
    }}
    .docs-title {{
      font-size: 16px;
      font-weight: 700;
      color: #202124;
      display: flex;
      align-items: center;
      gap: 8px;
    }}
    .badge-vnu {{
      background: #e8f0fe;
      color: #1a73e8;
      font-size: 11px;
      font-weight: 800;
      padding: 2px 6px;
      border-radius: 4px;
    }}
    .docs-menu-row {{
      font-size: 12px;
      color: var(--docs-muted);
      display: flex;
      gap: 14px;
      margin-top: 2px;
    }}
    .docs-menu-item {{
      cursor: pointer;
      padding: 1px 4px;
      border-radius: 4px;
    }}
    .docs-menu-item:hover {{
      background: var(--docs-hover);
      color: var(--docs-text);
    }}
    .docs-actions {{
      display: flex;
      align-items: center;
      gap: 10px;
    }}
    .btn-action {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 8px 14px;
      border-radius: 20px;
      font-size: 13px;
      font-weight: 600;
      text-decoration: none;
      cursor: pointer;
      transition: all 0.2s;
      border: 1px solid transparent;
    }}
    .btn-cloud {{
      background: #1a73e8;
      color: #ffffff;
      box-shadow: 0 2px 6px rgba(26, 115, 232, 0.25);
    }}
    .btn-cloud:hover {{ background: #1557b0; }}
    .btn-download {{
      background: #ffffff;
      color: #3c4043;
      border-color: var(--docs-border);
    }}
    .btn-download:hover {{ background: var(--docs-hover); }}

    /* Main Workspace Layout */
    .workspace-container {{
      display: flex;
      flex: 1;
      height: calc(100vh - 64px);
      overflow: hidden;
    }}
    /* Left Tabs Sidebar (Document Tabs) */
    aside.tabs-sidebar {{
      width: 280px;
      background: #ffffff;
      border-right: 1px solid var(--docs-border);
      display: flex;
      flex-direction: column;
      flex-shrink: 0;
      overflow-y: auto;
    }}
    .sidebar-header {{
      padding: 16px 14px 10px;
      font-size: 12px;
      font-weight: 800;
      color: var(--docs-muted);
      text-transform: uppercase;
      letter-spacing: 0.5px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      border-bottom: 1px solid #f1f3f4;
    }}
    .tab-list {{
      list-style: none;
      padding: 8px 0;
    }}
    .tab-item {{
      display: flex;
      align-items: center;
      gap: 10px;
      padding: 10px 16px;
      font-size: 13px;
      font-weight: 600;
      color: #3c4043;
      cursor: pointer;
      border-left: 3px solid transparent;
      transition: all 0.15s ease;
      line-height: 1.4;
    }}
    .tab-item:hover {{
      background: var(--docs-hover);
      color: #202124;
    }}
    .tab-item.active {{
      background: var(--docs-active);
      color: var(--docs-blue);
      border-left-color: var(--docs-blue);
      font-weight: 700;
    }}
    .tab-item.bonus-tab {{
      color: #b45309;
    }}
    .tab-item.bonus-tab.active {{
      background: #fffbeb;
      color: #b45309;
      border-left-color: #d97706;
    }}

    /* Document Stage Area (Right) */
    main.document-stage {{
      flex: 1;
      background: #eef2f6;
      overflow-y: auto;
      padding: 24px 20px 60px;
      display: flex;
      justify-content: center;
      -webkit-overflow-scrolling: touch;
    }}
    /* Standard Google Doc A4 Canvas */
    .doc-page {{
      background: #ffffff;
      width: 820px;
      max-width: 100%;
      min-height: 1050px;
      box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
      border-radius: 4px;
      padding: 50px 60px;
      line-height: 1.7;
      color: #202124;
    }}
    .tab-panel {{
      display: none;
      animation: fadeIn 0.25s ease;
    }}
    .tab-panel.active {{
      display: block;
    }}
    @keyframes fadeIn {{
      from {{ opacity: 0; transform: translateY(4px); }}
      to {{ opacity: 1; transform: translateY(0); }}
    }}

    /* Typography & Components in Doc */
    h1.page-title {{
      font-size: 24px;
      font-weight: 800;
      color: #1e3a8a;
      border-bottom: 2px solid #e2e8f0;
      padding-bottom: 12px;
      margin-bottom: 20px;
      line-height: 1.35;
    }}
    h2.section-heading {{
      font-size: 18px;
      font-weight: 800;
      color: #0f172a;
      margin: 24px 0 12px;
      display: flex;
      align-items: center;
      gap: 8px;
    }}
    p {{ margin-bottom: 14px; font-size: 14px; color: #334155; }}
    ul, ol {{ margin: 0 0 16px 24px; font-size: 14px; color: #334155; }}
    li {{ margin-bottom: 6px; }}

    /* Callout Boxes */
    .callout-box {{
      border-radius: 8px;
      padding: 16px 18px;
      margin: 16px 0 20px;
      font-size: 13.5px;
      line-height: 1.6;
    }}
    .callout-blue {{
      background: #eff6ff;
      border-left: 4px solid #1d4ed8;
      color: #1e3a8a;
    }}
    .callout-amber {{
      background: #fffbeb;
      border-left: 4px solid #d97706;
      color: #78350f;
    }}
    .callout-emerald {{
      background: #f0fdf4;
      border-left: 4px solid #059669;
      color: #065f46;
    }}

    /* Prompt Box with One-Click Copy */
    .prompt-card {{
      background: #0f172a;
      color: #f8fafc;
      border-radius: 8px;
      padding: 18px 20px;
      margin: 16px 0 20px;
      position: relative;
      border-left: 4px solid #38bdf8;
      font-family: Consolas, Monaco, monospace;
      font-size: 13px;
      line-height: 1.6;
    }}
    .prompt-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 10px;
      padding-bottom: 8px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.15);
      font-family: inherit;
    }}
    .prompt-role {{
      color: #38bdf8;
      font-weight: 800;
      font-size: 12px;
    }}
    .btn-copy-prompt {{
      background: rgba(255, 255, 255, 0.15);
      border: 1px solid rgba(255, 255, 255, 0.3);
      color: #ffffff;
      padding: 4px 10px;
      font-size: 12px;
      font-weight: 700;
      border-radius: 4px;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 4px;
      transition: all 0.2s;
    }}
    .btn-copy-prompt:hover {{
      background: #0284c7;
      border-color: #0284c7;
    }}
    .prompt-text {{
      white-space: pre-wrap;
      word-break: break-all;
    }}

    /* Figure Box */
    .figure-box {{
      margin: 18px 0 24px;
      text-align: center;
    }}
    .figure-img {{
      max-width: 100%;
      height: auto;
      border-radius: 6px;
      border: 1px solid #cbd5e1;
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    }}
    .figure-caption {{
      font-size: 12.5px;
      font-weight: 700;
      color: #1e3a8a;
      margin-top: 6px;
    }}

    /* Data Table */
    .data-table {{
      width: 100%;
      border-collapse: collapse;
      margin: 16px 0 20px;
      font-size: 13px;
    }}
    .data-table th {{
      background: #1e3a8a;
      color: #ffffff;
      padding: 8px 12px;
      font-weight: 700;
      border: 1px solid #cbd5e1;
      text-align: center;
    }}
    .data-table td {{
      padding: 8px 12px;
      border: 1px solid #cbd5e1;
      text-align: right;
    }}
    .data-table tr:nth-child(even) {{
      background: #f8fafc;
    }}
    .data-table td:first-child {{
      text-align: center;
      font-weight: 700;
    }}

    /* Mobile Responsive */
    @media (max-width: 900px) {{
      aside.tabs-sidebar {{
        width: 70px;
      }}
      .sidebar-title-text, .tab-title-text {{
        display: none;
      }}
      .tab-item {{
        justify-content: center;
        padding: 12px 0;
      }}
      .doc-page {{
        padding: 24px 18px;
      }}
    }}
  </style>
</head>
<body>

  <!-- Top Header Bar -->
  <header class="docs-header">
    <div class="docs-brand">
      <div class="docs-logo"><i class="fas fa-file-alt"></i></div>
      <div class="docs-title-block">
        <div class="docs-title">
          <span>萬能科技大學《商業軟體應用》期中專案操作手冊</span>
          <span class="badge-vnu">11501 企業管理系</span>
        </div>
        <div class="docs-menu-row">
          <span class="docs-menu-item" onclick="switchDocTab('tab-overview')">檔案</span>
          <span class="docs-menu-item" onclick="switchDocTab('tab-prompts')">編輯</span>
          <span class="docs-menu-item" onclick="switchDocTab('tab-bonus')">檢視</span>
          <span class="docs-menu-item" onclick="switchDocTab('tab-checklist')">工具</span>
          <span class="docs-menu-item" onclick="window.print()">列印 (Ctrl+P)</span>
        </div>
      </div>
    </div>
    <div class="docs-actions">
      <a href="https://docs.google.com/document/d/1J2bpLVkO6gyPXMCzVMXWa2nA-Bx9kOVU9FHH9PadNc4/edit?usp=sharing" target="_blank" class="btn-action btn-cloud" title="直接在瀏覽器開啟 Google Docs 雲端原檔">
        <i class="fab fa-google-drive"></i> 開啟 Google Doc 雲端版
      </a>
      <a href="downloads/商業軟體應用_期中報告操作手冊_個人履歷網站與產業數據分析.docx" download class="btn-action btn-download" title="下載完整 Word / Docs 手冊">
        <i class="fas fa-file-word" style="color:#2563eb;"></i> 下載手冊 (.docx)
      </a>
    </div>
  </header>

  <!-- Workspace Container -->
  <div class="workspace-container">

    <!-- Left Tabs Sidebar (Native Google Docs Document Tabs Style) -->
    <aside class="tabs-sidebar">
      <div class="sidebar-header">
        <span class="sidebar-title-text">文件分頁 (Document Tabs)</span>
        <i class="fas fa-layer-group"></i>
      </div>
      <ul class="tab-list">
        <li class="tab-item active" onclick="switchDocTab('tab-overview')">
          <i class="fas fa-bookmark"></i>
          <span class="tab-title-text">📌 守則與期中目標說明</span>
        </li>
        <li class="tab-item" onclick="switchDocTab('tab-setup')">
          <i class="fas fa-desktop"></i>
          <span class="tab-title-text">⚙️ 第一部分：Antigravity 安裝</span>
        </li>
        <li class="tab-item" onclick="switchDocTab('tab-sop')">
          <i class="fas fa-project-diagram"></i>
          <span class="tab-title-text">📊 第二部分：行銷企劃 SOP 流程</span>
        </li>
        <li class="tab-item" onclick="switchDocTab('tab-prompts')">
          <i class="fas fa-terminal"></i>
          <span class="tab-title-text">💬 第三部分：七大核心 Prompt</span>
        </li>
        <li class="tab-item" onclick="switchDocTab('tab-deploy')">
          <i class="fas fa-key"></i>
          <span class="tab-title-text">🔑 第四部分：GitHub Token 發布</span>
        </li>
        <li class="tab-item bonus-tab" onclick="switchDocTab('tab-bonus')">
          <i class="fas fa-chart-line"></i>
          <span class="tab-title-text">🌟 第五部分：產業數據專案加分</span>
        </li>
        <li class="tab-item" onclick="switchDocTab('tab-checklist')">
          <i class="fas fa-tasks"></i>
          <span class="tab-title-text">✅ 第六部分：期中成果檢核表</span>
        </li>
      </ul>
    </aside>

    <!-- Document Stage (Right) -->
    <main class="document-stage">
      <div class="doc-page">

        <!-- ========================================== -->
        <!-- TAB 1: 實務守則與期中目標說明 -->
        <!-- ========================================== -->
        <section id="tab-overview" class="tab-panel active">
          <h1 class="page-title">萬能科技大學《商業軟體應用》期中專案實戰操作手冊<br><span style="font-size:16px; font-weight:600; color:#64748b;">【個人商務履歷網站 ✕ 產業數據視覺化專案加分 ✕ GitHub Pages 雲端發布】</span></h1>
          
          <p style="font-size:13px; color:#64748b;">
            <strong>課程名稱</strong>：商業軟體應用 (11501) ｜ <strong>授課教師</strong>：邱俊維 博士 ｜ <strong>地點</strong>：(J501) 企業經營模擬室<br>
            <strong>實踐模式</strong>：100% 個人獨立微型商務作品集（零伺服器主機成本 ✕ 零課後負擔 ✕ GitHub Pages 永久成果網址）
          </p>

          <div class="callout-box callout-blue">
            <h3 style="margin-bottom:6px; font-size:15px; font-weight:800; color:#1d4ed8;"><i class="fas fa-bullhorn" style="margin-right:6px;"></i>【重要實務守則與期中目標說明】</h3>
            <p style="margin-bottom:8px; font-size:13.5px; color:#1e3a8a;">
              本課程重視進修部每位同學的個人職場競爭力與實用數位辦公能力。期中進度採取「100% 個人商務履歷網站落地實踐」模式。
            </p>
            <p style="margin-bottom:8px; font-size:13.5px; color:#1e3a8a;">
              授課教師本身具備成熟的獨立品牌電商架站技術；但考量全班同學「零伺服器主機成本、零課後額外負擔、統一公開互評與永久職涯展示」，
              期中報告的核心要求為：<strong>請同學們使用 Google Antigravity 做出屬於自己的「個人專業履歷與作品集網站」，並部署到 GitHub Pages，取得所有人皆能手機/電腦隨時瀏覽的公開網址交出期中成果！</strong>
            </p>
          </div>

          <div class="callout-box callout-amber">
            <h3 style="margin-bottom:6px; font-size:15px; font-weight:800; color:#b45309;"><i class="fas fa-star" style="margin-right:6px;"></i>🌟【重大專案加分亮點】</h3>
            <p style="margin-bottom:0; font-size:13.5px; color:#78350f;">
              若同學在個人履歷網站中，額外嵌入<strong>「有興趣的產業商業數據分析視覺化專案」</strong>（例如：全台寵物經濟毛小孩商機、台灣零售通路與電商消長趨勢、各產業薪資結構或餐飲連鎖門市分析等互動圖表與商管洞察），將由授課教師給予專案大幅加分肯定，打造超越同儕、人資眼見為憑的商管數位競爭力！
            </p>
          </div>
        </section>

        <!-- ========================================== -->
        <!-- TAB 2: 第一部分：Google Antigravity 安裝與 GitHub 配置 -->
        <!-- ========================================== -->
        <section id="tab-setup" class="tab-panel">
          <h1 class="page-title">第一部分：Google Antigravity App (v2.28.2) 安裝與環境配置指引</h1>
          
          <p>為了讓每位同學的企劃構想與個人履歷能夠快速落地並轉化為具體的數位互動原型，本課程全面導入現代化 Google Antigravity 應用程式。請依照以下步驟下載安裝與驗證：</p>

          <h2 class="section-heading">1.1 下載與安裝 Google Antigravity 桌面版應用程式</h2>
          <ul>
            <li><strong>官方下載入口</strong>：<a href="https://antigravity.google/download" target="_blank" style="color:#1a73e8;">https://antigravity.google/download</a></li>
            <li><strong>官方更新日誌專頁 (v2.28.2)</strong>：<a href="https://antigravity.google/docs/changelog?tab=hub" target="_blank" style="color:#1a73e8;">https://antigravity.google/docs/changelog?tab=hub</a></li>
            <li><strong>Google Antigravity 官方首頁</strong>：<a href="https://antigravity.google" target="_blank" style="color:#1a73e8;">https://antigravity.google</a></li>
          </ul>

          <div class="figure-box">
            <img src="{b64['fig1_1']}" class="figure-img" alt="Google Antigravity App 下載介面">
            <div class="figure-caption">▲ 圖 1-1 Google Antigravity 官方 App 下載頁面真實截圖</div>
          </div>

          <h2 class="section-heading">1.2 登入 GitHub 帳號並建立個人專案儲存庫（開 Repo）</h2>
          <p>GitHub 是全球專業軟體與企劃專案的託管平臺，亦是展示個人商務履歷與數位成果的最佳舞臺。</p>
          <ul>
            <li><strong>GitHub 官方登入入口</strong>：<a href="https://github.com/login" target="_blank" style="color:#1a73e8;">https://github.com/login</a>（支援直接以 Google 帳號快速登入）</li>
          </ul>

          <div class="figure-box">
            <img src="{b64['fig1_2']}" class="figure-img" alt="GitHub 登入介面">
            <div class="figure-caption">▲ 圖 1-2 GitHub 官方登入介面真實截圖</div>
          </div>

          <p><strong>建立新儲存庫五步驟指引：</strong></p>
          <ol>
            <li>登入後點擊右上角「<strong>+</strong>」，選擇「<strong>New repository</strong>」（新增儲存庫，即建立專案 Repo）。</li>
            <li><strong>專案命名規範</strong>：建議以履歷或專案英文命名（如 <code>resume-portfolio</code> 或 <code>business-profile</code>）。</li>
            <li><strong>權限設定</strong>：請務必勾選「<strong>Public</strong>」（公開），並勾選「<strong>Add a README file</strong>」。</li>
            <li>點擊綠色按鈕「<strong>Create repository</strong>」完成專案儲存庫建立。</li>
          </ol>

          <div class="figure-box">
            <img src="{b64['fig1_3']}" class="figure-img" alt="GitHub 建立新儲存庫介面">
            <div class="figure-caption">▲ 圖 1-3 GitHub 建立新儲存庫 (Create a new repository) 介面截圖</div>
          </div>
        </section>

        <!-- ========================================== -->
        <!-- TAB 3: 第二部分：行銷企劃 SOP 流程與邊界解讀 -->
        <!-- ========================================== -->
        <section id="tab-sop" class="tab-panel">
          <h1 class="page-title">第二部分：行銷企劃與商務分析 SOP 五大階段（期中評量邊界解讀）</h1>
          
          <p>本課程嚴謹依循行銷學理經典教材（凌政文 教授著《行銷企劃》圖 1-9）之五階段標準流程。授課教師特別將原圖重新繪製為現代數位流程圖，並精準標記【期中報告】與【期末報告】之學習進度邊界：</p>

          <div class="figure-box">
            <img src="{b64['fig2_1']}" class="figure-img" alt="行銷企劃五階段流程圖">
            <div class="figure-caption">▲ 圖 2-1 行銷企劃五階段標準流程圖與期中評量邊界對照</div>
          </div>

          <h2 class="section-heading">【行銷企劃五大階段與課程評量範疇對照】</h2>
          <ul>
            <li><strong>階段 1：啟動與分析（📌 期中評量範疇）</strong><br>
            核心步驟：接收任務／發現痛點 ➔ 外部總體趨勢 (PESTC) ➔ 內部資源條件盤點 ➔ 綜合 SWOT 因果矩陣。</li>
            <li><strong>階段 2：目標與定位（📌 期中評量範疇）</strong><br>
            核心步驟：界定商業目標 (SMART) ➔ 市場區隔 (S) ➔ 目標客群 (T) ➔ 價值定位 (P)。</li>
            <li><strong>階段 3：方案發想與設計（📌 期中終點里程碑）</strong><br>
            核心步驟：設計行銷組合方案 (4P：產品、價格、通路、推廣) ➔ 🏆 <strong>實質產出：個人商務履歷 ＋ 線上 MVP 原型網頁驗證（GitHub Pages）。</strong></li>
            <li><strong>階段 4：執行與控制（🏆 期末實踐範疇）</strong><br>
            核心步驟：盤點所需資源與供應鏈 ➔ 編製甘特圖時程表 ➔ 建立量化績效考核標準。</li>
            <li><strong>階段 5：企劃書撰寫（🏆 期末實踐範疇）</strong><br>
            核心步驟：文字潤飾與排版 ➔ 正式專案企劃書 ➔ 成果公開發布展示。</li>
          </ul>

          <div class="callout-box callout-emerald">
            <h3 style="margin-bottom:6px; font-size:15px; font-weight:800; color:#065f46;"><i class="fas fa-check-circle" style="margin-right:6px;"></i>【授課教師指引：期中評量邊界說明】</h3>
            <p style="margin-bottom:0; font-size:13.5px; color:#065f46;">
              期中報告的核心目的在於驗證「個人專業經歷、市場商業思維與數位實作能力的邏輯合理性」。因此，期中進度要求至【**階段 3 之產出：個人商務履歷 ＋ 初步企劃草案/數據分析展示**】即可！同學們無須過早煩惱龐大的預算編列或複雜的甘特圖時程，請專注將個人優勢與企管分析學理做紮實，並發布出清晰的線上 GitHub Pages 網站！
            </p>
          </div>
        </section>

        <!-- ========================================== -->
        <!-- TAB 4: 第三部分：七大核心商務 Prompt 指引與示範案例 -->
        <!-- ========================================== -->
        <section id="tab-prompts" class="tab-panel">
          <h1 class="page-title">第三部分：七大核心商務 Prompt 指引與示範案例（學生可直接複製）</h1>
          
          <p>以下示範案例採《樂肉選品 (LeRou Pet Goods)》寵物經濟專案，同學可依照個人選定之主題（服飾美妝、精品代購、二手車商務、文創餐飲、個人求職履歷等）彈性替換名稱！</p>

          <!-- Prompt 1 -->
          <h2 class="section-heading">步驟 1：【發掘痛點與創業動機 Prompt】</h2>
          <div class="prompt-card">
            <div class="prompt-header">
              <span class="prompt-role">🎭 設定角色：微型創業者 兼 商業分析師</span>
              <button class="btn-copy-prompt" onclick="copyText('prompt1')"><i class="fas fa-copy"></i> 複製 Prompt</button>
            </div>
            <div class="prompt-text" id="prompt1">身為微型創業者與商務企劃人員，我想以《樂肉選品》為題，主打常溫原肉烘乾零食與毛孩脆片。
請幫我從『市售零食添加物』、『鮮食冷鏈運費門檻』與『美學生活體驗』三方面，提煉出 3 個具體痛點與切入緣起。</div>
          </div>
          <div class="figure-box">
            <img src="{b64['fig3_1']}" class="figure-img" alt="痛點提煉對話截圖">
            <div class="figure-caption">▲ 圖 3-1 步驟 1 Google Antigravity Agent 痛點提煉對話實機截圖</div>
          </div>

          <!-- Prompt 2 -->
          <h2 class="section-heading">步驟 2：【外部總體環境 PESTC 深度分析 Prompt】</h2>
          <div class="prompt-card">
            <div class="prompt-header">
              <span class="prompt-role">🎭 設定角色：商務決策特助</span>
              <button class="btn-copy-prompt" onclick="copyText('prompt2')"><i class="fas fa-copy"></i> 複製 Prompt</button>
            </div>
            <div class="prompt-text" id="prompt2">請針對《樂肉選品》的常溫原肉烘乾零食（厚切雞肉乾、毛孩地瓜肉片），運用政治法律(P)、經濟(E)、社會文化(S)、科技(T)、綠色環保(C)五大構面進行 PESTC 總體環境分析，並說明對本企劃之啟發。</div>
          </div>
          <div class="figure-box">
            <img src="{b64['fig3_2']}" class="figure-img" alt="PESTC 分析對話截圖">
            <div class="figure-caption">▲ 圖 3-2 步驟 2 PESTC 總體環境分析對話實機截圖</div>
          </div>

          <!-- Prompt 3 -->
          <h2 class="section-heading">步驟 3：【內部資源盤點與假想敵防護 Prompt】</h2>
          <div class="prompt-card">
            <div class="prompt-header">
              <span class="prompt-role">🎭 設定角色：策略營運顧問</span>
              <button class="btn-copy-prompt" onclick="copyText('prompt3')"><i class="fas fa-copy"></i> 複製 Prompt</button>
            </div>
            <div class="prompt-text" id="prompt3">我身為微型創業者，啟動資金僅 3~5 萬、一人作業、無實體店面。請盤點我的內部優劣勢，並選定大型量販賣場的進口拼裝副產物肉乾為主要假想敵，規劃我的定位防護策略。</div>
          </div>
          <div class="figure-box">
            <img src="{b64['fig3_3']}" class="figure-img" alt="內部資源盤點截圖">
            <div class="figure-caption">▲ 圖 3-3 步驟 3 內部資源盤點與假想敵定位截圖</div>
          </div>

          <!-- Prompt 4 -->
          <h2 class="section-heading">步驟 4：【SWOT 因果推論四象限四部曲綜合矩陣 Prompt】</h2>
          <div class="prompt-card">
            <div class="prompt-header">
              <span class="prompt-role">🎭 設定角色：高級策略規劃師</span>
              <button class="btn-copy-prompt" onclick="copyText('prompt4')"><i class="fas fa-copy"></i> 複製 Prompt</button>
            </div>
            <div class="prompt-text" id="prompt4">請將上述《樂肉選品》的內外部條件交叉，嚴格按照 SO（積極開拓）、WO（借力補強）、ST（防禦轉化）、WT（避險聚焦）的四象限四部曲因果推論邏輯，產出策略矩陣。</div>
          </div>
          <div class="figure-box">
            <img src="{b64['fig3_4']}" class="figure-img" alt="SWOT 矩陣截圖">
            <div class="figure-caption">▲ 圖 3-4 步驟 4 SWOT 因果推論四象限矩陣實機截圖</div>
          </div>

          <!-- Prompt 5 -->
          <h2 class="section-heading">步驟 5：【SMART 企劃目標與三超前瞻思維 Prompt】</h2>
          <div class="prompt-card">
            <div class="prompt-header">
              <span class="prompt-role">🎭 設定角色：專案經理 (PMP)</span>
              <button class="btn-copy-prompt" onclick="copyText('prompt5')"><i class="fas fa-copy"></i> 複製 Prompt</button>
            </div>
            <div class="prompt-text" id="prompt5">請為《樂肉選品》期中 MVP 設定 30 天內可量化驗證的 SMART 目標，並融入『超前意識、超越常規、超越期望』的三超思維。</div>
          </div>
          <div class="figure-box">
            <img src="{b64['fig3_5']}" class="figure-img" alt="SMART 目標截圖">
            <div class="figure-caption">▲ 圖 3-5 步驟 5 SMART 目標設定實機截圖</div>
          </div>

          <!-- Prompt 6 -->
          <h2 class="section-heading">步驟 6：【STP 市場定位與 4P 行銷組合 Prompt】</h2>
          <div class="prompt-card">
            <div class="prompt-header">
              <span class="prompt-role">🎭 設定角色：行銷總監 (CMO)</span>
              <button class="btn-copy-prompt" onclick="copyText('prompt6')"><i class="fas fa-copy"></i> 複製 Prompt</button>
            </div>
            <div class="prompt-text" id="prompt6">請為我擬定 STP（市場區隔、目標客群、品牌定位），並規劃 4P 方案（包含厚切肉乾、脆脆洋芋片、透氣背心三款商品規格、常溫超取運費 60 元策略、以及 #毛孩卡滋挑戰 社群推廣）。</div>
          </div>
          <div class="figure-box">
            <img src="{b64['fig3_6']}" class="figure-img" alt="STP 與 4P 組合截圖">
            <div class="figure-caption">▲ 圖 3-6 步驟 6 STP 與 4P 行銷組合實機截圖</div>
          </div>

          <!-- Prompt 7 -->
          <h2 class="section-heading">步驟 7：【一鍵生成線上 MVP 網頁程式碼 Prompt】</h2>
          <div class="prompt-card">
            <div class="prompt-header">
              <span class="prompt-role">🎭 設定角色：全端工程師 兼 視覺設計師</span>
              <button class="btn-copy-prompt" onclick="copyText('prompt7')"><i class="fas fa-copy"></i> 複製 Prompt</button>
            </div>
            <div class="prompt-text" id="prompt7">請幫我閱讀 https://docs.google.com/document/d/1J2bpLVkO6gyPXMCzVMXWa2nA-Bx9kOVU9FHH9PadNc4/edit 此檔案，
並根據此檔案，幫我生成《樂肉選品》XXX主題 (請各位同學自行更改主題，不能以寵物食品，這是範例，可以用賣衣服、代購精品包、賣二手車等等主題不限) 初步企劃草案，
生成為一個單一檔案且可直接運行的現代日系極簡風格 (可更改風格) HTML/CSS 網頁（index.html），
包含個人/品牌故事、學理分析摘要、三款商品卡片與線上預購意向登記按鈕。

🌟【期中加分專區必加】：請在網頁中嵌入一個『產業商業數據視覺化儀表板 (Chart.js)』，展示近 5 年產業規模消長折線圖與營收結構甜甜圈圖，並附上 3 點商務洞察分析。
並幫我部屬到 GitHub，我不想自己上傳檔案所以給你這串 API key 你幫我上傳 (請貼上 GitHub Personal Access Token 亂碼)。</div>
          </div>
        </section>

        <!-- ========================================== -->
        <!-- TAB 5: 第四部分：GitHub API Token 生成與自動發布指引 -->
        <!-- ========================================== -->
        <section id="tab-deploy" class="tab-panel">
          <h1 class="page-title">第四部分：GitHub Personal Access Token (API Key) 生成與自動發布指引</h1>
          
          <p>為了讓同學們享受現代 Vibe Coding『動口不動手』的流暢體驗，可以直接將 GitHub API Token 提供給 Antigravity，讓 AI 助理自動將生成的 index.html 推送至個人 GitHub 儲存庫，徹底免除手動上傳檔案的瑣碎步驟！</p>

          <h2 class="section-heading">4.1 生成 GitHub Personal Access Token (classic) 四步驟：</h2>
          <p><strong>步驟 1</strong>：點擊個人 GitHub 右上角頭像 ➔ 選擇「<strong>Settings</strong>」➔ 頁面捲動至最左下角點選「<strong>Developer settings</strong>」。</p>
          <div class="figure-box">
            <img src="{b64['fig4_1']}" class="figure-img" alt="Developer settings 截圖">
            <div class="figure-caption">▲ 圖 4-1 進入 GitHub Settings 點選最下方 Developer settings</div>
          </div>

          <p><strong>步驟 2</strong>：點擊「Personal access tokens」➔ 選擇「Tokens (classic)」➔ 點選「Generate new token (classic)」。<br>
          <strong>步驟 3</strong>：設定 Note 名稱為「<code>antigravity-deploy</code>」，Expiration 選擇「30 days」或「No expiration」，並在 Scopes 中務必勾選「<strong>repo</strong>」（包含完整儲存庫讀寫權限）與「<strong>workflow</strong>」。</p>
          <div class="figure-box">
            <img src="{b64['fig4_2']}" class="figure-img" alt="設定 Token 權限截圖">
            <div class="figure-caption">▲ 圖 4-2 設定 Token 名稱、有效期限並勾選 repo 存取權限</div>
          </div>

          <p><strong>步驟 4</strong>：滑動至頁面最底端，點選綠色按鈕「<strong>Generate token</strong>」生成密鑰金鑰。</p>
          <div class="figure-box">
            <img src="{b64['fig4_3']}" class="figure-img" alt="點擊 Generate token 按鈕截圖">
            <div class="figure-caption">▲ 圖 4-3 捲動至最下方點擊綠色 Generate token 按鈕</div>
          </div>

          <div class="callout-box callout-amber" style="background:#fef2f2; border-left-color:#ef4444; color:#991b1b;">
            <strong>⚠️ 【極重要安全提示】：</strong>複製這串 Token 亂碼 (以 <code>ghp_</code> 開頭)，此金鑰僅會出現一次！請妥善保存，切勿隨意散佈給無關他人！
          </div>
          <div class="figure-box">
            <img src="{b64['fig4_4']}" class="figure-img" alt="複製 Token 金鑰截圖">
            <div class="figure-caption">▲ 圖 4-4 複製產生的專屬 GitHub Token 金鑰亂碼</div>
          </div>

          <h2 class="section-heading">4.2 啟用 GitHub Pages 免費雲端靜態網頁發布：</h2>
          <ol>
            <li>進入專案儲存庫頁面，點選上方功能導覽列的「<strong>Settings</strong>」（設定）。</li>
            <li>在左側選單中找到「Code and automation」區塊，點選「<strong>Pages</strong>」。</li>
            <li>在「Build and deployment」底下的「Branch」設定：將分支改選為 <strong>main</strong>，資料夾維持 <strong>/(root)</strong>，點擊右側「<strong>Save</strong>」。</li>
            <li>等待約 1~2 分鐘重新整理頁面，頂部將出現綠色提示：「<code>Your site is live at https://[您的帳號].github.io/[專案名稱]/</code>」。</li>
            <li>此網址即為期中報告必須提交之「線上公開部署網址」！</li>
          </ol>
        </section>

        <!-- ========================================== -->
        <!-- TAB 6: 第五部分：【期中專案加分亮點】產業數據專區 -->
        <!-- ========================================== -->
        <section id="tab-bonus" class="tab-panel">
          <h1 class="page-title" style="color:#b45309;"><i class="fas fa-crown" style="color:#f59e0b; margin-right:8px;"></i>第五部分：【期中專案加分亮點】產業商業數據分析視覺化專區</h1>
          
          <p>為了鼓勵同學將課堂所學之商業軟體與數據處理思維運用於職場求職，凡於個人履歷網站中加入「產業商業數據視覺化專區（Business Data Visualization Showcase）」者，將享有期中報告顯著加分！</p>

          <h2 class="section-heading">📊 示範資料集：台灣寵物經濟產業規模與毛孩登記趨勢（財政部與農業部官方統計）</h2>
          
          <table class="data-table">
            <thead>
              <tr>
                <th>年度</th>
                <th>產業營業額 (億元)</th>
                <th>營業家數 (家)</th>
                <th>商品買賣佔比</th>
                <th>照顧服務佔比</th>
                <th>犬貓登記總數 (萬隻)</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>2019</td>
                <td>280.2</td>
                <td>6,850</td>
                <td>83.5%</td>
                <td>6.8%</td>
                <td>230</td>
              </tr>
              <tr>
                <td>2020</td>
                <td>315.4</td>
                <td>7,230</td>
                <td>83.8%</td>
                <td>7.2%</td>
                <td>255</td>
              </tr>
              <tr>
                <td>2021</td>
                <td>345.8</td>
                <td>7,810</td>
                <td>84.1%</td>
                <td>7.9%</td>
                <td>275</td>
              </tr>
              <tr>
                <td>2022</td>
                <td>387.3</td>
                <td>8,335</td>
                <td>83.5%</td>
                <td>8.5%</td>
                <td>295</td>
              </tr>
              <tr>
                <td>2023</td>
                <td>430.5</td>
                <td>8,847</td>
                <td>82.8%</td>
                <td>9.3%</td>
                <td>315</td>
              </tr>
            </tbody>
          </table>

          <h2 class="section-heading">💬 加分專案 Prompt 指令：</h2>
          <div class="prompt-card" style="border-left-color:#f59e0b;">
            <div class="prompt-header">
              <span class="prompt-role" style="color:#fde047;">🎭 設定角色：商業數據視覺化專家</span>
              <button class="btn-copy-prompt" onclick="copyText('promptBonus')" style="background:#d97706;"><i class="fas fa-copy"></i> 複製加分 Prompt</button>
            </div>
            <div class="prompt-text" id="promptBonus">請在我的個人履歷網頁（index.html）下方新增一個『產業商業數據分析視覺化專案 (Industry Data Insights)』區塊。
使用上述台灣寵物經濟 2019~2023 官方統計數據（營業額由 280.2 億成長至 430.5 億，毛孩登記突破 315 萬隻，商品佔比 83%、照顧服務佔比 9%），
引入 Chart.js 繪製兩組高質感互動圖表：
1. 雙軸折線圖：營業額成長趨勢 ✕ 毛孩登記數走勢。
2. 環形甜甜圈圖：寵物產業三大營收結構佔比。
圖表需具備手機 RWD 自適應與滑鼠懸停數值提示 (Tooltip)，並附上 3 點企管商務洞察（高複合成長、貓派崛起帶動小宅經濟、高毛利精緻照護爆發）。</div>
          </div>
        </section>

        <!-- ========================================== -->
        <!-- TAB 7: 第六部分：期中專案檢核表 -->
        <!-- ========================================== -->
        <section id="tab-checklist" class="tab-panel">
          <h1 class="page-title">第六部分：期中專案檢核清單與互評成果指引</h1>
          
          <p>請同學們在期中報告截止前，逐項確認以下 7 項完成指標：</p>

          <div style="background:#ffffff; border:1px solid #cbd5e1; border-radius:8px; padding:20px; line-height:2.0; font-size:14px;">
            <div><input type="checkbox" id="c1" checked> <label for="c1"><strong>1.</strong> 已下載安裝 Google Antigravity App (v2.28.2) 並使用個人 Google 帳號登入。</label></div>
            <div><input type="checkbox" id="c2" checked> <label for="c2"><strong>2.</strong> 已於 GitHub 建立公開儲存庫 (Public Repo) 並完成 Personal Access Token 設定。</label></div>
            <div><input type="checkbox" id="c3" checked> <label for="c3"><strong>3.</strong> 已運用 Antigravity 完成痛點提煉、PESTC、內部資源、SWOT 因果推論矩陣、SMART 目標與 STP+4P 規劃。</label></div>
            <div><input type="checkbox" id="c4" checked> <label for="c4"><strong>4.</strong> 已成功生成包含個人商務履歷、企劃草案、商品/經歷卡片與預購意向登記的 index.html 網頁。</label></div>
            <div><input type="checkbox" id="c5" checked> <label for="c5" style="color:#b45309;"><strong>5. 【加分項確認】</strong>：網頁已嵌入有興趣的產業商業數據分析視覺化專案 (Chart.js 互動圖表與商務洞察)。</label></div>
            <div><input type="checkbox" id="c6" checked> <label for="c6"><strong>6.</strong> 已開啟 GitHub Pages，並確認手機與電腦皆能順暢瀏覽公開網址 (https://[帳號].github.io/[專案名]/)。</label></div>
            <div><input type="checkbox" id="c7" checked> <label for="c7"><strong>7.</strong> 已於課程教學平台完成期中成果公開網址提交，參與全班觀摩互評！</label></div>
          </div>

          <div style="margin-top:24px; text-align:center;">
            <a href="https://docs.google.com/document/d/1J2bpLVkO6gyPXMCzVMXWa2nA-Bx9kOVU9FHH9PadNc4/edit?usp=sharing" target="_blank" class="btn-action btn-cloud" style="padding:10px 24px; font-size:14px;">
              <i class="fab fa-google-drive"></i> 在 Google Docs 雲端原檔開啟
            </a>
          </div>
        </section>

      </div>
    </main>
  </div>

  <script>
    function switchDocTab(tabId) {{
      document.querySelectorAll('.tab-item').forEach(item => {{
        item.classList.toggle('active', item.getAttribute('onclick').includes(tabId));
      }});
      document.querySelectorAll('.tab-panel').forEach(panel => {{
        panel.classList.toggle('active', panel.id === tabId);
      }});
      document.querySelector('.document-stage').scrollTo({{ top: 0, behavior: 'smooth' }});
    }}

    function copyText(elemId) {{
      const text = document.getElementById(elemId).innerText;
      navigator.clipboard.writeText(text).then(() => {{
        alert("📋 Prompt 提示詞已複製到剪貼簿！可直接貼進 Google Antigravity 對話框。");
      }}).catch(err => {{
        alert("複製失敗，請手動複製。");
      }});
    }}
  </script>
</body>
</html>
"""

out_html = os.path.join(base_dir, "Google_Docs_期中報告操作手冊(以分頁劃分).html")
with open(out_html, "w", encoding="utf-8") as f:
    f.write(html_content)
print(f"Generated Google Docs HTML Web App: {out_html} ({os.path.getsize(out_html):,} bytes)")
