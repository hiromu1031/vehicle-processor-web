"""
あさひ国際会計 業務支援ツール
車検証処理、財務諸表処理など複数の機能を提供
"""
import streamlit as st
from webapp.vehicle_processor_web import VehicleProcessorWeb
from webapp.financial_processor_web import FinancialProcessorWeb
from webapp.pdf_splitter_web import PDFSplitterWeb

# ページ設定
st.set_page_config(
    page_title="業務支援ツール | あさひ国際会計",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# カスタムCSS
st.markdown("""
<style>
    /* メインコンテナ */
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }

    /* ヘッダースタイル */
    .header-container {
        background: white;
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        border: 2px solid #1e3c72;
    }

    .header-title {
        color: #1e3c72;
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
        text-align: center;
    }

    .header-subtitle {
        color: #4a5568;
        font-size: 1.1rem;
        text-align: center;
        margin-top: 0.5rem;
    }

    /* カードスタイル */
    .card {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
        margin-bottom: 1.5rem;
    }

    .card-title {
        color: #1e3c72;
        font-size: 1.3rem;
        font-weight: 600;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
    }

    /* ボタンスタイル */
    .stButton > button {
        background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        font-size: 1.1rem;
        font-weight: 600;
        border-radius: 8px;
        transition: all 0.3s ease;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(30, 60, 114, 0.3);
    }

    /* アップロードエリア */
    .uploadedFile {
        border-left: 4px solid #2a5298;
        padding-left: 1rem;
    }

    /* プログレスバー */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
    }

    /* インフォメーション */
    .info-box {
        background: #e0e7ff;
        border-left: 4px solid #2a5298;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }

    /* 成功メッセージ */
    .success-box {
        background: #d1fae5;
        border-left: 4px solid #10b981;
        padding: 1rem;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

def check_password():
    """パスワード認証をチェック"""
    # ===== テスト運用中はパスワード不要 =====
    # 本番運用時は以下の行を削除してパスワード認証を有効化してください
    return True
    # ==========================================

    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False

    if st.session_state.authenticated:
        return True

    # 認証画面
    st.markdown("""
    <div class="header-container">
        <h1 class="header-title">🔐 業務支援ツール</h1>
        <p class="header-subtitle">あさひ国際会計株式会社 | ログイン</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">🔑 認証</div>', unsafe_allow_html=True)

        password = st.text_input(
            "パスワードを入力してください",
            type="password",
            placeholder="パスワード",
            label_visibility="collapsed"
        )

        st.markdown("<br>", unsafe_allow_html=True)

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

        st.markdown('</div>', unsafe_allow_html=True)

        st.info("💡 社内メンバーの方は、共有されたパスワードを入力してください。")

    return False


def main():
    """メインアプリケーション"""

    # 認証チェック
    if not check_password():
        st.stop()

    # ヘッダー
    st.markdown("""
    <div class="header-container">
        <h1 class="header-title">📊 業務支援ツール</h1>
        <p class="header-subtitle">あさひ国際会計株式会社 | 車検証処理・財務諸表処理</p>
    </div>
    """, unsafe_allow_html=True)

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

    # 機能選択（ラジオボタン）
    st.markdown('<div class="card">', unsafe_allow_html=True)
    selected_function = st.radio(
        "処理機能を選択してください",
        ["📊 財務処理", "🚗 車両処理", "📄 PDF分割ツール"],
        index=1,  # デフォルトで車両処理を選択
        horizontal=True,
        label_visibility="collapsed"
    )
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # 選択された機能を表示
    if selected_function == "📊 財務処理":
        financial_processing_tab()
    elif selected_function == "🚗 車両処理":
        vehicle_processing_tab()
    elif selected_function == "📄 PDF分割ツール":
        pdf_splitter_tab()


def vehicle_processing_tab():
    """車両処理タブ"""

    # 使い方ガイド
    st.markdown("""
    <div class="card">
        <div class="card-title">📖 使い方</div>
        <p>
        <strong>1.</strong> 会社名を入力<br>
        <strong>2.</strong> 車検証ファイルをアップロード（JPG/PNG/PDF、複数可）<br>
        <strong>3.</strong> 「車両台帳を生成」ボタンをクリック<br>
        <strong>4.</strong> 生成されたExcelファイルをダウンロード
        </p>
    </div>
    """, unsafe_allow_html=True)

    # メイン入力エリア
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">📝 会社情報</div>', unsafe_allow_html=True)

    company_name = st.text_input(
        "会社名（必須）",
        placeholder="例: 株式会社野木工業",
        help="車両台帳Excelのファイル名に使用されます",
        label_visibility="collapsed"
    )

    st.markdown('</div>', unsafe_allow_html=True)

    # ファイルアップロードエリア
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">📎 車検証ファイル</div>', unsafe_allow_html=True)

    uploaded_files = st.file_uploader(
        "車検証ファイルをアップロード",
        type=['jpg', 'jpeg', 'png', 'pdf'],
        accept_multiple_files=True,
        help="複数のファイルを一度にアップロードできます（JPG、PNG、PDF対応）",
        label_visibility="collapsed"
    )

    # ファイル情報表示
    if uploaded_files:
        st.markdown(f"""
        <div class="success-box">
            ✅ <strong>{len(uploaded_files)}件</strong>のファイルがアップロードされました
        </div>
        """, unsafe_allow_html=True)

        with st.expander("📋 アップロードされたファイル一覧を表示"):
            for idx, file in enumerate(uploaded_files, 1):
                file_size_mb = file.size / (1024 * 1024)
                st.write(f"**{idx}.** {file.name} `({file_size_mb:.2f} MB)`")

    st.markdown('</div>', unsafe_allow_html=True)

    # 生成ボタン
    if not company_name:
        st.markdown("""
        <div class="info-box">
            ⚠️ 会社名を入力してください
        </div>
        """, unsafe_allow_html=True)
        st.stop()

    if not uploaded_files:
        st.markdown("""
        <div class="info-box">
            ℹ️ 車検証ファイルをアップロードしてください
        </div>
        """, unsafe_allow_html=True)
        st.stop()

    # 処理実行
    st.markdown('<div class="card">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        if st.button("🚀 車両台帳を生成する", type="primary", use_container_width=True):
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
                st.markdown(f"""
                <div class="success-box">
                    <h3 style="margin: 0; color: #065f46;">✅ 処理完了！</h3>
                    <p style="margin: 0.5rem 0 0 0;">{len(uploaded_files)}件のファイルを処理しました</p>
                </div>
                """, unsafe_allow_html=True)

                st.markdown("<br>", unsafe_allow_html=True)

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
                st.markdown(f"""
                <div style="background: #fee2e2; border-left: 4px solid #ef4444; padding: 1rem; border-radius: 5px;">
                    <h4 style="margin: 0; color: #991b1b;">❌ エラーが発生しました</h4>
                    <p style="margin: 0.5rem 0 0 0; color: #7f1d1d;">{str(e)}</p>
                </div>
                """, unsafe_allow_html=True)

                with st.expander("詳細なエラー情報"):
                    st.exception(e)

                st.info("💡 問題が解決しない場合は、管理者に連絡してください。")

    st.markdown('</div>', unsafe_allow_html=True)


def financial_processing_tab():
    """財務処理タブ"""

    # 使い方ガイド
    st.markdown("""
    <div class="card">
        <div class="card-title">📖 使い方</div>
        <p>
        <strong>1.</strong> 会社名を入力<br>
        <strong>2.</strong> 各期の決算書PDFをアップロード（最小構成: 表紙、PL、BS、販管費、原価内訳）<br>
        <strong>3.</strong> 科目明細PDF（最新期のみ）をアップロード<br>
        <strong>4.</strong> 「財務概要を生成」ボタンをクリック<br>
        <strong>5.</strong> 生成されたExcelファイルをダウンロード
        </p>
    </div>
    """, unsafe_allow_html=True)

    # 会社名入力
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">📝 会社情報</div>', unsafe_allow_html=True)

    company_name = st.text_input(
        "会社名（必須）",
        placeholder="例: 株式会社野木工業",
        help="財務概要Excelのファイル名に使用されます",
        label_visibility="collapsed",
        key="financial_company_name"
    )

    st.markdown('</div>', unsafe_allow_html=True)

    # 決算書PDFアップロード（3期分）
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">📎 決算書PDF（3期分）</div>', unsafe_allow_html=True)

    st.markdown("**💡 ヒント:** 古い期から順番にアップロードしてください（Period 1 → Period 2 → Period 3）")
    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("**Period 1（最古）**")
        period1_pdf = st.file_uploader(
            "Period 1 PDF",
            type=['pdf'],
            help="最も古い期の決算書PDF",
            label_visibility="collapsed",
            key="period1"
        )

    with col2:
        st.markdown("**Period 2（中間）**")
        period2_pdf = st.file_uploader(
            "Period 2 PDF",
            type=['pdf'],
            help="中間期の決算書PDF",
            label_visibility="collapsed",
            key="period2"
        )

    with col3:
        st.markdown("**Period 3（最新）**")
        period3_pdf = st.file_uploader(
            "Period 3 PDF",
            type=['pdf'],
            help="最新期の決算書PDF",
            label_visibility="collapsed",
            key="period3"
        )

    st.markdown('</div>', unsafe_allow_html=True)

    # 科目明細PDFアップロード
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">📎 科目明細PDF（最新期のみ）</div>', unsafe_allow_html=True)

    account_details_pdf = st.file_uploader(
        "科目明細PDF",
        type=['pdf'],
        help="最新期の科目明細PDF",
        label_visibility="collapsed",
        key="account_details"
    )

    st.markdown('</div>', unsafe_allow_html=True)

    # アップロード状況表示
    uploaded_count = sum([
        1 if period1_pdf else 0,
        1 if period2_pdf else 0,
        1 if period3_pdf else 0,
        1 if account_details_pdf else 0
    ])

    if uploaded_count > 0:
        st.markdown(f"""
        <div class="success-box">
            ✅ <strong>{uploaded_count}件</strong>のファイルがアップロードされました
        </div>
        """, unsafe_allow_html=True)

    # 生成ボタン
    if not company_name:
        st.markdown("""
        <div class="info-box">
            ⚠️ 会社名を入力してください
        </div>
        """, unsafe_allow_html=True)
        return

    if not any([period1_pdf, period2_pdf, period3_pdf]):
        st.markdown("""
        <div class="info-box">
            ℹ️ 少なくとも1期分の決算書PDFをアップロードしてください
        </div>
        """, unsafe_allow_html=True)
        return

    # 処理実行
    st.markdown('<div class="card">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        if st.button("🚀 財務概要を生成する", type="primary", use_container_width=True):
            try:
                # プログレスバー表示
                progress_bar = st.progress(0)
                status_text = st.empty()

                status_text.text("処理を開始しています...")
                progress_bar.progress(10)

                # プロセッサ初期化
                processor = FinancialProcessorWeb()
                progress_bar.progress(20)

                # 各期の処理
                status_text.text("決算書を解析中...")
                progress_bar.progress(30)

                # Excel生成
                excel_bytes = processor.process_uploaded_files(
                    period1_pdf,
                    period2_pdf,
                    period3_pdf,
                    account_details_pdf,
                    company_name
                )

                progress_bar.progress(90)
                status_text.text("Excelファイルを生成中...")

                # 完了
                progress_bar.progress(100)
                status_text.empty()
                progress_bar.empty()

                # 成功メッセージ
                st.markdown(f"""
                <div class="success-box">
                    <h3 style="margin: 0; color: #065f46;">✅ 処理完了！</h3>
                    <p style="margin: 0.5rem 0 0 0;">{uploaded_count}件のファイルを処理しました</p>
                </div>
                """, unsafe_allow_html=True)

                st.markdown("<br>", unsafe_allow_html=True)

                # ダウンロードボタン
                st.download_button(
                    label="📥 財務概要をダウンロード",
                    data=excel_bytes,
                    file_name=f"財務概要_{company_name}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )

                st.balloons()

            except Exception as e:
                st.markdown(f"""
                <div style="background: #fee2e2; border-left: 4px solid #ef4444; padding: 1rem; border-radius: 5px;">
                    <h4 style="margin: 0; color: #991b1b;">❌ エラーが発生しました</h4>
                    <p style="margin: 0.5rem 0 0 0; color: #7f1d1d;">{str(e)}</p>
                </div>
                """, unsafe_allow_html=True)

                with st.expander("詳細なエラー情報"):
                    st.exception(e)

                st.info("💡 問題が解決しない場合は、管理者に連絡してください。")

    st.markdown('</div>', unsafe_allow_html=True)


def pdf_splitter_tab():
    """PDF分割ツールタブ"""

    # 使い方ガイド
    st.markdown("""
    <div class="card">
        <div class="card-title">📖 使い方</div>
        <p>
        <strong>1.</strong> 決算書PDFファイルを複数アップロード（3-4個まとめてOK）<br>
        <strong>2.</strong> 「ページを解析」ボタンをクリック<br>
        <strong>3.</strong> 解析結果を確認（どのページが何の資料か表示されます）<br>
        <strong>4.</strong> 「PDFを分割・統合して生成」ボタンをクリック<br>
        <strong>5.</strong> ZIPファイルをダウンロード（期ごとに整理されたPDFが入っています）
        </p>
    </div>
    """, unsafe_allow_html=True)

    # PDFアップロードエリア
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">📎 決算書PDFファイル</div>', unsafe_allow_html=True)

    st.markdown("""
    **💡 ヒント:**
    - 複数のPDFファイルをまとめてアップロードできます
    - 期が混在していても自動的に整理されます
    - 資料が複数PDFに分かれていても統合されます
    """)

    uploaded_pdfs = st.file_uploader(
        "決算書PDFをアップロード",
        type=['pdf'],
        accept_multiple_files=True,
        help="決算書が含まれるPDFファイルを選択してください",
        label_visibility="collapsed",
        key="pdf_splitter_upload"
    )

    # ファイル情報表示
    if uploaded_pdfs:
        st.markdown(f"""
        <div class="success-box">
            ✅ <strong>{len(uploaded_pdfs)}件</strong>のPDFファイルがアップロードされました
        </div>
        """, unsafe_allow_html=True)

        with st.expander("📋 アップロードされたファイル一覧"):
            for idx, file in enumerate(uploaded_pdfs, 1):
                file_size_mb = file.size / (1024 * 1024)
                st.write(f"**{idx}.** {file.name} `({file_size_mb:.2f} MB)`")

    st.markdown('</div>', unsafe_allow_html=True)

    # 解析ボタン
    if not uploaded_pdfs:
        st.markdown("""
        <div class="info-box">
            ℹ️ PDFファイルをアップロードしてください
        </div>
        """, unsafe_allow_html=True)
        return

    # 解析処理
    st.markdown('<div class="card">', unsafe_allow_html=True)

    # セッションステートで解析結果を保持
    if 'page_analysis' not in st.session_state:
        st.session_state.page_analysis = None

    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        if st.button("🔍 ページを解析する", type="primary", use_container_width=True):
            try:
                # プログレスバー表示
                progress_bar = st.progress(0)
                status_text = st.empty()

                status_text.text("PDFファイルを読み込んでいます...")
                progress_bar.progress(10)

                # プロセッサ初期化
                processor = PDFSplitterWeb()
                progress_bar.progress(20)

                # ページ解析
                status_text.text(f"ページを解析中... (0/{len(uploaded_pdfs)} files)")

                page_analysis = processor.analyze_pdfs(uploaded_pdfs)

                progress_bar.progress(90)
                status_text.text("解析結果を整理中...")

                # セッションステートに保存
                st.session_state.page_analysis = page_analysis

                # 完了
                progress_bar.progress(100)
                status_text.empty()
                progress_bar.empty()

                st.success(f"✅ 解析完了！{len(page_analysis)}ページを解析しました")

            except Exception as e:
                st.error(f"❌ エラーが発生しました: {str(e)}")
                st.exception(e)

    st.markdown('</div>', unsafe_allow_html=True)

    # 解析結果表示
    if st.session_state.page_analysis:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">📊 解析結果</div>', unsafe_allow_html=True)

        # 期ごとにグループ化して表示
        periods = {}
        for page in st.session_state.page_analysis:
            period = page.get("fiscal_period", "不明")
            if period not in periods:
                periods[period] = []
            periods[period].append(page)

        # 期ごとに表示
        for period, pages in sorted(periods.items()):
            with st.expander(f"**{period}** ({len(pages)}ページ)", expanded=True):
                for page in pages:
                    doc_type = page.get("document_type", "不明")
                    file_name = page.get("file_name", "")
                    page_num = page.get("page_num", 0) + 1
                    summary = page.get("content_summary", "")

                    st.markdown(f"""
                    - **{doc_type}**: `{file_name}` p.{page_num}
                      - {summary}
                    """)

        st.markdown('</div>', unsafe_allow_html=True)

        # PDF生成ボタン
        st.markdown('<div class="card">', unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 3, 1])
        with col2:
            if st.button("📦 PDFを分割・統合して生成", type="primary", use_container_width=True):
                try:
                    # プログレスバー表示
                    progress_bar = st.progress(0)
                    status_text = st.empty()

                    status_text.text("PDFを生成中...")
                    progress_bar.progress(30)

                    # PDF分割・統合
                    processor = PDFSplitterWeb()
                    zip_bytes = processor.split_and_merge_pdfs(
                        uploaded_pdfs,
                        st.session_state.page_analysis
                    )

                    progress_bar.progress(90)
                    status_text.text("ZIPファイルを作成中...")

                    # 完了
                    progress_bar.progress(100)
                    status_text.empty()
                    progress_bar.empty()

                    # 成功メッセージ
                    st.markdown(f"""
                    <div class="success-box">
                        <h3 style="margin: 0; color: #065f46;">✅ 生成完了！</h3>
                        <p style="margin: 0.5rem 0 0 0;">期ごとに整理されたPDFファイルをZIPにまとめました</p>
                    </div>
                    """, unsafe_allow_html=True)

                    st.markdown("<br>", unsafe_allow_html=True)

                    # ダウンロードボタン
                    st.download_button(
                        label="📥 ZIPファイルをダウンロード",
                        data=zip_bytes,
                        file_name="決算書_整理済み.zip",
                        mime="application/zip",
                        use_container_width=True
                    )

                    st.balloons()

                except Exception as e:
                    st.error(f"❌ エラーが発生しました: {str(e)}")
                    st.exception(e)

        st.markdown('</div>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()
