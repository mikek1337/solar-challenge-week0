# Solar Challenge Week 0 - Data Analysis Notebooks

This repository contains Jupyter notebooks and Python scripts for exploratory data analysis and data cleaning of solar resource datasets from various West African countries.

## Structure
solar-challenge-week0/ │ ├── scripts/ │ ├── preprocess.py # Data cleaning and outlier handling functions │ ├── report.py # Data quality reporting and plotting functions │ └── __init__.py # Makes scripts a Python package │ ├── notebooks/ │ ├── benin_eda.ipynb # EDA for Benin dataset │ ├── sierraleone_eda.ipynb # EDA for Sierra Leone dataset │ └── togo_eda.ipynb # EDA for Togo dataset │ └── data/ ├── benin-malanville.csv ├── sierraleone-bumbuna.csv └── togo-dapaong_qc.csv

## Notebooks

- **benin_eda.ipynb**  
  Manual data cleaning, outlier handling (z-score), and visualization for Benin data.

- **togo_eda.ipynb**  
  Uses shared scripts for cleaning (`clean_data`), missing value analysis, and data quality reporting. Plots time series for GHI, DNI, DHI, Tamb.

- **sierraleone_eda.ipynb**  
  Similar workflow as Togo, using shared scripts for cleaning and reporting. Uses `plot_time_series` from `report.py` for visualization.

## Scripts

- **preprocess.py**  
  - `clean_data(df, cols)`: Cleans data, handles missing values, clips out-of-range values, and replaces outliers.
  - `find_and_replace_outliers_with_median(df, cols)`: Replaces outliers with median using IQR.
  - `find_columns_with_missing_value(df, threshold)`: Lists columns with missing values above a threshold.

- **report.py**  
  - `data_quality_report(df)`: Summarizes missing, zero, negative, and out-of-range values.
  - `plot_time_series(df)`: Plots GHI, DNI, DHI, Tamb vs. Timestamp as a line chart.

## Usage

1. **Install dependencies**  
   Make sure you have the required Python packages (see `requirements.txt`).

2. **Run notebooks**  
   Open any notebook in `notebooks/` and run the cells.  
   The notebooks import functions from `scripts/` for consistent data processing.

3. **Custom scripts**  
   You can import and use the cleaning and reporting functions in your own notebooks or scripts:

   ```python
   import sys
   sys.path.append('../scripts')
   from preprocess import clean_data, find_columns_with_missing_value
   from report import data_quality_report, plot_time_series