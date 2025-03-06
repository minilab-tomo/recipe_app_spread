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

# ✅ 動作確認
df = get_data()
print(df)
