import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sb
def data_quality_report(df: pd.DataFrame) -> pd.DataFrame:
    """
    Generates a data quality report for a given pandas DataFrame.
    The report includes the following metrics for each column:
    - Missing Values: Number of missing (NaN) values.
    - Zero Values: Number of zero values.
    - Negative Values: Number of negative values (for numeric columns only).
    - Out of Range: For specific columns ('GHI', 'RH', 'Tamb'), counts values outside predefined valid ranges:
        - 'GHI': 0 to 1500
        - 'RH': 0 to 100
        - 'Tamb': -20 to 60
    Parameters:
        df (pd.DataFrame): The input DataFrame to analyze.
    Returns:
        pd.DataFrame: A DataFrame summarizing data quality metrics for each column.
    """
    
    report = pd.DataFrame({
        'Missing Values': df.isna().sum(),
        'Zero Values': (df == 0).sum(),
        'Negative Values': (df.select_dtypes(include=np.number) < 0).sum()
    })

    # Value range checks
    ranges = {
        'GHI': (0, 1500),
        'RH': (0, 100),
        'Tamb': (-20, 60)
    }
    for col, (min_val, max_val) in ranges.items():
        report.loc[col, 'Out of Range'] = ((df[col] < min_val) | (df[col] > max_val)).sum()

    return report

def plot_time_series(df:pd.DataFrame):
    """
    Plots time series data for specified columns ('GHI', 'DNI', 'DHI', 'Tamb') from a DataFrame.
    Parameters:
        df (pd.DataFrame): Input DataFrame containing a 'Timestamp' column and the columns to plot.
    Displays:
        A matplotlib figure showing the time series of the selected columns against 'Timestamp'.
    """

    plt.figure(figsize=(14, 8))
    plot_cols = ['GHI', 'DNI', 'DHI', 'Tamb']

    for col in plot_cols:
        plt.plot(df['Timestamp'], df[col], label=col)

    plt.xlabel('Timestamp')
    plt.ylabel('Value')
    plt.title('Time Series Analysis of GHI, DNI, DHI, Tamb')
    plt.legend()
    plt.tight_layout()
    plt.show()

def correlation_matrix(df:pd.DataFrame, cols:list, name:str):
    plt.figure(figsize=(10, 8))
    sb.heatmap(df[cols].corr(), annot=True, fmt='.2f', cmap='coolwarm', square=True)
    plt.title(f'Correlation Matrix for {name}')
    plt.show()