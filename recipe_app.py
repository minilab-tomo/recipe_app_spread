import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

# 🔑 Google Sheets API 認証
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_file("credentials.json", scopes=scope)
client = gspread.authorize(creds)

# 📦 Google Sheets を開く
SHEET_NAME = "食材管理"
WORKSHEET_NAME = "Stock"
sheet = client.open(SHEET_NAME).worksheet(WORKSHEET_NAME)

# 📌 データ取得
def get_data():
    data = sheet.get_all_records()
    return pd.DataFrame(data)

# 📌 データ更新（Google Sheetsへ反映）
def update_data(df):
    sheet.clear()
    sheet.append_row(df.columns.tolist())  # ヘッダーを追加
    for row in df.itertuples(index=False):
        sheet.append_row(list(row))

# 📌 食材の追加
def add_ingredient(name, quantity, category):
    df = get_data()
    new_id = int(df["id"].max()) + 1 if not df.empty else 1
    new_row = [int(new_id), name, int(quantity), category]
    sheet.append_row(new_row)

# 📌 数量変更
def update_quantity(item_id, new_quantity):
    df = get_data()
    df.loc[df["id"] == item_id, "quantity"] = int(new_quantity)
    update_data(df)

# 📌 食材の削除
def delete_ingredient(item_id):
    df = get_data()
    df = df[df["id"] != item_id]
    update_data(df)

# 📌 メイン画面（食品在庫管理）
st.title("📦 食品在庫管理")

# 🛒 データ取得
df = get_data()

# 📊 食材一覧表示（横並び & 高さを揃える）
if not df.empty:
    for _, row in df.iterrows():
        col1, col2, col3 = st.columns([5, 3, 2])  # 列の比率を調整
        with col1:
            st.write(row["name"])
        with col2:
            new_quantity = st.number_input(
                "", min_value=0, value=int(row["quantity"]), key=f"qty_{row['id']}",
                label_visibility="collapsed"
            )
            if new_quantity != row["quantity"]:
                update_quantity(row["id"], new_quantity)
        with col3:
            st.button("❌", key=f"delete_{row['id']}", on_click=delete_ingredient, args=(row["id"],))

# ➕ 食材追加（全要素の高さを完全に揃える）
with st.form("add_ingredient_form"):
    col1, col2, col3, col4 = st.columns([4, 3, 3, 2])  # 列の比率を調整
    with col1:
        name = st.text_input("", placeholder="食材名", label_visibility="collapsed")  # 高さ統一
    with col2:
        category = st.selectbox("", ["主食", "肉類", "野菜類", "その他"], index=0, label_visibility="collapsed")  # 高さ統一
    with col3:
        quantity = st.number_input("", min_value=1, value=1, label_visibility="collapsed")  # 高さ統一
    with col4:
        submitted = st.form_submit_button("追加", use_container_width=True)  # ボタンの高さ統一
    if submitted:
        add_ingredient(name, quantity, category)
        st.success(f"✅ {name} を追加しました！")
        st.rerun()


# import streamlit as st
# import gspread
# from google.oauth2.service_account import Credentials
# import pandas as pd

# # 🔑 Google Sheets API 認証
# scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
# creds = Credentials.from_service_account_file("credentials.json", scopes=scope)
# client = gspread.authorize(creds)

# # 📦 Google Sheets を開く
# SHEET_NAME = "食材管理"
# WORKSHEET_NAME = "Stock"
# sheet = client.open(SHEET_NAME).worksheet(WORKSHEET_NAME)

# # 📌 データ取得
# def get_data():
#     data = sheet.get_all_records()
#     return pd.DataFrame(data)

# # 📌 データ更新（Google Sheetsへ反映）
# def update_data(df):
#     sheet.clear()
#     sheet.append_row(df.columns.tolist())  # ヘッダーを追加
#     for row in df.itertuples(index=False):
#         sheet.append_row(list(row))

# # 📌 食材の追加
# def add_ingredient(name, quantity, category):
#     df = get_data()
#     new_id = int(df["id"].max()) + 1 if not df.empty else 1
#     new_row = [int(new_id), name, int(quantity), category]
#     sheet.append_row(new_row)

# # 📌 数量変更
# def update_quantity(item_id, new_quantity):
#     df = get_data()
#     df.loc[df["id"] == item_id, "quantity"] = int(new_quantity)
#     update_data(df)

# # 📌 食材の削除
# def delete_ingredient(item_id):
#     df = get_data()
#     df = df[df["id"] != item_id]
#     update_data(df)

# # 📌 メイン画面（食品在庫管理）
# st.title("📦 食品在庫管理")

# # 🛒 データ取得
# df = get_data()

# # 📊 食材一覧表示（横並び & 高さを揃える）
# if not df.empty:
#     for _, row in df.iterrows():
#         col1, col2, col3 = st.columns([5, 3, 2])  # 列の比率を調整
#         with col1:
#             st.write(row["name"])
#         with col2:
#             new_quantity = st.number_input(
#                 "", min_value=0, value=int(row["quantity"]), key=f"qty_{row['id']}",
#                 label_visibility="collapsed"
#             )
#             if new_quantity != row["quantity"]:
#                 update_quantity(row["id"], new_quantity)
#         with col3:
#             st.button("❌", key=f"delete_{row['id']}", on_click=delete_ingredient, args=(row["id"],))

# # ➕ 食材追加（高さを揃えて一列に）
# with st.form("add_ingredient_form"):
#     col1, col2, col3, col4 = st.columns([5, 3, 3, 2])  # 列幅を統一
#     with col1:
#         name = st.text_input("", placeholder="食材名", label_visibility="collapsed")  # 高さ調整
#     with col2:
#         category = st.selectbox("", ["主食", "肉類", "野菜類", "その他"], index=None, placeholder="カテゴリ名")  # 高さ調整
#     with col3:
#         quantity = st.number_input("", min_value=1, value=1, label_visibility="collapsed")  # 高さ調整
#     with col4:
#         st.markdown("<br>", unsafe_allow_html=True)  # ボタンを他と高さを揃えるための空行
#         submitted = st.form_submit_button("追加")
#     if submitted:
#         add_ingredient(name, quantity, category)
#         st.success(f"✅ {name} を追加しました！")
#         st.rerun()





# import streamlit as st
# import gspread
# from google.oauth2.service_account import Credentials
# import pandas as pd

# # 🔑 Google Sheets API 認証
# scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
# creds = Credentials.from_service_account_file("credentials.json", scopes=scope)
# client = gspread.authorize(creds)

# # 📦 Google Sheets を開く
# SHEET_NAME = "食材管理"
# WORKSHEET_NAME = "Stock"
# sheet = client.open(SHEET_NAME).worksheet(WORKSHEET_NAME)

# # 📌 データ取得
# def get_data():
#     data = sheet.get_all_records()
#     return pd.DataFrame(data)

# # 📌 データ更新（Google Sheetsへ反映）
# def update_data(df):
#     sheet.clear()
#     sheet.append_row(df.columns.tolist())  # ヘッダーを追加
#     for row in df.itertuples(index=False):
#         sheet.append_row(list(row))

# # 📌 食材の追加
# def add_ingredient(name, quantity, category):
#     df = get_data()
#     new_id = int(df["id"].max()) + 1 if not df.empty else 1
#     new_row = [int(new_id), name, int(quantity), category]
#     sheet.append_row(new_row)

# # 📌 数量変更
# def update_quantity(item_id, new_quantity):
#     df = get_data()
#     df.loc[df["id"] == item_id, "quantity"] = int(new_quantity)
#     update_data(df)

# # 📌 食材の削除
# def delete_ingredient(item_id):
#     df = get_data()
#     df = df[df["id"] != item_id]
#     update_data(df)

# # 📌 メイン画面（食品在庫管理）
# st.title("📦 食品在庫管理")

# # 🛒 データ取得
# df = get_data()

# # 📊 食材一覧表示（横並び & 高さを揃える）
# if not df.empty:
#     for _, row in df.iterrows():
#         col1, col2, col3 = st.columns([5, 3, 2])  # 列の比率を調整
#         with col1:
#             st.write(row["name"])
#         with col2:
#             new_quantity = st.number_input(
#                 "", min_value=0, value=int(row["quantity"]), key=f"qty_{row['id']}",
#                 label_visibility="collapsed"
#             )
#             if new_quantity != row["quantity"]:
#                 update_quantity(row["id"], new_quantity)
#         with col3:
#             st.button("❌", key=f"delete_{row['id']}", on_click=delete_ingredient, args=(row["id"],))

# # ➕ 食材追加
# with st.form("add_ingredient_form"):
#     col1, col2, col3 = st.columns([5, 3, 2])  # 追加フォームのレイアウトも統一
#     with col1:
#         name = st.text_input("食材名")
#     with col2:
#         quantity = st.number_input("", min_value=1, value=1, label_visibility="collapsed")
#     with col3:
#         submitted = st.form_submit_button("追加")
#     if submitted:
#         add_ingredient(name, quantity, "その他")  # デフォルトカテゴリを設定
#         st.success(f"✅ {name} を追加しました！")
#         st.rerun()




# # import streamlit as st
# # import gspread
# # from google.oauth2.service_account import Credentials
# # import pandas as pd

# # # 🔑 Google Sheets API 認証
# # scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
# # creds = Credentials.from_service_account_file("credentials.json", scopes=scope)
# # client = gspread.authorize(creds)

# # # 📦 Google Sheets を開く
# # SHEET_NAME = "食材管理"
# # WORKSHEET_NAME = "Stock"
# # sheet = client.open(SHEET_NAME).worksheet(WORKSHEET_NAME)

# # # 📌 データ取得
# # def get_data():
# #     data = sheet.get_all_records()
# #     return pd.DataFrame(data)

# # # 📌 データ更新（Google Sheetsへ反映）
# # def update_data(df):
# #     sheet.clear()
# #     sheet.append_row(df.columns.tolist())  # ヘッダーを追加
# #     for row in df.itertuples(index=False):
# #         sheet.append_row(list(row))

# # # 📌 食材の追加
# # def add_ingredient(name, quantity, category):
# #     df = get_data()
# #     new_id = int(df["id"].max()) + 1 if not df.empty else 1
# #     new_row = [int(new_id), name, int(quantity), category]
# #     sheet.append_row(new_row)

# # # 📌 数量変更
# # def update_quantity(item_id, new_quantity):
# #     df = get_data()
# #     df.loc[df["id"] == item_id, "quantity"] = int(new_quantity)
# #     update_data(df)

# # # 📌 食材の削除
# # def delete_ingredient(item_id):
# #     df = get_data()
# #     df = df[df["id"] != item_id]
# #     update_data(df)

# # # 📌 メイン画面（食品在庫管理）
# # st.title("📦 食品在庫管理")

# # # 🛒 データ取得
# # df = get_data()

# # # 📊 食材一覧表示
# # if not df.empty:
# #     for _, row in df.iterrows():
# #         col1, col2, col3 = st.columns([4, 3, 3])
# #         col1.write(row["name"])
# #         new_quantity = col2.number_input(
# #             "", min_value=0, value=int(row["quantity"]), key=f"qty_{row['id']}")
# #         if new_quantity != row["quantity"]:
# #             update_quantity(row["id"], new_quantity)
# #         col3.button("❌ 削除", key=f"delete_{row['id']}", on_click=delete_ingredient, args=(row["id"],))

# # # ➕ 食材追加
# # with st.form("add_ingredient_form"):
# #     name = st.text_input("食材名")
# #     quantity = st.number_input("", min_value=1, value=1)
# #     category = st.selectbox("カテゴリ", ["主食", "肉類", "野菜類", "その他"])
# #     submitted = st.form_submit_button("追加")
# #     if submitted:
# #         add_ingredient(name, quantity, category)
# #         st.success(f"✅ {name} を追加しました！")
# #         st.rerun()





# # import streamlit as st
# # import gspread
# # from google.oauth2.service_account import Credentials
# # import pandas as pd

# # # 🔑 Google Sheets API 認証
# # scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
# # creds = Credentials.from_service_account_file("credentials.json", scopes=scope)
# # client = gspread.authorize(creds)

# # # 📦 Google Sheets を開く
# # SHEET_NAME = "食材管理"
# # WORKSHEET_NAME = "Stock"
# # sheet = client.open(SHEET_NAME).worksheet(WORKSHEET_NAME)

# # # 📌 データ取得
# # def get_data():
# #     data = sheet.get_all_records()
# #     return pd.DataFrame(data)

# # # 📌 データ更新（Google Sheetsへ反映）
# # def update_data(df):
# #     sheet.clear()
# #     sheet.append_row(df.columns.tolist())  # ヘッダーを追加
# #     for row in df.itertuples(index=False):
# #         sheet.append_row(list(row))

# # # 📌 食材の追加
# # def add_ingredient(name, quantity, category):
# #     df = get_data()
# #     new_id = int(df["id"].max()) + 1 if not df.empty else 1
# #     new_row = [int(new_id), name, int(quantity), category]
# #     sheet.append_row(new_row)

# # # 📌 数量変更
# # def update_quantity(item_id, new_quantity):
# #     df = get_data()
# #     df.loc[df["id"] == item_id, "quantity"] = int(new_quantity)
# #     update_data(df)

# # # 📌 食材の削除
# # def delete_ingredient(item_id):
# #     df = get_data()
# #     df = df[df["id"] != item_id]
# #     update_data(df)

# # # 📌 メイン画面（食品在庫管理）
# # st.title("📦 食品在庫管理")

# # # 🛒 データ取得
# # df = get_data()

# # # 📊 食材一覧表示
# # if not df.empty:
# #     for _, row in df.iterrows():
# #         col1, col2, col3 = st.columns([4, 3, 3])
# #         col1.write(row["name"])
# #         new_quantity = col2.number_input(
# #             "数量", min_value=0, value=int(row["quantity"]), key=f"qty_{row['id']}")
# #         if new_quantity != row["quantity"]:
# #             update_quantity(row["id"], new_quantity)
# #         col3.button("❌ 削除", key=f"delete_{row['id']}", on_click=delete_ingredient, args=(row["id"],))

# # # ➕ 食材追加
# # with st.form("add_ingredient_form"):
# #     name = st.text_input("食材名")
# #     quantity = st.number_input("数量", min_value=1, value=1)
# #     category = st.selectbox("カテゴリ", ["主食", "肉類", "野菜類", "その他"])
# #     submitted = st.form_submit_button("追加")
# #     if submitted:
# #         add_ingredient(name, quantity, category)
# #         st.success(f"✅ {name} を追加しました！")
# #         st.rerun()
