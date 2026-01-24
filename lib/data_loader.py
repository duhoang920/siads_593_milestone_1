# This .py file will be used for functions that help with the import/loading of data files into DataFrames.
# Importing python packages
import pandas as pd

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