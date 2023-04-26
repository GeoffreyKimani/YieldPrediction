import os

import pandas as pd

from YieldPrediction.consts.constants import COUNTRY_LIST

ROOT_PATH = os.getcwd()
DATA_PATH = ROOT_PATH + '/Data'

country_data = dict.fromkeys(COUNTRY_LIST)

"""Read the country data"""
for country, data in country_data.items():
    country_data[country] = pd.read_excel(f"{DATA_PATH}/Gyga{country}.xlsx", sheet_name="Station Year")

"""EDA and cleaning"""
# Get the initial null values
for country, data in country_data.items():
    print(country, "\n", "*" * 10)
    print(data.isnull().sum())  # get null values
    print("\n")

# Fill the null values
# Select only the numeric columns
numeric_cols = ['YA', 'YW', 'YP', 'WPP']

for country, data in country_data.items():
    print(country)
    # Group by Area
    grouped = data.groupby('STATIONNAME')

    # Fill missing values within each group
    filled = grouped[numeric_cols].transform(lambda x: x.fillna(x.mean()))

    # Merge the filled DataFrame with the original DataFrame
    country_data[country] = pd.concat([data.drop(numeric_cols, axis=1), filled], axis=1)
    print(country_data[country])

# get null values after
for country, data in country_data.items():
    print(country, "\n", "*" * 10)
    print(data.isnull().sum())  # get null values
    print("\n")

# drop the remaining nul values
for country, data in country_data.items():
    country_data[country] = data.dropna()

# get null values after
for country, data in country_data.items():
    print(country, "\n", "*" * 10)
    print(data.isnull().sum())  # get null values
    print("\n")

"""Concatenate the datasets"""
yield_df = pd.concat(list(country_data.values()))
print(f"Final yield dataset: {yield_df}")
