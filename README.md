# スキャンフォルダ整理ツール

## 概要
売り手から受領した資料(PDF/画像)から各種台帳Excelを自動生成するツール

## 業務フロー
1. 売り手から資料受領 → 「スキャン（その他）」フォルダに格納
2. 本ツールで自動処理:
   - 決算書PDF → 財務概要Excel
   - 車検証画像 → 車両台帳Excel
   - 従業員名簿画像 → 従業員台帳Excel
3. 生成されたExcel + ホームページURL → IM生成

## フォルダ構造
```
A9XX_会社名/
├── スキャン（その他）/
│   ├── １決算書〇/          # 決算書PDF(複数年度)
│   ├── ２従業員名簿/         # 従業員名簿・履歴書(PDF/画像)
│   └── ６車検証〇/           # 車検証(画像)
├── 決算書打ち込み/
│   └── 財務概要_会社名.xlsx  # 自動生成
├── 従業員台帳/
│   └── 従業員一覧_会社名.xlsx # 自動生成
└── 車両台帳/
    └── 車両台帳_会社名.xlsx  # 自動生成
```

## 技術仕様

### 使用技術
- Python 3.12+
- Claude API (Sonnet 4.5): 文書解析・情報抽出
- openpyxl: Excel操作
- pandas: データ処理
- PyMuPDF (fitz): PDF処理
- Pillow: 画像処理

### 処理フロー

#### 1. 決算書処理
```
スキャン/１決算書〇/*.pdf
  ↓ Claude API (PDF → 構造化データ)
  ↓ 複数年度のPL/BS/科目データ抽出
  ↓ openpyxlでExcel書き込み
決算書打ち込み/財務概要_会社名.xlsx
```

#### 2. 車検証処理
```
スキャン/６車検証〇/*.jpg
  ↓ Claude API (画像 → 構造化データ)
  ↓ 各車両の登録情報抽出
  ↓ openpyxlでExcel書き込み
車両台帳/車両台帳_会社名.xlsx
```

#### 3. 従業員名簿処理
```
スキャン/２従業員名簿/*.jpg
  ↓ Claude API (画像 → 構造化データ)
  ↓ 従業員の基本情報・資格抽出
  ↓ openpyxlでExcel書き込み
従業員台帳/従業員一覧_会社名.xlsx
```

## エラーハンドリング
- ファイル読み込みエラー: スキップしてログ出力
- Claude API エラー: リトライ(最大3回)
- データ抽出失敗: 空行として出力し、手動修正を促す
- Excel書き込みエラー: 致命的エラーとして終了

## 使用方法

### 🌐 Webアプリ版（推奨）

社内メンバー全員が使えるWebアプリ版を提供しています。

**アクセス方法:**
1. ブラウザで https://share.streamlit.io/asahi-int/vehicle-processor-web にアクセス
2. パスワードを入力してログイン
3. 会社名を入力
4. 車検証ファイルをアップロード（複数可）
5. 「車両台帳を生成」ボタンをクリック
6. 生成されたExcelファイルをダウンロード

**対応フォーマット:** JPG, JPEG, PNG, PDF
**最大ファイルサイズ:** 50MB
**処理時間:** 1ファイルあたり約30秒

### ローカルでWebアプリを起動

```bash
# 依存パッケージをインストール
pip install -r requirements.txt

# .streamlit/secrets.toml にAPIキーとパスワードを設定
# （既に設定済みの場合はスキップ）

# Streamlitアプリを起動
streamlit run streamlit_app.py
```

ブラウザで http://localhost:8501 が自動的に開きます。

### 💻 CLI版（従来版）

CLI版は既存の企業フォルダ構造を前提とした処理を行います。

```bash
# 全自動モード
python -m document_processor --company A918_株式会社野木工業

# 個別処理
python -m document_processor --company A918_株式会社野木工業 --only financial
python -m document_processor --company A918_株式会社野木工業 --only vehicles
python -m document_processor --company A918_株式会社野木工業 --only employees
```
