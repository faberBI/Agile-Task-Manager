import streamlit as st
import hashlib
import json
import io
import pandas as pd
from utils import charts, kanban, reports, notifications
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# -----------------------------
# LOGIN SICURO
# -----------------------------
st.sidebar.title("🔐 Login")

with open("users.json") as f:
    users = json.load(f)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

def check_login(username, password):
    hashed_input = hashlib.sha256(password.encode()).hexdigest()
    return users.get(username) == hashed_input

if not st.session_state.logged_in:
    username_input = st.sidebar.text_input("Username")
    password_input = st.sidebar.text_input("Password", type="password")
    if st.sidebar.button("Login"):
        if check_login(username_input, password_input):
            st.session_state.logged_in = True
            st.session_state.username = username_input
            st.sidebar.success(f"Benvenuto {username_input}")
        else:
            st.sidebar.error("Username o password errati")
else:
    st.sidebar.success(f"Benvenuto {st.session_state.username}")

# -----------------------------
# TEMPLATE EXCEL
# -----------------------------
st.sidebar.subheader("📄 Scarica Template Excel")
def generate_template():
    columns = ["Task", "Assegnato a", "Stato", "Story Points", "Data fine"]
    df_template = pd.DataFrame(columns=columns)
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        df_template.to_excel(writer, index=False, sheet_name="Tasks")
    buffer.seek(0)
    return buffer

st.sidebar.download_button(
    "📥 Scarica Template Excel",
    data=generate_template(),
    file_name="template_tasks.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

# -----------------------------
# FUNZIONI PER CARICARE DATI
# -----------------------------
def load_excel(uploaded_file):
    in_memory_file = io.BytesIO(uploaded_file.read())
    df = pd.read_excel(in_memory_file, engine="openpyxl")
    df["Data fine"] = pd.to_datetime(df["Data fine"], errors="coerce", dayfirst=True)
    return df

def load_google_sheet(json_keyfile, sheet_name):
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(json_keyfile, scope)
    client = gspread.authorize(creds)
    sheet = client.open(sheet_name).sheet1
    data = sheet.get_all_records()
    df = pd.DataFrame(data)
    df["Data fine"] = pd.to_datetime(df["Data fine"], errors="coerce")
    return df

# -----------------------------
# DASHBOARD APP
# -----------------------------
if st.session_state.logged_in:
    st.subheader("📊 Dashboard")

    # Scegli fonte dati
    data_source = st.radio("Seleziona fonte dati:", ["Excel", "Google Sheet"])
    df = pd.DataFrame()
    
    if data_source == "Excel":
        uploaded_file = st.file_uploader("Carica Excel", type=["xlsx"])
        if uploaded_file:
            df = load_excel(uploaded_file)
    
    elif data_source == "Google Sheet":
        st.info("Serve il file JSON della service account e il nome del Sheet")
        json_file = st.file_uploader("JSON Service Account", type=["json"])
        sheet_name = st.text_input("Nome Sheet")
        if json_file and sheet_name:
            with open("temp_key.json", "wb") as f:
                f.write(json_file.read())
            df = load_google_sheet("temp_key.json", sheet_name)

    if not df.empty:
        df = df[df["Assegnato a"] == st.session_state.username]

        # Metriche principali
        st.metric("Totale Task", len(df))
        st.metric("Task Completati", len(df[df["Stato"].str.lower() == "completato"]))
        st.metric("Story Points Totali", df["Story Points"].sum())

        # Grafici multipli
        st.subheader("📈 Grafici")
        st.pyplot(charts.plot_tasks_per_week(df, date_col="Data fine"))
        st.pyplot(charts.plot_tasks_per_state(df))
        st.pyplot(charts.plot_velocity(df))
        total_story_points = df["Story Points"].sum()
        st.pyplot(charts.plot_burndown(df, total_story_points))

        # Kanban semplice
        kanban.show_kanban(df)

        # Esportazione report
        if st.button("📥 Esporta PDF"):
            st.download_button("Scarica PDF", reports.export_pdf(df), "report.pdf")
        if st.button("📥 Esporta Excel"):
            st.download_button("Scarica Excel", reports.export_excel(df), "report.xlsx")

        # Notifiche task in ritardo
        overdue = notifications.check_overdue_tasks(df)
        if not overdue.empty:
            st.warning(f"{len(overdue)} task sono in ritardo!")
else:
    st.info("Effettua il login per accedere all'app")
