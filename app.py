import streamlit as st
import json
import hashlib
import io
import pandas as pd
from utils import data_loader, charts, kanban, reports, notifications

# -----------------------------
# LOGIN SICURO
# -----------------------------
st.sidebar.title("🔐 Login")

# Carica utenti da JSON
with open("users.json") as f:
    users = json.load(f)

username = st.sidebar.text_input("Username")
password = st.sidebar.text_input("Password", type="password")

def check_login(username, password):
    hashed_input = hashlib.sha256(password.encode()).hexdigest()
    return users.get(username) == hashed_input

# -----------------------------
# TEMPLATE EXCEL
# -----------------------------
st.sidebar.subheader("📄 Scarica Template Excel")
def generate_template():
    columns = ["Task", "Assegnato a", "Stato", "Story Points", "Scadenza"]
    df_template = pd.DataFrame(columns=columns)
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        df_template.to_excel(writer, index=False, sheet_name="Tasks")
    buffer.seek(0)
    return buffer

st.sidebar.download_button(
    label="📥 Scarica Template Excel",
    data=generate_template(),
    file_name="template_tasks.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

# -----------------------------
# LOGIN E DASHBOARD
# -----------------------------
if st.sidebar.button("Login"):
    if check_login(username, password):
        st.sidebar.success(f"Benvenuto {username}")

        # Caricamento file Excel
        uploaded_file = st.file_uploader("Carica Excel o scegli Google Sheet", type=["xlsx", "xls"])
        if uploaded_file:
            df = data_loader.load_excel(uploaded_file)
            df = df[df["Assegnato a"] == username]

            # DASHBOARD
            st.subheader("📊 Dashboard")
            st.metric("Totale Task", len(df))
            st.metric("Task Completati", len(df[df["Stato"] == "Completato"]))

            # GRAFICI
            st.pyplot(charts.plot_tasks_per_week(df))
            st.pyplot(charts.plot_velocity(df))
            total_story_points = df["Story Points"].sum()
            st.pyplot(charts.plot_burndown(df, total_story_points))

            # KANBAN INTERATTIVO
            kanban.show_kanban(df)

            # ESPORTAZIONE REPORT
            if st.button("📥 Esporta PDF"):
                st.download_button("Scarica PDF", reports.export_pdf(df), "report.pdf")
            if st.button("📥 Esporta Excel"):
                st.download_button("Scarica Excel", reports.export_excel(df), "report.xlsx")

            # NOTIFICHE TASK IN RITARDO
            overdue = notifications.check_overdue_tasks(df)
            if not overdue.empty:
                st.warning(f"{len(overdue)} task sono in ritardo!")
                # Esempio invio email
                # notifications.send_email(sender, password, receiver, subject, body)

    else:
        st.sidebar.error("Username o password errati")
else:
    st.sidebar.info("Inserisci le credenziali per accedere")
