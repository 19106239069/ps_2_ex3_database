"""Visualisation functions for NBA analysis."""

import matplotlib.pyplot as plt
import pandas as pd

from matplotlib.axes import Axes
from matplotlib.figure import Figure


def plot_scoring_trends(
    df: pd.DataFrame,
) -> tuple[Figure, Axes]:
    """Plot average NBA game scoring by season."""

    if df.empty:
        raise ValueError("The scoring DataFrame is empty.")

    fig, ax = plt.subplots(figsize=(14, 6))

    ax.plot(
        df["season_start_year"],
        df["avg_total_points"],
        marker="o",
        markersize=3,
        linewidth=1.8,
    )

    ax.set_title(
        "Evolution of Average NBA Game Scoring (1946–2023)",
        fontsize=15,
    )

    ax.set_xlabel("NBA Season", fontsize=12)

    ax.set_ylabel(
        "Average Total Points per Game",
        fontsize=12,
    )

    tick_data = df.iloc[::5]

    ax.set_xticks(tick_data["season_start_year"])

    ax.set_xticklabels(
        tick_data["season"],
        rotation=45,
        ha="right",
    )

    ax.grid(alpha=0.3)

    fig.tight_layout()

    return fig, ax


def plot_three_point_trends(
    df: pd.DataFrame,
) -> tuple[Figure, Axes]:
    """Plot three-point attempt share by season."""

    if df.empty:
        raise ValueError("The three-point DataFrame is empty.")

    # Create a complete year index so missing seasons
    # appear as gaps rather than being connected.
    start_year = int(df["season_start_year"].min())
    end_year = int(df["season_start_year"].max())

    plot_data = df.set_index("season_start_year").reindex(
        range(start_year, end_year + 1)
    )

    fig, ax = plt.subplots(figsize=(14, 6))

    ax.plot(
        plot_data.index,
        plot_data["three_point_attempt_share"],
        marker="o",
        markersize=4,
        linewidth=2,
    )

    ax.set_title(
        "The Three-Point Revolution in NBA History (1985–2023)",
        fontsize=15,
    )

    ax.set_xlabel("NBA Season", fontsize=12)

    ax.set_ylabel(
        "Three-Point Attempts (% of All Field Goal Attempts)",
        fontsize=11,
    )

    tick_years = list(range(start_year, end_year + 1, 5))

    ax.set_xticks(tick_years)

    ax.set_xticklabels(
        [f"{year}-{(year + 1) % 100:02d}" for year in tick_years],
        rotation=45,
        ha="right",
    )

    ax.grid(alpha=0.3)

    fig.tight_layout()

    return fig, ax
