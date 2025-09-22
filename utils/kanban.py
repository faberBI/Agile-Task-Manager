import streamlit as st
from streamlit_sortable import sortable_list

def show_kanban(df):
    stati = df["Stato"].unique()
    columns = st.columns(len(stati))
    kanban_data = {}
    for i, stato in enumerate(stati):
        with columns[i]:
            st.markdown(f"### {stato}")
            tasks = df[df["Stato"]==stato]["Task"].tolist()
            updated_tasks = sortable_list(tasks)
            kanban_data[stato] = updated_tasks
    return kanban_data
