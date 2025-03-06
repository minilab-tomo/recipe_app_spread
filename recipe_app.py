import streamlit as st
import gspread
import json  # ← jsonをインポート
from google.oauth2.service_account import Credentials
import pandas as pd

# # 🔑 Streamlit Secrets から Google 認証情報を取得
# service_account_info = json.loads(st.secrets["GCP_CREDENTIALS"])
# creds = Credentials.from_service_account_info(service_account_info)

# # 📦 Google Sheets API に接続
# client = gspread.authorize(creds)

# 🔑 Streamlit Secrets から Google 認証情報を取得
service_account_info = json.loads(st.secrets["GCP_CREDENTIALS"])

# 🔹 **スコープを明示的に設定**
scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]
creds = Credentials.from_service_account_info(service_account_info, scopes=scope)

# 📦 Google Sheets API に接続
client = gspread.authorize(creds)


# 📌 データ取得関数
SHEET_NAME = "食材管理"
WORKSHEET_NAME = "Stock"
sheet = client.open(SHEET_NAME).worksheet(WORKSHEET_NAME)

def get_data():
    """Google Sheets からデータを取得し、DataFrame に変換"""
    data = sheet.get_all_records()
    return pd.DataFrame(data)

def update_data(df):
    """Google Sheets のデータを更新"""
    sheet.clear()
    sheet.append_row(df.columns.tolist())  # ヘッダーを追加
    for row in df.itertuples(index=False):
        sheet.append_row(list(row))

def add_ingredient(name, quantity, category):
    """食材を追加"""
    df = get_data()
    new_id = df["id"].max() + 1 if not df.empty else 1
    new_row = [new_id, name, quantity, category]
    sheet.append_row(new_row)

def update_quantity(item_id, change):
    """数量を変更"""
    df = get_data()
    df.loc[df["id"] == item_id, "quantity"] += change
    df.loc[df["quantity"] < 0, "quantity"] = 0  # マイナス値防止
    update_data(df)

def delete_ingredient(item_id):
    """食材を削除"""
    df = get_data()
    df = df[df["id"] != item_id]
    update_data(df)

# 📌 Streamlit UI
st.title("📦 食品在庫管理")

df = get_data()

# 📊 食材一覧表示
if not df.empty:
    for _, row in df.iterrows():
        col1, col2, col3, col4 = st.columns([4, 2, 2, 2])
        col1.write(row["name"])
        col2.write(f"{row['quantity']}")  # 「数量:」は削除
        col3.button("+", key=f"plus_{row['id']}", on_click=update_quantity, args=(row["id"], 1))
        col3.button("-", key=f"minus_{row['id']}", on_click=update_quantity, args=(row["id"], -1))
        col4.button("❌", key=f"delete_{row['id']}", on_click=delete_ingredient, args=(row["id"],))

# ➕ 食材追加
with st.form("add_ingredient_form"):
    name = st.text_input("", placeholder="食材名")  # 食材名をプレースホルダーに
    category = st.selectbox("", ["主食", "肉類", "野菜類", "その他"], format_func=lambda x: "カテゴリ名" if x == "" else x)
    quantity = st.number_input("", min_value=1, value=1, placeholder="数量")  # 数量のプレースホルダー
    submitted = st.form_submit_button("追加")
    if submitted:
        add_ingredient(name, quantity, category)
        st.success(f"✅ {name} を追加しました！")
        st.rerun()
