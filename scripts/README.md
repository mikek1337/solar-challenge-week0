# scripts/

This directory contains Python scripts for data preprocessing and reporting for the Solar Data Discovery project.

## Files

- **preprocess.py**  
  Provides functions for cleaning and preprocessing the dataset:
  - `find_and_replace_outliers_with_median(df, cols, iqr_multiplier=1.5)`:  
    Detects outliers in specified columns using the IQR method and replaces them with the median.
  - `clean_data(df, cols)`:  
    Removes the 'Comments' column, forward-fills missing values, clips specified columns to non-negative values, clips 'RH' to [0, 100], and replaces outliers with the median.

- **report.py**  
  Provides a function for generating a data quality report:
  - `data_quality_report(df)`:  
    Returns a DataFrame summarizing missing values, zero values, negative values, and out-of-range values for key columns.

## Usage

Import the functions in your analysis scripts or notebooks:

```python
from scripts.preprocess import clean_data, find_and_replace_outliers_with_median
from scripts.report import data_quality_report