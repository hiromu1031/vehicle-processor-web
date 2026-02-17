"""
あさひ国際会計 業務支援ツール
車検証処理、財務諸表処理など複数の機能を提供
"""
import streamlit as st
import streamlit.components.v1 as components
from webapp.vehicle_processor_web import VehicleProcessorWeb
from webapp.financial_processor_web import FinancialProcessorWeb
from webapp.company_research_web import CompanyResearchWeb
from webapp.employee_processor_web import EmployeeProcessorWeb
from webapp.im_generator_web import IMGeneratorWeb

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

def show_notification(title: str, message: str):
    """ブラウザ通知を表示"""
    notification_html = f"""
    <script>
        // 通知の許可を要求
        if (Notification.permission === "granted") {{
            new Notification("{title}", {{
                body: "{message}",
                icon: "📊",
                requireInteraction: true
            }});
        }} else if (Notification.permission !== "denied") {{
            Notification.requestPermission().then(function (permission) {{
                if (permission === "granted") {{
                    new Notification("{title}", {{
                        body: "{message}",
                        icon: "📊",
                        requireInteraction: true
                    }});
                }}
            }});
        }}
    </script>
    """
    components.html(notification_html, height=0)


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
        ["📋 IM作成", "📊 財務処理", "🚗 車両処理", "👥 従業員台帳", "🔍 企業調査"],
        index=2,  # デフォルトで車両処理を選択
        horizontal=True,
        label_visibility="collapsed"
    )
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # 選択された機能を表示
    if selected_function == "📋 IM作成":
        im_generation_tab()
    elif selected_function == "📊 財務処理":
        financial_processing_tab()
    elif selected_function == "🚗 車両処理":
        vehicle_processing_tab()
    elif selected_function == "👥 従業員台帳":
        employee_ledger_tab()
    elif selected_function == "🔍 企業調査":
        company_research_tab()


def im_generation_tab():
    """IM下書き自動生成タブ"""

    # 使い方ガイド
    st.markdown("""
    <div class="card">
        <div class="card-title">📖 使い方</div>
        <p>
        <strong>1.</strong> 会社名を入力<br>
        <strong>2.</strong> すべての資料をアップロード（決算書、会社案内、組織図、資産リストなど、複数可）<br>
        <strong>3.</strong> 「IM下書きを生成」ボタンをクリック<br>
        <strong>4.</strong> 生成されたExcelファイルをダウンロード（5シート構成）
        </p>
    </div>
    """, unsafe_allow_html=True)

    # メイン入力エリア
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">📝 会社情報</div>', unsafe_allow_html=True)

    company_name = st.text_input(
        "会社名（必須）",
        placeholder="例: 株式会社野木工業",
        help="IM下書きExcelのファイル名に使用されます",
        label_visibility="collapsed",
        key="im_company_name"
    )

    st.markdown('</div>', unsafe_allow_html=True)

    # ファイルアップロードエリア
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">📎 資料ファイル（すべて）</div>', unsafe_allow_html=True)

    st.markdown("""
    **💡 アップロードする資料:**
    - 決算書PDF（3期分） - 財務情報を抽出
    - 会社案内PDF/画像 - 会社概要、事業内容を抽出
    - 組織図、従業員リスト - 組織・人員情報を抽出
    - 車両台帳、資産リスト - 資産情報を抽出
    - 借入金明細 - 負債情報を抽出
    - 取引先リスト - 取引先情報を抽出
    - その他資料 - すべて統合してIM下書きを作成
    """)

    uploaded_files = st.file_uploader(
        "資料ファイルをアップロード（まとめて選択可能）",
        type=['jpg', 'jpeg', 'png', 'pdf', 'xlsx', 'xls'],
        accept_multiple_files=True,
        help="すべての資料を一度にアップロードしてください",
        label_visibility="collapsed",
        key="im_files"
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

    # 出力内容の説明
    st.markdown("""
    <div class="card">
        <div class="card-title">📋 出力内容（Excel）</div>
        <p>以下の5シートで構成されたExcelファイルを生成します：</p>
        <ul>
            <li>📄 <strong>シート1: 会社概要</strong> - 会社名、所在地、代表者、設立日、事業内容、強みなど</li>
            <li>💰 <strong>シート2: 財務サマリー</strong> - 3期比較（売上、利益、資産、負債など）</li>
            <li>👥 <strong>シート3: 組織・従業員</strong> - 従業員数、部門構成、役員情報など</li>
            <li>🏢 <strong>シート4: 資産・負債</strong> - 車両、不動産、設備、借入金など</li>
            <li>📊 <strong>シート5: その他情報</strong> - 取引先、その他特記事項など</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

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
            ℹ️ 資料ファイルをアップロードしてください
        </div>
        """, unsafe_allow_html=True)
        st.stop()

    # 処理実行
    st.markdown('<div class="card">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        if st.button("🚀 IM下書きを生成する", type="primary", use_container_width=True):
            try:
                # プログレスバー表示
                progress_bar = st.progress(0)
                status_text = st.empty()

                status_text.text("処理を開始しています...")
                progress_bar.progress(10)

                # プロセッサ初期化
                processor = IMGeneratorWeb()
                progress_bar.progress(20)

                # 各ファイルを処理
                status_text.text(f"資料を解析中... (0/{len(uploaded_files)})")

                # ファイル処理
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
                    <p style="margin: 0.5rem 0 0 0;">{len(uploaded_files)}件の資料を処理し、5シート構成のIM下書きを作成しました</p>
                </div>
                """, unsafe_allow_html=True)

                st.markdown("<br>", unsafe_allow_html=True)

                # ダウンロードボタン
                st.download_button(
                    label="📥 IM下書きをダウンロード",
                    data=excel_bytes,
                    file_name=f"IM下書き_{company_name}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )

                st.balloons()

                # ブラウザ通知
                show_notification(
                    "IM下書き生成完了！",
                    f"{company_name}のIM下書きが完成しました。"
                )

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


def employee_ledger_tab():
    """従業員台帳タブ"""

    # 使い方ガイド
    st.markdown("""
    <div class="card">
        <div class="card-title">📖 使い方</div>
        <p>
        <strong>1.</strong> 会社名を入力<br>
        <strong>2.</strong> 従業員情報ファイルをアップロード（手書きメモ、写真、Excel、PDF、複数可）<br>
        <strong>3.</strong> 「従業員台帳を生成」ボタンをクリック<br>
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
        help="従業員台帳Excelのファイル名に使用されます",
        label_visibility="collapsed",
        key="employee_company_name"
    )

    st.markdown('</div>', unsafe_allow_html=True)

    # ファイルアップロードエリア
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">📎 従業員情報ファイル</div>', unsafe_allow_html=True)

    st.markdown("""
    **💡 対応フォーマット:**
    - 画像ファイル（JPG、PNG）- 手書きメモや名簿の写真
    - PDFファイル - 従業員リスト、給与明細など
    - Excelファイル - バラバラなフォーマットのExcelも統合可能
    """)

    uploaded_files = st.file_uploader(
        "従業員情報ファイルをアップロード",
        type=['jpg', 'jpeg', 'png', 'pdf', 'xlsx', 'xls'],
        accept_multiple_files=True,
        help="複数のファイルを一度にアップロードできます",
        label_visibility="collapsed",
        key="employee_files"
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
            ℹ️ 従業員情報ファイルをアップロードしてください
        </div>
        """, unsafe_allow_html=True)
        st.stop()

    # 処理実行
    st.markdown('<div class="card">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        if st.button("🚀 従業員台帳を生成する", type="primary", use_container_width=True):
            try:
                # プログレスバー表示
                progress_bar = st.progress(0)
                status_text = st.empty()

                status_text.text("処理を開始しています...")
                progress_bar.progress(10)

                # プロセッサ初期化
                processor = EmployeeProcessorWeb()
                progress_bar.progress(20)

                # 各ファイルを処理
                status_text.text(f"従業員情報を解析中... (0/{len(uploaded_files)})")

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
                    label="📥 従業員台帳をダウンロード",
                    data=excel_bytes,
                    file_name=f"従業員台帳_{company_name}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )

                st.balloons()

                # ブラウザ通知
                show_notification(
                    "従業員台帳生成完了！",
                    f"{company_name}の従業員台帳が完成しました。"
                )

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


def company_research_tab():
    """企業情報調査タブ"""

    # 使い方ガイド
    st.markdown("""
    <div class="card">
        <div class="card-title">📖 使い方</div>
        <p>
        <strong>1.</strong> 会社名、住所、代表者名を入力<br>
        <strong>2.</strong> 「企業情報を調査」ボタンをクリック<br>
        <strong>3.</strong> AIが保有する情報から企業情報を抽出（採用情報、インタビュー、ニュースなど）<br>
        <strong>4.</strong> 生成されたWord文書をダウンロード
        </p>
        <p style="color: #666; font-size: 0.9rem; margin-top: 0.5rem;">
        ⚠️ 簡易版：2025年1月までのAIトレーニングデータから情報を抽出（リアルタイムWeb検索ではありません）
        </p>
    </div>
    """, unsafe_allow_html=True)

    # 入力エリア
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">📝 企業情報</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        company_name = st.text_input(
            "会社名（必須）",
            placeholder="例: 株式会社野木工業",
            help="調査対象の会社名を入力してください",
            key="research_company_name"
        )

        address = st.text_input(
            "所在地（必須）",
            placeholder="例: 東京都中央区日本橋",
            help="会社の所在地を入力してください",
            key="research_address"
        )

    with col2:
        representative = st.text_input(
            "代表者名（必須）",
            placeholder="例: 山田太郎",
            help="代表取締役の氏名を入力してください",
            key="research_representative"
        )

        st.markdown("<br>", unsafe_allow_html=True)
        st.info("💡 入力した情報をもとにAIが保有するデータから企業情報を抽出します")

    st.markdown('</div>', unsafe_allow_html=True)

    # 検索対象の説明
    st.markdown("""
    <div class="card">
        <div class="card-title">🔍 抽出内容</div>
        <p>以下の情報をAIトレーニングデータから抽出します：</p>
        <ul>
            <li>📌 会社概要・事業内容</li>
            <li>👥 採用情報（求人、社員数、待遇など）</li>
            <li>🎤 代表者インタビュー・発言</li>
            <li>📰 ニュース・プレスリリース</li>
        </ul>
        <p><strong>※ 確実な情報のみを抽出します（推測・捏造なし）</strong></p>
    </div>
    """, unsafe_allow_html=True)

    # バリデーション
    if not company_name or not address or not representative:
        st.markdown("""
        <div class="info-box">
            ⚠️ すべての項目を入力してください
        </div>
        """, unsafe_allow_html=True)
        return

    # 処理実行
    st.markdown('<div class="card">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        if st.button("🔍 企業情報を調査する", type="primary", use_container_width=True):
            try:
                # プログレスバー表示
                progress_bar = st.progress(0)
                status_text = st.empty()

                status_text.text("情報抽出を開始しています...")
                progress_bar.progress(10)

                # プロセッサ初期化
                processor = CompanyResearchWeb()
                progress_bar.progress(20)

                # AIトレーニングデータから情報抽出
                status_text.text(f"「{company_name}」の情報を抽出中...")
                progress_bar.progress(30)

                company_info = processor.search_company_info(
                    company_name,
                    address,
                    representative
                )

                progress_bar.progress(70)
                status_text.text("情報を整理しています...")

                # Word文書生成
                word_bytes = processor.generate_word_report(company_info)

                progress_bar.progress(95)
                status_text.text("Word文書を生成中...")

                # 完了
                progress_bar.progress(100)
                status_text.empty()
                progress_bar.empty()

                # 成功メッセージ
                sections_count = len(company_info.get("sections", []))
                st.markdown(f"""
                <div class="success-box">
                    <h3 style="margin: 0; color: #065f46;">✅ 調査完了！</h3>
                    <p style="margin: 0.5rem 0 0 0;">{sections_count}カテゴリの情報を収集しました</p>
                </div>
                """, unsafe_allow_html=True)

                st.markdown("<br>", unsafe_allow_html=True)

                # ダウンロードボタン
                st.download_button(
                    label="📥 調査レポートをダウンロード（Word）",
                    data=word_bytes,
                    file_name=f"企業情報調査_{company_name}.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    use_container_width=True
                )

                st.balloons()

                # ブラウザ通知
                show_notification(
                    "企業調査完了！",
                    f"{company_name}の情報収集が完了しました。"
                )

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


if __name__ == "__main__":
    main()
# PDF分割ツール機能は削除されました（メモリ問題のため）
# 必要に応じて将来的に再実装可能
