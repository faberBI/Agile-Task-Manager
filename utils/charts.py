import matplotlib.pyplot as plt

def plot_tasks_per_week(df):
    df["Settimana"] = df["Data fine"].dt.isocalendar().week
    tasks_per_week = df.groupby("Settimana").size()
    fig, ax = plt.subplots()
    tasks_per_week.plot(kind="bar", ax=ax)
    ax.set_ylabel("Numero task")
    ax.set_xlabel("Settimana")
    return fig

def plot_velocity(df):
    df["Settimana"] = df["Data fine"].dt.isocalendar().week
    velocity = df[df["Stato"]=="Completato"].groupby("Settimana")["Story Points"].sum()
    fig, ax = plt.subplots()
    velocity.plot(marker="o", ax=ax)
    ax.set_ylabel("Story Points")
    ax.set_xlabel("Settimana")
    return fig

def plot_burndown(df, total_story_points):
    df_sorted = df.sort_values("Data fine")
    df_sorted["Story Points"] = df_sorted["Story Points"].fillna(0)
    completed_cumsum = df_sorted["Story Points"].cumsum()
    remaining = total_story_points - completed_cumsum
    fig, ax = plt.subplots()
    ax.plot(df_sorted["Data fine"], remaining, marker="o")
    ax.set_ylabel("Story Points Rimanenti")
    ax.set_xlabel("Data")
    ax.set_title("Burn-down Chart")
    return fig
