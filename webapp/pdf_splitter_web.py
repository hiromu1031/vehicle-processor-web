"""
決算書PDF統合・分割プロセッサ（Web版）
複数のPDFファイルから必要なページを抽出・統合して期ごとに整理
"""
from io import BytesIO
from typing import List, Dict, Any, Tuple
import fitz  # PyMuPDF
import zipfile
from collections import defaultdict

from utils.claude_client import ClaudeClient


class PDFSplitterWeb:
    """決算書PDF統合・分割プロセッサ（Web版）"""

    def __init__(self):
        self.claude_client = ClaudeClient()

    def compress_pdf(self, pdf_bytes: bytes) -> bytes:
        """
        PDFファイルを圧縮

        Args:
            pdf_bytes: 元のPDFファイルのバイトデータ

        Returns:
            圧縮後のPDFファイルのバイトデータ
        """
        try:
            # PDFを開く
            pdf_doc = fitz.open(stream=pdf_bytes, filetype="pdf")

            # 新しいPDFを作成
            compressed_doc = fitz.open()

            # 各ページを低解像度で再レンダリング
            for page in pdf_doc:
                # ページを画像として取得（解像度を下げる）
                pix = page.get_pixmap(matrix=fitz.Matrix(1.0, 1.0), alpha=False)

                # 新しいページを作成（元のページサイズを維持）
                new_page = compressed_doc.new_page(
                    width=page.rect.width,
                    height=page.rect.height
                )

                # 画像をページに挿入
                new_page.insert_image(
                    new_page.rect,
                    pixmap=pix
                )

            # メタデータをクリア
            compressed_doc.set_metadata({})

            # PDFをバイトデータとして保存
            compressed_bytes = compressed_doc.tobytes(
                garbage=4,  # ガベージコレクションを実行
                deflate=True,  # 圧縮を有効化
            )

            compressed_doc.close()
            pdf_doc.close()

            return compressed_bytes

        except Exception as e:
            print(f"PDF圧縮エラー: {str(e)}")
            # 圧縮に失敗した場合は元のPDFを返す
            return pdf_bytes

    def analyze_pdfs(self, uploaded_files: List) -> Tuple[List[Dict[str, Any]], Dict[str, bytes]]:
        """
        アップロードされたPDFファイルを解析し、各ページの情報を取得

        Args:
            uploaded_files: Streamlit UploadedFileのリスト

        Returns:
            ページ情報のリスト
            [
                {
                    "file_name": "決算書1.pdf",
                    "page_num": 1,
                    "fiscal_period": "第25期",
                    "fiscal_year": "2024",
                    "document_type": "表紙",
                    "content_summary": "...",
                },
                ...
            ]
        """
        all_pages = []
        pdf_cache = {}  # ファイル名とバイトデータのキャッシュ

        for uploaded_file in uploaded_files:
            file_bytes = uploaded_file.read()
            file_name = uploaded_file.name

            # バイトデータをキャッシュ
            pdf_cache[file_name] = file_bytes

            # PDFを開く
            pdf_document = fitz.open(stream=file_bytes, filetype="pdf")

            # 各ページを解析
            for page_num in range(len(pdf_document)):
                try:
                    page = pdf_document[page_num]

                    # ページを画像に変換（解像度を下げて軽量化）
                    pix = page.get_pixmap(matrix=fitz.Matrix(1.5, 1.5))  # 1.5倍の解像度
                    img_bytes = pix.tobytes("jpeg", quality=85)  # JPEGで圧縮

                    # 画像サイズをチェック（5MB以上なら警告）
                    img_size_mb = len(img_bytes) / (1024 * 1024)
                    if img_size_mb > 5:
                        print(f"警告: {file_name} p.{page_num + 1} の画像サイズが大きすぎます: {img_size_mb:.2f}MB")
                        # さらに解像度を下げる
                        pix = page.get_pixmap(matrix=fitz.Matrix(1.0, 1.0))
                        img_bytes = pix.tobytes("jpeg", quality=70)

                    # Claude APIでページ内容を解析
                    page_info = self.claude_client.analyze_image_bytes(
                        img_bytes,
                        f"{file_name}_page_{page_num + 1}.jpg",
                        self._get_page_analysis_prompt()
                    )

                    if isinstance(page_info, dict) and not page_info.get("error"):
                        page_info["file_name"] = file_name
                        page_info["page_num"] = page_num
                        all_pages.append(page_info)
                    else:
                        # エラーが発生した場合もページ情報を保持
                        print(f"ページ解析エラー: {file_name} p.{page_num + 1}: {page_info.get('error', '不明なエラー')}")

                except Exception as e:
                    print(f"ページ処理エラー: {file_name} p.{page_num + 1}: {str(e)}")
                    # エラーが発生してもスキップして次のページへ

            pdf_document.close()

        return all_pages, pdf_cache

    def split_and_merge_pdfs(
        self,
        pdf_cache: Dict[str, bytes],
        page_analysis: List[Dict[str, Any]]
    ) -> BytesIO:
        """
        解析結果をもとに、PDFを期ごと・資料種類ごとに分割・統合

        Args:
            pdf_cache: ファイル名とバイトデータのマッピング
            page_analysis: analyze_pdfs()の結果

        Returns:
            ZIPファイルのバイトストリーム
        """
        # ファイル名とPDFドキュメントのマッピングを作成
        pdf_docs = {}
        for file_name, file_bytes in pdf_cache.items():
            pdf_docs[file_name] = fitz.open(stream=file_bytes, filetype="pdf")

        # 期ごと・資料種類ごとにページをグルーピング
        grouped_pages = self._group_pages_by_period(page_analysis)

        # 新しいPDFを生成
        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for group_name, pages in grouped_pages.items():
                if not pages:
                    continue

                # 新しいPDFドキュメントを作成
                new_pdf = fitz.open()

                for page_info in pages:
                    source_pdf = pdf_docs[page_info["file_name"]]
                    page_num = page_info["page_num"]

                    # ページをコピー
                    new_pdf.insert_pdf(source_pdf, from_page=page_num, to_page=page_num)

                # PDFをバイトストリームに保存
                pdf_bytes = new_pdf.tobytes()
                new_pdf.close()

                # ZIPに追加
                zip_file.writestr(f"{group_name}.pdf", pdf_bytes)

        # すべてのPDFドキュメントを閉じる
        for pdf_doc in pdf_docs.values():
            pdf_doc.close()

        zip_buffer.seek(0)
        return zip_buffer

    def _get_page_analysis_prompt(self) -> str:
        """ページ解析用プロンプト"""
        return """
このページの内容を解析して、以下の情報をJSONで返してください。

## 抽出する情報

1. **決算期情報**
   - fiscal_period: 期数（例: "第25期"、"第3期"）
   - fiscal_year: 決算年（例: "2024"、"令和6年"）
   - fiscal_year_end: 決算日（例: "2024年9月30日"、"令和6年9月30日"）

2. **資料の種類**（document_type）
   以下のいずれかを判定してください：
   - "表紙": 決算書の表紙、タイトルページ
   - "損益計算書" または "PL": 売上高、営業利益などの損益項目
   - "貸借対照表" または "BS": 資産、負債、純資産の項目
   - "販管費明細" または "販管費": 販売費及び一般管理費の内訳
   - "原価明細" または "原価内訳": 売上原価の内訳
   - "科目明細": 勘定科目の詳細一覧（普通預金、売掛金など）
   - "注記": 注記事項、会計方針など
   - "その他": 上記に該当しない場合

3. **内容の要約**
   - content_summary: このページの内容を1-2行で要約

## JSONフォーマット

{
  "fiscal_period": "第25期",
  "fiscal_year": "2024",
  "fiscal_year_end": "2024年9月30日",
  "document_type": "損益計算書",
  "content_summary": "売上高から当期純利益までの損益項目を記載した損益計算書"
}

**重要:**
- 期数や年度が記載されていない場合は空文字列 "" を設定
- 資料の種類が判別できない場合は "その他" を設定
- 必ずJSON形式で返してください（コードブロック不要）
"""

    def _group_pages_by_period(self, page_analysis: List[Dict[str, Any]]) -> Dict[str, List[Dict]]:
        """
        ページ情報を期ごと・資料種類ごとにグルーピング

        Returns:
            {
                "Period1_第23期": [page_info, ...],
                "Period2_第24期": [page_info, ...],
                "Period3_第25期": [page_info, ...],
                "科目明細_第25期": [page_info, ...],
            }
        """
        # 期ごとに分類
        periods = defaultdict(lambda: defaultdict(list))

        for page_info in page_analysis:
            fiscal_period = page_info.get("fiscal_period", "不明")
            doc_type = page_info.get("document_type", "その他")

            # 科目明細は別グループ
            if "科目" in doc_type:
                periods[fiscal_period]["科目明細"].append(page_info)
            else:
                periods[fiscal_period][doc_type].append(page_info)

        # 期の順序を判定（第○期の数字で並び替え）
        sorted_periods = self._sort_periods(list(periods.keys()))

        # グループ名とページのマッピング
        grouped = {}

        for idx, period in enumerate(sorted_periods, start=1):
            # 期ごとのページ（科目明細以外）
            period_pages = []
            for doc_type in ["表紙", "損益計算書", "PL", "貸借対照表", "BS", "販管費明細", "販管費", "原価明細", "原価内訳"]:
                if doc_type in periods[period]:
                    period_pages.extend(periods[period][doc_type])

            if period_pages:
                grouped[f"Period{idx}_{period}"] = period_pages

            # 科目明細（最新期のみ）
            if idx == len(sorted_periods) and "科目明細" in periods[period]:
                grouped[f"科目明細_{period}"] = periods[period]["科目明細"]

        return grouped

    def _sort_periods(self, periods: List[str]) -> List[str]:
        """
        期のリストを古い順にソート

        Args:
            periods: ["第25期", "第23期", "第24期"]

        Returns:
            ["第23期", "第24期", "第25期"]
        """
        def extract_period_number(period: str) -> int:
            # "第25期" -> 25
            import re
            match = re.search(r'第?(\d+)期', period)
            if match:
                return int(match.group(1))
            return 0

        return sorted(periods, key=extract_period_number)
