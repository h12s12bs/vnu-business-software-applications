# -*- coding: utf-8 -*-
"""
Generate professorial-grade Midterm Manual for Business Software Applications:
1. downloads/商業軟體應用_期中報告操作手冊_個人履歷網站與產業數據分析.docx
2. 商業軟體應用_期中報告操作手冊.docx
3. downloads/商業軟體應用_期中報告操作手冊.md
Following Dr. Chun-Wei Chiu's pedagogical style from the Google Doc:
- Antigravity v2.28.2 & GitHub Pages setup
- 7 core prompts (Problem, PESTC, Internal Resources, SWOT, SMART, STP+4P, One-click MVP generation)
- Fine-tuned for Business Software Applications (履歷 + 產業數據分析專案加分)
- GitHub Personal Access Token (classic) auto-deployment guidance
- High-res embedded screenshots
- Zero forbidden terms
"""
import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

base_dir = r"g:\我的雲端硬碟\萬能科技大學\備課\11501課表\11501商業軟體應用"
assets_ref_dir = os.path.join(base_dir, "assets", "midterm_ref_images")
downloads_dir = os.path.join(base_dir, "downloads")
os.makedirs(downloads_dir, exist_ok=True)

def set_cell_background(cell, fill_hex):
    tcPr = cell._element.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=140, bottom=140, left=180, right=180):
    tcPr = cell._element.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def create_prompt_box(doc, role_title, prompt_text, output_summary="", tip_text=""):
    """Creates a distinct styled table box representing the copyable prompt and AI output."""
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    
    cell = table.cell(0, 0)
    cell.width = Inches(6.4)
    set_cell_background(cell, "F8FAFC")
    set_cell_margins(cell, top=140, bottom=140, left=180, right=180)
    
    tcPr = cell._element.get_or_add_tcPr()
    borders = parse_xml(f'''
        <w:tcBorders {nsdecls("w")}>
            <w:top w:val="single" w:sz="6" w:space="0" w:color="CBD5E1"/>
            <w:left w:val="single" w:sz="24" w:space="0" w:color="0284C7"/>
            <w:bottom w:val="single" w:sz="6" w:space="0" w:color="CBD5E1"/>
            <w:right w:val="single" w:sz="6" w:space="0" w:color="CBD5E1"/>
        </w:tcBorders>
    ''')
    tcPr.append(borders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(4)
    run_badge = p.add_run(f"📋 【學生可直接複製之 Prompt 指令】 ｜ 🎭 設定角色：{role_title}\n")
    run_badge.bold = True
    run_badge.font.size = Pt(10.5)
    run_badge.font.color.rgb = RGBColor(2, 132, 199)
    
    run_text = p.add_run(prompt_text)
    run_text.font.size = Pt(9.5)
    run_text.font.name = "Consolas"
    run_text.font.color.rgb = RGBColor(15, 23, 42)
    
    if output_summary:
        p_out = cell.add_paragraph()
        p_out.paragraph_format.space_before = Pt(6)
        p_out.paragraph_format.space_after = Pt(2)
        r_out_title = p_out.add_run("🤖 【Google Antigravity Agent 真實輸出解析與對齊】：\n")
        r_out_title.bold = True
        r_out_title.font.size = Pt(9.5)
        r_out_title.font.color.rgb = RGBColor(5, 150, 105)
        
        r_out = p_out.add_run(output_summary)
        r_out.font.size = Pt(9)
        r_out.font.color.rgb = RGBColor(51, 65, 85)
        
    if tip_text:
        p2 = cell.add_paragraph()
        p2.paragraph_format.space_before = Pt(4)
        p2.paragraph_format.space_after = Pt(2)
        run_tip = p2.add_run(f"💡 企管系人機協作要領：{tip_text}")
        run_tip.font.size = Pt(9)
        run_tip.font.italic = True
        run_tip.font.color.rgb = RGBColor(180, 83, 9)

    doc.add_paragraph().paragraph_format.space_after = Pt(4)

def add_screenshot_figure(doc, img_name, fig_num_title, width=Inches(6.0)):
    """Embeds screenshot image with caption."""
    img_path = os.path.join(assets_ref_dir, img_name)
    if os.path.exists(img_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(6)
        p_img.paragraph_format.space_after = Pt(3)
        doc.add_picture(img_path, width=width)
        
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_before = Pt(2)
        p_cap.paragraph_format.space_after = Pt(6)
        r_num = p_cap.add_run(f"▲ {fig_num_title}")
        r_num.bold = True
        r_num.font.size = Pt(9.5)
        r_num.font.color.rgb = RGBColor(30, 58, 138)

def build_docx_manual():
    doc = Document()
    
    # Page setup
    for sec in doc.sections:
        sec.top_margin = Inches(1.0)
        sec.bottom_margin = Inches(1.0)
        sec.left_margin = Inches(1.0)
        sec.right_margin = Inches(1.0)
        
    # Styles
    styles = doc.styles
    normal_style = styles['Normal']
    normal_style.font.name = '微軟正黑體'
    normal_style.font.size = Pt(11)
    normal_style.font.color.rgb = RGBColor(15, 23, 42)
    
    # Document Title
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(0)
    p_title.paragraph_format.space_after = Pt(4)
    r_title = p_title.add_run("萬能科技大學《商業軟體應用》期中專案實戰操作手冊\n【個人商務履歷網站 ✕ 產業數據視覺化專案加分 ✕ GitHub Pages 雲端發布】")
    r_title.bold = True
    r_title.font.size = Pt(18)
    r_title.font.color.rgb = RGBColor(15, 23, 42)
    
    # Metadata bar
    p_meta = doc.add_paragraph()
    p_meta.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_meta.paragraph_format.space_before = Pt(2)
    p_meta.paragraph_format.space_after = Pt(16)
    r_meta = p_meta.add_run("課程名稱：商業軟體應用 (11501) ｜ 授課教師：邱俊維 博士 ｜ 地點：(J501) 企業經營模擬室 (電腦教室)\n實務模式：100% 個人獨立數位商務作品集（零伺服器成本 ✕ 零課後負擔 ✕ GitHub Pages 永久成果網址）")
    r_meta.font.size = Pt(9.5)
    r_meta.font.color.rgb = RGBColor(100, 116, 139)
    
    # Callout Box: Midterm Guideline & Grading Focus
    t_rule = doc.add_table(rows=1, cols=1)
    t_rule.alignment = WD_TABLE_ALIGNMENT.CENTER
    c_rule = t_rule.cell(0, 0)
    c_rule.width = Inches(6.4)
    set_cell_background(c_rule, "EFF6FF")
    set_cell_margins(c_rule, top=140, bottom=140, left=180, right=180)
    
    tcPr = c_rule._element.get_or_add_tcPr()
    borders = parse_xml(f'''
        <w:tcBorders {nsdecls("w")}>
            <w:top w:val="single" w:sz="6" w:space="0" w:color="93C5FD"/>
            <w:left w:val="single" w:sz="24" w:space="0" w:color="1D4ED8"/>
            <w:bottom w:val="single" w:sz="6" w:space="0" w:color="93C5FD"/>
            <w:right w:val="single" w:sz="6" w:space="0" w:color="93C5FD"/>
        </w:tcBorders>
    ''')
    tcPr.append(borders)
    
    p_r = c_rule.paragraphs[0]
    p_r.paragraph_format.space_before = Pt(2)
    p_r.paragraph_format.space_after = Pt(2)
    r_r1 = p_r.add_run("【重要實務守則與期中目標說明】\n")
    r_r1.bold = True
    r_r1.font.size = Pt(11)
    r_r1.font.color.rgb = RGBColor(29, 78, 216)
    
    rule_desc = (
        "本課程重視進修部每位同學的個人職場競爭力與實用數位辦公能力。期中進度採取「100% 個人商務履歷網站落地實踐」模式。\n"
        "授課教師本身具備成熟的獨立品牌電商架站技術；但考量全班同學「零伺服器主機成本、零課後額外負擔、統一公開互評與永久職涯展示」，"
        "期中報告的核心要求為：請同學們使用 Google Antigravity 做出屬於自己的「個人專業履歷與作品集網站」，並部署到 GitHub Pages，"
        "取得所有人皆能手機/電腦隨時瀏覽的公開網址作為期中成果！\n\n"
        "🌟【重大加分亮點】：若同學在個人履歷網站中，額外嵌入「有興趣的產業商業數據分析視覺化專案」"
        "（例如：全台寵物經濟毛小孩商機、台灣零售通路與電商消長趨勢、餐飲連鎖門市分析等互動圖表與商管洞察），"
        "將由授課教師給予專案大幅加分肯定，打造超越同儕、人資眼見為憑的商管數位競爭力！"
    )
    r_r2 = p_r.add_run(rule_desc)
    r_r2.font.size = Pt(9.5)
    r_r2.font.color.rgb = RGBColor(30, 58, 138)
    
    doc.add_paragraph().paragraph_format.space_after = Pt(8)
    
    # -------------------------------------------------------------
    # PART 1
    # -------------------------------------------------------------
    h1 = doc.add_paragraph()
    h1.paragraph_format.space_before = Pt(14)
    h1.paragraph_format.space_after = Pt(4)
    r_h1 = h1.add_run("第一部分：Google Antigravity App (v2.28.2) 安裝與環境配置指引")
    r_h1.bold = True
    r_h1.font.size = Pt(14)
    r_h1.font.color.rgb = RGBColor(15, 23, 42)
    
    p_p1 = doc.add_paragraph(
        "為了讓每位同學的企劃構想與個人履歷能夠快速落地並轉化為具體的數位互動原型，"
        "本課程全面導入現代化 Google Antigravity 應用程式。請依照以下步驟下載安裝與驗證："
    )
    p_p1.paragraph_format.space_after = Pt(6)
    
    p_step1 = doc.add_paragraph()
    p_step1.paragraph_format.space_before = Pt(2)
    p_step1.paragraph_format.space_after = Pt(2)
    p_step1.add_run("1.1 下載與安裝 Google Antigravity 桌面版應用程式\n").bold = True
    p_step1.add_run("• 官方下載入口：https://antigravity.google/download\n")
    p_step1.add_run("• 官方更新日誌專頁 (v2.28.2)：https://antigravity.google/docs/changelog?tab=hub\n")
    p_step1.add_run("• Google Antigravity 官方首頁：https://antigravity.google\n")
    p_step1.add_run(
        "• 操作步驟指引：\n"
        "  1. 點擊上方官方連結進入 Google Antigravity 官方下載專頁，確認版本為最新穩定版本 v2.28.2。\n"
        "  2. 依據個人電腦作業系統（Windows / macOS）下載對應安裝套件（.exe 或 .dmg）。\n"
        "  3. 執行安裝程式，依照畫面指示完成安裝與初始化設定。\n"
        "  4. 啟動 Google Antigravity App，使用個人的 Google 帳號登入完成驗證。"
    )
    
    add_screenshot_figure(doc, "image9.png", "圖 1-1 Google Antigravity 官方 App 下載頁面真實截圖")
    
    p_step2 = doc.add_paragraph()
    p_step2.paragraph_format.space_before = Pt(8)
    p_step2.paragraph_format.space_after = Pt(2)
    p_step2.add_run("1.2 登入 GitHub 帳號並建立個人專案儲存庫（開 Repo）\n").bold = True
    p_step2.add_run("GitHub 是全球專業軟體與企劃專案的託管平臺，亦是展示個人商務履歷與數位成果的最佳舞臺。\n")
    p_step2.add_run("• GitHub 官方登入入口：https://github.com/login （支援直接用 Google 帳號連動登入）\n")
    p_step2.add_run(
        "• 操作步驟指引：\n"
        "  1. 點選上方登入連結前往 GitHub 官方頁面。已有帳號者直接登入；新同學請輸入 Email 完成註冊。"
    )
    
    add_screenshot_figure(doc, "image14.png", "圖 1-2 GitHub 官方登入介面真實截圖")
    
    p_step2_cont = doc.add_paragraph(
        "  2. 登入後點擊右上角「+」，選擇「New repository」（新增儲存庫，即建立專案 Repo）。\n"
        "  3. 專案命名規範：建議以履歷或專案英文命名（如 resume-portfolio 或 business-profile）。\n"
        "  4. 權限設定：請務必勾選「Public」（公開），並勾選「Add a README file」。\n"
        "  5. 點擊綠色按鈕「Create repository」完成專案儲存庫建立。"
    )
    p_step2_cont.paragraph_format.space_after = Pt(4)
    
    add_screenshot_figure(doc, "image10.png", "圖 1-3 GitHub 建立新儲存庫 (Create a new repository) 介面截圖")
    
    # -------------------------------------------------------------
    # PART 2
    # -------------------------------------------------------------
    h2 = doc.add_paragraph()
    h2.paragraph_format.space_before = Pt(14)
    h2.paragraph_format.space_after = Pt(4)
    r_h2 = h2.add_run("第二部分：行銷企劃與商務分析 SOP 五大階段（期中評量邊界解讀）")
    r_h2.bold = True
    r_h2.font.size = Pt(14)
    r_h2.font.color.rgb = RGBColor(15, 23, 42)
    
    p_p2 = doc.add_paragraph(
        "本課程嚴謹依循行銷學理經典教材（凌政文 教授著《行銷企劃》圖 1-9）之五階段標準流程。"
        "授課教師特別將原圖重新繪製為現代數位流程圖，並精準標記【期中報告】與【期末報告】之學習進度邊界："
    )
    p_p2.paragraph_format.space_after = Pt(6)
    
    add_screenshot_figure(doc, "image11.png", "圖 2-1 行銷企劃五階段標準流程圖與期中評量邊界對照")
    
    p_phases = doc.add_paragraph()
    p_phases.paragraph_format.space_before = Pt(2)
    p_phases.paragraph_format.space_after = Pt(6)
    p_phases.add_run("【行銷企劃五大階段與課程評量範疇對照】\n").bold = True
    p_phases.add_run("• 階段 1：啟動與分析（📌 期中評量範疇）\n  - 核心步驟：接收任務／發現痛點 ➔ 外部總體趨勢 (PESTC) ➔ 內部資源條件盤點 ➔ 綜合 SWOT 矩陣。\n")
    p_phases.add_run("• 階段 2：目標與定位（📌 期中評量範疇）\n  - 核心步驟：界定商業目標 (SMART) ➔ 市場區隔 (S) ➔ 目標客群 (T) ➔ 價值定位 (P)。\n")
    p_phases.add_run("• 階段 3：方案發想與設計（📌 期中終點里程碑）\n  - 核心步驟：設計行銷組合 (4P) ➔ 🏆 實質產出：個人商務履歷 ＋ 線上 MVP 原型網頁驗證。\n")
    p_phases.add_run("• 階段 4：執行與控制（🏆 期末實踐範疇）\n  - 核心步驟：盤點所需資源與供應鏈 ➔ 編製甘特圖時程表 ➔ 建立量化績效考核標準。\n")
    p_phases.add_run("• 階段 5：企劃書撰寫（🏆 期末實踐範疇）\n  - 核心步驟：文字潤飾與排版 ➔ 正式專案企劃書 ➔ 成果公開發布展示。\n")
    
    p_note = doc.add_paragraph()
    p_note.paragraph_format.space_before = Pt(4)
    p_note.paragraph_format.space_after = Pt(8)
    r_note_head = p_note.add_run("【授課教師指引：期中評量邊界說明】\n")
    r_note_head.bold = True
    r_note_head.font.color.rgb = RGBColor(180, 83, 9)
    p_note.add_run(
        "請同學們特別留意：期中報告的核心目的在於驗證「個人專業經歷、市場商業思維與數位實作能力的邏輯合理性」。"
        "因此，期中進度要求至【階段 3 之產出：個人商務履歷 ＋ 初步企劃草案/數據分析展示】即可！"
        "同學們無須過早煩惱龐大的預算編列或複雜的甘特圖時程，請專注將個人優勢與企管分析學理做紮實，並發布出清晰的線上 GitHub Pages 網站！"
    )
    
    # -------------------------------------------------------------
    # PART 3: 7 Prompts
    # -------------------------------------------------------------
    h3 = doc.add_paragraph()
    h3.paragraph_format.space_before = Pt(14)
    h3.paragraph_format.space_after = Pt(4)
    r_h3 = h3.add_run("第三部分：七大核心商務 Prompt 指引與示範案例（學生可直接複製）")
    r_h3.bold = True
    r_h3.font.size = Pt(14)
    r_h3.font.color.rgb = RGBColor(15, 23, 42)
    
    doc.add_paragraph(
        "以下為期中專案七大標準步驟。每個步驟均附帶「學生可直接複製之 Prompt 指令」與「Google Antigravity 真實輸出解析」。"
        "示範案例採《樂肉選品 (LeRou Pet Goods)》寵物經濟專案，同學可依照個人選定之主題（服飾美妝、精品代購、二手車商務、文創餐飲、個人求職履歷等）彈性替換名稱！"
    )
    
    # Step 1
    doc.add_paragraph("步驟 1：【發掘痛點與創業動機 Prompt】").bold = True
    p1_prompt = (
        "身為微型創業者與商務企劃人員，我想以《樂肉選品》為題，主打常溫原肉烘乾零食與毛孩脆片。\n"
        "請幫我從『市售零食添加物』、『鮮食冷鏈運費門檻』與『美學生活體驗』三方面，提煉出 3 個具體痛點與切入緣起。"
    )
    p1_output = (
        "1. 市售零食過度添加與成分不透明：市售大包裝肉乾多含甘油、人工防腐劑與肉粉混充，飼主難以辨認真實肉源，缺乏安全信任感。\n"
        "2. 鮮食冷鏈運費高昂成微型創業阻礙：低溫冷凍宅配單筆運費動輒 160~220 元，大幅提高初次購買門檻；反之，「常溫原肉烘乾零食」超取僅需 60 元，保存期長且無腐壞存貨壓力。\n"
        "3. 寵物日常點心欠缺美學儀式感：傳統零食包裝俗豔且質地死硬，缺乏能讓飼主與毛孩一同享受下午茶的「卡滋脆片」體驗與極簡設計。"
    )
    create_prompt_box(doc, "微型創業者 兼 商業分析師", p1_prompt, p1_output, "開啟 Google Antigravity App，貼上指令觀察 AI 如何梳理出切入市場的清晰脈絡。")
    add_screenshot_figure(doc, "image2.png", "圖 3-1 步驟 1 Google Antigravity Agent 痛點提煉對話實機截圖")
    
    # Step 2
    doc.add_paragraph("步驟 2：【外部總體環境 PESTC 深度分析 Prompt】").bold = True
    p2_prompt = (
        "請針對《樂肉選品》的常溫原肉烘乾零食（厚切雞肉乾、毛孩地瓜肉片），運用政治法律、經濟、社會文化、科技、綠色環保五大構面進行 PESTC 總體環境分析，並說明對本企劃之啟發。"
    )
    p2_output = (
        "• P (政治法律)：農業部嚴格抽驗寵物食品添加物，100% 原肉慢烘零食成分單純，化嚴格法規為信任優勢。\n"
        "• E (經濟環境)：小額精緻點心具抗跌口紅效應，搭配 60 元常溫超取，大幅提升首購下單轉化率。\n"
        "• S (社會文化)：少子化與毛孩擬人化普及，飼主樂於與毛孩共度下午茶時光，原肉洋芋片切中陪伴需求。\n"
        "• T (科技創新)：專業低溫熱風慢烘機普及，65°C~70°C 保留原始肉香，個人小批量現烘品質優異。\n"
        "• C (綠色環保)：嚴選在地國產檢驗合格肉品與在地農民黃金地瓜，縮短食物里程，落實永續友善。"
    )
    create_prompt_box(doc, "商務決策特助", p2_prompt, p2_output, "PESTC 能幫助同學站在宏觀視角檢視商業機會，為後續 SWOT 分析奠定堅實客觀基礎。")
    add_screenshot_figure(doc, "image5.png", "圖 3-2 步驟 2 PESTC 總體環境分析對話實機截圖")
    
    # Step 3
    doc.add_paragraph("步驟 3：【內部資源盤點與假想敵防護 Prompt】").bold = True
    p3_prompt = (
        "我身為微型創業者，啟動資金僅 3~5 萬、一人作業、無實體店面。請盤點我的內部優劣勢，並選定大型量販賣場的進口拼裝副產物肉乾為主要假想敵，規劃我的定位防護策略。"
    )
    p3_output = (
        "1. 內部資源盤點：\n"
        "   • 優勢：靈活敏捷、精通 AI 提示詞工程與 GitHub Pages 零伺服器架站技術、無實體店面租金壓力。\n"
        "   • 劣勢：初期產能受限於單機烘烤批次、缺乏大規模原料採購議價優勢。\n"
        "2. 假想敵精準辨認：大型量販賣場大包裝促銷肉乾（低價拼裝肉、含化學防腐劑）。\n"
        "3. 我方定位防護策略：\n"
        "   • 不與大廠進行價格正面衝突，將戰場移至「100% 看得見的原切肉絲纖維」與「無鹽無油酥脆洋芋片」。\n"
        "   • 堅持小批量新鮮現烘，以「極致安心透明」構築難以撼動的品牌護城河。"
    )
    create_prompt_box(doc, "策略營運顧問", p3_prompt, p3_output, "正確認識假想敵，能避免微型創業者在不具備規模優勢的領域浪費資源。")
    add_screenshot_figure(doc, "image17.png", "圖 3-3 步驟 3 內部資源盤點與假想敵定位截圖")
    
    # Step 4
    doc.add_paragraph("步驟 4：【SWOT 因果推論四象限四部曲綜合矩陣 Prompt】").bold = True
    p4_prompt = (
        "請將上述《樂肉選品》的內外部條件交叉，嚴格按照 SO（積極開拓）、WO（借力補強）、ST（防禦轉化）、WT（避險聚焦）的四象限四部曲因果推論邏輯，產出策略矩陣。"
    )
    p4_output = (
        "• SO 積極開拓策略：發揮 100% 原肉厚切與常溫超取的成本優勢，結合社群「人寵同享下午茶脆片」視覺內容，迅速拓展全台青年飼主客群。\n"
        "• WO 借力補強策略：藉由常溫超商取貨的極佳便利性，以「每週新鮮限量出爐」的預購模式運作，將產能有限轉化為「新鮮現烘」的稀缺優勢。\n"
        "• ST 防禦轉化策略：面對同質性手工點心的競爭，主動將烘烤溫度、時間、水分檢驗報告與在地農民來源全數以 QR Code 公開透明化，化威脅為品質防線。\n"
        "• WT 避險聚焦策略：嚴格控制初期原料採購，不囤積非必要設備，專注於「雞肉厚切乾」與「地瓜雞肉洋芋片」兩大明星單品，實現穩健獲利與資金周轉。"
    )
    create_prompt_box(doc, "高級策略規劃師", p4_prompt, p4_output, "SWOT 不僅是條列四個象限，更重要的是兩兩交叉碰撞出的『因果行動推論』！")
    add_screenshot_figure(doc, "image6.png", "圖 3-4 步驟 4 SWOT 因果推論四象限矩陣實機截圖")
    
    # Step 5
    doc.add_paragraph("步驟 5：【SMART 企劃目標與三超前瞻思維 Prompt】").bold = True
    p5_prompt = (
        "請為《樂肉選品》期中 MVP 設定 30 天內可量化驗證的 SMART 目標，並融入『超前意識、超越常規、超越期望』的三超思維。"
    )
    p5_output = (
        "1. SMART 目標：\n"
        "   • S (具體)：發布 GitHub Pages 線上專頁，上架厚切雞肉乾與金薯原肉脆片。\n"
        "   • M (可衡量)：上線 30 天內達成 200 次真實瀏覽、收集 30 份試吃預購意向。\n"
        "   • A (可達成)：運用校園人際圈與社群分享，設定試吃優惠價，指標穩健。\n"
        "   • R (相關性)：實質驗證常溫配送對提高下單轉化率的效益，作為期末決策基礎。\n"
        "   • T (時限)：於學期第八週前完成 GitHub Pages 部署並開放登記。\n"
        "2. 三超前瞻思維：\n"
        "   • 超前意識：先以低風險常溫烘乾零食切入市場驗證，為未來的鮮食版圖打下客群基石。\n"
        "   • 超越常規：研發如洋芋片般酥脆的薄切脆片工藝，牙口不好的老犬老貓亦能輕鬆享用。\n"
        "   • 超越期望：隨包附贈「毛孩每日熱量換算與點心給予量對照小卡」，提供貼心關懷。"
    )
    create_prompt_box(doc, "專案經理 (PMP)", p5_prompt, p5_output, "SMART 結合三超思維，讓企劃目標兼具落地執行力與驚豔評審的亮點！")
    add_screenshot_figure(doc, "image15.png", "圖 3-5 步驟 5 SMART 目標設定實機截圖")
    
    # Step 6
    doc.add_paragraph("步驟 6：【STP 市場定位與 4P 行銷組合 Prompt】").bold = True
    p6_prompt = (
        "請為我擬定 STP（市場區隔、目標客群、品牌定位），並規劃 4P 方案（包含厚切肉乾、脆脆洋芋片、透氣背心三款商品規格、常溫超取運費 60 元策略、以及 #毛孩卡滋挑戰 社群推廣）。"
    )
    p6_output = (
        "• STP 定位宣言：鎖定 20~35 歲都會男女飼主，品牌主張：「樂肉選品，讓毛孩每一口都快樂。」——專注於常溫低溫慢烘原肉點心與生活美學的微型寵物選品品牌。\n"
        "• 產品 (Product)：\n"
        "  - 明星商品 A：【低溫原切】黃金熟成雞胸肉乾（厚切 80g，72 小時慢烘）。\n"
        "  - 明星商品 B：【卡滋脆脆】毛孩專屬金薯雞肉洋芋片（薄切 60g，酥脆可口）。\n"
        "  - 風格選品 C：日系大地色親膚純棉透氣背心（常溫搭配出貨）。\n"
        "• 價格 (Price)：原肉乾 NT$ 160 / 包；原肉洋芋片 NT$ 140 / 包；任選 3 包享體驗組合價 NT$ 399。\n"
        "• 通路 (Place)：線上以個人 GitHub Pages 作為品牌型錄展示，串接 Google 表單，提供常溫超取（運費僅需 60 元）。\n"
        "• 推廣 (Promotion)：發起「#毛孩卡滋挑戰」短影音徵集，錄下毛孩咀嚼洋芋片時的香脆聲音，創造社群自然擴散。"
    )
    create_prompt_box(doc, "行銷總監 (CMO)", p6_prompt, p6_output, "4P 方案中的通路策略正好與 GitHub Pages 靜態網站發布形成完美閉環！")
    add_screenshot_figure(doc, "image8.png", "圖 3-6 步驟 6 STP 與 4P 行銷組合實機截圖")
    
    # Step 7
    doc.add_paragraph("步驟 7：【一鍵生成線上 MVP 網頁程式碼 Prompt】").bold = True
    p7_prompt = (
        "請幫我閱讀 https://docs.google.com/document/d/1Z55W_Y8xOGER5BzoSfbBk9Mt7efRR_4P1R8MLjcO774/edit 此檔案，\n"
        "並根據此檔案，幫我生成《樂肉選品》XXX主題 (請各位同學自行更改主題，不能以寵物食品，這是範例，可以用賣衣服、代購精品包、賣二手車等等主題不限) 初步企劃草案，\n"
        "生成為一個單一檔案且可直接運行的現代日系極簡風格 (可更改風格) HTML/CSS 網頁（index.html），\n"
        "包含個人/品牌故事、學理分析摘要、三款商品卡片與線上預購意向登記按鈕。\n\n"
        "🌟【期中加分專區必加】：請在網頁中嵌入一個『產業商業數據視覺化儀表板 (Chart.js)』，展示近 5 年產業規模消長折線圖與營收結構甜甜圈圖，並附上 3 點商務洞察分析。\n"
        "並幫我部屬到 GitHub，我不想自己上傳檔案所以給你這串 API key 你幫我上傳 (請貼上 GitHub Personal Access Token 亂碼)。"
    )
    p7_output = (
        "• 產出成果：包含完整 <!DOCTYPE html> 規格的 index.html 檔案。\n"
        "• 視覺特色：自帶 Google Fonts 字體、CSS Flex/Grid 現代化排版、卡片懸停陰影、Chart.js 互動圖表。\n"
        "• 響應式相容：手機與電腦均有專屬 RWD 介面，完美解決跑版問題。"
    )
    create_prompt_box(doc, "全端工程師 兼 視覺設計師", p7_prompt, p7_output, "這一步將前面所有學理企劃直接具象化為真正的可上線網站！")
    
    # -------------------------------------------------------------
    # PART 4: GitHub API Token & Pages
    # -------------------------------------------------------------
    h4 = doc.add_paragraph()
    h4.paragraph_format.space_before = Pt(14)
    h4.paragraph_format.space_after = Pt(4)
    r_h4 = h4.add_run("第四部分：GitHub Personal Access Token (API Key) 生成與自動發布指引")
    r_h4.bold = True
    r_h4.font.size = Pt(14)
    r_h4.font.color.rgb = RGBColor(15, 23, 42)
    
    doc.add_paragraph(
        "為了讓同學們享受現代 Vibe Coding『動口不動手』的流暢體驗，可以直接將 GitHub API Token 提供給 Antigravity，"
        "讓 AI 助理自動將生成的 index.html 推送至個人 GitHub 儲存庫，徹底免除手動上傳檔案的瑣碎步驟！"
    )
    
    p_tok1 = doc.add_paragraph()
    r_tok_head = p_tok1.add_run("4.1 生成 GitHub Personal Access Token (classic) 四步驟：\n")
    r_tok_head.bold = True
    p_tok1.add_run(
        "1. 點擊個人 GitHub 右上角頭像 ➔ 選擇「Settings」➔ 頁面捲動至最左下角點選「Developer settings」。"
    )
    add_screenshot_figure(doc, "image12.png", "圖 4-1 進入 GitHub Settings 點選最下方 Developer settings")
    
    doc.add_paragraph(
        "2. 點擊「Personal access tokens」➔ 選擇「Tokens (classic)」➔ 點選「Generate new token (classic)」。\n"
        "3. 設定 Note 名稱為「antigravity-deploy」，Expiration 選擇「30 days」或「No expiration」，並在 Scopes 中務必勾選「repo」（包含完整儲存庫讀寫權限）與「workflow」。"
    )
    add_screenshot_figure(doc, "image16.png", "圖 4-2 設定 Token 名稱、有效期限並勾選 repo 存取權限")
    
    doc.add_paragraph(
        "4. 滑動至頁面最底端，點選綠色按鈕「Generate token」生成密鑰金鑰。"
    )
    add_screenshot_figure(doc, "image13.png", "圖 4-3 捲動至最下方點擊綠色 Generate token 按鈕")
    
    p_warn = doc.add_paragraph()
    p_warn.paragraph_format.space_before = Pt(4)
    p_warn.paragraph_format.space_after = Pt(4)
    r_w = p_warn.add_run("⚠️ 【極重要安全提示】：複製這串 Token 亂碼 (以 ghp_ 開頭)，此金鑰僅會出現一次！請妥善保存，切勿隨意散佈給無關他人！")
    r_w.bold = True
    r_w.font.color.rgb = RGBColor(220, 38, 38)
    
    add_screenshot_figure(doc, "image7.png", "圖 4-4 複製產生的專屬 GitHub Token 金鑰亂碼")
    
    doc.add_paragraph(
        "4.2 啟用 GitHub Pages 免費雲端靜態網頁發布：\n"
        "GitHub Pages 能將儲存庫中的 HTML、CSS、JavaScript 檔案，一鍵發布為全世界皆可瀏覽的真實公開網站。\n"
        "• 查看 GitHub Pages 官方指引：https://pages.github.com/\n"
        "• 啟用步驟：\n"
        "  1. 進入專案儲存庫頁面，點選上方功能導覽列的「Settings」（設定）。\n"
        "  2. 在左側選單中找到「Code and automation」區塊，點選「Pages」。\n"
        "  3. 在「Build and deployment」底下的「Branch」設定：將分支改選為 main，資料夾維持 /(root)，點擊右側「Save」。\n"
        "  4. 等待約 1~2 分鐘重新整理頁面，頂部將出現綠色提示：「Your site is live at https://[您的帳號].github.io/[專案名稱]/」。\n"
        "  5. 此網址即為期中報告必須提交之「線上公開部署網址」！"
    )
    
    # -------------------------------------------------------------
    # PART 5: Bonus - Industry Data Visualization Showcase
    # -------------------------------------------------------------
    h5 = doc.add_paragraph()
    h5.paragraph_format.space_before = Pt(14)
    h5.paragraph_format.space_after = Pt(4)
    r_h5 = h5.add_run("第五部分：【期中專案加分亮點】有興趣的產業商業數據分析視覺化專區")
    r_h5.bold = True
    r_h5.font.size = Pt(14)
    r_h5.font.color.rgb = RGBColor(180, 83, 9)
    
    doc.add_paragraph(
        "為了鼓勵同學將課堂所學之商業軟體與數據處理思維運用於職場求職，"
        "凡於個人履歷網站中加入「產業商業數據視覺化專區（Business Data Visualization Showcase）」者，"
        "將享有期中報告顯著加分！以下提供三大企管推薦公開數據庫與現成示範代碼："
    )
    
    # Data Table
    table_data = doc.add_table(rows=6, cols=6)
    table_data.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_data.autofit = False
    
    headers = ["年度", "產業營業額 (億元)", "營業家數 (家)", "商品買賣佔比", "照顧服務佔比", "犬貓登記總數 (萬隻)"]
    widths = [Inches(0.8), Inches(1.2), Inches(1.1), Inches(1.1), Inches(1.1), Inches(1.1)]
    
    for c_idx, h in enumerate(headers):
        cell = table_data.cell(0, c_idx)
        cell.width = widths[c_idx]
        set_cell_background(cell, "1E3A8A")
        set_cell_margins(cell, 80, 80, 100, 100)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.bold = True
        r.font.size = Pt(9)
        r.font.color.rgb = RGBColor(255, 255, 255)
        
    rows_val = [
        ["2019", "280.2", "6,850", "83.5%", "6.8%", "230"],
        ["2020", "315.4", "7,230", "83.8%", "7.2%", "255"],
        ["2021", "345.8", "7,810", "84.1%", "7.9%", "275"],
        ["2022", "387.3", "8,335", "83.5%", "8.5%", "295"],
        ["2023", "430.5", "8,847", "82.8%", "9.3%", "315"]
    ]
    
    for r_idx, row in enumerate(rows_val):
        for c_idx, val in enumerate(row):
            cell = table_data.cell(r_idx + 1, c_idx)
            cell.width = widths[c_idx]
            bg = "F8FAFC" if r_idx % 2 == 1 else "FFFFFF"
            set_cell_background(cell, bg)
            set_cell_margins(cell, 60, 60, 80, 80)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_idx == 0 else WD_ALIGN_PARAGRAPH.RIGHT
            r = p.add_run(val)
            r.font.size = Pt(9)
            if c_idx == 0:
                r.bold = True
                
    doc.add_paragraph().paragraph_format.space_after = Pt(6)
    
    p_bonus_prompt = (
        "【加分專案 Prompt 指令】：\n"
        "「請在我的個人履歷網頁（index.html）下方新增一個『產業商業數據分析視覺化專案 (Industry Data Insights)』區塊。\n"
        "使用上述台灣寵物經濟 2019~2023 官方統計數據（營業額由 280.2 億成長至 430.5 億，毛孩登記突破 315 萬隻，商品佔比 83%、照顧服務佔比 9%），\n"
        "引入 Chart.js 繪製兩組高質感互動圖表：\n"
        "1. 雙軸折線圖：營業額成長趨勢 ✕ 毛孩登記數走勢。\n"
        "2. 環形甜甜圈圖：寵物產業三大營收結構佔比。\n"
        "圖表需具備手機 RWD 自適應與滑鼠懸停數值提示 (Tooltip)，並附上 3 點企管商務洞察（高複合成長、貓派崛起帶動小宅經濟、高毛利精緻照護爆發）。」"
    )
    create_prompt_box(doc, "商業數據視覺化專家", p_bonus_prompt, tip_text="這項加分項目能讓你的個人履歷在眾多求職者中脫穎而出，證明你具備『數據解讀 ✕ 前端展示 ✕ 商業分析』全方位能力！")
    
    # -------------------------------------------------------------
    # PART 6: Submission Checklist
    # -------------------------------------------------------------
    h6 = doc.add_paragraph()
    h6.paragraph_format.space_before = Pt(14)
    h6.paragraph_format.space_after = Pt(4)
    r_h6 = h6.add_run("第六部分：期中專案檢核清單與互評成果指引")
    r_h6.bold = True
    r_h6.font.size = Pt(14)
    r_h6.font.color.rgb = RGBColor(15, 23, 42)
    
    checklist = [
        "已下載安裝 Google Antigravity App (v2.28.2) 並使用個人 Google 帳號登入。",
        "已於 GitHub 建立公開儲存庫 (Public Repo) 並完成 Personal Access Token 設定。",
        "已運用 Antigravity 完成痛點提煉、PESTC、內部資源、SWOT 因果推論矩陣、SMART 目標與 STP+4P 規劃。",
        "已成功生成包含個人商務履歷、企劃草案、商品/經歷卡片與預購意向登記的 index.html 網頁。",
        "【加分項確認】：網頁已嵌入有興趣的產業商業數據分析視覺化專案 (Chart.js 互動圖表與商務洞察)。",
        "已開啟 GitHub Pages，並確認手機與電腦皆能順暢瀏覽公開網址 (https://[帳號].github.io/[專案名]/)。",
        "已於課程教學平台完成期中成果公開網址提交，參與全班觀摩互評！"
    ]
    
    for item in checklist:
        p_c = doc.add_paragraph()
        p_c.paragraph_format.space_before = Pt(1)
        p_c.paragraph_format.space_after = Pt(2)
        r_box = p_c.add_run(" [  ]  ")
        r_box.bold = True
        r_box.font.color.rgb = RGBColor(2, 132, 199)
        r_txt = p_c.add_run(item)
        r_txt.font.size = Pt(10)
        
    doc.add_paragraph().paragraph_format.space_after = Pt(12)
    
    # Save outputs
    out_docx_1 = os.path.join(downloads_dir, "商業軟體應用_期中報告操作手冊_個人履歷網站與產業數據分析.docx")
    out_docx_2 = os.path.join(base_dir, "商業軟體應用_期中報告操作手冊.docx")
    doc.save(out_docx_1)
    doc.save(out_docx_2)
    print(f"Saved: {out_docx_1} ({os.path.getsize(out_docx_1):,} bytes)")
    print(f"Saved: {out_docx_2} ({os.path.getsize(out_docx_2):,} bytes)")

if __name__ == "__main__":
    build_docx_manual()
