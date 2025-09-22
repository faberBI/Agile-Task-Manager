import streamlit as st
from config.auth_config import authenticator
from utils import data_loader, charts, kanban, reports, notifications

# --- LOGIN ---
name, auth_status, username = authenticator.login("Login", "main")

if auth_status:
    st.sidebar.success(f"Benvenuto {name}")

    # --- CARICAMENTO FILE ---
    uploaded_file = st.file_uploader("Carica Excel o scegli Google Sheet", type=["xlsx", "xls"])
    if uploaded_file:
        df = data_loader.load_excel(uploaded_file)
        df = df[df["Assegnato a"]==name]

        st.subheader("📊 Dashboard")
        st.metric("Totale Task", len(df))
        st.metric("Task Completati", len(df[df["Stato"]=="Completato"]))

        # Grafici
        st.pyplot(charts.plot_tasks_per_week(df))
        st.pyplot(charts.plot_velocity(df))
        total_story_points = df["Story Points"].sum()
        st.pyplot(charts.plot_burndown(df, total_story_points))

        # Kanban interattivo
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
            # Esempio invio email
            # notifications.send_email(sender, password, receiver, subject, body)

elif auth_status == False:
    st.error("Username/password errati")
else:
    st.warning("Inserisci le credenziali")
