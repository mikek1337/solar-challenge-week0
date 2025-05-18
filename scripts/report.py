import pandas as pd
import numpy as np
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