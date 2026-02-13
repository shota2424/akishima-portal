import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

# --- ページ設定 ---
st.set_page_config(page_title="昭島市政ポータル v0.1", layout="wide", page_icon="🏙️")

# --- かっこいいUIのためのCSS ---
st.markdown("""
    <style>
    .stApp { background-color: #f0f2f6; }
    .card { background: white; padding: 20px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 15px; border-left: 6px solid #1f77b4; }
    .tag { background: #e1f5fe; color: #01579b; padding: 2px 10px; border-radius: 15px; font-size: 0.8rem; font-weight: bold; }
    .source { color: #6c757d; font-size: 0.85rem; text-decoration: none; }
    </style>
    """, unsafe_allow_html=True)

# --- DB接続（SQLite） ---
def get_connection():
    # 実際にはGitHubにDBファイルを上げない場合は、起動時に初期化するロジックが必要
    conn = sqlite3.connect("akishima.db", check_same_thread=False)
    return conn

# --- メイン画面 ---
def main():
    st.title("🏙️ 昭島市政データ基盤 (v0.1)")
    st.caption("議会・予算・計画を構造化し、市民の『知りたい』を根拠付きで支える")

    menu = st.sidebar.selectbox("メニュー切り替え", ["CouncilScope (議会検索)", "CityFinanceGlass (予算分析)"])

    conn = get_connection()

    if menu == "CouncilScope (議会検索)":
        st.header("🔍 会議録エージェント")
        q = st.text_input("キーワードを入力（例：水道、教育、開発）", "")
        
        # モックデータ表示（DBがない場合用）
        data = [
            {"speaker": "○市長（臼井伸介君）", "content": "昭島市の将来を見据えたインフラ整備は喫緊の課題です。特に水道の耐震化については...", "tag": "インフラ", "summary": "水道耐震化の重要性を強調", "page": 5, "url": "#"},
            {"speaker": "○１番（中島議員）", "content": "市民から要望の多い、子供の遊び場の確保について具体策を伺います。", "tag": "子育て", "summary": "公園設置の具体策を質問", "page": 12, "url": "#"}
        ]
        
        for item in data:
            if q in item["content"] or q == "":
                st.markdown(f"""
                <div class="card">
                    <span class="tag">#{item['tag']}</span><br>
                    <strong>{item['speaker']}</strong>
                    <p style="color: #444; margin-top: 10px;"><b>AI要約:</b> {item['summary']}</p>
                    <p>{item['content']}</p>
                    <a class="source" href="{item['url']}">📄 昭島市議会 会議録 (p.{item['page']})</a>
                </div>
                """, unsafe_allow_html=True)

    elif menu == "CityFinanceGlass (予算分析)":
        st.header("📊 予算の使い道を見える化")
        # 簡易予算データ
        df = pd.DataFrame({
            "項目": ["民生費", "総務費", "教育費", "土木費", "衛生費"],
            "金額(億円)": [120, 50, 35, 30, 25]
        })
        fig = px.bar(df, x="項目", y="金額(億円)", color="項目", title="令和6年度 当初予算(主要項目)")
        st.plotly_chart(fig, use_container_width=True)
        st.info("※データ出典：昭島市当初予算書概要")

if __name__ == "__main__":
    main()
