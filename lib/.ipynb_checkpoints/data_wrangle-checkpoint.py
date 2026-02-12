# This .py file will be used for functions that help with the data wrangling.
# Importing python packages
import pandas as pd

# ---- Section 1: Modular Functions ----
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

def remove_cols(df, col_names):
    """
        Takes a list of new column(s) and removes them from the dataframe.        
    
        Parameters
        ----------
        string.list
            A list of column names.
    
        Returns
        -------
        pandas.DataFrame
            A DataFrame with the specified columns removed.
    """
    df_new = df.drop(col_names, axis=1)
    
    return df_new

def remove_rows(df, col, row_values):
    pattern = '|'.join(row_values)
    df_new = df[~df[col].str.contains(pattern, na=False)]

    return df_new
    
def remove_nan_cols(df):
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

def remove_nan_rows(df):
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
    # Drop rows where all columns from the 4th column onwards are blank
    cols_to_check = df.columns[3:]
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


def remove_leading_wspace(df, col_names):
    """
        Remove leading white spaces from column.
    
        Parameters
        ----------
        pandas.DataFrame
            A DataFrame containing all original rows
        string
            Name of the column(s)
    
        Returns
        -------
        pandas.DataFrame
            1. A DataFrame containing rows with only the State.
            2. A DataFrame containing rows with the City, State.
    """
    df[col_names] = df[col_names].str.lstrip()
    
    return df

def df_split(df, col_names, value1, value2):
    df_value1 = df[df[col_names] == value1].copy()
    df_value2 =  df[df[col_names] == value2].copy()

    return df_value1, df_value2

def df_combo(df1, df2, col_name, how):
    df_combined = pd.merge(df1, df2, on=col_name, how=how)
    return df_combined

def grab_cols_for_visual(df, col_names):
    df_only_cols = df[final_col_list]
    return df_only_cols

def df_transpose():
    print("transpose df")

    
# ---- Section 2: Specific Functions ----

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
    
def df_split_state_city(df, col_names):
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
    df_state_only = df[~df[col_names].str.contains(',')].reset_index(drop=True)
    # Remove leading white spaces from column 'Label (Grouping)'
    df_state_only = remove_leading_wspace(df_state_only, 'Label (Grouping)')
    
    # Rows with city and State (contains a comma)
    df_state_city = df[df[col_names].str.contains(',')].reset_index(drop=True)
    # Remove leading white spaces from column 'Label (Grouping)'
    df_state_city = remove_leading_wspace(df_state_city, 'Label (Grouping)')

    return df_state_only, df_state_city

def remove_percent(df):
    for col in df.columns:
        if df[col].astype(str).str.contains('%').any():
            df[col] = df[col].astype(str).str.replace('%', '', regex=False)
            df.rename(columns={col: f"{col} - %"}, inplace=True)
    return df

def remove_symbol(df):
    df = df.astype(str).replace('±', '', regex=True)
    return df

def census_filter_cols(df):
    final_col_list = [
    'State',
    'Label (Grouping)',
    'SEX AND AGE!!Total population',
    'SEX AND AGE!!Total population!!Male',
    'SEX AND AGE!!Total population!!Female',
    'SEX AND AGE!!Total population!!18 years and over',
    'SEX AND AGE!!Total population!!18 years and over!!Male',
    'SEX AND AGE!!Total population!!18 years and over!!Female',
    'EDUCATIONAL ATTAINMENT!!Population 25 years and over',
    'EDUCATIONAL ATTAINMENT!!Population 25 years and over!!High school graduate or higher',
    'EDUCATIONAL ATTAINMENT!!Population 25 years and over!!High school graduate or higher!!Male, high school graduate or higher',
    'EDUCATIONAL ATTAINMENT!!Population 25 years and over!!High school graduate or higher!!Female, high school graduate or higher',
    'VETERAN STATUS!!Civilian population 18 years and over',
    'VETERAN STATUS!!Civilian population 18 years and over!!Civilian veteran',
    'EMPLOYMENT STATUS!!Population 16 years and over',
    'EMPLOYMENT STATUS!!Population 16 years and over!!In labor force',
    'EMPLOYMENT STATUS!!Population 16 years and over!!In labor force!!Civilian labor force',
    'EMPLOYMENT STATUS!!Population 16 years and over!!In labor force!!Civilian labor force!!Employed',
    'EMPLOYMENT STATUS!!Population 16 years and over!!In labor force!!Civilian labor force!!Unemployed',
    'EMPLOYMENT STATUS!!Population 16 years and over!!In labor force!!Civilian labor force!!Unemployed!!Unemployment Rate',
    'EMPLOYMENT STATUS!!Population 16 years and over!!In labor force!!Armed Forces',
    'EMPLOYMENT STATUS!!Population 16 years and over!!Not in labor force',
    'COMMUTING TO WORK!!Workers 16 years and over',
    'COMMUTING TO WORK!!Workers 16 years and over!!Car, truck, or van - drove alone',
    'COMMUTING TO WORK!!Workers 16 years and over!!Car, truck, or van - carpooled',
    'COMMUTING TO WORK!!Workers 16 years and over!!Public transportation (excluding taxicab)',
    'COMMUTING TO WORK!!Workers 16 years and over!!Walked',
    'COMMUTING TO WORK!!Workers 16 years and over!!Other means',
    'COMMUTING TO WORK!!Workers 16 years and over!!Worked from home',
    'COMMUTING TO WORK!!Workers 16 years and over!!Mean travel time to work (minutes)',
    'INCOME IN THE PAST 12 MONTHS (IN 2022 INFLATION-ADJUSTED DOLLARS)!!Households',
    'INCOME IN THE PAST 12 MONTHS (IN 2022 INFLATION-ADJUSTED DOLLARS)!!Households!!Median household income (dollars)',
    'INCOME IN THE PAST 12 MONTHS (IN 2022 INFLATION-ADJUSTED DOLLARS)!!Households!!With earnings',
    'INCOME IN THE PAST 12 MONTHS (IN 2022 INFLATION-ADJUSTED DOLLARS)!!Households!!With earnings!!Mean earnings (dollars)',
    'INCOME IN THE PAST 12 MONTHS (IN 2022 INFLATION-ADJUSTED DOLLARS)!!Households!!With Social Security income',
    'INCOME IN THE PAST 12 MONTHS (IN 2022 INFLATION-ADJUSTED DOLLARS)!!Households!!With Social Security income!!Mean Social Security income (dollars)',
    'INCOME IN THE PAST 12 MONTHS (IN 2022 INFLATION-ADJUSTED DOLLARS)!!Households!!With Supplemental Security Income',
    'INCOME IN THE PAST 12 MONTHS (IN 2022 INFLATION-ADJUSTED DOLLARS)!!Households!!With Supplemental Security Income!!Mean Supplemental Security Income (dollars)',
    'INCOME IN THE PAST 12 MONTHS (IN 2022 INFLATION-ADJUSTED DOLLARS)!!Households!!With cash public assistance income',
    'INCOME IN THE PAST 12 MONTHS (IN 2022 INFLATION-ADJUSTED DOLLARS)!!Households!!With cash public assistance income!!Mean cash public assistance income (dollars)',
    'INCOME IN THE PAST 12 MONTHS (IN 2022 INFLATION-ADJUSTED DOLLARS)!!Households!!With retirement income',
    'INCOME IN THE PAST 12 MONTHS (IN 2022 INFLATION-ADJUSTED DOLLARS)!!Households!!With retirement income!!Mean retirement income (dollars)',
    'INCOME IN THE PAST 12 MONTHS (IN 2022 INFLATION-ADJUSTED DOLLARS)!!Households!!With Food Stamp/SNAP benefits',
    'INCOME IN THE PAST 12 MONTHS (IN 2022 INFLATION-ADJUSTED DOLLARS)!!Individuals',
    'INCOME IN THE PAST 12 MONTHS (IN 2022 INFLATION-ADJUSTED DOLLARS)!!Individuals!!Per capita income (dollars)',
    'INCOME IN THE PAST 12 MONTHS (IN 2022 INFLATION-ADJUSTED DOLLARS)!!Individuals!!With earnings for full-time, year-round workers:!!Male',
    'INCOME IN THE PAST 12 MONTHS (IN 2022 INFLATION-ADJUSTED DOLLARS)!!Individuals!!With earnings for full-time, year-round workers:!!Female',
    # 'INCOME IN THE PAST 12 MONTHS (IN 2022 INFLATION-ADJUSTED DOLLARS)!!Individuals!!Mean earnings (dollars) for full-time, year-round workers:!!Male',
    # 'INCOME IN THE PAST 12 MONTHS (IN 2022 INFLATION-ADJUSTED DOLLARS)!!Individuals!!Mean earnings (dollars) for full-time, year-round workers:!!Female',
    'INCOME IN THE PAST 12 MONTHS (IN 2022 INFLATION-ADJUSTED DOLLARS)!!Individuals!!Median earnings (dollars) full-time, year-round workers:!!Male',
    'INCOME IN THE PAST 12 MONTHS (IN 2022 INFLATION-ADJUSTED DOLLARS)!!Individuals!!Median earnings (dollars) full-time, year-round workers:!!Female',
    'HEALTH INSURANCE COVERAGE!!Civilian noninstitutionalized population',
    'HEALTH INSURANCE COVERAGE!!Civilian noninstitutionalized population!!With private health insurance',
    'HEALTH INSURANCE COVERAGE!!Civilian noninstitutionalized population!!With public coverage',
    'HEALTH INSURANCE COVERAGE!!Civilian noninstitutionalized population!!No health insurance coverage',
    'POVERTY RATES FOR FAMILIES AND PEOPLE FOR WHOM POVERTY STATUS IS DETERMINED!!All people!!18 years and over',
    'VEHICLES AVAILABLE!!Occupied housing units',
    'VEHICLES AVAILABLE!!Occupied housing units!!None',
    'VEHICLES AVAILABLE!!Occupied housing units!!1 or more',
    'SELECTED MONTHLY OWNER COSTS AS A PERCENTAGE OF HOUSEHOLD INCOME IN THE PAST 12 MONTHS!!Housing units with a mortgage (excluding units where SMOC cannot be computed)',
    'SELECTED MONTHLY OWNER COSTS AS A PERCENTAGE OF HOUSEHOLD INCOME IN THE PAST 12 MONTHS!!Housing units with a mortgage (excluding units where SMOC cannot be computed)!!Less than 30 percent',
    'SELECTED MONTHLY OWNER COSTS AS A PERCENTAGE OF HOUSEHOLD INCOME IN THE PAST 12 MONTHS!!Housing units with a mortgage (excluding units where SMOC cannot be computed)!!30 percent or more'
    ]
    df_only_cols = df[final_col_list]

    return df_only_cols

def census_rename_cols(df):
    df_rename_cols = df.rename(columns={
    'SEX AND AGE!!Total population': 'Total Pop',
    'SEX AND AGE!!Total population!!Male': 'Total Pop - Male',
    'SEX AND AGE!!Total population!!Female': 'Total Pop - Female',
    'SEX AND AGE!!Total population!!18 years and over': 'Total Pop 18 and Over',
    'SEX AND AGE!!Total population!!18 years and over!!Male': 'Total Pop 18 and Over – Male',
    'SEX AND AGE!!Total population!!18 years and over!!Female': 'Total Pop 18 and Over – Female',
    'EDUCATIONAL ATTAINMENT!!Population 25 years and over': 'Pop 25 and Over - Educated',
    'EDUCATIONAL ATTAINMENT!!Population 25 years and over!!High school graduate or higher': 'Pop 25 and Over – HS Graduate or Higher',
    'EDUCATIONAL ATTAINMENT!!Population 25 years and over!!High school graduate or higher!!Male, high school graduate or higher': 'Pop 25 and Over – Male HS and Over',
    'EDUCATIONAL ATTAINMENT!!Population 25 years and over!!High school graduate or higher!!Female, high school graduate or higher': 'Pop 25 and Over – Female HS and Over',
    'VETERAN STATUS!!Civilian population 18 years and over': 'Civilian Pop 18 and Over',
    'VETERAN STATUS!!Civilian population 18 years and over!!Civilian veteran': 'Civilian Veterans 18 and Over',
    'EMPLOYMENT STATUS!!Population 16 years and over': 'Pop 16 and Over',
    'EMPLOYMENT STATUS!!Population 16 years and over!!In labor force': 'Pop 16 and Over – Labor Force',
    'EMPLOYMENT STATUS!!Population 16 years and over!!In labor force!!Civilian labor force': 'Pop 16 and Over – Civilian Labor',
    'EMPLOYMENT STATUS!!Population 16 years and over!!In labor force!!Civilian labor force!!Employed': 'Pop 16 and Over – Employed',
    'EMPLOYMENT STATUS!!Population 16 years and over!!In labor force!!Civilian labor force!!Unemployed': 'Pop 16 and Over – Unemployed',
    'EMPLOYMENT STATUS!!Population 16 years and over!!In labor force!!Civilian labor force!!Unemployed!!Unemployment Rate': 'Unemployment Rate – 16 and Over',
    'EMPLOYMENT STATUS!!Population 16 years and over!!In labor force!!Armed Forces': 'Pop 16 and Over – Armed Forces',
    'EMPLOYMENT STATUS!!Population 16 years and over!!Not in labor force': 'Pop 16 and Over – Not in Labor Force',
    'COMMUTING TO WORK!!Workers 16 years and over': 'Workers 16 and Over',
    'COMMUTING TO WORK!!Workers 16 years and over!!Car, truck, or van - drove alone': 'Workers 16 and Over – Drove Alone',
    'COMMUTING TO WORK!!Workers 16 years and over!!Car, truck, or van - carpooled': 'Workers 16 and Over – Carpooled',
    'COMMUTING TO WORK!!Workers 16 years and over!!Public transportation (excluding taxicab)': 'Workers 16 and Over – Public Transit',
    'COMMUTING TO WORK!!Workers 16 years and over!!Walked': 'Workers 16 and Over – Walked',
    'COMMUTING TO WORK!!Workers 16 years and over!!Other means': 'Workers 16 and Over – Other Transport',
    'COMMUTING TO WORK!!Workers 16 years and over!!Worked from home': 'Workers 16 and Over – Work From Home',
    'COMMUTING TO WORK!!Workers 16 years and over!!Mean travel time to work (minutes)': 'Avg Commute Time (Min)',
    'INCOME IN THE PAST 12 MONTHS (IN 2022 INFLATION-ADJUSTED DOLLARS)!!Households': 'Households With Income',
    'INCOME IN THE PAST 12 MONTHS (IN 2022 INFLATION-ADJUSTED DOLLARS)!!Households!!Median household income (dollars)': 'Median Household Income',
    'INCOME IN THE PAST 12 MONTHS (IN 2022 INFLATION-ADJUSTED DOLLARS)!!Households!!With earnings': 'Households With Earnings',
    'INCOME IN THE PAST 12 MONTHS (IN 2022 INFLATION-ADJUSTED DOLLARS)!!Households!!With earnings!!Mean earnings (dollars)': 'Mean Household Earnings',
    'INCOME IN THE PAST 12 MONTHS (IN 2022 INFLATION-ADJUSTED DOLLARS)!!Households!!With Social Security income': 'Households With Social Security Income',
    'INCOME IN THE PAST 12 MONTHS (IN 2022 INFLATION-ADJUSTED DOLLARS)!!Households!!With Social Security income!!Mean Social Security income (dollars)': 'Mean Social Security Income',
    'INCOME IN THE PAST 12 MONTHS (IN 2022 INFLATION-ADJUSTED DOLLARS)!!Households!!With Supplemental Security Income': 'Households With Suppliemental Security Income',
    'INCOME IN THE PAST 12 MONTHS (IN 2022 INFLATION-ADJUSTED DOLLARS)!!Households!!With Supplemental Security Income!!Mean Supplemental Security Income (dollars)': 'Mean Suppliemental Security Income',
    'INCOME IN THE PAST 12 MONTHS (IN 2022 INFLATION-ADJUSTED DOLLARS)!!Households!!With cash public assistance income': 'Households With Cash Assistance',
    'INCOME IN THE PAST 12 MONTHS (IN 2022 INFLATION-ADJUSTED DOLLARS)!!Households!!With cash public assistance income!!Mean cash public assistance income (dollars)': 'Mean Cash Assistance Income',
    'INCOME IN THE PAST 12 MONTHS (IN 2022 INFLATION-ADJUSTED DOLLARS)!!Households!!With retirement income': 'Households With Retirement Income',
    'INCOME IN THE PAST 12 MONTHS (IN 2022 INFLATION-ADJUSTED DOLLARS)!!Households!!With retirement income!!Mean retirement income (dollars)': 'Mean Retirement Income',
    'INCOME IN THE PAST 12 MONTHS (IN 2022 INFLATION-ADJUSTED DOLLARS)!!Households!!With Food Stamp/SNAP benefits': 'Households With SNAP',
    'INCOME IN THE PAST 12 MONTHS (IN 2022 INFLATION-ADJUSTED DOLLARS)!!Individuals': 'Individuals With Income',
    'INCOME IN THE PAST 12 MONTHS (IN 2022 INFLATION-ADJUSTED DOLLARS)!!Individuals!!Per capita income (dollars)': 'Per Capita Income',
    'INCOME IN THE PAST 12 MONTHS (IN 2022 INFLATION-ADJUSTED DOLLARS)!!Individuals!!With earnings for full-time, year-round workers:!!Male': 'FTYR Workers – Male',
    'INCOME IN THE PAST 12 MONTHS (IN 2022 INFLATION-ADJUSTED DOLLARS)!!Individuals!!With earnings for full-time, year-round workers:!!Female': 'FTYR Workers – Female',
    # 'INCOME IN THE PAST 12 MONTHS (IN 2022 INFLATION-ADJUSTED DOLLARS)!!Individuals!!Mean earnings (dollars) for full-time, year-round workers:!!Male'': 'Mean Earnings – FTYR Male',
    # 'INCOME IN THE PAST 12 MONTHS (IN 2022 INFLATION-ADJUSTED DOLLARS)!!Individuals!!Mean earnings (dollars) for full-time, year-round workers:!!Female': 'Mean Earnings – FTYR Female',
    'INCOME IN THE PAST 12 MONTHS (IN 2022 INFLATION-ADJUSTED DOLLARS)!!Individuals!!Median earnings (dollars) full-time, year-round workers:!!Male': 'Median Earnings – FTYR Male',
    'INCOME IN THE PAST 12 MONTHS (IN 2022 INFLATION-ADJUSTED DOLLARS)!!Individuals!!Median earnings (dollars) full-time, year-round workers:!!Female': 'Median Earnings – FTYR Female',
    'HEALTH INSURANCE COVERAGE!!Civilian noninstitutionalized population': 'Civilian Noninstitutionalized Pop',
    'HEALTH INSURANCE COVERAGE!!Civilian noninstitutionalized population!!With private health insurance': 'Pop With Private Health Insurance',
    'HEALTH INSURANCE COVERAGE!!Civilian noninstitutionalized population!!With public coverage': 'Pop With Public Health Insurance',
    'HEALTH INSURANCE COVERAGE!!Civilian noninstitutionalized population!!No health insurance coverage': 'Pop Uninsured',
    'POVERTY RATES FOR FAMILIES AND PEOPLE FOR WHOM POVERTY STATUS IS DETERMINED!!All people!!18 years and over': 'Pop 18 and Over Below Poverty',
    'VEHICLES AVAILABLE!!Occupied housing units': 'Occupied Housing Units',
    'VEHICLES AVAILABLE!!Occupied housing units!!None': 'Households With No Vehicles',
    'VEHICLES AVAILABLE!!Occupied housing units!!1 or more': 'Households With 1 and Over Vehicles',
    'SELECTED MONTHLY OWNER COSTS AS A PERCENTAGE OF HOUSEHOLD INCOME IN THE PAST 12 MONTHS!!Housing units with a mortgage (excluding units where SMOC cannot be computed)': 'Owner-Occupied With Mortgage',
    'SELECTED MONTHLY OWNER COSTS AS A PERCENTAGE OF HOUSEHOLD INCOME IN THE PAST 12 MONTHS!!Housing units with a mortgage (excluding units where SMOC cannot be computed)!!Less than 30 percent': 'Mortgage Costs  less than 30 percent Income',
    'SELECTED MONTHLY OWNER COSTS AS A PERCENTAGE OF HOUSEHOLD INCOME IN THE PAST 12 MONTHS!!Housing units with a mortgage (excluding units where SMOC cannot be computed)!!30 percent or more': 'Mortgage Costs 30 precent or more of Income'
        }
    )

    return df_rename_cols

    