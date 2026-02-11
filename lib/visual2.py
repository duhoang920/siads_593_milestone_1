# This .py file will be used for functions that help create the visualizations to support EDA.
# Importing Python packages

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# ---- Section 1: Modular Functions ----

# Function to plot a boxplot and a histogram along the same scale

def histogram_boxplot(data, feature, figsize = (12, 7), kde = True, bins = None):

    """
    Boxplot and histogram combined

    data: dataframe
    feature: dataframe column
    figsize: size of figure (default (12, 7))
    kde: whether to show the density curve (default False)
    bins: number of bins for histogram (default None)
    """
 
    f2, (ax_box2, ax_hist2) = plt.subplots(
        nrows = 2,      # Number of rows of the subplot grid = 2
        sharex = True,  # x-axis will be shared among all subplots
        gridspec_kw = {"height_ratios": (0.25, 0.75)},
        figsize = figsize
       
    )                   # Creating the 2 subplots

   
    sns.boxplot(
        data = data, x = feature, ax = ax_box2, showmeans = True, color = "#EC8165"
    )                   # Boxplot will be created and a star will indicate the mean value of the column
    sns.histplot(
        data = data, x = feature, ax = ax_hist2, bins = bins, palette = "#4C72B0"
    ) if bins else sns.histplot(
        data = data, x = feature, kde = kde, ax = ax_hist2
    )                   # For histogram
    ax_hist2.axvline(
        data[feature].mean(),
        color = "green", 
        linestyle = "--",
        label="Mean"
    )                   # Add mean to the histogram
    ax_hist2.axvline(
        data[feature].median(), 
        color = "red", 
        linestyle = "--",
        label="Median",
        
    )                   # Add median to the histogram

    ax_hist2.legend()

    # --- TITLE + LAYOUT LAST ---
    title = f"Distribution of {feature} Across U.S. States"
    f2.suptitle(title, fontsize=14, y=0.93)
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.show()
    plt.close(f2)

     
def select_columns(df, column_names):
    """
        Selects specified columns from a data frame
    
        Parameters
        ----------
        df : pandas.DataFrame
        columns : list of column names to run a correlation 
 
        Returns
        -------
        pandas.DataFrame
            A dataframe with only the columns of interest
            
            
    """
    df_specific_columns = df[column_names]

    return df_specific_columns
    

def create_corrplot(df, column_names, corr_method):
    """
        Create a correlation heatmap for specified columns in a data frame
    
        Parameters
        ----------
        df : pandas.DataFrame
        columns : list of column names to run a correlation 
        corr_method : correlation coefficient method ("pearson", "spearman", "kendall"
 
        Returns
        -------
        None
    """
    
    
    corr_df = select_columns(df, column_names)

    corr_obj = corr_df.corr(method=corr_method)

    
    plt.figure(figsize=(10,8))
    sns.heatmap(
        corr_obj,
        annot=True,
        fmt=".2f",
        cmap="coolwarm",
        center=0
    )
    plt.title(f'{corr_method} Correlation of Chronic Diseases Among Adults Across the U.S. States')
    plt.tight_layout()
    plt.show()

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
    ax: matplotlib.axes.Axes
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

    sns.regplot(
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