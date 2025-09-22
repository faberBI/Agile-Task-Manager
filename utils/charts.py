import matplotlib.pyplot as plt
import pandas as pd

def plot_tasks_per_week(df, date_col="Data fine"):
    # Assicurati che la colonna data sia datetime
    df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
    
    # Raggruppa per settimana e conta i task
    tasks_per_week = df.groupby(pd.Grouper(key=date_col, freq="W")).size()
    
    # Crea la figura
    fig, ax = plt.subplots()
    tasks_per_week.plot(kind="bar", ax=ax)
    ax.set_title("Task per settimana")
    ax.set_xlabel("Settimana")
    ax.set_ylabel("Numero Task")
    
    return fig  # ✅ Restituisci la figura


def plot_tasks_per_state(df):
    counts = df["Stato"].value_counts()
    fig, ax = plt.subplots()
    counts.plot(kind="pie", autopct='%1.1f%%', ax=ax)
    ax.set_ylabel("")
    ax.set_title("Task per Stato")
    return fig

def plot_velocity(df):
    df_sorted = df.sort_values("Data fine")
    velocity = df_sorted.groupby("Assegnato a")["Story Points"].sum()
    fig, ax = plt.subplots()
    velocity.plot(kind="bar", ax=ax)
    ax.set_title("Velocity")
    ax.set_ylabel("Story Points")
    return fig

def plot_burndown(df, total_story_points):
    df_sorted = df.sort_values("Data fine")
    completed_points = df_sorted[df_sorted["Stato"].str.lower()=="completato"]["Story Points"].cumsum()
    remaining = total_story_points - completed_points
    fig, ax = plt.subplots()
    ax.plot(remaining.index, remaining.values, marker='o')
    ax.set_title("Burndown Chart")
    ax.set_xlabel("Task completati")
    ax.set_ylabel("Story Points rimanenti")
    return fig

