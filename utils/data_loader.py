import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def load_google_sheet(json_keyfile, sheet_name):
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(json_keyfile, scope)
    client = gspread.authorize(creds)
    sheet = client.open(sheet_name).sheet1
    data = sheet.get_all_records()
    df = pd.DataFrame(data)
    df["Data fine"] = pd.to_datetime(df["Data fine"])
    return df

def load_excel(file):
    df = pd.read_excel(file, engine="openpyxl")
    df["Data fine"] = pd.to_datetime(df["Data fine"])
    return df

import io

def load_excel(uploaded_file):
    in_memory_file = io.BytesIO(uploaded_file.read())
    df = pd.read_excel(in_memory_file, engine="openpyxl")

    # Standardizza nomi colonne
    df.columns = df.columns.str.strip()

    # Standardizza stato
    df["Stato"] = df["Stato"].str.lower().replace({"incorso": "in corso"})

    # Converte Data fine in datetime
    df["Data fine"] = pd.to_datetime(df["Data fine"], errors="coerce", dayfirst=True, format=None)

    return df

