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
        sb.lineplot(df, x='Timestamp', y=col)
        #plt.plot(df['Timestamp'], df[col], label=col)

    plt.xlabel('Timestamp')
    plt.ylabel('Value')
    plt.title('Time Series Analysis of GHI, DNI, DHI, Tamb')
    plt.legend()
    plt.tight_layout()
    plt.show()

def correlation_matrix(df:pd.DataFrame, cols:list, name:str):
    """
    Generates and displays a correlation matrix heatmap for the specified columns of a DataFrame.

    Args:
        df (pd.DataFrame): The input DataFrame containing the data.
        cols (list): List of column names to include in the correlation matrix.
        name (str): A name or label to use in the plot title.

    Displays:
        A heatmap plot of the correlation matrix for the specified columns.
    """
    plt.figure(figsize=(10, 8))
    sb.heatmap(df[cols].corr(), annot=True, fmt='.2f', cmap='coolwarm', square=True)
    plt.title(f'Correlation Matrix for {name}')
    plt.show()

def plot_bubble_chart(df:pd.DataFrame):
    """
    Plots a bubble chart of Global Horizontal Irradiance (GHI) versus ambient temperature (Tamb) with bubble sizes representing BP.

    Parameters:
        df (pd.DataFrame): DataFrame containing at least the columns 'Tamb', 'GHI', and 'BP'.

    Displays:
        A matplotlib figure showing a scatter plot where:
            - X-axis: 'Tamb' (ambient temperature)
            - Y-axis: 'GHI' (Global Horizontal Irradiance)
            - Bubble size: 'BP'
    """
    plt.figure(figsize=(10, 8))
    sb.scatterplot(df,x='Tamb', y='GHI', size='RH', sizes=(20,200))
    plt.title(f'Bubble chart GHI vs. Tamb')
    plt.show()

def plot_scatter_chart(df: pd.DataFrame):
    """
    Plots scatter charts to visualize relationships between wind and irradiance variables.
    - WS vs GHI
    - WSgust vs GHI
    - WD vs GHI
    - RH vs Tamb
    - RH vs GHI
    """
    plt.figure(figsize=(10, 6))
    sb.scatterplot(data=df, x='WS', y='GHI')
    plt.title('Wind Speed (WS) vs Global Horizontal Irradiance (GHI)')
    plt.xlabel('Wind Speed (WS)')
    plt.ylabel('GHI')
    plt.show()

    plt.figure(figsize=(10, 6))
    sb.scatterplot(data=df, x='WSgust', y='GHI')
    plt.title('Wind Gust (WSgust) vs Global Horizontal Irradiance (GHI)')
    plt.xlabel('Wind Gust (WSgust)')
    plt.ylabel('GHI')
    plt.show()

    plt.figure(figsize=(10, 6))
    sb.scatterplot(data=df, x='WD', y='GHI')
    plt.title('Wind Direction (WD) vs Global Horizontal Irradiance (GHI)')
    plt.xlabel('Wind Direction (WD)')
    plt.ylabel('GHI')
    plt.show()

    plt.figure(figsize=(10, 6))
    sb.scatterplot(data=df, x='RH', y='Tamb')
    plt.title('Relative Humidity (RH) vs Ambient Temperature (Tamb)')
    plt.xlabel('Relative Humidity (RH)')
    plt.ylabel('Ambient Temperature (Tamb)')
    plt.show()

    plt.figure(figsize=(10, 6))
    sb.scatterplot(data=df, x='RH', y='GHI')
    plt.title('Relative Humidity (RH) vs Global Horizontal Irradiance (GHI)')
    plt.xlabel('Relative Humidity (RH)')
    plt.ylabel('GHI')
    plt.show()
   
def plot_histogram_chart(df:pd.DataFrame):
    """
    Plots a 2D histogram (heatmap) of 'GHI' versus 'RH' from the given DataFrame.

    Parameters:
        df (pd.DataFrame): The input DataFrame containing at least the 'GHI' and 'RH' columns.

    Displays:
        A 2D histogram plot showing the joint distribution of 'GHI' and 'RH'.
    """
    plt.figure(figsize=(10, 8))
    sb.histplot(data=df, x='GHI', y='RH', bins=30, pthresh=0.1, cmap='Blues')
    plt.title('2D Histogram of GHI vs RH')
    plt.xlabel('GHI')
    plt.ylabel('RH')
    plt.grid(axis='both', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

def plot_avg_moda_modb(df:pd.DataFrame):
    average_mod_by_cleaning = df.groupby('Cleaning')[['ModA', 'ModB']].mean().reset_index()
    print(average_mod_by_cleaning)

    combine = average_mod_by_cleaning.melt(
        id_vars='Cleaning',
        value_vars=['ModA', 'ModB'],
        var_name='Module',
        value_name='Avg value'
    )
    plt.figure(figsize=(8, 6))
    sb.barplot(data=combine, x='Cleaning', y='Avg value', hue='Module')
    plt.title('Average ModA and ModB by Cleaning Flag')
    plt.xlabel('Cleaning Flag') # Assuming 0 and 1 represent different cleaning states
    plt.ylabel('Average Module Value')
    plt.xticks(ticks=average_mod_by_cleaning['Cleaning'], labels=average_mod_by_cleaning['Cleaning']) # Ensure all cleaning flags are shown on x-axis
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()

def plot_redial(df:pd.DataFrame):
    """
    Plots a polar scatter plot of wind speed versus wind direction.
    Parameters:
        df (pd.DataFrame): A pandas DataFrame containing at least two columns:
            - 'WD': Wind direction in degrees.
            - 'WS': Wind speed.
    The function converts wind direction from degrees to radians and plots wind speed as the radius.
    The polar plot is oriented such that 0 degrees points east and increases clockwise.
    """
    theta = np.deg2rad(df['WD'])
    r = df['WS']
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw={'projection': 'polar'})
    ax.scatter(theta, r, alpha=0.5, s=5) 

    
    ax.set_theta_zero_location("E") 
    ax.set_theta_direction(-1)     

    ax.set_xticks(np.linspace(0, 2 * np.pi, 8, endpoint=False))
    ax.set_xticklabels(['E', 'SE', 'S', 'SW', 'W', 'NW', 'N', 'NE'])
    ax.set_title('Wind Speed vs. Wind Direction', va='bottom')
    ax.grid(True)
    plt.show()

def plot_RH_relation(df:pd.DataFrame):
    """
    Plots the relationship between relative humidity (RH) and two variables: ambient temperature (Tamb) and global horizontal irradiance (GHI).

    Parameters:
        df (pd.DataFrame): DataFrame containing at least the columns 'RH', 'Tamb', and 'GHI'.

    The function creates two line plots:
        1. RH vs Tamb
        2. RH vs GHI

    Displays each plot sequentially.
    """
    sb.lineplot(df, x='RH', y='Tamb')
    plt.title(f' GHI')
    plt.show()
    sb.lineplot(df, x='RH', y='GHI')
    plt.title(f' GHI')
    plt.show()
