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
    df_drop_cols = df.dropna(how='all')
    return df_drop_cols

def remove_rows(df):
    """
        Removes all empty rows in a DataFrame.
    
        Parameters
        ----------
        pandas.DataFrame
            A DataFrame containing all original rows
    
        Returns
        -------
        pandas.DataFrame
            A DataFrame containing non-empty rows.
    """
    df_drop_rows = df.dropna(axis=0, how='all')
    return df_drop_rows

def df_formater(df):
    df.insert(loc=0, column='State', value=" ")
    check_list = ['Total population', 'Estimate', 'Margin of Error']
    fill_value = None
    for index, row in df.iterrows():
        value = row['Label (Grouping)'].lstrip()
        # print(value)
        if value not in check_list:
            fill_value = value
            # print(fill_value)
            df.at[index, 'State'] = fill_value
        elif value in check_list:
            fill_value2 = fill_value
            df.at[index, 'State'] = fill_value2          
        
    return df