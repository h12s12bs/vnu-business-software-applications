# -*- coding: utf-8 -*-
"""
Generate Week 03 Practice Material ZIP package:
downloads/Week03_商業企劃書實作素材包.zip
Containing:
1. 01_原始未排版草案_鼎新商業企劃_智慧零售新事業.docx
2. 02_財務預算明細_CAPEX與OPEX採購估算表.xlsx
3. 03_示範標準範本_標準商業企劃書排版規範.docx
4. 04_README_第三週實作指引與CLEAR提示詞.txt
"""
import os
import zipfile
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

base_dir = r"g:\我的雲端硬碟\萬能科技大學\備課\11501課表\11501商業軟體應用"
downloads_dir = os.path.join(base_dir, "downloads")
os.makedirs(downloads_dir, exist_ok=True)

temp_dir = os.path.join(downloads_dir, "temp_w03_pack")
os.makedirs(temp_dir, exist_ok=True)

# 1. 01_原始未排版草案_鼎新商業企劃_智慧零售新事業.docx
doc_draft = docx.Document()
p0 = doc_draft.add_paragraph("鼎新商業企劃案_校園智慧零售新事業草案(未排版初稿)")
p0.runs[0].font.size = Pt(14)
p0.runs[0].font.bold = True

texts = [
    "撰寫小組：智慧校園營運小組  日期：2026年3月",
    "【專案緣起與構想】\n隨著大專院校學生與教職員對健康意識的抬頭，傳統校園周邊油膩、高鈉、缺乏蔬菜的外食生態已無法滿足現代消費需求。本專案擬於北區主要大學城設立新型態「低卡健康快煮餐盒」門市，結合手機 App 預先點餐、自動化快煮出餐設備，將平均取餐時間由 12 分鐘壓縮至 90 秒內。本企劃預估於營運第 8 個月達成損益平衡點，第一年預計服務超過 120,000 人次，創造新台幣 1,500 萬元營業額。",
    "【市場痛點分析】\n根據 2025 年校園飲食滿意度問卷調查（回收有效樣本 1,200 份），歸納出三大關鍵痛點：\n1. 尖峰排隊過長：中午 12:00-12:40 尖峰時段，學餐平均排隊超過 15 分鐘，嚴重壓縮學生午休時間。\n2. 營養失衡與高熱量：市售便當平均熱量高達 850-1,000 大卡，缺乏足量優質蛋白質與原型蔬菜。\n3. 客製化程度低：無法針對個人健身、減脂需求彈性替換澱粉或調整主食份量。",
    "【商業模式與核心特色】\n結合智慧冷鏈儲藏、自動蒸煮機與專屬點餐 App。學生於下課前 10 分鐘手機下單，到達門市掃描 QR Code 即可於保溫取餐櫃 10 秒取餐。提供高蛋白雞胸餐盒、低GI藜麥舒肥魚餐盒與全素高纖蔬食餐盒等多元組合。",
    "【初步預算評估】\n初期門市智慧終端與 POS 系統 120,000 元，節能展示櫃改造 250,000 元，行銷宣傳 60,000 元，初次物料備貨 150,000 元。資本支出與營運費用總計約 580,000 元。",
    "【待辦事項】\n1. 請依據公文標準版面（上下左右各 2.54cm）重新配置版面。\n2. 封面與正文需設定分節符號並斷開頁首頁尾連結。\n3. 使用 AI 提煉 350 字正式執行摘要並套用樣式結構。\n4. 整理出標準三線財務預算表格。"
]

for t in texts:
    p = doc_draft.add_paragraph(t)
    p.paragraph_format.line_spacing = 1.0
    p.paragraph_format.space_after = Pt(4)

draft_path = os.path.join(temp_dir, "01_原始未排版草案_鼎新商業企劃_智慧零售新事業.docx")
doc_draft.save(draft_path)

# 2. 02_財務預算明細_CAPEX與OPEX採購估算表.xlsx
wb = openpyxl.Workbook()
ws = wb.active
ws.title = "專案財務預算明細表"

# Header Title
ws.merge_cells("A1:E1")
ws["A1"] = "鼎新校園智慧零售新事業專案 ── 資本支出(CAPEX)與營運費用(OPEX)明細表"
ws["A1"].font = Font(name="微軟正黑體", size=14, bold=True, color="FFFFFF")
ws["A1"].fill = PatternFill(start_color="1E3A8A", end_color="1E3A8A", fill_type="solid")
ws["A1"].alignment = Alignment(horizontal="center", vertical="center")
ws.row_dimensions[1].height = 36

headers = ["編號", "費用類別", "預算項目具體說明", "預估金額 (NT$)", "備註與核銷規範"]
for col_idx, h in enumerate(headers, 1):
    cell = ws.cell(row=2, column=col_idx, value=h)
    cell.font = Font(name="微軟正黑體", size=11, bold=True, color="1E3A8A")
    cell.fill = PatternFill(start_color="DBEAFE", end_color="DBEAFE", fill_type="solid")
    cell.alignment = Alignment(horizontal="center", vertical="center")
ws.row_dimensions[2].height = 26

budget_data = [
    [1, "資本支出 (CAPEX)", "門市智慧取餐終端與雙螢幕 POS 主機", 120000, "含三年原廠保固與到府維修"],
    [2, "資本支出 (CAPEX)", "門市節能環保智能溫控展示櫃改造", 250000, "符合綠建築一級節能標章"],
    [3, "資本支出 (CAPEX)", "快煮廚房自動蒸煮機與冷鏈保鮮設備", 430000, "通過 SGS 食品級安全認證"],
    [4, "營業費用 (OPEX)", "首季校園數位社群精準廣告宣傳", 60000, "鎖定校園周邊 3 公里受眾"],
    [5, "營業費用 (OPEX)", "初次原物料備貨與營運週轉預備金", 150000, "維持 45 天安全庫存水位"],
    [6, "營業費用 (OPEX)", "雲端點餐系統 SaaS 平台年費及金流手續費", 35000, "支援 LINE Pay 與悠遊卡支付"]
]

thin_border = Border(
    left=Side(style='thin', color='CBD5E1'),
    right=Side(style='thin', color='CBD5E1'),
    top=Side(style='thin', color='CBD5E1'),
    bottom=Side(style='thin', color='CBD5E1')
)

for row_idx, r_data in enumerate(budget_data, 3):
    ws.row_dimensions[row_idx].height = 22
    for col_idx, val in enumerate(r_data, 1):
        cell = ws.cell(row=row_idx, column=col_idx, value=val)
        cell.font = Font(name="微軟正黑體", size=10)
        cell.border = thin_border
        if col_idx == 1:
            cell.alignment = Alignment(horizontal="center", vertical="center")
        elif col_idx == 4:
            cell.alignment = Alignment(horizontal="right", vertical="center")
            cell.number_format = "#,##0"
        elif col_idx == 2:
            cell.alignment = Alignment(horizontal="center", vertical="center")
        else:
            cell.alignment = Alignment(horizontal="left", vertical="center")

# Total Row
tot_row = 9
ws.row_dimensions[tot_row].height = 26
ws.cell(row=tot_row, column=1, value="")
ws.cell(row=tot_row, column=2, value="總計 (Total)")
ws.cell(row=tot_row, column=2).font = Font(name="微軟正黑體", size=11, bold=True, color="1E3A8A")
ws.cell(row=tot_row, column=2).alignment = Alignment(horizontal="center", vertical="center")
ws.cell(row=tot_row, column=3, value="CAPEX ＋ OPEX 合計預算金額")
ws.cell(row=tot_row, column=3).font = Font(name="微軟正黑體", size=10, italic=True)
ws.cell(row=tot_row, column=4, value="=SUM(D3:D8)")
ws.cell(row=tot_row, column=4).font = Font(name="微軟正黑體", size=11, bold=True, color="B91C1C")
ws.cell(row=tot_row, column=4).number_format = "$#,##0"
ws.cell(row=tot_row, column=4).alignment = Alignment(horizontal="right", vertical="center")
ws.cell(row=tot_row, column=5, value="首年種子營運資金編列無誤")
ws.cell(row=tot_row, column=5).font = Font(name="微軟正黑體", size=10)

for c in range(1, 6):
    ws.cell(row=tot_row, column=c).border = thin_border
    ws.cell(row=tot_row, column=c).fill = PatternFill(start_color="FEF3C7", end_color="FEF3C7", fill_type="solid")

ws.column_dimensions['A'].width = 8
ws.column_dimensions['B'].width = 20
ws.column_dimensions['C'].width = 38
ws.column_dimensions['D'].width = 18
ws.column_dimensions['E'].width = 30

xlsx_path = os.path.join(temp_dir, "02_財務預算明細_CAPEX與OPEX採購估算表.xlsx")
wb.save(xlsx_path)

# 3. 03_示範標準範本_標準商業企劃書排版規範.docx (Copy from existing or create)
existing_demo = os.path.join(base_dir, "downloads", "Week03_商業企劃書標準架構與起草練習.docx")
demo_path = os.path.join(temp_dir, "03_示範標準範本_標準商業企劃書排版規範.docx")
if os.path.exists(existing_demo):
    import shutil
    shutil.copy2(existing_demo, demo_path)

# 4. 04_README_第三週實作指引與CLEAR提示詞.txt
readme_text = """========================================================================
萬能科技大學 企業管理系 11501《商業軟體應用》
第 03 週 實作素材包指引：Word 商業企劃書標準結構與 AI 輔助起草實務
授課教師：邱俊維 博士 ｜ 地點：J501 企業經營模擬室
========================================================================

【本包包含 4 份核心實作素材】：
1. 01_原始未排版草案_鼎新商業企劃_智慧零售新事業.docx
   -> 混亂草稿，字型不一、無邊界設定、無分節符號。學生將引導 AI 將其重構為國際級商務企劃書！
2. 02_財務預算明細_CAPEX與OPEX採購估算表.xlsx
   -> 資本支出 (CAPEX) 與營業費用 (OPEX) 明細表，提供給 AI 進行標準三線表格排版。
3. 03_示範標準範本_標準商業企劃書排版規範.docx
   -> 完成品對照標準範本，包含 2.54cm 邊界、分節符號、執行摘要與三線表格。
4. 04_README_第三週實作指引與CLEAR提示詞.txt
   -> 本說明文件。

【第三週 5 大實作關卡快速導航】：
[關卡一]：版面標準 2.54cm 與微軟正黑體 12pt、行距 1.25 倍配置。
[關卡二]：封面插入分節符號「下一頁」，進入頁首頁尾取消「連結到前一節」，正文頁碼自第 1 頁起算。
[關卡三]：複製 CLEAR 提示詞，指令 AI 起草「350 字執行摘要」與五大黃金結構。
[關卡四]：將財務預算重構為 APA 頂級「三線表格」（去除直框線，保留上下粗線與欄頭細線）。
[關卡五]：全選按 F9 刷新功能變數，自動插入層次目錄並存檔雲端！

【學習保證】：
100% 零作業負擔！課堂練習成果直接存入個人 Google 雲端硬碟，期中期末報告現成可用！
"""
readme_path = os.path.join(temp_dir, "04_README_第三週實作指引與CLEAR提示詞.txt")
with open(readme_path, "w", encoding="utf-8") as f:
    f.write(readme_text)

# Pack into ZIP
zip_filename = os.path.join(downloads_dir, "Week03_商業企劃書實作素材包.zip")
with zipfile.ZipFile(zip_filename, "w", zipfile.ZIP_DEFLATED) as zf:
    for f in os.listdir(temp_dir):
        fp = os.path.join(temp_dir, f)
        zf.write(fp, arcname=f)

print(f"Successfully generated: {zip_filename} ({os.path.getsize(zip_filename):,} bytes)")

# Clean temp dir
import shutil
shutil.rmtree(temp_dir)
