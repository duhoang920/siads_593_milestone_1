# Importing python packages
import pandas as pd
import numpy as np

def load_csv(file):
    """
        Load a CSV file into a pandas DataFrame.
    
        Parameters
        ----------
        file : str or file-like object
            Path to the CSV file or a file-like object.
    
        Returns
        -------
        pandas.DataFrame
            A DataFrame containing the data from the CSV file.
            
    """
    return pd.read_csv(file)


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