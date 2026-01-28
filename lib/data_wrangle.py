# This .py file will be used for functions that help with the data wrangling.
# Importing python packages
import pandas as pd

def add_cols(df, col_names, start_position=0):
    """
        Inserts a list of new column(s) at the specified position, shiftin existing columns to the right.
        Sets the default value of the newly added column(s) as " ".        
    
        Parameters
        ----------
        pandas.DataFrame
            A DataFrame containing all original rows.
        string.list
            A list of column names.
        integer
            A starting column position.
    
        Returns
        -------
        pandas.DataFrame
            A DataFrame containing new columns added at the specified position.
    """
    
    for index, col in enumerate(col_names):
        df.insert(start_position + index, col, value=" ")

    return df

def df_formater(df):
    """
        Formats the DataFrame, but adding the State to the correct row.
    
        Parameters
        ----------
        pandas.DataFrame
            A DataFrame containing all original rows.
        string.list
            A list of column names.
        integer
            A starting column position.
    
        Returns
        -------
        pandas.DataFrame
            A DataFrame containing new columns added at the specified position.
    """
    
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
    # Drop rows where all columns from the third column onwards are blank
    cols_to_check = df.columns[2:]
    # Use dropna on the subset of columns
    df_drop_rows = df.dropna(how='all', subset=cols_to_check)
    
    return df_drop_rows

def col_name_changer(df, og_string, new_string):
    """
        Updates all column names.
    
        Parameters
        ----------
        pandas.DataFrame
            A DataFrame containing all original rows
        string.og_string
            Original String or set of characters within the column name to replace.
        string.new_string
            New string or set of characters to be replaced to in the column name.
    
        Returns
        -------
        pandas.DataFrame
            A DataFrame containing new column names.
    """
    df.columns = [col.replace(og_string, new_string) for col in df.columns]

    return df

def df_split(df):
    """
        Splits the DataFrame into 2 DataFrames.
    
        Parameters
        ----------
        pandas.DataFrame
            A DataFrame containing all original rows
    
        Returns
        -------
        pandas.DataFrame
            1. A DataFrame containing rows with only the State.
            2. A DataFrame containing rows with the City, State.
    """
    # Rows with just the State (no comma)
    df_state_only = df[~df['State'].str.contains(',')].reset_index(drop=True)
    # Remove leading white spaces from column 'Label (Grouping)'
    df_state_only['Label (Grouping)'] = df_state_only['Label (Grouping)'].str.lstrip()
    
    # Rows with city and State (contains a comma)
    df_state_city = df[df['State'].str.contains(',')].reset_index(drop=True)
    # Remove leading white spaces from column 'Label (Grouping)'
    df_state_city['Label (Grouping)'] = df_state_city['Label (Grouping)'].str.lstrip()

    return df_state_only, df_state_city