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

def drop_columns(df, column_strings):
    """
        Searches for certain strings in column names and drops those columns
    
        Parameters
        ----------
        pandas.DataFrame
            A dataframe with all original columns
        string.list
            List of strings to search for in the column names 
 
        Returns
        -------
        pandas.DataFrame
            A dataframe without the columns that had the strings specified
            
    """

    df_dropped = df.copy()
    for search_string in column_strings: 
        df_dropped = df_dropped.drop([col for col in df_dropped.columns if search_string in col], axis = 1)

    return df_dropped

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

def rename_columns(df, column_name_mappings):
    """
        Changes column names
    
        Parameters
        ----------
        pandas.DataFrame
            A DataFrame containing all original rows
        dict
            A dictionary with each key as the original column name and value as the new column name
    
        Returns
        -------
        pandas.DataFrame
            A DataFrame containing new column names.
    """

    df = df.rename(columns=column_name_mappings)

    return df

def column_value_changer(df, column_name, rename_mapping):
    """
        Renames values within a specified column
    
        Parameters
        ----------
        pandas.DataFrame
            A dataframe with all original columns
        string
            Column to rename the values in
        dict
            Dictionary that maps the old column values (key) to the new ones (value)
 
        Returns
        -------
        pandas.DataFrame
            Dataframe with updated value names in specified columns
            
            
    """
    df_renamed = df.copy()
    df_renamed[column_name] = df_renamed[column_name].replace(rename_mapping)

    return df_renamed

def filter_dataframe(df, columns_with_include, values_to_include,
                    columns_with_exclude, values_to_exclude):
    """
        Filter rows based on features of interest
    
        Parameters
        ----------
        pandas.DataFrame
        
        string.list 
            list of columns with values in include
        string.list
            list of values to include
        string.list
            list of columns with values to exclude
        string.list
            list of values to exclude
 
        Returns
        -------
        pandas.DataFrame
            A filtered dataframe
            
            
    """

    # check to make sure there are values listed for each column name
    if len(columns_with_include) != len(values_to_include):
        raise Exception("Each column listed must have values passed to filter on.")

    # key check to make sure the columns exist in the data frame
    missing_cols = [col for col in columns_with_include if col not in df.columns]
    if missing_cols:
        raise KeyError(f"The following columns were not found in the DataFrame: {missing_cols}")

    missing_cols = [col for col in columns_with_exclude if col not in df.columns]
    if missing_cols:
        raise KeyError(f"The following columns were not found in the DataFrame: {missing_cols}")

    # create copy to filter
    filtered_df = df.copy()

    # zip to match include column list with values to include
    for col, val_list in zip(columns_with_include, values_to_include):
        # apply filter for included values
        filtered_df = filtered_df[filtered_df[col].isin(val_list)]

    # zip to match exclude column list with values to exclude
    for col, val_list in zip(columns_with_exclude, values_to_exclude):
        # apply filter for excluded values
        filtered_df = filtered_df[~filtered_df[col].isin(val_list)]
        
    return filtered_df



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

# def grab_cols_for_visual(df, col_names):
#     df_only_cols = df[final_col_list]
#     return df_only_cols


def select_columns(df, column_names):
    """
        Selects specified columns from a data frame
        DOES SAME THING AS GRAB COLS FOR VISUAL -snj
    
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

def df_transpose():
    print("transpose df")

    
# ---- Section 2: Specific Functions for Census Data ----

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
    

def numeric_converter(df, start_col=0):
    if start_col == 0:
        cols_to_convert = df.columns[:]
    else:
        cols_to_convert = df.columns[start_col:]
        
    for col in cols_to_convert:
        df[col] = df[col].str.replace(',', '', regex=False)
        df[col] = pd.to_numeric(df[col], errors='coerce')
    return df


# ---- Section 3: Specific Functions for Chronic Disease Data ----

def stratify_dataframe(df, column, value):
    """
        Stratifies data frame based on single column and value specified
        For example: Select only "overall" values or only specific race values
    
        Parameters
        ----------
        df : pandas.DataFrame
        columns : column with stratifying values
        value : stratifying value name
 
        Returns
        -------
        pandas.DataFrame
            A stratified dataframe
            
            
    """
    # create copy to stratify
    stratified_df = df.copy()

    # apply filter to select only those rows
    stratified_df = stratified_df[stratified_df[column]==value]

    return stratified_df


def pivot_questions(df):
    """
        Pivots a data frame so that it turns the values in the Quesiton column into
        individual columns 
    
        Parameters
        ----------
        df : pandas.DataFrame
 
        Returns
        -------
        pandas.DataFrame
            The pivoted data frame
            
            
    """
    # pivot on the "Question" column and include the data value and low and high confidence limits for each
    df = df.pivot(index='State', columns='Question',
                   values=['DataValue', 'LowConfidenceLimit', 'HighConfidenceLimit'])

    # rename the columns so they are in the format "Question - Value"
    df.columns = [f'{q}-{val}' for val, q in df.columns]

    # reset the index
    df = df.reset_index()

    return df

def process_chronic_disease_data():
    """
        Runs through the workflow utilizing defined functions to process the chronic disease data
    
        Parameters
        ----------
        None
 
        Returns
        -------
        pandas.DataFrame
            The finalized data frame
            
            
    """
    # filter values in raw chronic disease data - year, data type, question, and state
    columns_include = ['YearStart','DataValueType','Question']
    values_include = [[2022],['Crude Prevalence'],['Diabetes among adults','Obesity among adults','Arthritis among adults',
                                                    'Food insecure in the past 12 months among households',
                                                    'Chronic obstructive pulmonary disease among adults',
                                                    'Lack of health insurance among adults aged 18-64',
                                                    'Lack of reliable transportation in the past 12 months among adults',
                                                    'Unable to pay mortgage, rent, or utility bills in the past 12 months among adults',
                                                    'Current asthma among adults']]
    columns_exclude = ['LocationDesc']
    values_exclude = [['Guam','District of Columbia','Puerto Rico','United States','Virgin Islands']]
    
    cd_filtered_df = filter_dataframe(df = df_indicators_raw,
                                   columns_with_include = columns_include,
                                   values_to_include = values_include,
                                   columns_with_exclude = columns_exclude,
                                   values_to_exclude = values_exclude)
    # update values in the 'Question' column to readable names
    cd_rename_mapping_dict = {'Arthritis among adults': 'Arthritis', 
                      'Current asthma among adults': 'Asthma',
                      'Unable to pay mortgage, rent, or utility bills in the past 12 months among adults': 'Bill Payment Instability',
                      'Obesity among adults': 'Obesity',
                      'Diabetes among adults': 'Diabetes',
                      'Lack of reliable transportation in the past 12 months among adults': 'Transportation Instability',
                      'Chronic obstructive pulmonary disease among adults': 'COPD'
                     }
    
    cd_renamed_df = column_value_changer(cd_filtered_df, 'Question', cd_rename_mapping_dict)

    # select columns of interest
    cd_column_name_list = ['LocationDesc','Question','DataValueUnit','DataValue',
                        'Stratification1','LowConfidenceLimit','HighConfidenceLimit',
                        'Geolocation']
    
    cd_selected_columns = select_columns(cd_renamed_df, cd_column_name_list)

    # rename state column for later join
    cd_state_rename = {'LocationDesc': 'State'}
    cd_state_rename_df = rename_columns(cd_selected_columns, cd_state_rename)

    # process each stratification and append to a list 
    
    cd_processed_dfs = []
    stratifications = [
        'Overall', 'Male', 'Female',
        'Hispanic', 'White, non-Hispanic', 'Black, non-Hispanic',
        'Hawaiian or Pacific Islander, non-Hispanic',
        'American Indian or Alaska Native, non-Hispanic',
        'Asian, non-Hispanic',
        'Multiracial, non-Hispanic'
    ]
                       
    
    for strat in stratifications:
        # filter to the specified value
        temp_df = stratify_dataframe(cd_state_rename_df, 'Stratification1', strat)
        # pivot to make each question its own column
        temp_df = pivot_questions(temp_df)
        # add prefixes and update 'State' column
        prefix = f'{strat} - '
        temp_df = temp_df.add_prefix(prefix)
        temp_df = temp_df.rename(columns={f'{prefix}State': 'State'})
        
        cd_processed_dfs.append(temp_df)
    
    # merge all processed chronic disease dataframes together 
    chronic_disease_final = cd_processed_dfs[0]
    for next_df in cd_processed_dfs[1:]:
        chronic_disease_final = pd.merge(chronic_disease_final, next_df, on='State', how='outer')

    return chronic_disease_final
    

# ---- Section 4: Specific Functions for Diabetes and Census Cateories ----

def diabete_metrics_all(df):
    """
        Grabs all of the columns of interest for the Diabetes vs Metrics
    
        Parameters
        ----------
        df : pandas.DataFrame
 
        Returns
        -------
        pandas.DataFrame
            DataFrame filtered down to all of releveant columns.
            
            
    """
    cols = [
        'State',
        'Overall - Diabetes-DataValue',
        'Males - Diabetes-DataValue',
        'Females - Diabetes-DataValue',
        'est - Total Pop',
        'est - Total Pop 18 and Over - %',
        'est - Total Pop 18 and Over – Male - %',
        'est - Total Pop 18 and Over – Female - %',
        'est - Pop 25 and Over - Educated',
        'est - Pop 16 and Over',
        'est - Pop 16 and Over – Employed - %',
        'est - Pop 16 and Over – Unemployed - %',
        'est - Workers 16 and Over',
        'est - Workers 16 and Over – Drove Alone - %',
        'est - Workers 16 and Over – Carpooled - %',
        'est - Workers 16 and Over – Public Transit - %',
        'est - Workers 16 and Over – Walked - %',
        'est - Workers 16 and Over – Other Transport - %',
        'est - Workers 16 and Over – Work From Home - %',
        'est - Households With Income',
        'est - Households With Earnings - %',
        'est - Median Household Income',
        'est - Households With Social Security Income - %',
        'est - Households With Suppliemental Security Income - %',
        'est - Households With Cash Assistance - %',
        'est - Households With SNAP - %',
        'est - Civilian Noninstitutionalized Pop',
        'est - Pop With Private Health Insurance - %',
        'est - Pop With Public Health Insurance - %', 
        'est - Pop Uninsured - %',
        'est - Pop 18 and Over Below Poverty - %'
    ]
    
    dia_met_df = select_columns(df, cols)

    return dia_met_df

def diabete_v_overall(df):
    cols = [
        'State',
        'Overall - Diabetes-DataValue',
        'Males - Diabetes-DataValue',
        'Females - Diabetes-DataValue',
        'est - Total Pop',
        'est - Total Pop 18 and Over - %',
        'est - Total Pop 18 and Over – Male - %',
        'est - Total Pop 18 and Over – Female - %'
    ]
    
    df_temp1 = select_columns(df, cols)

    # Need to make a copy b/c pandas warning you about “chained assignment”—you’re trying to assign into a DataFrame object that was created by slicing/filtering another DataFrame, and pandas can’t   guarantee whether you’re modifying the original data or just a temporary copy. This is exactly what SettingWithCopyWarning is about.
    df_final= df_temp1.copy()

    # Calculating total population sub-groups.
    df_final['Total Pop 18 and Over'] = df_final['est - Total Pop'] * (df_final['est - Total Pop 18 and Over - %'] / 100)
    df_final['Total Pop 18 and Over – Male'] = df_final['est - Total Pop'] * (df_final['est - Total Pop 18 and Over – Male - %'] / 100)
    df_final['Total Pop 18 and Over – Female'] = df_final['est - Total Pop'] * (df_final['est - Total Pop 18 and Over – Female - %'] / 100)
    

    # # Cacluating total Diabetes "Crude Prevalence" for each sup group.
    df_final['Diabetes Prevalance - 18 and over'] = df_final['Total Pop 18 and Over'] * (df_final['Overall - Diabetes-DataValue'] / 100)
    df_final['Diabetes Prevalance - Males 18 and over'] = df_final['Total Pop 18 and Over – Male'] * (df_final['Males - Diabetes-DataValue'] /100)
    df_final['Diabetes Prevalance - Females 18 and over'] = df_final['Total Pop 18 and Over – Female'] * (df_final['Females - Diabetes-DataValue'] / 100)

    return df_final

def diabete_v_educated(df):
    cols = [
        'State',
        'Overall - Diabetes-DataValue',
        'est - Pop 25 and Over - Educated'
    ]
    
    df_temp1 = select_columns(df, cols)

    # Need to make a copy b/c pandas warning you about “chained assignment”—you’re trying to assign into a DataFrame object that was created by slicing/filtering another DataFrame, and pandas can’t   guarantee whether you’re modifying the original data or just a temporary copy. This is exactly what SettingWithCopyWarning is about.
    df_final = df_temp1.copy()

    # # Cacluating total Diabetes "Crude Prevalence" for each sup group.
    df_final['Diabetes Prevalance - 25 and over - Edu'] = df_final['est - Pop 25 and Over - Educated'] * (df_final['Overall - Diabetes-DataValue'] /100)

    return df_final

def diabete_v_employement(df):
    cols = [
        'State',
        'Overall - Diabetes-DataValue',
        'Males - Diabetes-DataValue',
        'Females - Diabetes-DataValue',
        'est - Pop 16 and Over',
        'est - Pop 16 and Over – Employed - %',
        'est - Pop 16 and Over – Unemployed - %'

    ]

    df_temp1 = select_columns(df, cols)

    # Need to make a copy b/c pandas warning you about “chained assignment”—you’re trying to assign into a DataFrame object that was created by slicing/filtering another DataFrame, and pandas can’t   guarantee whether you’re modifying the original data or just a temporary copy. This is exactly what SettingWithCopyWarning is about.
    df_final= df_temp1.copy()

    # Calculating total population sub-groups.
    df_final['Total Pop 16 and Over - Employed'] = df_final['est - Pop 16 and Over'] * (df_final['est - Pop 16 and Over – Employed - %'] / 100)
    df_final['Total Pop 16 and Over - Unemployed'] = df_final['est - Pop 16 and Over'] * (df_final['est - Pop 16 and Over – Unemployed - %'] / 100)
    

    # Cacluating total Diabetes "Crude Prevalence" for each sup group.
    df_final['Diabetes Prevalance - 16 and Over - Employed'] = df_final['Total Pop 16 and Over - Employed'] * (df_final['Overall - Diabetes-DataValue'] / 100)
    df_final['Total Pop 16 and Over - Unemployed'] = df_final['Total Pop 16 and Over - Unemployed'] * (df_final['Overall - Diabetes-DataValue'] / 100)

    return df_final

def diabete_v_commute(df):
    cols = [
        'State',
        'Overall - Diabetes-DataValue',
        'est - Workers 16 and Over',
        'est - Workers 16 and Over – Drove Alone - %',
        'est - Workers 16 and Over – Carpooled - %',
        'est - Workers 16 and Over – Public Transit - %',
        'est - Workers 16 and Over – Walked - %',
        'est - Workers 16 and Over – Other Transport - %',
        'est - Workers 16 and Over – Work From Home - %'
    ]

    df_temp1 = select_columns(df, cols)

    # Need to make a copy b/c pandas warning you about “chained assignment”—you’re trying to assign into a DataFrame object that was created by slicing/filtering another DataFrame, and pandas can’t   guarantee whether you’re modifying the original data or just a temporary copy. This is exactly what SettingWithCopyWarning is about.
    df_final= df_temp1.copy()

    # Calculating total population sub-groups.
    df_final['Workers 16 and Over - That Drive or Carpool'] = df_final['est - Workers 16 and Over'] * ((df_final['est - Workers 16 and Over – Drove Alone - %'] + df_final['est - Workers 16 and Over – Carpooled - %'])/ 100)
    df_final['Workers 16 and Over - Public Transit'] = df_final['est - Workers 16 and Over'] * (df_final['est - Workers 16 and Over – Public Transit - %'] / 100)
    df_final['Workers 16 and Over - Walk'] = df_final['est - Workers 16 and Over'] * (df_final['est - Workers 16 and Over – Walked - %'] / 100)
    df_final['Workers 16 and Over - Other Transport'] = df_final['est - Workers 16 and Over'] * (df_final['est - Workers 16 and Over – Other Transport - %'] / 100)
    df_final['Workers 16 and Over - WFH'] = df_final['est - Workers 16 and Over'] * (df_final['est - Workers 16 and Over – Work From Home - %'] / 100)

    # Cacluating total Diabetes "Crude Prevalence" for each sup group.
    df_final['Diabetes Prevalance - People Who Drive to Work'] = df_final['Workers 16 and Over - That Drive or Carpool'] * (df_final['Overall - Diabetes-DataValue'] / 100)
    df_final['Diabetes Prevalance - People Who Use Public Transit'] = df_final['Workers 16 and Over - Public Transit'] * (df_final['Overall - Diabetes-DataValue'] / 100)
    df_final['Diabetes Prevalance - People Who Walk'] = df_final['Workers 16 and Over - Walk'] * (df_final['Overall - Diabetes-DataValue'] / 100)
    df_final['Diabetes Prevalance - People Who Use Other Transport'] = df_final['Workers 16 and Over - Other Transport'] * (df_final['Overall - Diabetes-DataValue'] / 100)
    df_final['Diabetes Prevalance - People Who WFH'] = df_final['Workers 16 and Over - WFH'] * (df_final['Overall - Diabetes-DataValue'] / 100)
    
    return df_final

def diabete_v_income(df):

    cols = [
        'State',
        'Overall - Diabetes-DataValue',
        'est - Households With Income',
        'est - Households With Earnings - %',
        'est - Median Household Income',
        'est - Households With Social Security Income - %',
        'est - Households With Suppliemental Security Income - %',
        'est - Households With Cash Assistance - %',
        'est - Households With SNAP - %'
    ]

    df_temp1 = select_columns(df, cols)

    # Need to make a copy b/c pandas warning you about “chained assignment”—you’re trying to assign into a DataFrame object that was created by slicing/filtering another DataFrame, and pandas can’t   guarantee whether you’re modifying the original data or just a temporary copy. This is exactly what SettingWithCopyWarning is about.
    df_final= df_temp1.copy()

    # Calculating total population sub-groups.
    df_final['Households with Earnings'] = df_final['est - Households With Income'] * (df_final['est - Households With Earnings - %'] / 100)
    df_final['Households with SSI'] = df_final['est - Households With Income'] * (df_final['est - Households With Social Security Income - %'] / 100)
    df_final['Households with Supplimential'] = df_final['est - Households With Income'] * (df_final['est - Households With Suppliemental Security Income - %'] / 100)
    df_final['Households with Cash Assistance'] = df_final['est - Households With Income'] * (df_final['est - Households With Cash Assistance - %'] / 100)
    df_final['Households with SNAP'] = df_final['est - Households With Income'] * (df_final['est - Households With SNAP - %'] / 100)
    
    financial_assist_percentage = (
        df_final['est - Households With Social Security Income - %'] + 
        df_final['est - Households With Suppliemental Security Income - %'] + 
        df_final['est - Households With Cash Assistance - %'] +
        df_final['est - Households With SNAP - %']
    )
        
    df_final['Households with Financial Assistant'] = df_final['est - Households With Income'] * (financial_assist_percentage/ 100)

    # Cacluating total Diabetes "Crude Prevalence" for each sup group.
    df_final['Diabetes Prevalance - Households with income'] = df_final['Households with Earnings'] * (df_final['Overall - Diabetes-DataValue'] / 100)
    df_final['Diabetes Prevalance - Households with SSI'] = df_final['Households with SSI'] * (df_final['Overall - Diabetes-DataValue'] / 100)
    df_final['Diabetes Prevalance - Households with Supplimental'] = df_final['Households with Supplimential'] * (df_final['Overall - Diabetes-DataValue'] / 100)
    df_final['Diabetes Prevalance - Households with Cash Assistance'] = df_final['Households with Cash Assistance'] * (df_final['Overall - Diabetes-DataValue'] / 100)
    df_final['Diabetes Prevalance - Households with SNAP'] = df_final['Households with SNAP'] * (df_final['Overall - Diabetes-DataValue'] / 100)
    df_final['Diabetes Prevalance - Financial Assistant'] = df_final['Households with Financial Assistant'] * (df_final['Overall - Diabetes-DataValue'] / 100)

    return df_final

def diabete_v_health_insurance(df):
    cols = [
        'State',
        'Overall - Diabetes-DataValue',
        'est - Civilian Noninstitutionalized Pop',
        'est - Pop With Private Health Insurance - %',
        'est - Pop With Public Health Insurance - %', 
        'est - Pop Uninsured - %',
    ]

    df_temp1 = select_columns(df, cols)

    # Need to make a copy b/c pandas warning you about “chained assignment”—you’re trying to assign into a DataFrame object that was created by slicing/filtering another DataFrame, and pandas can’t   guarantee whether you’re modifying the original data or just a temporary copy. This is exactly what SettingWithCopyWarning is about.
    df_final= df_temp1.copy()

    # Calculating total population sub-groups.
    df_final['Pop with Private Health Insurance'] = df_final['est - Civilian Noninstitutionalized Pop'] * (df_final['est - Pop With Private Health Insurance - %'] / 100)
    df_final['Pop with Public Health Insurance'] = df_final['est - Civilian Noninstitutionalized Pop'] * (df_final['est - Pop With Public Health Insurance - %'] / 100)
    df_final['Pop with Health Insurance'] = df_final['est - Civilian Noninstitutionalized Pop'] * ((df_final['est - Pop With Private Health Insurance - %'] + df_final['est - Pop With Public Health Insurance - %'])/ 100)
    df_final['Pop with Without Health Insurance'] = df_final['est - Civilian Noninstitutionalized Pop'] * (df_final['est - Pop Uninsured - %'] / 100)

    # Cacluating total Diabetes "Crude Prevalence" for each sup group.
    df_final['Diabetes Prevalance - Pop with Private Health Insurance'] = df_final['Pop with Private Health Insurance'] * (df_final['Overall - Diabetes-DataValue'] / 100)
    df_final['Diabetes Prevalance - Pop with Public Health Insurance'] = df_final['Pop with Public Health Insurance'] * (df_final['Overall - Diabetes-DataValue'] / 100)
    df_final['Diabetes Prevalance - Pop with Health Insurance'] = df_final['Pop with Health Insurance'] * (df_final['Overall - Diabetes-DataValue'] / 100)
    df_final['Diabetes Prevalance - Pop without Health Insurance'] = df_final['Pop with Without Health Insurance'] * (df_final['Overall - Diabetes-DataValue'] / 100)

    return df_final

def diabete_v_poverty(df):
    cols = [
        'State',
        'Overall - Diabetes-DataValue',
        'est - Total Pop',
        'est - Total Pop 18 and Over - %',
        'est - Pop 18 and Over Below Poverty - %'
    ]

    df_temp1 = select_columns(df, cols)

    # Need to make a copy b/c pandas warning you about “chained assignment”—you’re trying to assign into a DataFrame object that was created by slicing/filtering another DataFrame, and pandas can’t   guarantee whether you’re modifying the original data or just a temporary copy. This is exactly what SettingWithCopyWarning is about.
    df_final= df_temp1.copy()

    # Calculating total population sub-groups.
    df_final['Total Pop 18 and Over'] = df_final['est - Total Pop'] * (df_final['est - Total Pop 18 and Over - %'] / 100)
    df_final['Total Pop 18 and Over Below Poverty'] = df_final['Total Pop 18 and Over'] * (df_final['est - Pop 18 and Over Below Poverty - %'] / 100)
    df_final['Total Pop 18 and Over Above Poverty'] = df_final['Total Pop 18 and Over'] * ((100 - df_final['est - Pop 18 and Over Below Poverty - %']) / 100)

    # Cacluating total Diabetes "Crude Prevalence" for each sup group.
    df_final['Diabetes Prevalance - Pop 18 and Over Below Poverty'] = df_final['Total Pop 18 and Over Below Poverty'] * (df_final['Overall - Diabetes-DataValue'] / 100)
    df_final['Diabetes Prevalance - Pop 18 and Over Above Poverty'] = df_final['Total Pop 18 and Over Above Poverty'] * (df_final['Overall - Diabetes-DataValue'] / 100)

    return df_final
    