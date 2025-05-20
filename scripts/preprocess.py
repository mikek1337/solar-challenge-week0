import pandas as pd
import numpy as np
def find_and_replace_outliers_with_median(df, cols, threshold=3):
    """
    Detects outliers in specified numeric columns of a DataFrame using the z-score method and replaces them with the column median.
    Parameters:
        df (pd.DataFrame): The input DataFrame to process.
        cols (list of str): List of column names to check for outliers and replace them.
        threshold (float, optional): The z-score threshold to identify outliers. Default is 3.
    Returns:
        pd.DataFrame: A copy of the DataFrame with outliers in the specified columns replaced by the median value of each column.
    Notes:
        - Only numeric columns are processed; non-numeric columns are skipped with a warning.
        - If a column's standard deviation is zero, outlier detection is skipped for that column.
        - Outliers are defined as values with an absolute z-score greater than the specified threshold.
        - The function prints progress and warnings during execution.
    """
    df_cleaned = df.copy()  # Create a copy to avoid modifying the original DataFrame

    print(f"Processing columns: {cols}")

    for col in cols:
        if col not in df.columns:
            print(f"Warning: Column '{col}' not found in DataFrame. Skipping.")
            continue

        # Ensure the column is numeric
        if not pd.api.types.is_numeric_dtype(df_cleaned[col]):
            print(f"Warning: Column '{col}' is not numeric. Skipping outlier detection/replacement.")
            continue

        col_mean = df_cleaned[col].mean()
        col_std = df_cleaned[col].std()
        if col_std == 0:
            print(f"Warning: Standard deviation is zero for column '{col}'. Skipping outlier detection/replacement.")
            continue

        z_scores = (df_cleaned[col] - col_mean) / col_std
        outlier_mask = z_scores.abs() > threshold
        outlier_indices_col = df_cleaned.index[outlier_mask]

        if len(outlier_indices_col) == 0:
            print(f"No outliers found in column '{col}' using z-score threshold {threshold}.")
            continue

        print(f"Found {len(outlier_indices_col)} outliers in column '{col}'.")
        median_value = df_cleaned[col].median()
        print(f"Median value for '{col}' (used for replacement): {median_value}")

        df_cleaned.loc[outlier_indices_col, col] = median_value
        print(f"Outliers in column '{col}' replaced with median.")

    return df_cleaned

def find_columns_with_missing_value(df:pd.DataFrame, threshold=0.05)->list:
    """
    Identifies columns in a DataFrame with a proportion of missing values above a specified threshold.
    Parameters:
        df (pd.DataFrame): The input DataFrame to analyze for missing values.
        threshold (float, optional): The minimum proportion (between 0 and 1) of missing values required for a column to be considered as having excessive missing data. Defaults to 0.05 (5%).
    Returns:
        list: A list of column names where the proportion of missing values exceeds the given threshold.
    Prints:
        A message indicating that columns above the threshold are being returned.
    """
    null_columns = df.isnull().sum()
    total_row = len(df)
    null_percentage = (null_columns/total_row)*100;
    missing_columns = df.columns[null_percentage > threshold]
    print('columns above the threshold')
    return missing_columns.to_list()

def clean_data(df:pd.DataFrame,cols:list)-> pd.DataFrame:
    """
    Cleans and preprocesses the input DataFrame by performing several operations:
    1. Converts the 'Timestamp' column to datetime.
    2. Drops the 'Comments' column and forward-fills missing values.
    3. Clips the specified columns to have a minimum value of 0.
    4. Clips the 'RH' column to be within the range [0, 100].
    5. Replaces outliers in the specified columns and 'Tamb' with the median value.
    6. Resets the DataFrame index.
    Args:
        df (pd.DataFrame): The input DataFrame containing the data to be cleaned.
        cols (list): List of column names to clip and check for outliers.
    Returns:
        pd.DataFrame: The cleaned and preprocessed DataFrame with reset index.
    """
    
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    clean_data = df.drop(columns=['Comments']).ffill()
    for col in cols:
        clean_data.loc[clean_data[col] < 0, col] = np.nan
    clean_data['RH'].clip(0, 100)
    clean_data = find_and_replace_outliers_with_median(clean_data, cols + ['Tamb'])
    
    return clean_data.reset_index(drop=True)

def load_countries(paths:list):
    """
    Loads and concatenates country data from a list of file paths.

    Args:
        paths (list): A list of file paths, each containing country data.

    Returns:
        pandas.DataFrame: A DataFrame containing the concatenated data from all provided file paths.
    """
    full_df = pd.concat([load_country_data(path) for path in paths], ignore_index=True)
    return full_df
   
def load_country_data(path:str):
    """
    Loads data from the specified file path, extracts the country name from the file path,
    and adds it as a new column 'Country' to the DataFrame.

    Args:
        path (str): The file path to the data file. The country name is expected to be the first part
            of the filename, separated by an underscore, and located in the third segment of the path.

    Returns:
        pandas.DataFrame: The loaded DataFrame with an additional 'Country' column.
    """
    df = load_data(path)
    country = path.split('/')[2].split('_')[0]
    df['Country'] = country
    return df 
    
def load_data(path:str):
    """
    Loads data from a CSV file at the specified path, parsing the 'Timestamp' column as dates.

    Args:
        path (str): The file path to the CSV file.

    Returns:
        pandas.DataFrame: The loaded data with parsed dates if successful.
        None: If the provided path is not a string.

    Raises:
        None: Prints an error message if the path is not a string.
    """
    try:
        return pd.read_csv(path, parse_dates=['Timestamp']);
    except TypeError:
        print("Path not a string")
        return