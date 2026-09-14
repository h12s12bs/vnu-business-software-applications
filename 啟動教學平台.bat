@echo off
chcp 65001 >nul
title 萬能科技大學 - 商業軟體應用 ✕ Agentic AI ✕ iPAS AI 應用規劃師 教學平台

echo ======================================================================
echo   萬能科技大學【商業軟體應用 ✕ Agentic AI ✕ iPAS 考證】教學平台
echo   授課教師：邱俊維 博士 (Dr. Chun-Wei Chiu)
echo   課程代碼：H0910004 ｜ 授課班級：進企管四系 1 甲 (J501 電腦教室)
echo ======================================================================
echo.

where python >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo [提醒] 本機尚未安裝 Python 環境。
    echo 您仍可直接點擊「平台首頁(單機離線直接點開).html」在瀏覽器離線運行全功能！
    pause
    exit /b 1
)

echo [1/2] 正在為您啟動教學伺服器與開啟瀏覽器...
start "" http://localhost:5000

echo [2/2] 伺服器啟動中，電腦教室學生連線網址即將顯示於下方：
echo.
python app.py

pause
