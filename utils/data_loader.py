import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def load_excel(file):
    df = pd.read_excel(file)
    df["Data fine"] = pd.to_datetime(df["Data fine"])
    return df

def load_google_sheet(json_keyfile, sheet_name):
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(json_keyfile, scope)
    client = gspread.authorize(creds)
    sheet = client.open(sheet_name).sheet1
    data = sheet.get_all_records()
    df = pd.DataFrame(data)
    df["Data fine"] = pd.to_datetime(df["Data fine"])
    return df
