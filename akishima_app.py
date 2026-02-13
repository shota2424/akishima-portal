import streamlit as st
import pandas as pd
import sqlite3
import pdfplumber
import requests
import io

# --- ページ設定 ---
st.set_page_config(page_title="昭島市政ポータル v0.1", layout="wide")

# --- データベース準備 ---
def get_connection():
    conn = sqlite3.connect("akishima.db", check_same_thread=False)
    conn.execute("CREATE TABLE IF NOT EXISTS city_data (title TEXT, page INTEGER, content TEXT, url TEXT)")
    return conn

# --- PDF解析エンジン ---
def ingest_pdf(url, title):
    conn = get_connection()
    try:
        response = requests.get(url)
        with pdfplumber.open(io.BytesIO(response.content)) as pdf:
            for i, page in enumerate(pdf.pages):
                text = page.extract_text()
                if text:
                    conn.execute("INSERT INTO city_data VALUES (?, ?, ?, ?)", (title, i + 1, text, url))
        conn.commit()
        return True
    except Exception as e:
        st.error(f"解析エラー: {e}")
        return False

# --- メイン画面 ---
st.title("🏙️ 昭島市政データ基盤 (v0.1)")

menu = st.sidebar.selectbox("メニュー", ["データ検索", "データ取り込み (管理)"])

if menu == "データ取り込み (管理)":
    st.header("⚙️ 本物のPDFを取り込む")
    st.write("昭島市の公式サイトにあるPDFのURLを入力して、基盤に学習させます。")
    
    pdf_url = st.text_input("PDFのURL", "https://www.city.akishima.lg.jp/s036/010/010/010/010/r6yosangaiyo.pdf")
    pdf_title = st.text_input("資料のタイトル", "令和6年度予算概要")
    
    if st.button("このPDFを解析して取り込む"):
        with st.spinner("解析中... 数秒かかります"):
            success = ingest_pdf(pdf_url, pdf_title)
            if success:
                st.success(f"「{pdf_title}」の取り込みが完了しました！")

elif menu == "データ検索":
    st.header("🔍 基盤内データ検索")
    q = st.text_input("検索したいキーワード（例：水道、教育、公園）")
    
    if q:
        conn = get_connection()
        # SQLで本物のデータを検索
        df = pd.read_sql("SELECT * FROM city_data WHERE content LIKE ?", conn, params=(f'%{q}%',))
