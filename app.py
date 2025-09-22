import streamlit as st
import hashlib
import json
import io
import pandas as pd
import matplotlib.pyplot as plt
from utils import kanban, reports, notifications
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

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def check_login(username, password):
    return users.get(username) == hash_password(password)

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
# FUNZIONI CARICAMENTO DATI
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
    df["Data fine"] = pd.to_datetime(df["Data fine"], errors="coerce", dayfirst=True)
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
        # Filtra per utente loggato
        df = df[df["Assegnato a"] == st.session_state.username]

        # Metriche principali
        st.metric("Totale Task", len(df))
        st.metric("Task Completati", len(df[df["Stato"] == "completato"]))
        st.metric("Story Points Totali", df["Story Points"].sum())

        # -----------------------------
        # GRAFICI
        # -----------------------------
        st.subheader("📈 Grafici")

        # Tasks per settimana
        df["Settimana"] = df["Data fine"].dt.to_period("W").astype(str)
        tasks_week = df.groupby("Settimana").size()
        fig1, ax1 = plt.subplots()
        tasks_week.plot(kind="bar", ax=ax1)
        ax1.set_title("Task per settimana")
        ax1.set_xlabel("Settimana")
        ax1.set_ylabel("Numero Task")
        st.pyplot(fig1)

        # Tasks per Stato
        tasks_state = df["Stato"].value_counts()
        fig2, ax2 = plt.subplots()
        tasks_state.plot(kind="pie", autopct='%1.1f%%', ax=ax2)
        ax2.set_ylabel("")
        ax2.set_title("Task per Stato")
        st.pyplot(fig2)

        # Velocity
        velocity = df.groupby("Assegnato a")["Story Points"].sum()
        fig3, ax3 = plt.subplots()
        velocity.plot(kind="bar", ax=ax3)
        ax3.set_title("Velocity")
        ax3.set_ylabel("Story Points")
        st.pyplot(fig3)

        # Burndown
        df_sorted = df.sort_values("Data fine")
        completed_points = df_sorted[df_sorted["Stato"]=="completato"]["Story Points"].cumsum()
        total_points = df["Story Points"].sum()
        remaining = total_points - completed_points
        fig4, ax4 = plt.subplots()
        ax4.plot(remaining.index, remaining.values, marker='o')
        ax4.set_title("Burndown Chart")
        ax4.set_xlabel("Task completati")
        ax4.set_ylabel("Story Points rimanenti")
        st.pyplot(fig4)

        # -----------------------------
        # Kanban semplice
        # -----------------------------
        kanban.show_kanban(df)

        # -----------------------------
        # Esportazione report
        # -----------------------------
        if st.button("📥 Esporta PDF"):
            st.download_button("Scarica PDF", reports.export_pdf(df), "report.pdf")
        if st.button("📥 Esporta Excel"):
            st.download_button("Scarica Excel", reports.export_excel(df), "report.xlsx")

        # -----------------------------
        # Notifiche task in ritardo
        # -----------------------------
        overdue = notifications.check_overdue_tasks(df)
        if not overdue.empty:
            st.warning(f"{len(overdue)} task sono in ritardo!")
else:
    st.info("Effettua il login per accedere all'app")
