# This .py file will be used for functions that help with the data wrangling.
# Importing python packages
import pandas as pd

def remove_cols(df):
    """
        Removes all empty columns in a DataFrame.
    
        Parameters
        ----------
        pandas.DataFrame
            A DataFrame containing all original columns
    
        Returns
        -------
        pandas.DataFrame
            A DataFrame containing non-empty columns.
    """
    df_drop_cols = df.dropna(axis=1, how='all')
    return df_drop_cols

def df_formater(df):
    df.insert(loc=0, column='State', value=True)
    return df