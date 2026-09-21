# -*- coding: utf-8 -*-
"""
Generate professorial-grade Week 02 Practice Manual (.docx)
Matching the 0910 Vibe Coding Workshop Manual pedagogy:
- Step-by-step clear guidance
- Prominent copyable Prompt boxes right alongside each step
- 100% Zero-typing workflow using Antigravity Desktop / Google AI Studio
- Automated Git Push instruction without manual Add File
- Full connection to Word ATS Resume, Excel Long-Term Care BI, and Web Dashboard
"""
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

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
    cell.width = Inches(6.5)
    set_cell_background(cell, "F8FAFC")
    set_cell_margins(cell, top=160, bottom=160, left=200, right=200)
    
    # Border styling (Navy left border 4.5pt, gray top/right/bottom 1pt)
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
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(4)
    run_badge = p.add_run(f"📋 【可直接複製之 Prompt 指令】 ｜ 🎭 設定角色：{role_title}\n")
    run_badge.bold = True
    run_badge.font.size = Pt(11)
    run_badge.font.color.rgb = RGBColor(2, 132, 199)
    
    run_text = p.add_run(prompt_text)
    run_text.font.size = Pt(10)
    run_text.font.name = "Consolas"
    run_text.font.color.rgb = RGBColor(15, 23, 42)
    
    if tip_text:
        p2 = cell.add_paragraph()
        p2.paragraph_format.space_before = Pt(6)
        p2.paragraph_format.space_after = Pt(0)
        run_tip = p2.add_run(f"💡 經理人操作要領：{tip_text}")
        run_tip.font.size = Pt(9.5)
        run_tip.font.italic = True
        run_tip.font.color.rgb = RGBColor(180, 83, 9)

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

def build_docx():
    doc = Document()
    
    # Page Margins (Standard 2.54 cm = 1 inch)
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        
    # Document Title Header
    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_after = Pt(2)
    r_uni = p_title.add_run("萬能科技大學 企業管理系 11501 學期《商業軟體應用》\n")
    r_uni.font.size = Pt(12)
    r_uni.font.color.rgb = RGBColor(100, 116, 139)
    
    r_main = p_title.add_run("第 02 週 Vibe Coding ✕ Agentic AI 課堂實作逐步操作手冊")
    r_main.font.size = Pt(18)
    r_main.bold = True
    r_main.font.color.rgb = RGBColor(30, 58, 138)
    
    p_sub = doc.add_paragraph()
    p_sub.paragraph_format.space_after = Pt(12)
    r_sub = p_sub.add_run("【核心理念】：零手打！你就是專案總監，動口動腦下 Prompt，叫 Agentic AI 全自動執行！\n授課教師：邱俊維 博士 ｜ 授課地點：J501 電腦教室 ｜ 上課時間：每週一 20:10~21:40")
    r_sub.font.size = Pt(10.5)
    r_sub.font.color.rgb = RGBColor(71, 85, 105)

    # Info Notice Box (No Homework / No Exam)
    t_info = doc.add_table(rows=1, cols=1)
    c_info = t_info.cell(0, 0)
    c_info.width = Inches(6.5)
    set_cell_background(c_info, "ECFDF5")
    set_cell_margins(c_info, 120, 120, 160, 160)
    p_inf = c_info.paragraphs[0]
    p_inf.paragraph_format.space_after = Pt(0)
    r_inf = p_inf.add_run("🎓 課堂學習承諾與免作業宣告：\n"
                          "1. 【免作業負擔】：本課程採課堂實務演練導向，今晚無課後作業繳交負擔、無上機小考測驗壓力。\n"
                          "2. 【學期評量準則】：平時出席率 30% ＋ 期中專案報告 30% ＋ 期末整合成果 40%。\n"
                          "3. 【成果即資產】：今晚完成的 GitHub 倉儲與會議記錄，自動作為第 09 週期中書面報告現成素材！")
    r_inf.font.size = Pt(9.5)
    r_inf.font.color.rgb = RGBColor(6, 95, 70)
    doc.add_paragraph().paragraph_format.space_after = Pt(10)

    # Section 1: Tool Setup
    h1 = doc.add_heading("一、 電腦教室雙軌工具開啟（免安裝、抗崩潰）", level=1)
    p1 = doc.add_paragraph("電腦教室設有還原機制，每週重開機檔案會重置。為避免連線壅塞，今晚提供兩種最簡便的 AI 協作工具：")
    
    t_tools = doc.add_table(rows=3, cols=3)
    t_tools.style = 'Table Grid'
    headers = ["協作工具", "開啟方式", "適合情境與優勢"]
    for i, h in enumerate(headers):
        cell = t_tools.cell(0, i)
        cell.text = h
        set_cell_background(cell, "1E3A8A")
        p = cell.paragraphs[0]
        p.runs[0].font.color.rgb = RGBColor(255, 255, 255)
        p.runs[0].bold = True
        p.runs[0].font.size = Pt(10)

    tool_data = [
        ("軌道 A：Antigravity 桌面版 (極力推薦)", "開啟電腦桌面上的「Antigravity」軟體，直接進入對話視窗", "具備本機檔案管理權限，可直接下指令叫 AI 自動存檔並執行 Git Push，學生完全不用自己打指令！"),
        ("軌道 B：Google AI Studio / Gemini 網頁版", "在 Chrome 開啟 aistudio.google.com 或 gemini.google.com，以個人 Google 帳號登入", "純網頁免安裝、免金鑰、絕不塞車！適合直接對話取得高品質 Markdown 文案。")
    ]
    for r_idx, (col1, col2, col3) in enumerate(tool_data, start=1):
        t_tools.cell(r_idx, 0).text = col1
        t_tools.cell(r_idx, 1).text = col2
        t_tools.cell(r_idx, 2).text = col3
        for c in range(3):
            set_cell_margins(t_tools.cell(r_idx, c), 100, 100, 120, 120)
            t_tools.cell(r_idx, c).paragraphs[0].runs[0].font.size = Pt(9.5)
            
    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # Section 2: Mission 1
    doc.add_heading("二、 實作關卡一：調度 AI 自動建立企業四層樹與 README 首頁 (15 分鐘)", level=1)
    p_m1 = doc.add_paragraph()
    p_m1.add_run("【任務目標】：").bold = True
    p_m1.add_run("徹底告別手工建立資料夾！指揮 AI 規劃標準四層治理樹 (00_Admin ~ 03_Deliverables) 與 README.md 導覽手冊。\n")
    p_m1.add_run("【一步一步帶你做 SOP】：\n").bold = True
    p_m1.add_run("• 步驟 1：開啟 Antigravity 桌面版（或 Google AI Studio 網頁版）。\n"
                 "• 步驟 2：複製下方【任務一 Prompt】，貼入對話框按下 Enter 送出。\n"
                 "• 步驟 3：觀測 AI 秒速產出包含專案簡介、四層資料夾與 ISO 8601 規範之 README.md 全文。\n"
                 "• 步驟 4：若使用 Antigravity 桌面版，可直接加一句：『請將上述內容自動存為本專案的 README.md 檔案』，AI 自動在背景建好！")
    
    prompt_m1 = (
        "【角色設定】：你是一位頂級企業數位資產架構師與知識管理總監。\n"
        "【背景情境】：我們是萬能科大企業管理系「商業軟體應用」專案團隊，正在建立標準化企業數位倉儲（專案名稱：vnu-business-docs）。\n"
        "【約束限制】：\n"
        "1. 建立標準四層樹狀資料夾治理架構，目錄代碼為：\n"
        "   - 00_Admin（專案章程、權限名冊、行政規章）\n"
        "   - 01_Raw_Data（未經加工的外部原始資料、市場調研報表）\n"
        "   - 02_Working_Drafts（進行中的企劃草案、Word 底稿、數據分析過程）\n"
        "   - 03_Deliverables（經總監簽核的最終交付報告、發布檔）\n"
        "2. 產出一份專業的 README.md 導航首頁，包含專案簡介、四層目錄結構說明、ISO 8601 命名規範與團隊維護清單。\n"
        "3. 語法必須完全符合 GitHub Markdown 規範。\n"
        "【核心任務】：請為我起草產出完整的 README.md 原始內容，供我直接作為專案首頁！"
    )
    create_prompt_box(doc, "企業資深數位資產架構師", prompt_m1, "零手工敲指令！由 AI 代理人自動規劃企業級架構並建立首頁。")

    # Section 3: Mission 2
    doc.add_heading("三、 實作關卡二：指令 AI 自動生成標準公文與四欄對齊決策表格 (15 分鐘)", level=1)
    p_m2 = doc.add_paragraph()
    p_m2.add_run("【任務目標】：").bold = True
    p_m2.add_run("告別手工畫表格與計算欄位冒號！指令 AI 自動生成 Markdown 商業公文、主管引用框、金額強制靠右表格與待辦核選清單。\n")
    p_m2.add_run("【一步一步帶你做 SOP】：\n").bold = True
    p_m2.add_run("• 步驟 1：複製下方【任務二 Prompt】。\n"
                 "• 步驟 2：貼入 AI 對話框送出，觀察 AI 在 3 秒內自主計算冒號位置（|:---:| 置中、|---:| 靠右對齊）。\n"
                 "• 步驟 3：檢查產出的四欄表格（分區、門市數、報廢率改善、預估月效益），金額欄位是否已靠右對齊！")
    
    prompt_m2 = (
        "【角色設定】：你是一位擁有 10 年跨國零售與商務管理經驗的總經理特助。\n"
        "【背景情境】：公司正在推動「全台門市智慧數位轉型與 POS 系統升級專案」，需向董事會呈報標準公文與營運效益分析。\n"
        "【約束限制】：\n"
        "1. 產出標準 Markdown 商業公文：包含一級標題、二級案由、高階主管核示引用框 (>)。\n"
        "2. 繪製一張四欄營運數據分析表（分區、門市數、鮮食報廢率改善、預估月效益/預算），數值與金額欄位強制靠右對齊 (|---:|)。\n"
        "3. 條列 3 項具體行動對策，使用帶有負責人與截止日期的 Markdown 核選清單 (- [ ])。\n"
        "4. 格式嚴謹工整，杜絕口語冗詞。\n"
        "【核心任務】：請產出符合上述規格的完整 Markdown 公文草案！"
    )
    create_prompt_box(doc, "總經理室資深特助 兼 商業營運分析師", prompt_m2, "完全不用手工對齊，AI 自動精確設定 |---:| 靠右語法。")

    # Section 4: Mission 3 (Raw Transcript + Master CLEAR)
    doc.add_heading("四、 實作關卡三：真實會議逐字稿 ✕ AI 自主結構化淬鍊 (20 分鐘)", level=1)
    p_m3 = doc.add_paragraph()
    p_m3.add_run("【任務目標】：").bold = True
    p_m3.add_run("模擬真實跨部門高階例會！將充滿閒談、發散提問與零碎數字的口語逐字稿，交給 AI 5 秒鐘淬鍊為 ISO 級正式決議公文。\n")
    p_m3.add_run("【一步一步帶你做 SOP】：\n").bold = True
    p_m3.add_run("• 步驟 1：複製下方【真實會議錄音速記文本】。\n"
                 "• 步驟 2：複製下方【任務三 Master CLEAR 提示詞】，將逐字稿接在下方，一起貼入 AI 對話框送出！\n"
                 "• 步驟 3：觀測 AI 代理人自主執行四部曲：\n"
                 "   ① 自動過濾口語閒聊廢話\n"
                 "   ② 自動計算 18 家門市 × 85,000 元 = 153 萬元硬體總預算\n"
                 "   ③ 自動繪製 4 欄對齊營運分析表格\n"
                 "   ④ 自動條列明確分派負責人（Susan、Kevin、Linda）的待辦清單！")

    # Box for raw transcript
    t_raw = doc.add_table(rows=1, cols=1)
    c_raw = t_raw.cell(0, 0)
    c_raw.width = Inches(6.5)
    set_cell_background(c_raw, "FEF3C7")
    set_cell_margins(c_raw, 140, 140, 180, 180)
    p_raw = c_raw.paragraphs[0]
    p_raw.paragraph_format.space_after = Pt(0)
    p_raw.add_run("🎙️ 【真實企業跨部門例會現場錄音逐字稿（請複製此段）】：\n").bold = True
    p_raw.runs[0].font.color.rgb = RGBColor(146, 64, 14)
    raw_text = (
        "【會議時間】：2026年9月21日 晚間例會\n"
        "【出席人員】：總經理 David、營運部經理 Susan、資訊部經理 Kevin、財務部經理 Linda\n"
        "【會議原始錄音速記】：\n"
        "David（總經理）：「大家晚安。今天主要討論我們全台18家門市導入智慧零售POS系統的事情。Susan，你們營運部上個月鮮食報廢率到底降下來沒有？」\n"
        "Susan（營運部）：「報告總經理，目前我們北區6家門市試辦電子標籤和即期品動態折扣，報廢率從上季的 8.2% 降到了 5.1%，光是鮮食一個月就省下 42 萬台幣！但是中區和南區門市還在用手動貼貼紙，報廢率還是高達 7.9%。」\n"
        "David：「好，那這件事不能拖。Susan，妳在10月15號前，把中南區12家門市的電子標籤導入計畫和教育訓練時程排出來。Kevin，系統連線問題解決了嗎？」\n"
        "Kevin（資訊部）：「資訊部這邊報告，新版雲端 POS 和庫存系統已經完成壓力測試。但是硬體採購需要追加預算，18家門市升級掃描槍和雙螢幕主機，每家門市報價是 85,000 元，總共需要 153 萬元。另外還有雲端伺服器每個月租金 35,000 元。」\n"
        "Linda（財務部）：「我打個岔，財務部已經審核過這筆預算。153萬硬體採購可以動用第三季資本支出，但伺服器月租必須控制在年度 IT 運營預算內。另外，供應商合約必須加入 SLA 99.9% 正常運作保證，否則延遲上線每天要罰款千分之二。」\n"
        "David：「很好，大家聽清楚。第一，資訊部 Kevin 在本週五（9/25）前把採購合約修改好送法務和 Linda 審核。第二，營運部 Susan 負責門市店長培訓。第三，全案目標在11月1日全台18家門市正式上線。請大家按照 ISO 規範，把這份會議記錄整理成正式 Markdown 專案企劃底稿，存入雲端儲存庫。」"
    )
    r_rt = p_raw.add_run(raw_text)
    r_rt.font.size = Pt(9.5)
    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    prompt_m3 = (
        "【角色設定】：你是一位具備 10 年高階行政管理經驗的總經理特助 兼 企業數位流程架構師。\n"
        "【背景情境】：公司剛召開完第 4 季門市智慧零售升級專案例會，現場口語對話零碎雜亂。\n"
        "【約束限制】：\n"
        "1. 嚴格使用繁體中文（台灣商務專業語氣），格式工整清爽。\n"
        "2. 絕不捏造未提及的數據；涉及金額與時程必須 100% 精準計算。\n"
        "3. 輸出需包含：\n"
        "   (a) 正式會議基本資訊與案由\n"
        "   (b) 門市營運分析四欄表格（分區、門市數、報廢率改善、採購預算/效益，金額欄位強制靠右對齊 |---:|）\n"
        "   (c) 具備負責人與明確截止日期的 Markdown 待辦核選清單 (- [ ])。\n"
        "【核心任務】：請將以上提供的會議錄音逐字稿整理為符合 ISO 規範之正式 Markdown 會議決議底稿！"
    )
    create_prompt_box(doc, "高階行政特助 兼 數位流程架構師", prompt_m3, "原本要加班 2 小時整理的雜亂速記，AI 代理人 5 秒鐘自主產出符合 ISO 規範的公文！")

    # Section 5: Mission 4 (Self-correction & One-click Git push)
    doc.add_heading("五、 實作關卡四：專案總監 HITL 審核 ✕ 指令自我修復 ✕ 一句話自動 Git Push (10 分鐘)", level=1)
    p_m4 = doc.add_paragraph()
    p_m4.add_run("【任務目標】：").bold = True
    p_m4.add_run("學生扮演專案總監查核數據，發現小瑕疵【絕不手動改】，動口下指令叫 AI 自我修正，並直接指令 Antigravity 自動建檔並 Git Push 推上 GitHub 雲端！\n")
    p_m4.add_run("【一步一步帶你做 SOP】：\n").bold = True
    p_m4.add_run("• 步驟 1：總監數據把關（核對 153 萬硬體總額、SLA 99.9% 罰則與 11/1 上線目標）。\n"
                 "• 步驟 2：複製下方【自我修復 ＋ 自動 Git Push Prompt】，貼給 Antigravity 桌面版。\n"
                 "• 步驟 3：觀測 Antigravity 終端機自主執行：自動建立 `03_Deliverables/` 資料夾 ➔ 寫入修復後檔案 ➔ 自動執行 `git add`, `git commit` 與 `git push`！\n"
                 "• 步驟 4：打開手機或瀏覽器造訪個人的 GitHub 倉儲，刷新頁面，親眼見證成果已安全永久保存在全球雲端！")

    prompt_m4 = (
        "【角色設定】：你是一位資深專案總監與敏捷教練。\n"
        "【背景情境】：剛才由你起草的「門市數位轉型會議記錄」初稿已完成，現在進行專案總監複審 (Human-in-the-Loop)。\n"
        "【修復需求】：\n"
        "1. 營運表格中，請將第二欄「門市數」由原本靠左改為「置中對齊 (|:---:|)」。\n"
        "2. 在財務部 Linda 的決議後面，強調「供應商若延遲上線，每日處以合約總額千分之二罰款之 SLA 條款」。\n"
        "3. 在待辦清單中，將資訊部 Kevin 的合約修正任務標註【優先級：最高 (Urgent)】。\n"
        "4. 在文末追加一節「期末延伸效益」，說明本專案將於第 11-12 週導入 Excel 儀表板、第 15 週串聯 PPT 簡報。\n"
        "【交付指令】：\n"
        "請依上述修改輸出完整內容，直接幫我存入本專案的「03_Deliverables/2026-09-21_門市數位轉型會議記錄_v1.0.md」，並自動執行 git add, git commit 與 git push 推送到 GitHub 雲端！"
    )
    create_prompt_box(doc, "智慧零售數位轉型專案總監", prompt_m4, "一句話叫 Antigravity 自動修復、自動存檔、自動 Git Push，學生完全不用自己打命令！")

    # Section 6: Mission 5 (Word ATS Resume Bonus)
    doc.add_heading("六、 實作彩蛋關卡：調度 AI 起草個人專屬【高階商務 ATS 履歷】並一鍵貼入 Word (15 分鐘)", level=1)
    p_m5 = doc.add_paragraph()
    p_m5.add_run("【任務目標】：").bold = True
    p_m5.add_run("這是進修部企管系同學最實戰的超值資產！調度 AI 扮演頂級外商獵頭顧問，根據個人背景起草一份具備國際競爭力的「ATS 最佳化高階商務履歷」，並體驗一鍵貼入 Word 自動轉換為專業版面！\n")
    p_m5.add_run("【一步一步帶你做 SOP】：\n").bold = True
    p_m5.add_run("• 步驟 1：複製下方【ATS 履歷起草 Prompt】，將括號中的 [姓名] 與現職經歷替換為個人背景（或直接使用預設模擬內容）。\n"
                 "• 步驟 2：貼入 Antigravity 桌面版（或 Google AI Studio 網頁版）送出，5 秒鐘見證 AI 產出具備 STAR 原則與量化成果的高階履歷！\n"
                 "• 步驟 3：全選複製 AI 產出的 Markdown 內容，打開電腦上的 Microsoft Word 貼上，親眼見證標題樣式、職能清單與專案成就瞬間排版完成！\n"
                 "• 步驟 4：對 Antigravity 說：『請幫我存為 03_Deliverables/個人高階商務履歷_v1.0.md 並自動 push 到 GitHub！』下課手機打開隨時展示！")

    prompt_m5 = (
        "【角色設定】：你是一位擁有 15 年跨國高階獵頭經驗的資深顧問兼人資長。\n"
        "【背景情境】：我是萬能科技大學企業管理系（進修部）的學生，白天在職場工作，希望運用 AI 起草一份具備國際競爭力的「高階商務 ATS 最佳化專業履歷」。\n"
        "【個人背景資訊】：\n"
        "- 姓名：[請填寫個人姓名，如：王小明]\n"
        "- 學歷：萬能科技大學 企業管理系（進修學士班在學中，主修商業軟體應用、智慧決策、大數據分析）\n"
        "- 現職/經歷：[請填寫現職，如：連鎖零售門市副店長 / 行政採購專員 / 倉儲物流專員]\n"
        "- 核心職能：流程自動化、跨部門溝通、門市營運管理、成本控制、Office 辦公應用、AI 代理人協同\n"
        "【約束限制】：\n"
        "1. 嚴格使用 Markdown 語法排版，方便我一鍵複製貼入 Word 自動套用階層樣式。\n"
        "2. 經歷描述嚴格遵循【STAR 原則】（情境、任務、行動、結果），行動動詞需強烈有力（如：主導、優化、提升、節省）。\n"
        "3. 輸出包含：\n"
        "   (a) 核心專業個人簡介 (Executive Summary，150 字)\n"
        "   (b) 六大核心職能關鍵字標籤卡\n"
        "   (c) 工作經歷與量化成就（包含具體百分比與營收數據）\n"
        "   (d) 教育背景與專業證照（經濟部 iPAS「AI 應用規劃師」等）\n"
        "【核心任務】：請為我起草產出這份專業、具備高說服力的高階商務履歷！"
    )
    create_prompt_box(doc, "全球頂級獵頭顧問 兼 外商人資長 (CHRO)", prompt_m5, "複製貼入 Word 即可一秒擁有排版工整的外商級履歷，還能存於 GitHub 作為個人數位資產！")

    # Section 7: Semester Big Cases Preview (0910 connection)
    doc.add_heading("七、 學期後續大案藍圖：今晚基礎如何直通高階商業應用？", level=1)
    p_map = doc.add_paragraph("今晚學會的 Markdown 結構化思維與 CLEAR 提示詞框架，是全學期三大商業實戰大案的核心發動機：")

    t_map = doc.add_table(rows=4, cols=4)
    t_map.style = 'Table Grid'
    m_headers = ["學習階段", "核心工具", "對標 0910 研習精華案例", "期末產出資產"]
    for i, h in enumerate(m_headers):
        cell = t_map.cell(0, i)
        cell.text = h
        set_cell_background(cell, "0F172A")
        p = cell.paragraphs[0]
        p.runs[0].font.color.rgb = RGBColor(255, 255, 255)
        p.runs[0].bold = True
        p.runs[0].font.size = Pt(9.5)

    map_rows = [
        ("模組二 (第 3~6 週)", "Microsoft Word", "Word 操作履歷：調度 AI 起草個人專屬【ATS 最佳化高階商務履歷自傳】與標案企劃書", "高階職場履歷與標準公文排版"),
        ("模組三 (第 7~12 週)", "Microsoft Excel", "Excel ✕ AI 資料整理：清理【台灣長照高齡化真實開放數據】，使用 XLOOKUP 樞紐分析", "長照醫療營運多維交叉報表"),
        ("模組四與五 (第 13~18 週)", "PowerPoint ✕ Web", "簡報長照趨勢分析 ＆ 資料庫分析到儀表板：生成 10 頁麥肯錫簡報與單檔案【動態營運儀表板】", "高階決策簡報與互動儀表板 MVP")
    ]
    for r_idx, r_data in enumerate(map_rows, start=1):
        for c_idx, val in enumerate(r_data):
            cell = t_map.cell(r_idx, c_idx)
            cell.text = val
            set_cell_margins(cell, 100, 100, 120, 120)
            cell.paragraphs[0].runs[0].font.size = Pt(9)
            if c_idx == 2:
                cell.paragraphs[0].runs[0].bold = True
                cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(2, 132, 199)

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # Section 8: FAQ
    doc.add_heading("八、 課堂常見突發狀況排解指南 (FAQ)", level=1)
    faqs = [
        ("Q1：下課後電腦教室重開機，剛才做的檔案會不見嗎？",
         "A1：完全不會！因為剛才已經透過 Antigravity 自動 push 到全球 GitHub 雲端伺服器，檔案已永久安全留存。回家用手機或個人筆電登入 GitHub 即可隨時查看。"),
        ("Q2：如果 Antigravity 出現網路限制無法自動 push 怎麼辦？",
         "A2：完全不用慌張！請打開 GitHub 倉儲網頁，點選右上角『Add file』➔『Create new file』，檔名輸入『03_Deliverables/2026-09-21_會議記錄.md』，把 AI 產出的文字貼上，點綠色『Commit changes』，10 秒手動備援存檔！"),
        ("Q3：今晚需要把這個檔案交給老師打分數嗎？",
         "A3：不需要！本課程無每週作業負擔，只要課堂跟隨邱老師步驟做完、確認檔案已存在自己的 GitHub 倉儲，即達成今晚學習指標，期中專案報告時再進行成果展示即可！")
    ]
    for q, a in faqs:
        p_q = doc.add_paragraph()
        p_q.paragraph_format.space_after = Pt(2)
        r_q = p_q.add_run(q)
        r_q.bold = True
        r_q.font.size = Pt(10)
        r_q.font.color.rgb = RGBColor(30, 58, 138)
        
        p_a = doc.add_paragraph()
        p_a.paragraph_format.space_after = Pt(6)
        r_a = p_a.add_run(a)
        r_a.font.size = Pt(9.5)
        r_a.font.color.rgb = RGBColor(51, 65, 85)

    target_path = "downloads/Week02_商業檔案結構化與Markdown練習.docx"
    doc.save(target_path)
    print(f"Successfully generated high-grade manual: {target_path}")

if __name__ == "__main__":
    build_docx()
