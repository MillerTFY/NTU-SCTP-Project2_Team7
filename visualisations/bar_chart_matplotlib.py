# visualisations/bar_chart_matplotlib.py
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from config import query_model, BQ_DATASET, BQ_TABLE

def plot_top_5_songs():
    # 1. Query your dbt model in BigQuery
    sql = f"""
        SELECT track_name,artist_name, count(recording_msid) AS play_count  
        FROM `{BQ_DATASET}.{BQ_TABLE}`
        GROUP BY track_name,artist_name
        ORDER BY play_count DESC LIMIT 5
    """
    df = query_model(sql)
    print(df)

    # 2. Plot
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle("Top 5 Songs Listened", fontsize=16, fontweight="bold")

    # --- Bar chart 1: play count by track ---
    axes[0].bar(df["track_name"], df["play_count"], color="#4A90D9", edgecolor="white")
    axes[0].set_title("Play Count by Track")
    axes[0].set_xlabel("Track Name")
    axes[0].set_ylabel("Number of Times Listened")
    axes[0].tick_params(axis="x", rotation=90)

    # --- Bar chart 2: play count by artist ---
    axes[1].bar(df["artist_name"], df["play_count"], color="#50C878", edgecolor="white")
    axes[1].set_title("Play Count by Artist")
    axes[1].set_xlabel("Artist Name")
    axes[1].set_ylabel("Number of Times Listened")
    axes[1].yaxis.set_major_formatter(mticker.FuncFormatter(
        lambda x, _: f"{x:,.0f}"
    ))
    axes[1].tick_params(axis="x", rotation=90)

    plt.tight_layout()
    plt.savefig("../visualisations/top-5-songs.png", dpi=150, bbox_inches="tight")
    plt.show()
    print("Chart saved to visualisations/top-5-songs.png")

if __name__ == "__main__":
    plot_top_5_songs()