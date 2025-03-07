import streamlit as st
import gspread
import json
from google.oauth2.service_account import Credentials
import pandas as pd

# バージョン1.0.4 -> 1.0.5 (実質) 諦めない！
# ✅ 削除ボタンを右に配置
# ✅ 数量の±ボタンを復元
# ✅ 食品追加欄を1列に並べる
# ✅ レイアウトを微調整

# 🔑 Streamlit Secrets から Google 認証情報を取得
service_account_info = json.loads(st.secrets["GCP_CREDENTIALS"])
scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]
creds = Credentials.from_service_account_info(service_account_info, scopes=scopes)
client = gspread.authorize(creds)

# 📌 Google Sheets の設定
SHEET_NAME = "食材管理"
WORKSHEET_NAME = "Stock"
sheet = client.open(SHEET_NAME).worksheet(WORKSHEET_NAME)

# 📌 データ取得
def get_data():
    data = sheet.get_all_records()
    return pd.DataFrame(data)

# 📌 データ更新
def update_data(df):
    sheet.clear()
    sheet.append_row(df.columns.tolist())  # ヘッダー
    for row in df.itertuples(index=False):
        sheet.append_row(list(row))

# 📌 食材の追加
def add_ingredient(name, quantity, category):
    df = get_data()
    # 新しいIDを生成
    if not df.empty:
        new_id = int(df["id"].max() + 1)
    else:
        new_id = 1
    quantity = int(quantity)
    new_row = [new_id, name, quantity, category]
    sheet.append_row(new_row)
    st.rerun()

# 📌 数量変更（±ボタン）
def change_quantity(item_id, change):
    df = get_data()
    df.loc[df["id"] == item_id, "quantity"] += change
    df.loc[df["quantity"] < 0, "quantity"] = 0  # マイナス防止
    update_data(df)
    st.rerun()

# 📌 食材の削除
def delete_ingredient(item_id):
    df = get_data()
    df = df[df["id"] != item_id]
    update_data(df)
    st.rerun()

# **📌 CSS を適用**
st.markdown(
    """
    <style>
        /* ======= 全体レイアウト調整 ======= */
        input[type="text"], select, input[type="number"] {
            max-width: 70px !important; /* 幅 */
            height: 28px !important;    /* 高さ */
            font-size: 14px !important;
        }

        .stButton > button {
            width: 50px !important;
            height: 30px !important;
            font-size: 14px !important;
            background-color: #4CAF50;
            color: white;
            border-radius: 5px;
        }

        /* 食材一覧の行で、削除ボタンを右に寄せたい場合はcolumnsで調整 */
        /* ±ボタンもinlineで表示する */
        .qty-buttons {
            display: flex;
            gap: 3px;
            align-items: center;
        }

        /* 新規追加欄を1行にする: columnsで配置しやすくする */
    </style>
    """,
    unsafe_allow_html=True
)

# 📌 タイトル
st.title("📦 食品在庫管理 v1.0.4");

# 📌 データ読み込み
df = get_data()

# 📊 食材一覧
if not df.empty:
    for _, row in df.iterrows():
        # columns: [Name(3), quantity display & ±(2), delete(1)]
        c1, c2, c3 = st.columns([3,3,1])
        c1.write(row["name"])
        with c2:
            # 数量表示 & ±
            st.write(f"数量: {row['quantity']}")
            with st.container():
                colA, colB = st.columns([1,1])
                if colA.button("-", key=f"minus_{row['id']}"):
                    change_quantity(row["id"], -1)
                if colB.button("+", key=f"plus_{row['id']}"):
                    change_quantity(row["id"], 1)
        c3.button("❌", key=f"del_{row['id']}", on_click=delete_ingredient, args=(row["id"],))

# ➕ 食材追加(1列)
with st.form("add_ingredient_form", clear_on_submit=True):
    col1, col2, col3, col4 = st.columns([2,2,2,1])
    name = col1.text_input("", placeholder="食材名", max_chars=10, label_visibility="collapsed")
    category = col2.selectbox("", ["主食", "肉類", "野菜類", "その他"], label_visibility="collapsed")
    quantity = col3.number_input("", min_value=1, value=1, label_visibility="collapsed")
    submitted = col4.form_submit_button("➕")

    if submitted and name:
        add_ingredient(name, quantity, category)
