import streamlit as st
import gspread
import json
from google.oauth2.service_account import Credentials
import pandas as pd

# 🔑 Streamlit Secrets から Google 認証情報を取得
service_account_info = json.loads(st.secrets["GCP_CREDENTIALS"])

# 🔹 スコープ設定
scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]
creds = Credentials.from_service_account_info(service_account_info, scopes=scope)

# 📦 Google Sheets API に接続
client = gspread.authorize(creds)

# 📌 Google Sheets の設定
SHEET_NAME = "食材管理"
WORKSHEET_NAME = "Stock"
sheet = client.open(SHEET_NAME).worksheet(WORKSHEET_NAME)

# 📌 データ取得（キャッシュ無効化）
def get_data():
    data = sheet.get_all_records()
    return pd.DataFrame(data)

# 📌 データ更新
def update_data(df):
    sheet.clear()
    sheet.append_row(df.columns.tolist())  # ヘッダー追加
    for row in df.itertuples(index=False):
        sheet.append_row(list(row))

# 📌 食材の追加
def add_ingredient(name, quantity, category):
    df = get_data()
    new_id = int(df["id"].max() + 1) if not df.empty else 1  # `int64` → `int` に変換
    quantity = int(quantity)  # `quantity` も `int` に変換
    new_row = [new_id, name, quantity, category]
    sheet.append_row(new_row)
    st.rerun()  # ✅ 追加後に即座に更新

# 📌 数量変更
def update_quantity(item_id, quantity):
    df = get_data()
    df.loc[df["id"] == item_id, "quantity"] = int(quantity)  # `int64` → `int` に変換
    update_data(df)
    st.rerun()  # ✅ 変更後に即座に更新

# 📌 食材の削除
def delete_ingredient(item_id):
    df = get_data()
    df = df[df["id"] != item_id]
    update_data(df)
    st.rerun()  # ✅ 削除後に即座に更新

# 📌 **CSS で入力欄を小さくする**
st.markdown(
    """
    <style>
        /* 🔹 入力欄を小さくする */
        input[type="text"], select, input[type="number"] {
            max-width: 70px !important; /* 🔹 幅を小さく */
            height: 30px !important; /* 🔹 高さ調整 */
            font-size: 14px !important; /* 🔹 文字サイズ */
        }
        /* 🔹 ボタンのサイズ調整 */
        .stButton > button {
            width: 50px !important;
            height: 30px !important;
            font-size: 12px !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# 📌 メイン画面（食品在庫管理）
st.title("📦 食品在庫管理")

df = get_data()

# 📊 **食材一覧表示**
if not df.empty:
    for _, row in df.iterrows():
        col1, col2, col3 = st.columns([3, 1, 0.8])  # 🔹 削除ボタンの幅を調整
        col1.write(row["name"])
        quantity = col2.number_input("", min_value=0, value=row["quantity"], key=f"qty_{row['id']}", label_visibility="collapsed")
        col3.button("❌", key=f"delete_{row['id']}", on_click=delete_ingredient, args=(row["id"],))

# ➕ **食材追加**
with st.form("add_ingredient_form", clear_on_submit=True):
    col1, col2, col3, col4 = st.columns([3, 3, 1, 1])  # 🔹 入力欄の比率調整
    name = col1.text_input("", placeholder="食材名", max_chars=10, label_visibility="collapsed")
    category = col2.selectbox("", ["主食", "肉類", "野菜類", "その他"], label_visibility="collapsed")
    quantity = col3.number_input("", min_value=1, value=1, label_visibility="collapsed")
    submitted = col4.form_submit_button("追加")

    if submitted and name:
        add_ingredient(name, quantity, category)
