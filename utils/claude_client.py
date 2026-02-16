"""
Claude API クライアント
"""
import base64
import time
import json
from pathlib import Path
from typing import Dict, Any, Optional, List
import anthropic

# 絶対インポートと相対インポートの両方に対応
try:
    from ..config import (
        ANTHROPIC_API_KEY,
        CLAUDE_MODEL,
        MAX_TOKENS,
        TEMPERATURE,
        MAX_RETRIES,
        RETRY_DELAY,
    )
except ImportError:
    from config import (
        ANTHROPIC_API_KEY,
        CLAUDE_MODEL,
        MAX_TOKENS,
        TEMPERATURE,
        MAX_RETRIES,
        RETRY_DELAY,
    )


class ClaudeClient:
    """Claude API クライアント"""

    def __init__(self):
        self.client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    def _strip_code_blocks(self, text: str) -> str:
        """
        コードブロックを削除してJSONのみを抽出

        Args:
            text: レスポンステキスト

        Returns:
            コードブロックを削除したテキスト
        """
        # ```json と ``` を削除
        text = text.strip()
        if text.startswith("```json"):
            text = text[7:]  # ```json を削除
        elif text.startswith("```"):
            text = text[3:]  # ``` を削除
        if text.endswith("```"):
            text = text[:-3]  # ``` を削除
        return text.strip()

    def analyze_image(
        self, image_path: str, prompt: str, response_format: str = "json"
    ) -> Dict[str, Any]:
        """
        画像を解析して構造化データを抽出

        Args:
            image_path: 画像ファイルパス
            prompt: 抽出指示プロンプト
            response_format: "json" または "text"

        Returns:
            解析結果(辞書またはテキスト)
        """
        path = Path(image_path)
        if not path.exists():
            raise FileNotFoundError(f"画像ファイルが見つかりません: {image_path}")

        # 画像をBase64エンコード
        with open(path, "rb") as f:
            image_data = base64.standard_b64encode(f.read()).decode("utf-8")

        # 拡張子からメディアタイプを判定
        ext = path.suffix.lower()
        media_type_map = {
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".png": "image/png",
            ".gif": "image/gif",
            ".webp": "image/webp",
        }
        media_type = media_type_map.get(ext, "image/jpeg")

        # APIリクエスト
        for attempt in range(MAX_RETRIES):
            try:
                message = self.client.messages.create(
                    model=CLAUDE_MODEL,
                    max_tokens=MAX_TOKENS,
                    temperature=TEMPERATURE,
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "image",
                                    "source": {
                                        "type": "base64",
                                        "media_type": media_type,
                                        "data": image_data,
                                    },
                                },
                                {"type": "text", "text": prompt},
                            ],
                        }
                    ],
                )

                response_text = message.content[0].text

                if response_format == "json":
                    # コードブロックを削除
                    response_text = self._strip_code_blocks(response_text)
                    # JSONをパース
                    return json.loads(response_text)
                else:
                    return {"text": response_text}

            except anthropic.RateLimitError:
                if attempt < MAX_RETRIES - 1:
                    print(f"レート制限エラー。{RETRY_DELAY}秒後にリトライします...")
                    time.sleep(RETRY_DELAY)
                else:
                    raise
            except json.JSONDecodeError as e:
                print(f"JSON解析エラー: {e}")
                print(f"レスポンス: {response_text}")
                # JSONとしてパースできない場合はテキストとして返す
                return {"error": "JSON解析失敗", "raw_text": response_text}
            except Exception as e:
                if attempt < MAX_RETRIES - 1:
                    print(f"エラーが発生しました: {e}。リトライします...")
                    time.sleep(RETRY_DELAY)
                else:
                    raise

    def analyze_pdf(
        self, pdf_path: str, prompt: str, response_format: str = "json"
    ) -> Dict[str, Any]:
        """
        PDFを解析して構造化データを抽出

        Args:
            pdf_path: PDFファイルパス
            prompt: 抽出指示プロンプト
            response_format: "json" または "text"

        Returns:
            解析結果(辞書またはテキスト)
        """
        path = Path(pdf_path)
        if not path.exists():
            raise FileNotFoundError(f"PDFファイルが見つかりません: {pdf_path}")

        # PDFをBase64エンコード
        with open(path, "rb") as f:
            pdf_data = base64.standard_b64encode(f.read()).decode("utf-8")

        # APIリクエスト
        for attempt in range(MAX_RETRIES):
            try:
                message = self.client.messages.create(
                    model=CLAUDE_MODEL,
                    max_tokens=MAX_TOKENS,
                    temperature=TEMPERATURE,
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "document",
                                    "source": {
                                        "type": "base64",
                                        "media_type": "application/pdf",
                                        "data": pdf_data,
                                    },
                                },
                                {"type": "text", "text": prompt},
                            ],
                        }
                    ],
                )

                response_text = message.content[0].text

                if response_format == "json":
                    # コードブロックを削除
                    response_text = self._strip_code_blocks(response_text)
                    # JSONをパース
                    return json.loads(response_text)
                else:
                    return {"text": response_text}

            except anthropic.RateLimitError:
                if attempt < MAX_RETRIES - 1:
                    print(f"レート制限エラー。{RETRY_DELAY}秒後にリトライします...")
                    time.sleep(RETRY_DELAY)
                else:
                    raise
            except json.JSONDecodeError as e:
                print(f"JSON解析エラー: {e}")
                print(f"レスポンス: {response_text}")
                return {"error": "JSON解析失敗", "raw_text": response_text}
            except Exception as e:
                if attempt < MAX_RETRIES - 1:
                    print(f"エラーが発生しました: {e}。リトライします...")
                    time.sleep(RETRY_DELAY)
                else:
                    raise

    def analyze_image_bytes(
        self, image_data: bytes, filename: str, prompt: str, response_format: str = "json"
    ) -> Dict[str, Any]:
        """
        画像バイトデータを解析して構造化データを抽出

        Args:
            image_data: 画像のバイトデータ
            filename: ファイル名（拡張子判定用）
            prompt: 抽出指示プロンプト
            response_format: "json" または "text"

        Returns:
            解析結果(辞書またはテキスト)
        """
        # 拡張子からメディアタイプを判定
        ext = Path(filename).suffix.lower()
        media_type_map = {
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".png": "image/png",
            ".gif": "image/gif",
            ".webp": "image/webp",
        }
        media_type = media_type_map.get(ext, "image/jpeg")

        # Base64エンコード
        image_b64 = base64.standard_b64encode(image_data).decode("utf-8")

        # APIリクエスト
        for attempt in range(MAX_RETRIES):
            try:
                message = self.client.messages.create(
                    model=CLAUDE_MODEL,
                    max_tokens=MAX_TOKENS,
                    temperature=TEMPERATURE,
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "image",
                                    "source": {
                                        "type": "base64",
                                        "media_type": media_type,
                                        "data": image_b64,
                                    },
                                },
                                {"type": "text", "text": prompt},
                            ],
                        }
                    ],
                )

                response_text = message.content[0].text

                if response_format == "json":
                    # コードブロックを削除
                    response_text = self._strip_code_blocks(response_text)
                    # JSONをパース
                    return json.loads(response_text)
                else:
                    return {"text": response_text}

            except anthropic.RateLimitError:
                if attempt < MAX_RETRIES - 1:
                    print(f"レート制限エラー。{RETRY_DELAY}秒後にリトライします...")
                    time.sleep(RETRY_DELAY)
                else:
                    raise
            except json.JSONDecodeError as e:
                print(f"JSON解析エラー: {e}")
                print(f"レスポンス: {response_text}")
                # JSONとしてパースできない場合はテキストとして返す
                return {"error": "JSON解析失敗", "raw_text": response_text}
            except Exception as e:
                if attempt < MAX_RETRIES - 1:
                    print(f"エラーが発生しました: {e}。リトライします...")
                    time.sleep(RETRY_DELAY)
                else:
                    raise

    def analyze_pdf_bytes(
        self, pdf_data: bytes, prompt: str, response_format: str = "json"
    ) -> Dict[str, Any]:
        """
        PDFバイトデータを解析して構造化データを抽出

        Args:
            pdf_data: PDFのバイトデータ
            prompt: 抽出指示プロンプト
            response_format: "json" または "text"

        Returns:
            解析結果(辞書またはテキスト)
        """
        # Base64エンコード
        pdf_b64 = base64.standard_b64encode(pdf_data).decode("utf-8")

        # APIリクエスト
        for attempt in range(MAX_RETRIES):
            try:
                message = self.client.messages.create(
                    model=CLAUDE_MODEL,
                    max_tokens=MAX_TOKENS,
                    temperature=TEMPERATURE,
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "document",
                                    "source": {
                                        "type": "base64",
                                        "media_type": "application/pdf",
                                        "data": pdf_b64,
                                    },
                                },
                                {"type": "text", "text": prompt},
                            ],
                        }
                    ],
                )

                response_text = message.content[0].text

                if response_format == "json":
                    # コードブロックを削除
                    response_text = self._strip_code_blocks(response_text)
                    # JSONをパース
                    return json.loads(response_text)
                else:
                    return {"text": response_text}

            except anthropic.RateLimitError:
                if attempt < MAX_RETRIES - 1:
                    print(f"レート制限エラー。{RETRY_DELAY}秒後にリトライします...")
                    time.sleep(RETRY_DELAY)
                else:
                    raise
            except json.JSONDecodeError as e:
                print(f"JSON解析エラー: {e}")
                print(f"レスポンス: {response_text}")
                return {"error": "JSON解析失敗", "raw_text": response_text}
            except Exception as e:
                if attempt < MAX_RETRIES - 1:
                    print(f"エラーが発生しました: {e}。リトライします...")
                    time.sleep(RETRY_DELAY)
                else:
                    raise

    def analyze_multiple_images(
        self, image_paths: List[str], prompt: str, response_format: str = "json"
    ) -> Dict[str, Any]:
        """
        複数の画像を一度に解析

        Args:
            image_paths: 画像ファイルパスのリスト
            prompt: 抽出指示プロンプト
            response_format: "json" または "text"

        Returns:
            解析結果
        """
        content = []

        # 各画像をBase64エンコードして追加
        for image_path in image_paths:
            path = Path(image_path)
            if not path.exists():
                print(f"警告: 画像ファイルが見つかりません: {image_path}")
                continue

            with open(path, "rb") as f:
                image_data = base64.standard_b64encode(f.read()).decode("utf-8")

            ext = path.suffix.lower()
            media_type_map = {
                ".jpg": "image/jpeg",
                ".jpeg": "image/jpeg",
                ".png": "image/png",
                ".gif": "image/gif",
                ".webp": "image/webp",
            }
            media_type = media_type_map.get(ext, "image/jpeg")

            content.append(
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": media_type,
                        "data": image_data,
                    },
                }
            )

        # プロンプトを最後に追加
        content.append({"type": "text", "text": prompt})

        # APIリクエスト
        for attempt in range(MAX_RETRIES):
            try:
                message = self.client.messages.create(
                    model=CLAUDE_MODEL,
                    max_tokens=MAX_TOKENS,
                    temperature=TEMPERATURE,
                    messages=[{"role": "user", "content": content}],
                )

                response_text = message.content[0].text

                if response_format == "json":
                    # コードブロックを削除
                    response_text = self._strip_code_blocks(response_text)
                    return json.loads(response_text)
                else:
                    return {"text": response_text}

            except anthropic.RateLimitError:
                if attempt < MAX_RETRIES - 1:
                    print(f"レート制限エラー。{RETRY_DELAY}秒後にリトライします...")
                    time.sleep(RETRY_DELAY)
                else:
                    raise
            except json.JSONDecodeError as e:
                print(f"JSON解析エラー: {e}")
                print(f"レスポンス: {response_text}")
                return {"error": "JSON解析失敗", "raw_text": response_text}
            except Exception as e:
                if attempt < MAX_RETRIES - 1:
                    print(f"エラーが発生しました: {e}。リトライします...")
                    time.sleep(RETRY_DELAY)
                else:
                    raise
