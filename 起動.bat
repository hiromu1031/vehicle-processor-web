@echo off
chcp 65001 > nul
echo ========================================
echo 車検証処理ツールを起動しています...
echo ========================================
echo.

cd /d "%~dp0"

echo Streamlitを起動中...
echo.
echo ブラウザが自動的に開きます。
echo 開かない場合は、以下のURLにアクセスしてください：
echo http://localhost:8501
echo.
echo 終了するには、このウィンドウを閉じてください。
echo ========================================
echo.

streamlit run streamlit_app.py

pause
