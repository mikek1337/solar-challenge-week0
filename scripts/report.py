import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sb
def data_quality_report(df: pd.DataFrame) -> pd.DataFrame:
    """Generate comprehensive data quality report"""
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