"""
車検証処理Webアプリ
車検証画像/PDFをアップロードして、車両台帳Excelを自動生成するツール
"""
import streamlit as st
from webapp.vehicle_processor_web import VehicleProcessorWeb

# ページ設定
st.set_page_config(
    page_title="車検証処理ツール",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def check_password():
    """パスワード認証をチェック"""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False

    if st.session_state.authenticated:
        return True

    # 認証画面
    st.title("🔐 車検証処理ツール - ログイン")
    st.markdown("---")

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        password = st.text_input(
            "パスワードを入力してください",
            type="password",
            placeholder="パスワード"
        )

        if st.button("ログイン", type="primary", use_container_width=True):
            try:
                correct_password = st.secrets["APP_PASSWORD"]
            except:
                # ローカル開発用（secrets.tomlがない場合）
                correct_password = "asahi2025"

            if password == correct_password:
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("❌ パスワードが正しくありません")

        st.info("💡 社内メンバーの方は、共有されたパスワードを入力してください。")

    return False


def main():
    """メインアプリケーション"""

    # 認証チェック
    if not check_password():
        st.stop()

    # ヘッダー
    st.title("🚗 車検証処理ツール")
    st.markdown("""
    車検証の画像またはPDFをアップロードすると、自動的に車両台帳Excelを生成します。

    **使い方:**
    1. 会社名を入力
    2. 車検証ファイルをアップロード（複数可）
    3. 「車両台帳を生成」ボタンをクリック
    4. 生成されたExcelファイルをダウンロード
    """)
    st.markdown("---")

    # サイドバーにログアウトボタン
    with st.sidebar:
        st.markdown("### メニュー")
        if st.button("🚪 ログアウト"):
            st.session_state.authenticated = False
            st.rerun()

        st.markdown("---")
        st.markdown("### ℹ️ 情報")
        st.info("""
        **対応フォーマット:**
        - JPG/JPEG
        - PNG
        - PDF

        **最大ファイルサイズ:**
        - 50MB

        **処理時間:**
        - 1ファイルあたり約30秒
        """)

    # メイン入力エリア
    col1, col2 = st.columns([1, 1])

    with col1:
        company_name = st.text_input(
            "📝 会社名（必須）",
            placeholder="例: 株式会社野木工業",
            help="車両台帳Excelのファイル名に使用されます"
        )

    with col2:
        st.markdown("&nbsp;")  # スペース調整

    # ファイルアップロード
    uploaded_files = st.file_uploader(
        "📎 車検証ファイルをアップロード（複数選択可）",
        type=['jpg', 'jpeg', 'png', 'pdf'],
        accept_multiple_files=True,
        help="複数のファイルを一度にアップロードできます"
    )

    # ファイル情報表示
    if uploaded_files:
        st.success(f"✅ {len(uploaded_files)}件のファイルがアップロードされました")
        with st.expander("📋 アップロードされたファイル一覧"):
            for idx, file in enumerate(uploaded_files, 1):
                file_size_mb = file.size / (1024 * 1024)
                st.write(f"{idx}. {file.name} ({file_size_mb:.2f} MB)")

    # 生成ボタン
    st.markdown("---")

    if not company_name:
        st.warning("⚠️ 会社名を入力してください")
        st.stop()

    if not uploaded_files:
        st.info("ℹ️ 車検証ファイルをアップロードしてください")
        st.stop()

    # 処理実行
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 車両台帳を生成", type="primary", use_container_width=True):
            try:
                # プログレスバー表示
                progress_bar = st.progress(0)
                status_text = st.empty()

                status_text.text("処理を開始しています...")
                progress_bar.progress(10)

                # プロセッサ初期化
                processor = VehicleProcessorWeb()
                progress_bar.progress(20)

                # 各ファイルを処理
                status_text.text(f"車検証を解析中... (0/{len(uploaded_files)})")

                # ファイル処理（進捗表示付き）
                excel_bytes = processor.process_uploaded_files(
                    uploaded_files,
                    company_name
                )

                progress_bar.progress(90)
                status_text.text("Excelファイルを生成中...")

                # 完了
                progress_bar.progress(100)
                status_text.empty()
                progress_bar.empty()

                # 成功メッセージ
                st.success(f"✅ 処理完了！{len(uploaded_files)}件のファイルを処理しました。")

                # ダウンロードボタン
                st.download_button(
                    label="📥 車両台帳をダウンロード",
                    data=excel_bytes,
                    file_name=f"車両台帳_{company_name}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )

                st.balloons()

            except Exception as e:
                st.error(f"❌ エラーが発生しました: {str(e)}")
                st.exception(e)
                st.info("💡 問題が解決しない場合は、管理者に連絡してください。")


if __name__ == "__main__":
    main()
