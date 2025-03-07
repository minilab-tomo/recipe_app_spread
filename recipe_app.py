import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import json

# 🔑 Streamlit Secrets から Google 認証情報を取得
service_account_info = json.loads(st.secrets["GCP_CREDENTIALS"])
creds = Credentials.from_service_account_info(service_account_info, scopes=[
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
])

# 📦 Google Sheets API に接続
client = gspread.authorize(creds)
SHEET_NAME = "食材管理"
WORKSHEET_NAME = "Stock"
sheet = client.open(SHEET_NAME).worksheet(WORKSHEET_NAME)

def get_data():
    """Google Sheets からデータを取得し、DataFrame に変換"""
    data = sheet.get_all_records()
    return pd.DataFrame(data)

def update_quantity(row_index, new_quantity):
    """Google Sheets の数量を更新"""
    sheet.update_cell(row_index + 2, 3, int(new_quantity))

def add_ingredient(name, quantity, category):
    """新しい食材を追加"""
    new_row = [name, int(quantity), category]
    sheet.append_row(new_row)

def delete_ingredient(row_index):
    """食材を削除"""
    sheet.delete_rows(row_index + 2)

# Streamlit UI
st.title("🥕 食材管理アプリ")

data = get_data()

for index, row in data.iterrows():
    col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
    col1.text(row["name"])
    quantity = col2.number_input("", value=row["quantity"], key=f"qty_{index}", step=1, min_value=0)
    with col3:
        st.button("-", key=f"dec_{index}", on_click=update_quantity, args=(index, row["quantity"] - 1))
        st.button("+", key=f"inc_{index}", on_click=update_quantity, args=(index, row["quantity"] + 1))
    with col4:
        st.button("❌", key=f"del_{index}", on_click=delete_ingredient, args=(index,))

st.subheader("新しい食材を追加")
col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
with col1:
    new_name = st.text_input("", placeholder="食材名")
with col2:
    new_category = st.selectbox("", ["主食", "肉類", "野菜類", "その他"], index=0)
with col3:
    new_quantity = st.number_input("", min_value=1, step=1, value=1)
with col4:
    st.button("➕", on_click=add_ingredient, args=(new_name, new_quantity, new_category))


# import streamlit as st
# import gspread
# from google.oauth2.service_account import Credentials
# import pandas as pd
# import json

# # 🔑 Streamlit Secrets から Google 認証情報を取得
# service_account_info = json.loads(st.secrets["GCP_CREDENTIALS"])
# creds = Credentials.from_service_account_info(service_account_info, scopes=["https://www.googleapis.com/auth/spreadsheets"])

# # 📦 Google Sheets API に接続
# client = gspread.authorize(creds)
# SHEET_NAME = "食材管理"
# WORKSHEET_NAME = "Stock"
# sheet = client.open(SHEET_NAME).worksheet(WORKSHEET_NAME)

# def get_data():
#     """Google Sheets からデータを取得し、DataFrame に変換"""
#     data = sheet.get_all_records()
#     return pd.DataFrame(data)

# def update_quantity(row_index, new_quantity):
#     """Google Sheets の数量を更新"""
#     sheet.update_cell(row_index + 2, 3, int(new_quantity))

# def add_ingredient(name, quantity, category):
#     """新しい食材を追加"""
#     new_row = [name, int(quantity), category]
#     sheet.append_row(new_row)

# def delete_ingredient(row_index):
#     """食材を削除"""
#     sheet.delete_rows(row_index + 2)

# # Streamlit UI
# st.title("🥕 食材管理アプリ")

# data = get_data()

# for index, row in data.iterrows():
#     col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
#     col1.text(row["name"])
#     quantity = col2.number_input("", value=row["quantity"], key=f"qty_{index}", step=1, min_value=0)
#     with col3:
#         st.button("-", key=f"dec_{index}", on_click=update_quantity, args=(index, row["quantity"] - 1))
#         st.button("+", key=f"inc_{index}", on_click=update_quantity, args=(index, row["quantity"] + 1))
#     with col4:
#         st.button("❌", key=f"del_{index}", on_click=delete_ingredient, args=(index,))

# st.subheader("新しい食材を追加")
# col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
# with col1:
#     new_name = st.text_input("", placeholder="食材名")
# with col2:
#     new_category = st.selectbox("", ["主食", "肉類", "野菜類", "その他"], index=0)
# with col3:
#     new_quantity = st.number_input("", min_value=1, step=1, value=1)
# with col4:
#     st.button("➕", on_click=add_ingredient, args=(new_name, new_quantity, new_category))



import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import json

# 🔑 Streamlit Secrets から Google 認証情報を取得
service_account_info = json.loads(st.secrets["GCP_CREDENTIALS"])
creds = Credentials.from_service_account_info(service_account_info, scopes=["https://www.googleapis.com/auth/spreadsheets"])

# 📦 Google Sheets API に接続
client = gspread.authorize(creds)
SHEET_NAME = "食材管理"
WORKSHEET_NAME = "Stock"
sheet = client.open(SHEET_NAME).worksheet(WORKSHEET_NAME)

def get_data():
    """Google Sheets からデータを取得し、DataFrame に変換"""
    data = sheet.get_all_records()
    return pd.DataFrame(data)

def update_quantity(row_index, new_quantity):
    """Google Sheets の数量を更新"""
    sheet.update_cell(row_index + 2, 3, int(new_quantity))

def add_ingredient(name, quantity, category):
    """新しい食材を追加"""
    new_row = [name, int(quantity), category]
    sheet.append_row(new_row)

def delete_ingredient(row_index):
    """食材を削除"""
    sheet.delete_rows(row_index + 2)

# Streamlit UI
st.title("🥕 食材管理アプリ")

data = get_data()

for index, row in data.iterrows():
    col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
    col1.text(row["name"])
    quantity = col2.number_input("", value=row["quantity"], key=f"qty_{index}", step=1, min_value=0)
    if col3.button("-", key=f"dec_{index}"):
        update_quantity(index, row["quantity"] - 1)
    if col3.button("+", key=f"inc_{index}"):
        update_quantity(index, row["quantity"] + 1)
    if col4.button("❌", key=f"del_{index}"):
        delete_ingredient(index)
        st.experimental_rerun()

st.subheader("新しい食材を追加")
new_name = st.text_input("食材名")
new_category = st.selectbox("カテゴリ", ["主食", "肉類", "野菜類", "その他"])
new_quantity = st.number_input("数量", min_value=1, step=1)

if st.button("➕"):
    add_ingredient(new_name, new_quantity, new_category)
    st.experimental_rerun()



# import streamlit as st
# import gspread
# import json
# from google.oauth2.service_account import Credentials
# import pandas as pd

# # 🔑 Streamlit Secrets から Google 認証情報を取得
# service_account_info = json.loads(st.secrets["GCP_CREDENTIALS"])
# scope = [
#     "https://www.googleapis.com/auth/spreadsheets",
#     "https://www.googleapis.com/auth/drive.file",
#     "https://www.googleapis.com/auth/drive"
# ]
# creds = Credentials.from_service_account_info(service_account_info, scopes=scope)
# client = gspread.authorize(creds)

# # 📌 Google Sheets の設定
# SHEET_NAME = "食材管理"
# WORKSHEET_NAME = "Stock"
# sheet = client.open(SHEET_NAME).worksheet(WORKSHEET_NAME)

# # 📌 データ取得
# def get_data():
#     data = sheet.get_all_records()
#     return pd.DataFrame(data)

# # 📌 データ更新
# def update_data(df):
#     sheet.clear()
#     sheet.append_row(df.columns.tolist())  # ヘッダー追加
#     for row in df.itertuples(index=False):
#         sheet.append_row(list(row))

# # 📌 食材の追加
# def add_ingredient(name, quantity, category):
#     df = get_data()
#     new_id = int(df["id"].max() + 1) if not df.empty else 1
#     quantity = int(quantity)
#     new_row = [new_id, name, quantity, category]
#     sheet.append_row(new_row)
#     st.rerun()

# # 📌 数量変更
# def update_quantity(item_id, quantity):
#     df = get_data()
#     df.loc[df["id"] == item_id, "quantity"] = int(quantity)
#     update_data(df)
#     st.rerun()

# # 📌 食材の削除
# def delete_ingredient(item_id):
#     df = get_data()
#     df = df[df["id"] != item_id]
#     update_data(df)
#     st.rerun()

# # **📌 CSS を適用**
# st.markdown(
#     """
#     <style>
#         /* 🔹 入力欄を小さくする */
#         input[type="text"], select, input[type="number"] {
#             max-width: 60px !important; /* 幅を小さく */
#             height: 25px !important; /* 高さを小さく */
#             font-size: 14px !important; /* 文字サイズ */
#         }
#         /* 🔹 ボタンのサイズ調整 */
#         .stButton > button {
#             width: 50px !important;
#             height: 30px !important;
#             font-size: 12px !important;
#         }
#         /* 🔹 数量変更と削除ボタンを揃える */
#         .stNumberInput, .stButton {
#             display: flex;
#             align-items: center;
#         }
#     </style>
#     """,
#     unsafe_allow_html=True
# )

# # 📌 **UIの表示**
# st.title("📦 食品在庫管理")

# df = get_data()

# # 📊 **食材一覧表示**
# if not df.empty:
#     for _, row in df.iterrows():
#         col1, col2, col3 = st.columns([2, 1, 1])  # 📌 削除ボタンの幅調整
#         col1.write(row["name"])
#         quantity = col2.number_input("", min_value=0, value=row["quantity"], key=f"qty_{row['id']}", label_visibility="collapsed")
#         col3.button("❌", key=f"delete_{row['id']}", on_click=delete_ingredient, args=(row["id"],))

# # ➕ **食材追加**
# with st.form("add_ingredient_form", clear_on_submit=True):
#     col1, col2, col3, col4 = st.columns([2, 2, 1, 1])  # 📌 入力欄の比率調整
#     name = col1.text_input("", placeholder="食材名", max_chars=10, label_visibility="collapsed")
#     category = col2.selectbox("", ["主食", "肉類", "野菜類", "その他"], label_visibility="collapsed")
#     quantity = col3.number_input("", min_value=1, value=1, label_visibility="collapsed")
#     submitted = col4.form_submit_button("追加")

#     if submitted and name:
#         add_ingredient(name, quantity, category)
