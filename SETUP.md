# セットアップガイド

## 1. 必要なパッケージのインストール

```bash
pip install anthropic pandas openpyxl
```

## 2. Claude API キーの設定

環境変数 `ANTHROPIC_API_KEY` を設定してください。

### Windows (PowerShell)
```powershell
$env:ANTHROPIC_API_KEY = "your-api-key-here"
```

### Windows (コマンドプロンプト)
```cmd
set ANTHROPIC_API_KEY=your-api-key-here
```

### 永続的な設定 (推奨)
システム環境変数として設定:
1. システムのプロパティ → 環境変数
2. ユーザー環境変数またはシステム環境変数に追加
3. 変数名: `ANTHROPIC_API_KEY`
4. 値: あなたのAPIキー

## 3. 使用方法

### 全自動モード (財務概要・車両台帳・従業員台帳を一括生成)
```bash
python -m document_processor.main --company A918_株式会社野木工業
```

### 個別処理モード

#### 車両台帳のみ生成
```bash
python -m document_processor.main --company A918_株式会社野木工業 --only vehicles
```

#### 従業員台帳のみ生成
```bash
python -m document_processor.main --company A918_株式会社野木工業 --only employees
```

#### 財務概要のみ生成
```bash
python -m document_processor.main --company A918_株式会社野木工業 --only financial
```

## 4. フォルダ構造

処理対象の企業フォルダは以下の構造を持つ必要があります:

```
A9XX_会社名/
├── スキャン（その他）/
│   ├── １決算書〇/          # 決算書PDF
│   ├── ２従業員名簿/         # 従業員名簿・履歴書(PDF/画像)
│   └── ６車検証〇/           # 車検証(画像)
├── 決算書打ち込み/           # 財務概要Excel出力先
├── 従業員台帳/              # 従業員台帳Excel出力先
└── 車両台帳/                # 車両台帳Excel出力先
```

## 5. トラブルシューティング

### エラー: 環境変数 ANTHROPIC_API_KEY が設定されていません
→ 環境変数を設定してください (上記の手順2を参照)

### エラー: フォルダが見つかりません
→ 企業フォルダのパスを確認してください
→ スキャンフォルダの構造を確認してください

### エラー: Claude API エラー
→ APIキーが正しいか確認してください
→ API利用制限に達していないか確認してください

## 6. テスト実行

まずは車両台帳のみで動作確認することをお勧めします:

```bash
python -m document_processor.main --company A918_株式会社野木工業 --only vehicles
```

成功すると、`A918_株式会社野木工業/車両台帳/車両台帳_株式会社野木工業.xlsx` が生成されます。
