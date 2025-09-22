import streamlit as st

def show_kanban(df):
    """
    Kanban semplice senza streamlit-sortable, usando st.columns e checkbox.
    """
    col1, col2, col3 = st.columns(3)
    status_columns = {"Da fare": col1, "In corso": col2, "Completato": col3}

    for status, col in status_columns.items():
        col.subheader(status)
        tasks = df[df["Stato"] == status]["Task"].tolist()
        for task in tasks:
            completed = col.checkbox(task, key=f"{status}_{task}", value=(status=="Completato"))
            if completed and status != "Completato":
                df.loc[df["Task"] == task, "Stato"] = "Completato"

