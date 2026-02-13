# This .py file will be used for functions that help create the visualizations to support EDA.
# Importing Python packages

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import seaborn as sns

# Visual colors for consistency
ORANGE = "#E56D09" 
TEAL   = "#0F8A83"
RED    = "#C62828"
GREEN  = "#2E7D32"
sns.set_theme(style="white", rc={"axes.grid": False})



# Function to rename key dataframe features to human-readable names

def rename_vis_columns(df):

    rename_map = {

        # -------------------------
        # Health - Overall
        # -------------------------
        "Overall - Diabetes-DataValue": "Diabetes Prev (%)",
        "Overall - Obesity-DataValue": "Obesity Prev (%)",
        "Overall - COPD-DataValue": "COPD Prev (%)",
        "Overall - Asthma-DataValue": "Asthma Prev (%)",
        "Overall - Arthritis-DataValue": "Arthritis Prev (%)",

        # -------------------------
        # Health - Male
        # -------------------------
        "Males - Diabetes-DataValue": "Diabetes Prev (%) (Male)",
        "Males - Obesity-DataValue": "Obesity Prev (%) (Male)",
        "Males - COPD-DataValue": "COPD Prev (%) (Male)",
        "Males - Asthma-DataValue": "Asthma Prev (%) (Male)",
        "Males - Arthritis-DataValue": "Arthritis Prev (%) (Male)",

        # -------------------------
        # Health - Female
        # -------------------------
        "Females - Diabetes-DataValue": "Diabetes Prev (%) (Female)",
        "Females - Obesity-DataValue": "Obesity Prev (%) (Female)",
        "Females - COPD-DataValue": "COPD Prev (%) (Female)",
        "Females - Asthma-DataValue": "Asthma Prev (%) (Female)",
        "Females - Arthritis-DataValue": "Arthritis Prev (%) (Female)",

        # -------------------------
        # Socioeconomic
        # -------------------------
        "est - Median Household Income": "Median Household Income",
        "est - Pop 18 and Over Below Poverty - %": "Below Poverty (%)",
        "est - Pop Uninsured - %": "Uninsured (%)",
        "est - Total Pop": "Total Population",
        "est - Total Pop - Male - %": "Total Population (%) (Male)",
        "est - Total Pop - Female - %":"Total Population (%) (Female)"
    }

    return df.rename(columns=rename_map)

    

# Function to plot a boxplot and a histogram along the same scale


def histogram_boxplot(data, feature, figsize = (12, 7), kde = True, bins = 15):

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
        data = data, x = feature, ax = ax_box2, showmeans = True, color = ORANGE)       # Boxplot will be created and a star will indicate the mean value of the column
    sns.histplot(
        data = data, x = feature, ax = ax_hist2, bins = bins, color = TEAL, kde=kde)
   
    ax_hist2.axvline(
        data[feature].mean(),
        color = "black", 
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


    # Title

    # Main title (figure-level)
    plt.suptitle(
        f"Distribution of {feature} Among Adults",
        fontsize=16,
        fontweight="bold",
        y=0.98
)

# Subtitle (figure-level) 
    fig = plt.gcf()
    fig.text(
        0.5, 0.90,
        "Across the U.S. States in 2022",
        ha="center",
        fontsize=14,
        color="black"
)

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
        corr_method : correlation coefficient method ("pearson", "spearman", "kendall")
 
        Returns
        -------
        None
    """

    ORANGE = "#D35400"
    TEAL = "#0F8A83"
    WHITE = "#FFFFFF"

    custom_cmap = LinearSegmentedColormap.from_list(
        "teal_white_orange",
        [TEAL, WHITE, ORANGE]
)
    
    
    corr_df = select_columns(df, column_names)

    corr_obj = corr_df.corr(method=corr_method)
    print(type(custom_cmap))
    
    plt.figure(figsize=(12,8))
    sns.heatmap(
        corr_obj,
        annot=True,
        fmt=".2f",
        cmap=custom_cmap,
        center=0,
        vmin=-1,
        vmax=1,
        annot_kws={"size": 10}
    )

    plt.xticks(fontsize=12, rotation=45)
    plt.yticks(fontsize=12, rotation=0)
    
     # Main Title 
    plt.suptitle(
        "Spearman Correlation of Chronic Disease Prevalence Among Adults",
        fontsize=16,
        fontweight="bold",
        y=0.80
    )
    # Subtitle
    plt.title(
        "Across the U.S. States in 2022",
        fontsize=14,
        color="black",
        pad=20
    )
    
    
    plt.tight_layout(rect=[0, 0, 1, 0.8])
    plt.show()


# Function to create a Scatter Plot Matrix of key features

def create_splom(df, column_names):
    """
    Create a scatter plot matrix (SPLOM) for selected columns.

    Parameters
        ----------
        df : pandas.DataFrame
        columns : list of column names to run a SPLOM
 
        Returns
        -------
        SPLOM chart

    """
    
    # Assign pairplot to variable 'g'
    g = sns.pairplot(
        df[column_names],
        kind='reg',
        diag_kind="kde",
        plot_kws={
            'ci': None,
            'line_kws':{'color':'gray'},
            "color": TEAL          
        },
        diag_kws={
            "color": ORANGE        
        }
    )
  
    
    g.fig.suptitle(
        "Scatter Plot Matrix of Chronic Disease Prevalence Among Adults",
        fontsize=16,
        fontweight="bold",
        y=0.99
    )
    
    g.fig.text(
        0.5, 0.94,
        "Across the U.S. States in 2022",
        ha="center",
        fontsize=14,
        color="black"
    )
      
    g.fig.subplots_adjust(top=0.90)
    plt.show()


 
# Barplot showing chronic disease prevalence across the top states

def plot_state_prevalence(  
    df,
    state_col="State",
    value_col=None,        
    feature=None,          
    subtitle="Across the U.S. States in 2022",
    top_n=None
):
    
    """
    Create a bar chart showing state-level prevalence for a selected chronic disease.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame containing state-level data.

    state_col : str, default="State"
        Column name representing U.S. states.

    value_col : str
        Column name of the prevalence metric to be plotted 
        (e.g., "Diabetes Prev (%)", "Obesity Prev (%)").

    feature : str, optional
        Human-readable name of the disease used for titles and axis labels 
        (e.g., "Diabetes"). If None, value_col will be used.

    subtitle : str, default="Across the U.S. States in 2022"
        Subtitle displayed below the main chart title.

    top_n : int, default=15
        Number of states to display, sorted by highest prevalence.
        If None, all states are displayed.

    Returns
    -------
    None
        Displays a formatted bar chart.
    """
    

    # Validation to ensure value_col is provided
    if value_col is None:
        raise ValueError("You must pass a value_col (e.g., 'Diabetes Prev (%)').")

    # If feature not provided, fall back to value_col
    if feature is None:
        feature = value_col

    plot_df = df[[state_col, value_col]].copy()
    plot_df[value_col] = pd.to_numeric(plot_df[value_col], errors="coerce")

    plot_df = (
        plot_df
        .dropna(subset=[value_col])
        .sort_values(value_col, ascending=False)
        .head(top_n)
    )

    plt.figure(figsize=(12, 8))

    ax = sns.barplot(
        data=plot_df,
        x=state_col,
        y=value_col,
        color=TEAL,
        alpha=.5  
    )

    
    plt.suptitle(
        f"{feature} Prevalence (%) by Top States",
        fontsize=18,
        fontweight="bold",
        y=0.98
    )

    plt.title(subtitle, fontsize=13, y=0.94)

    
    ax.set_ylabel(f"{feature} Prev. (%)")  
    ax.set_xlabel("")

    plt.xticks(rotation=45, ha="right")

    ax.grid(False)
    sns.despine()

    plt.tight_layout()
    plt.show()




def histogram_boxplot2(data, feature, ax_box, ax_hist, kde = True, bins = 15):
    sns.boxplot(
        data = data, x = feature, ax = ax_box, showmeans = True, color = "#D35400"
    )

    sns.histplot(
        data = data, x = feature, ax = ax_hist, bins = bins, color = TEAL, kde=kde)

    ax_hist.axvline(
        data[feature].mean(),
        color = "green", 
        linestyle = "--",
        label="Mean"
    )                   # Add mean to the histogram
    ax_hist.axvline(
        data[feature].median(), 
        color = "red", 
        linestyle = "--",
        label="Median",
        
    )                   # Add median to the histogram

    ax_hist.legend()
    ax_box.set(xlabel='')
    ax_hist.set(ylabel='Number of States')



def histogram_boxplot_grid(df, features, cols):
    import math
    n_features = len(features)
    rows = math.ceil(n_features / cols)
    
    fig, axes = plt.subplots(nrows=rows*2, 
                             ncols=cols, 
                             figsize = (15,12))
    axes = axes.flatten()

    for i, feature in enumerate(features):
        column_i = i % cols
        row_j = i // cols

        ax_i_box = (row_j * 2 * cols) + column_i
        ax_i_hist = ax_i_box + cols

        ax_box = axes[ax_i_box]
        ax_hist = axes[ax_i_hist]

        ax_box.sharex(ax_hist)

        histogram_boxplot2(df, feature, ax_box, ax_hist)

        ax_box.set_title(f"Distribution of {feature} Among Adults",
                         fontsize=16,
                         fontweight="bold")


    plt.tight_layout()
    plt.subplots_adjust(hspace=0.4)
    plt.show()

        


