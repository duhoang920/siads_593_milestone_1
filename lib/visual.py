# This .py file will be used for functions that help create the visualizations to support EDA.
# Importing Python packages

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sb




def plot_scatter_on_axis(
    df,
    x_col: str,
    y_col: str,
    ax,
    title: str | None = None,
    x_label: str | None = None,
    y_label: str | None = None,
):
    """
    Plot a scatter relationship on an existing Matplotlib axis.

    Parameters
    ----------
    df : pandas.DataFrame
        Wide dataframe (one row per state).
    x_col : str
        Predictor column name (e.g., income).
    y_col : str
        Outcome column name (e.g., diabetes prevalence).
    ax : matplotlib.axes.Axes
        Axis to draw on (supports subplot grids).
    title : str, optional
        Subplot title. Defaults to f"{y_col} vs {x_col}".
    x_label : str, optional
        X-axis label. Defaults to x_col (or blank if you prefer).
    y_label : str, optional
        Y-axis label. Defaults to y_col.

    Notes
    -----
    - This function does NOT reshape data.
    - It assumes df[x_col] and df[y_col] are already numeric (or plottable).
    """
    plot_df = df[[x_col, y_col]].dropna()

    sns.scatterplot(
        data=plot_df,
        x=x_col,
        y=y_col,
        ax=ax,
    )

    ax.set_title(title or f"{y_col} vs {x_col}", fontsize=10)
    ax.set_xlabel(x_label if x_label is not None else "")
    ax.set_ylabel(y_label if y_label is not None else y_col)


def plot_scatter_grid(
    df,
    x_cols: list[str],
    y_col: str,
    ncols: int = 3,
    fig_title: str | None = None,
    y_label: str = "Diabetes Prevalence (%)",
):
    """
    Create a small-multiples grid of scatterplots: one predictor per panel.

    Parameters
    ----------
    df : pandas.DataFrame
        Wide dataframe (one row per state).
    x_cols : list[str]
        Predictor columns to iterate over.
    y_col : str
        Outcome column (fixed across panels).
    ncols : int
        Number of columns in the grid.
    fig_title : str, optional
        Title for the entire figure.
    y_label : str
        Common y-axis label.

    Returns
    -------
    matplotlib.figure.Figure
        The created figure (useful for saving).
    """
    n_plots = len(x_cols)
    nrows = (n_plots + ncols - 1) // ncols  # ceiling division

    fig, axes = plt.subplots(nrows, ncols, figsize=(5 * ncols, 4 * nrows))
    axes = axes.flatten() if hasattr(axes, "flatten") else [axes]

    for ax, x_col in zip(axes, x_cols):
        plot_scatter_on_axis(
            df=df,
            x_col=x_col,
            y_col=y_col,
            ax=ax,
            title=x_col,          # short per-panel title
            x_label="",           # keep panels clean
            y_label=y_label,
        )

    # Turn off any unused panels
    for ax in axes[n_plots:]:
        ax.axis("off")

    if fig_title:
        fig.suptitle(fig_title, fontsize=16)

    fig.tight_layout()
    return fig