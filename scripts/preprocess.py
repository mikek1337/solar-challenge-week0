import pandas as pd
def find_and_replace_outliers_with_median(df, cols, iqr_multiplier=1.5):
    """
    Finds outliers in specified columns using the IQR method and replaces them
    with the median of their respective columns.

    Args:
        df (pd.DataFrame): The input pandas DataFrame.
        cols (list): A list of column names to check for outliers and replace.
        iqr_multiplier (float, optional): The multiplier for the IQR to define
                                           the outlier bounds. Defaults to 1.5
                                           (standard for box plots).

    Returns:
        pd.DataFrame: A new DataFrame with outliers replaced by the median.
                      Returns a copy, the original DataFrame is not modified.
    """
    df_cleaned = df.copy() # Create a copy to avoid modifying the original DataFrame

    print(f"Processing columns: {cols}")

    for col in cols:
        if col not in df.columns:
            print(f"Warning: Column '{col}' not found in DataFrame. Skipping.")
            continue

        # Ensure the column is numeric, as IQR and median are for numerical data
        if not pd.api.types.is_numeric_dtype(df_cleaned[col]):
             print(f"Warning: Column '{col}' is not numeric. Skipping outlier detection/replacement.")
             continue

        # Calculate Q1, Q3, and IQR for the current column
        Q1 = df_cleaned[col].quantile(0.25)
        Q3 = df_cleaned[col].quantile(0.75)
        IQR = Q3 - Q1

        # Define the lower and upper bounds for outlier detection
        lower_bound = Q1 - iqr_multiplier * IQR
        upper_bound = Q3 + iqr_multiplier * IQR

        # Identify outliers in the current column
        # Create a boolean mask: True for values outside the bounds
        outlier_mask = (df_cleaned[col] < lower_bound) | (df_cleaned[col] > upper_bound)

        # Get the indices of the outliers for this specific column
        outlier_indices_col = df_cleaned.index[outlier_mask]

        # Check if any outliers were found in this column
        if len(outlier_indices_col) == 0:
            print(f"No outliers found in column '{col}' using IQR multiplier {iqr_multiplier}.")
            continue

        print(f"Found {len(outlier_indices_col)} outliers in column '{col}'.")
        # print(f"Outlier indices in '{col}': {outlier_indices_col.tolist()}") # Uncomment to see indices

        # Calculate the median for the current column
        median_value = df_cleaned[col].median()

        print(f"Median value for '{col}' (used for replacement): {median_value}")

        # Replace the outlier values with the calculated median
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
        clean_data[col]=clean_data[col].clip(lower=0)
    clean_data['RH'].clip(0, 100)
    clean_data = find_and_replace_outliers_with_median(clean_data, cols + ['Tamb'])
    
    return clean_data.reset_index(drop=True)