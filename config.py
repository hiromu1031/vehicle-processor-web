"""
設定ファイル
"""
import os
from pathlib import Path

# Claude API設定
# Streamlit Secretsから取得を試み、フォールバックとして環境変数を使用
try:
    import streamlit as st
    ANTHROPIC_API_KEY = st.secrets.get("ANTHROPIC_API_KEY", os.getenv("ANTHROPIC_API_KEY"))
except ImportError:
    # Streamlitがインポートできない場合（CLI実行時）
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

if not ANTHROPIC_API_KEY:
    raise ValueError("環境変数 ANTHROPIC_API_KEY が設定されていません")

# モデル設定
CLAUDE_MODEL = "claude-sonnet-4-5-20250929"
MAX_TOKENS = 4096
TEMPERATURE = 0

# リトライ設定
MAX_RETRIES = 3
RETRY_DELAY = 2  # 秒

# フォルダ名設定
SCAN_FOLDER = "スキャン（その他）"
FINANCIAL_SCAN_FOLDER = "１決算書〇"
EMPLOYEE_SCAN_FOLDER = "２従業員名簿"
VEHICLE_SCAN_FOLDER = "６車検証〇"

FINANCIAL_OUTPUT_FOLDER = "決算書打ち込み"
EMPLOYEE_OUTPUT_FOLDER = "従業員台帳"
VEHICLE_OUTPUT_FOLDER = "車両台帳"

# Excelファイル名パターン
FINANCIAL_EXCEL_NAME = "財務概要_{company_name}.xlsx"
EMPLOYEE_EXCEL_NAME = "従業員一覧_{company_name}.xlsx"
VEHICLE_EXCEL_NAME = "車両台帳_{company_name}.xlsx"
