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

def save_df_to_csv(df, file_path):
    df.to_csv(file_path, index=False, encoding='utf-8-sig')
    print(f"Dataframe: {df} has been saved to {file_path}")