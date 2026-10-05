# -*- coding: utf-8 -*-
"""
Generate professorial-grade Week 03 Google Doc / Word Operation Manual:
- downloads/Week03_Vibe_Coding_Word商業企劃書_GoogleDocs操作手冊.docx
- Vibe_Coding_Google_Doc操作手冊.docx
Matching the 0910 Vibe Coding Workshop Manual pedagogy:
- Google Docs weekly document tabs / navigation outline
- Embedded high-res UI screenshots for every step
- Clear prompt boxes with copyable CLEAR prompts
- Starter files & raw unformatted disaster drafts
- Zero-typing workflow using Agentic AI
"""
import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

base_dir = r"g:\我的雲端硬碟\萬能科技大學\備課\11501課表\11501商業軟體應用"
assets_dir = os.path.join(base_dir, "assets", "manual_screenshots")
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

def create_prompt_box(doc, role_title, prompt_text, tip_text=""):
    """Creates a distinct styled table box representing the copyable prompt."""
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    
    cell = table.cell(0, 0)
    cell.width = Inches(6.3)
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
    run_badge = p.add_run(f"📋 【可直接複製之 Prompt 指令】 ｜ 🎭 設定角色：{role_title}\n")
    run_badge.bold = True
    run_badge.font.size = Pt(10.5)
    run_badge.font.color.rgb = RGBColor(2, 132, 199)
    
    run_text = p.add_run(prompt_text)
    run_text.font.size = Pt(9.5)
    run_text.font.name = "Consolas"
    run_text.font.color.rgb = RGBColor(15, 23, 42)
    
    if tip_text:
        p2 = cell.add_paragraph()
        p2.paragraph_format.space_before = Pt(4)
        p2.paragraph_format.space_after = Pt(2)
        run_tip = p2.add_run(f"💡 經理人操作要領：{tip_text}")
        run_tip.font.size = Pt(9)
        run_tip.font.italic = True
        run_tip.font.color.rgb = RGBColor(180, 83, 9)

    doc.add_paragraph().paragraph_format.space_after = Pt(4)

def add_screenshot_figure(doc, img_name, fig_num_title, explanation=""):
    """Embeds screenshot image with caption and shadow box."""
    img_path = os.path.join(assets_dir, img_name)
    if os.path.exists(img_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(6)
        p_img.paragraph_format.space_after = Pt(3)
        doc.add_picture(img_path, width=Inches(6.0))
        
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_before = Pt(2)
        p_cap.paragraph_format.space_after = Pt(6)
        r_num = p_cap.add_run(f"▲ {fig_num_title}")
        r_num.bold = True
        r_num.font.size = Pt(9.5)
        r_num.font.color.rgb = RGBColor(30, 58, 138)
        
        if explanation:
            r_exp = p_cap.add_run(f" —— {explanation}")
            r_exp.font.size = Pt(9)
            r_exp.font.color.rgb = RGBColor(100, 116, 139)
    else:
        p = doc.add_paragraph(f"[圖片未找到: {img_name}]")
        p.runs[0].font.color.rgb = RGBColor(220, 38, 38)

def add_disaster_box(doc, box_title, box_content):
    """Creates a distinct styled callout box representing raw unformatted draft data."""
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    
    cell = table.cell(0, 0)
    cell.width = Inches(6.3)
    set_cell_background(cell, "FEF2F2") # Soft light red
    set_cell_margins(cell, top=140, bottom=140, left=180, right=180)
    
    tcPr = cell._element.get_or_add_tcPr()
    borders = parse_xml(f'''
        <w:tcBorders {nsdecls("w")}>
            <w:top w:val="single" w:sz="6" w:space="0" w:color="FECACA"/>
            <w:left w:val="single" w:sz="24" w:space="0" w:color="DC2626"/>
            <w:bottom w:val="single" w:sz="6" w:space="0" w:color="FECACA"/>
            <w:right w:val="single" w:sz="6" w:space="0" w:color="FECACA"/>
        </w:tcBorders>
    ''')
    tcPr.append(borders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(4)
    run_title = p.add_run(f"📁 {box_title}\n")
    run_title.bold = True
    run_title.font.size = Pt(10)
    run_title.font.color.rgb = RGBColor(153, 27, 27)
    
    run_text = p.add_run(box_content)
    run_text.font.size = Pt(9)
    run_text.font.color.rgb = RGBColor(55, 65, 81)
    
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

def build_manual():
    doc = Document()
    
    # 2.54 cm margins
    for sec in doc.sections:
        sec.top_margin = Inches(1.0)
        sec.bottom_margin = Inches(1.0)
        sec.left_margin = Inches(1.0)
        sec.right_margin = Inches(1.0)
        
    # Header Information
    p_top = doc.add_paragraph()
    p_top.paragraph_format.space_after = Pt(2)
    r_uni = p_top.add_run("萬能科技大學 企業管理系 11501 學期《商業軟體應用》\n")
    r_uni.font.size = Pt(11)
    r_uni.font.color.rgb = RGBColor(100, 116, 139)
    
    r_title = p_top.add_run("Vibe Coding ✕ Agentic AI 智慧辦公 18 週操作手冊（Google Docs 分頁版）")
    r_title.bold = True
    r_title.font.size = Pt(18)
    r_title.font.color.rgb = RGBColor(30, 58, 138)
    
    p_meta = doc.add_paragraph()
    p_meta.paragraph_format.space_after = Pt(10)
    r_meta = p_meta.add_run(
        "【教學理念】：零手打！你就是商務專案總監，動口動腦下 Prompt，讓 Agentic AI 自動化執行！\n"
        "授課教師：邱俊維 博士 (Dr. Chun-Wei Chiu) ｜ 授課地點：J501 電腦教室 ｜ 上課時間：每週一 20:10~21:40\n"
        "參考規範：萬能科技大學 0910 研習《Vibe Coding 操作手冊》與企業商務實務標準"
    )
    r_meta.font.size = Pt(9.5)
    r_meta.font.color.rgb = RGBColor(71, 85, 105)

    # -------------------------------------------------------------
    # TAB 1: WEEK 01
    # -------------------------------------------------------------
    h_w01 = doc.add_heading("📑 第 01 週：AI 辦公先導觀念與協作基礎（CLEAR 提問與環境建置）", level=1)
    h_w01.style.font.color.rgb = RGBColor(30, 58, 138)
    p_w01 = doc.add_paragraph()
    p_w01.add_run("【模組概述】：開通 Google Cloud Shell 5GB 永續雲端環境與 GitHub，建立個人專案目錄。\n"
                  "【核心成果】：熟練 CLEAR（Context, Limits, Expectation, Action, Role）五大提問法則，將零碎會議記錄轉化為標準公文結構。")

    # -------------------------------------------------------------
    # TAB 2: WEEK 02
    # -------------------------------------------------------------
    h_w02 = doc.add_heading("📑 第 02 週：Markdown 檔案結構化與命名防呆（ISO 8601 與災難包重構）", level=1)
    h_w02.style.font.color.rgb = RGBColor(30, 58, 138)
    p_w02 = doc.add_paragraph()
    p_w02.add_run("【模組概述】：解析《Week02_企業混亂命名與版本災難實例包.zip》，徹底根絕『真的最終版.docx』之命名悲劇。\n"
                  "【核心成果】：指令 AI 自動依據 ISO 8601 (YYYY-MM-DD) 重建目錄樹，產出四欄右對齊公文與專案 README.md。")

    # -------------------------------------------------------------
    # TAB 3: WEEK 03 (MAIN FOCUS)
    # -------------------------------------------------------------
    h_w03 = doc.add_heading("🔥 第 03 週：Word 商業企劃書標準結構與 AI 輔助起草（本週核心主修）", level=1)
    h_w03.style.font.color.rgb = RGBColor(185, 28, 28) # Vibrant Highlight
    
    # Overview Banner
    p_w03_lead = doc.add_paragraph()
    r_lead = p_w03_lead.add_run("【本週核心宗旨】：商業企劃書是爭取投資補助與高階主管拍板的核心文件。一份及格的商業企劃書，格式規範（上下左右 2.54cm 標準邊界、分節符號切斷頁首頁尾、三線財務表格）往往比企劃點子本身更能決定投資人的信任度！本週我們完全零手打，引導 AI 代理人從混亂草案直接重構出頂級管顧規格企劃書！")
    r_lead.bold = True
    r_lead.font.size = Pt(10.5)
    r_lead.font.color.rgb = RGBColor(30, 58, 138)

    # Section 1: Case Scene
    doc.add_heading("一、 商業教學模擬情境與學習目標", level=2)
    p_scene = doc.add_paragraph()
    p_scene.add_run("【真實商業情境】：某校園智慧零售創業團隊構思「智慧校園低卡健康快煮餐盒」新事業提案，向投資人與育成中心爭取新台幣 300 萬元種子資金。然而，因為送交的企劃書邊界窄至 0.5cm 導致裝訂切字、連按 20 次 Enter 換頁導致排版全崩、封面印著頁碼且缺乏 350 字執行摘要，在初審階段即遭退件！\n").font.color.rgb = RGBColor(153, 27, 27)
    p_scene.add_run("【本週學習目標（OBE 產出導向）】：\n"
                    "1. 掌握公文標準版面設定公式（邊界上下左右各 2.54 cm / 1 英吋、行距 1.25 倍、段落後間距 6pt）。\n"
                    "2. 熟練分頁符 (Page Break) 與分節符 (Section Break) 之本質差異，實現封面無頁碼、內文自第 1 頁起算。\n"
                    "3. 運用 CLEAR 提示詞驅動 AI 產出商業企劃書黃金五結構與 350 字高品質執行摘要 (Executive Summary)。\n"
                    "4. 將零散財務採購資料轉化為標準商務 APA「三線表格」（去除多餘直框線，保留上下粗線與欄頭細線）。\n"
                    "5. 養成交件前按 Ctrl+A 全選並按 F9 刷新所有功能變數與自動目錄之肌肉記憶。")

    # Section 2: Files
    doc.add_heading("二、 實作素材檔案清單與下載指引", level=2)
    p_files = doc.add_paragraph()
    p_files.add_run("本週所有實作皆基於統一素材包，保證全班所有同學具有相同的數據基準，AI 產出精確一致、可受稽核！\n"
                    "📥 【下載檔案】：點擊課程平台「實務練習檔下載」或取得 ")
    r_zip_name = p_files.add_run("Week03_商業企劃書實作素材包.zip\n")
    r_zip_name.bold = True
    r_zip_name.font.color.rgb = RGBColor(2, 132, 199)
    p_files.add_run("內含 4 份核心文件：\n"
                    "• 檔案 1：01_原始未排版草案_鼎新商業企劃_智慧零售新事業.docx（待重構之混亂初稿）\n"
                    "• 檔案 2：02_財務預算明細_CAPEX與OPEX採購估算表.xlsx（CAPEX 120萬＋OPEX 21萬完整試算表）\n"
                    "• 檔案 3：03_示範標準範本_標準商業企劃書排版規範.docx（完美排版對照組）\n"
                    "• 檔案 4：04_README_第三週實作指引與CLEAR提示詞.txt（離線提示詞速查表）")

    # Embedded Disaster Callout Box
    add_disaster_box(
        doc,
        "災難素材檔案 1 原始內容：《01_原始未排版草案_鼎新商業企劃_智慧零售新事業.docx》",
        "智慧校園低卡健康快煮餐盒連鎖專案 商業企劃書 (未排版草稿)\n"
        "撰寫小組：智慧校園營運小組  日期：2026年3月\n"
        "【現況痛點】：學生與教職員外食普遍油膩高鈉，尖峰時段排隊超過 15 分鐘，缺乏客製化營養選擇。\n"
        "【解決方案】：引進智慧 POS 與自動蒸煮機，手機 App 預先點餐，90 秒快速取餐。預估第 8 個月達損益平衡點 (BEP)，首年服務 12 萬人次，創造 1,500 萬元營收。\n"
        "【財務需求】：初期設備建置 (CAPEX) 120 萬元，每月營運費用 (OPEX) 21 萬元。\n"
        "請依照標準版面 2.54cm、封面分節符號、350 字執行摘要、三線表格與自動目錄重構！"
    )

    # Section 3: Mission 1
    doc.add_heading("三、 實作關卡一：Word/Google Docs 版面標準 2.54cm 與段落規範設定 (10 分鐘)", level=2)
    p_m1 = doc.add_paragraph()
    p_m1.add_run("【步驟指引 SOP】：\n").bold = True
    p_m1.add_run("1. 開啟 Word 或 Google Docs，載入《01_原始未排版草案_鼎新商業企劃_智慧零售新事業.docx》。\n"
                 "2. 點擊頂部功能區【版面配置】(Layout) ➔ 點選【邊界】(Margins) ➔ 選擇【標準】（上下左右各 2.54 cm / 1 英吋）。\n"
                 "3. 點選【版面設定】右下角箭號開啟對話框，確認紙張方向為【直向】，套用至【整份文件】。\n"
                 "4. 按 Ctrl + A 全選文字，設定字型為【微軟正黑體 12pt】、行距為【1.25 倍】、段落後間距【6pt】。")
    
    add_screenshot_figure(doc, "fig3_1_page_setup.jpg", "圖 3-1：Word / Google Docs 版面設定對話框操作畫面", "設定邊界為上下左右各 2.54 cm（1 英吋），直向，套用至整份文件。")
    
    prompt_m1 = (
        "【角色設定】：你是一位熟悉台灣公文與國際商管排版標準的版面格式專家。\n"
        "【背景情境】：我們正在編輯「智慧校園健康快煮餐盒商業企劃書」，需設定符合國際標竿企業規範的版面參數。\n"
        "【約束限制】：\n"
        "1. 紙張尺寸：標準 A4 (21.0cm × 29.7cm)。\n"
        "2. 邊界設定：上下左右各 2.54 cm (1 英吋)，裝訂邊 0 cm。\n"
        "3. 字體搭配：中文標題與正文統一採用「微軟正黑體」，英文採用「Calibri」或「Segoe UI」。\n"
        "4. 行距規範：正文行高 1.25 至 1.3 倍，段落後間距 6pt，杜絕連續空行。\n"
        "【核心任務】：請為本份企劃書提供排版參數檢查清單，並說明為何 2.54cm 邊界能大幅提升評審公信力！"
    )
    create_prompt_box(doc, "國際商務排版審查顧問", prompt_m1, "公文標準邊界提供適度閱讀留白與批註空間，杜絕字體緊貼紙邊的業餘感。")

    # Section 4: Mission 2
    doc.add_heading("四、 實作關卡二：分節符號「下一頁」與頁首頁尾獨立頁碼 (15 分鐘)", level=2)
    p_m2 = doc.add_paragraph()
    p_m2.add_run("【步驟指引 SOP】：\n").bold = True
    p_m2.add_run("1. 將游標置於封面頁最後一行文字下方。\n"
                 "2. 點選【版面配置】➔【中斷點】(Breaks) ➔ 在【分節符號】區塊點選【下一頁】(Next Page)。\n"
                 "   ⚠️ 注意：千萬不要按 20 次 Enter 或插入普通「分頁符」！普通分頁符無法切斷章節格式。\n"
                 "3. 游標移動到第 2 頁（正文第一頁），在頁首或頁尾處「滑鼠連點兩下」進入頁首頁尾編輯模式。\n"
                 "4. 在功能區上方點擊【連結到前一節】(Link to Previous) 將其『取消反白選取』！\n"
                 "5. 點擊【頁碼】➔【頁碼格式】➔ 選擇起始頁碼為【1】。此時封面完全無頁碼，正文從第 1 頁起算！")
    
    add_screenshot_figure(doc, "fig3_2_breaks_section.jpg", "圖 3-2：插入分節符號與頁首頁尾斷開連結操作畫面", "在版面配置插入『分節符號：下一頁』，並於頁首頁尾工具取消『連結到前一節』。")
    
    prompt_m2 = (
        "【角色設定】：你是一位擁有 10 年經驗的 Word 長文件架構與自動化工程師。\n"
        "【背景情境】：我們正在製作一份 50 頁之商業企劃書，需要實現「封面乾淨無頁碼、目錄頁羅馬數字 (I, II)、正文阿拉伯數字自第 1 頁起算」之標準結構。\n"
        "【約束限制】：\n"
        "1. 條列分頁符 (Page Break) 與分節符 (Section Break) 的底層本質差異。\n"
        "2. 詳細列出 4 步驟防呆操作，防止發生「在封面按 Delete 刪除頁碼，導致整份文件頁碼全部消失」之災難。\n"
        "【核心任務】：請產出分節符號與頁首頁尾解綁 SOP 指南，供企管系學生建立標準規範！"
    )
    create_prompt_box(doc, "Word 長文件自動化架構師", prompt_m2, "切斷『連結到前一節』是分節的核心，否則刪除封面頁碼將導致全書頁碼同步被刪除。")

    # Section 5: Mission 3
    doc.add_heading("五、 實作關卡三：CLEAR 提示詞驅動 AI 秒級起草「執行摘要與五大黃金結構」 (20 分鐘)", level=2)
    p_m3 = doc.add_paragraph()
    p_m3.add_run("【步驟指引 SOP】：\n").bold = True
    p_m3.add_run("1. 複製下方【關卡三 Master CLEAR 提示詞】。\n"
                 "2. 開啟 Antigravity 或 Google AI Studio (aistudio.google.com)，貼入對話視窗送出。\n"
                 "3. 觀測 AI 代理人 3 秒內自主執行：\n"
                 "   ① 建立五大黃金結構骨架（執行摘要、市場痛點、商業模式、財務預算、里程碑風控）。\n"
                 "   ② 精確起草 350 字高品質「執行摘要」，涵蓋痛點數據、差異化護城河、損益平衡點 (BEP) 與首年營收推估。\n"
                 "   ③ 提煉 3 點未滿足深層需求 (Unmet Needs) 與競爭者比較矩陣。\n"
                 "4. 將產出的結構化內容複製，貼入 Word 企劃書正文中！")
    
    add_screenshot_figure(doc, "fig3_3_ai_prompt_chat.jpg", "圖 3-3：AI 代理人驅動商業企劃書與執行摘要起草畫面", "在對話視窗輸入 CLEAR 提示詞，AI 自動生成包含執行摘要與 3-line 表格的結構化企劃。")
    
    prompt_m3 = (
        "【角色設定】：你是一位擁有 15 年輔導經驗的頂級管理顧問公司資深專案總監 (Engagement Manager) 兼 創投評審委員。\n"
        "【背景情境】：依據專案草案《01_原始未排版草案_鼎新商業企劃_智慧零售新事業.docx》，為「智慧校園低卡健康快煮餐盒」新事業撰寫一份具備高說服力與投資公信力的正式商業企劃書。\n"
        "【約束限制】：\n"
        "1. 嚴格遵循標準商業企劃書五大黃金結構（執行摘要、市場痛點與競爭分析、商業模式與營運規劃、財務預算與ROI、執行時程與風險防範）。\n"
        "2. 文風沉穩專業，符合公文規範；不可捏造與草案衝突之數據。\n"
        "3. 執行摘要 (Executive Summary) 嚴格控制在 300~350 字，必須包含：(a) 痛點數據、(b) 差異化護城河（90秒取餐）、(c) 損益平衡點 (營運第8個月) 與首年營收推估 (1,500萬元)。\n"
        "4. 提供 3 點具體目標客群「未被滿足之深層需求 (Unmet Needs)」分析。\n"
        "【核心任務】：請輸出完整結構化企劃書核心章節初稿！"
    )
    create_prompt_box(doc, "頂級管顧資深專案總監 兼 創投評審", prompt_m3, "執行摘要是企劃書的靈魂，高階主管通常僅憑這 350 字決定是否撥款進一步評估！")

    # Section 6: Mission 4
    doc.add_heading("六、 實作關卡四：APA 頂級三線財務表格排版與樣式美化 (15 分鐘)", level=2)
    p_m4 = doc.add_paragraph()
    p_m4.add_run("【步驟指引 SOP】：\n").bold = True
    p_m4.add_run("1. 在 Word 中反白章節標題，依序套用樣式庫中的【標題 1】（第 1 章...）、【標題 2】（1.1 節...）。\n"
                 "2. 複製素材包《02_財務預算明細_CAPEX與OPEX採購估算表.xlsx》中的數據，或使用下方 Prompt 請 AI 產出。\n"
                 "3. 實施商務圖表減法原則（三線表排版）：\n"
                 "   ① 選取表格 ➔ 進入【表格設計】(Table Design) ➔ 框線選單選擇【無框線】。\n"
                 "   ② 表格頂端與底端設定【1.5pt 單線】。\n"
                 "   ③ 欄位標題下方設定【0.75pt 單線】。\n"
                 "   ④ 徹底去除所有刺眼的垂直格線與彩色背景！\n"
                 "4. 金額欄位靠右對齊，文字欄位靠左對齊，表頭置中。")
    
    add_screenshot_figure(doc, "fig3_4_styles_table.jpg", "圖 3-4：Word 階層樣式套用與 APA 頂級三線財務表格美化畫面", "透過常用樣式庫套用標題 1/2，並製作去除垂直邊框的標準頂級商務三線表格。")
    
    prompt_m4 = (
        "【角色設定】：你是一位資深財務分析師 兼 商務視覺設計總監。\n"
        "【背景情境】：將校園智慧零售專案的 CAPEX (120萬) 與 OPEX (21萬) 採購明細，整理為符合 APA 與頂級管顧出版品規範的標準「三線表格」。\n"
        "【約束限制】：\n"
        "1. 表格欄位：項次、費用類別 (CAPEX/OPEX)、預算項目說明、預估金額 (NT$)、審核與折舊備註。\n"
        "2. 金額欄位嚴格遵循三位一撇（如 $120,000），強制靠右對齊。\n"
        "3. 表格僅保留頂線 (1.5pt)、欄頭底線 (0.75pt)、表格底線 (1.5pt)，完全去除所有垂直格線。\n"
        "4. 提供表號與表名（如：表 4-1：校園智慧零售新事業資本支出與營運費用預算明細表）。\n"
        "【核心任務】：請產出符合上述規格的 Markdown 表格與 Word 排版步驟說明！"
    )
    create_prompt_box(doc, "資深財務分析師 兼 視覺設計總監", prompt_m4, "三線表是商管與學術界的最高審美標準，去除多餘墨水，只保留關鍵財務資訊。")

    # Section 7: Mission 5
    doc.add_heading("七、 實作關卡五：全選 F9 刷新與自動化目錄生成 (10 分鐘)", level=2)
    p_m5 = doc.add_paragraph()
    p_m5.add_run("【步驟指引 SOP】：\n").bold = True
    p_m5.add_run("1. 游標移動到第 2 頁目錄預留位置。\n"
                 "2. 點選功能區【參考資料】(References) ➔ 點選最左側【目錄】(Table of Contents) ➔ 選擇【自動目錄 1】。\n"
                 "   系統將在 0.5 秒內自動擷取全書所有「標題 1」與「標題 2」，並自動生成對齊的點狀虛線與頁碼！\n"
                 "3. 養成交件前強制肌肉記憶：按【Ctrl + A】全選整份文件，按下鍵盤【F9】鍵！\n"
                 "4. 在跳出的確認對話框中選擇【更新整個目錄】（而非僅更新頁碼），確保所有修改章節與頁碼 100% 準確！\n"
                 "5. 在 Google Docs 中，左側側邊欄將自動浮現文件大綱（Document Tabs / Outline），點擊即可秒級跳轉章節！")
    
    add_screenshot_figure(doc, "fig3_5_toc_tabs_nav.jpg", "圖 3-5：Word 與 Google Docs 自動目錄與左側分頁大綱導航畫面", "點擊插入自動目錄，按 F9 全域刷新；Google Docs 左側自動呈現層次分明的章節分頁。")
    
    prompt_m5 = (
        "【角色設定】：你是一位資深企業數位稽核長 (Digital Auditor)。\n"
        "【背景情境】：在提交商業企劃書給董事會之前，執行最後一道「防呆查核 (Poka-Yoke) 審計程序」。\n"
        "【約束限制】：\n"
        "1. 列出長文件交付前的 5 大致命地雷（如：目錄頁碼停在舊版未刷新、封面出現頁碼、邊界切字等）。\n"
        "2. 提供一份具備核選方塊 (- [ ]) 的交付審計清單。\n"
        "【核心任務】：請為專案團隊產出企劃書交付前的防呆檢核表！"
    )
    create_prompt_box(doc, "企業數位資產稽核長", prompt_m5, "交件前強制 Ctrl+A 接著按 F9 刷新功能變數，是專業商管經理人必備的肌肉記憶！")

    # Section 8: Cross-disciplinary extension (Long-term Care BI case reference)
    doc.add_heading("八、 跨界實戰延伸：智慧商務與長照趨勢數據分析（呼應 0910 研習手冊）", level=2)
    p_ext = doc.add_paragraph()
    p_ext.add_run("【0910 研習特色案例傳承】：\n").bold = True
    p_ext.add_run("在 0910 研習手冊中，老師特別展示了「長照趨勢分析」的跨界商業應用。商業軟體應用的核心能力是相通的：無論是校園智慧零售餐盒，還是高齡化社會的銀髮長照與智慧照護輔具企劃，企管同學只要掌握：\n"
                  "1. 結構化文字企劃（Word 標準五結構）\n"
                  "2. 統計數據清洗與分析（Excel / Google Sheets 樞紐與圖表）\n"
                  "3. 決策簡報與視覺化呈現（PowerPoint / Google Slides 母片與資訊圖表）\n"
                  "4. 一鍵發布網頁與儀表板（GitHub Pages 靜態託管）\n"
                  "即可跨界解決各行各業的複雜商業問題！同學可嘗試將今日學到的 CLEAR 提示詞架構，套用至「台灣高齡長照需求預測企劃書」，體驗 AI 智能體在不同產業維度的無縫遷移能力！")

    # Section 9: FAQ
    doc.add_heading("九、 經理人避坑指南與常見問題排解 (FAQ)", level=2)
    faqs = [
        ("Q1：為什麼我按 Delete 刪除封面的頁碼，結果整份報告 20 頁的頁碼全部消失了？",
         "A1：這是因為你沒有取消「連結到前一節 (Link to Previous)」！請先在封面與正文之間插入「分節符號（下一頁）」，然後滑鼠雙擊進入正文頁尾，在上方工具列點擊將「連結到前一節」關閉，之後再去刪除封面頁碼，正文頁碼就會完好無損。"),
        ("Q2：修改了章節文字或增減了內容後，目錄上的頁碼怎麼還是舊的？",
         "A2：Word 的目錄是功能變數 (Field)，不會即時自動跳轉。請養成習慣：按 Ctrl + A 全選整篇文件，接著按鍵盤【F9】，在跳出的對話框選擇「更新整個目錄」，所有章節與頁碼就會秒級校準！"),
        ("Q3：在 Google Docs 網頁版編輯，也能看到像 Word 一樣的左側分頁導航嗎？",
         "A3：可以！只要你在文中套用「標題 1 (Heading 1)」與「標題 2 (Heading 2)」，Google Docs 左側工具列點擊「文件大綱 (Outline)」或「分頁 (Tabs)」圖示，系統就會自動展開層次分明的章節目錄，點擊任一項目即可瞬間跳轉！"),
        ("Q4：今天上課練習的檔案，下課後會不會被電腦教室還原卡清除？",
         "A4：電腦重開機後本機 C 槽確實會自動還原。請務必將完成的 Word 檔案上傳至個人的 Google 雲端硬碟，或存放在 Google Cloud Shell 的 $HOME 永續空間。本練習為課堂實機演練，零隨堂作業負擔，檔案留存作為期中與期末成果的最佳素材！")
    ]
    for q, a in faqs:
        p_q = doc.add_paragraph()
        p_q.paragraph_format.space_before = Pt(4)
        p_q.paragraph_format.space_after = Pt(2)
        r_q = p_q.add_run(q)
        r_q.bold = True
        r_q.font.size = Pt(10)
        r_q.font.color.rgb = RGBColor(30, 58, 138)
        
        p_a = doc.add_paragraph()
        p_a.paragraph_format.space_before = Pt(0)
        p_a.paragraph_format.space_after = Pt(4)
        r_a = p_a.add_run(a)
        r_a.font.size = Pt(9.5)
        r_a.font.color.rgb = RGBColor(51, 65, 85)

    # -------------------------------------------------------------
    # TABS 4 TO 18 (PREVIEW OUTLINES)
    # -------------------------------------------------------------
    future_weeks = [
        (4, "Word 長篇營運報告樣式與多層次清單自動化", "多階層清單編號、樣式集統一管理、章節交叉參照與圖表目錄。"),
        (5, "商務表格視覺化與 APA 三線表排版實務", "高質感三線表原則、欄寬按字元自動最適化、跨頁標題列重複。"),
        (6, "Word 高效合併列印與大量套印名冊自動化", "主文件與 Excel 資料來源連結、功能變數篩選與跳過條件、個別文件分派。"),
        (7, "Excel 商業數據清洗與門市銷售整理實務", "資料清理函數 TRIM/CLEAN、文字分欄、閃電填入與重複值篩除。"),
        (8, "Excel 多條件統計與門市業績加總計算實務", "SUMIFS、COUNTIFS、AVERAGEIFS 函數多維度加總運算與公式防呆。"),
        (9, "期中專案報告標準範本與撰寫實務指南", "商業實務個案整合、Word 與 Excel 成果彙整、期中書面報告封裝。"),
        (10, "Excel 現代查表函數 XLOOKUP 跨表比對實務", "XLOOKUP 精準比對、雙向查詢、找不到值時防呆預設與批次套用。"),
        (11, "Excel 樞紐分析表與動態交叉分析篩選器", "多維度樞紐分析、值欄位計算方式、群組化日期與視覺化切片器。"),
        (12, "Excel 商業智慧圖表與視覺化儀表板設計", "組合圖表、次要座標軸、動態迷你圖與高階主管 KPI 儀表板。"),
        (13, "PowerPoint 商務簡報母片架構與版型設計", "投影片母片階層管理、自訂版面配置、色彩計畫與字型全域綁定。"),
        (14, "PowerPoint 資訊圖表化與高說服力商業排版", "SmartArt 商業流程轉化、視覺引導線條、高衝擊力商業數據呈現。"),
        (15, "PowerPoint 商業簡報動態轉場與演說節奏", "轉化 (Morph) 動畫應用、章節縮放摘要、簡報者檢視畫面與講稿節奏。"),
        (16, "跨軟體整合：Word + Excel + PPT 商業報告產出", "Excel 圖表動態連結至 Word/PPT、來源資料變更一鍵更新。"),
        (17, "Agentic AI 自動化辦公與專案成果雲端封裝", "多智能體協同流水線、專案成果一鍵封裝與 GitHub 靜態展示。"),
        (18, "期末實務專案成果展示與綜合評量", "個人商業數位資產成果匯報、全學期成長反思與就業實務對齊。")
    ]

    for w_num, w_title, w_desc in future_weeks:
        h = doc.add_heading(f"📑 第 {w_num:02d} 週：{w_title}", level=1)
        h.style.font.color.rgb = RGBColor(71, 85, 105)
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(6)
        r = p.add_run(f"【核心內容預告】：{w_desc}\n（後續週次實作手冊將隨課程進度逐步解鎖開放，敬請期待！）")
        r.font.size = Pt(9.5)
        r.font.color.rgb = RGBColor(148, 163, 184)

    # Save destinations
    out_docx_1 = os.path.join(downloads_dir, "Week03_Vibe_Coding_Word商業企劃書_GoogleDocs操作手冊.docx")
    out_docx_2 = os.path.join(base_dir, "Vibe_Coding_Google_Doc操作手冊.docx")
    
    doc.save(out_docx_1)
    doc.save(out_docx_2)
    print(f"Generated: {out_docx_1} ({os.path.getsize(out_docx_1):,} bytes)")
    print(f"Generated: {out_docx_2} ({os.path.getsize(out_docx_2):,} bytes)")

if __name__ == "__main__":
    build_manual()
