import streamlit as st
import hashlib
from utils import data_loader, charts, kanban, reports, notifications

# --- LOGIN CUSTOM ---
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Dizionario utenti: username -> password hash
users = {
    "Fds": hash_password("123"),
    "Mv": hash_password("456"),
    "Fs": hash_password("678"),
    "MR": hash_password("8910")
}

# Input login
st.sidebar.title("🔐 Login")
username = st.sidebar.text_input("Username")
password = st.sidebar.text_input("Password", type="password")

if st.sidebar.button("Login"):
    if username in users and users[username] == hash_password(password):
        st.sidebar.success(f"Benvenuto {username}")

        # --- CARICAMENTO FILE ---
        uploaded_file = st.file_uploader("Carica Excel o scegli Google Sheet", type=["xlsx", "xls"])
        if uploaded_file:
            df = data_loader.load_excel(uploaded_file)
            df = df[df["Assegnato a"] == username]

            st.subheader("📊 Dashboard")
            st.metric("Totale Task", len(df))
            st.metric("Task Completati", len(df[df["Stato"] == "Completato"]))

            # --- GRAFICI ---
            st.pyplot(charts.plot_tasks_per_week(df))
            st.pyplot(charts.plot_velocity(df))
            total_story_points = df["Story Points"].sum()
            st.pyplot(charts.plot_burndown(df, total_story_points))

            # --- KANBAN INTERATTIVO ---
            kanban.show_kanban(df)

            # --- ESPORTAZIONE REPORT ---
            if st.button("📥 Esporta PDF"):
                st.download_button("Scarica PDF", reports.export_pdf(df), "report.pdf")
            if st.button("📥 Esporta Excel"):
                st.download_button("Scarica Excel", reports.export_excel(df), "report.xlsx")

            # --- NOTIFICHE TASK IN RITARDO ---
            overdue = notifications.check_overdue_tasks(df)
            if not overdue.empty:
                st.warning(f"{len(overdue)} task sono in ritardo!")
                # Esempio invio email
                # notifications.send_email(sender, password, receiver, subject, body)
    else:
        st.sidebar.error("Username o password errati")
else:
    st.sidebar.info("Inserisci le credenziali per accedere")
