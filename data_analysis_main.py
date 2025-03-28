import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import sys
import os

def analyze_print_data(input_path, output_path):
    with open(output_path, 'a') as file:
        data = pd.read_csv(input_path)

        numeric_columns = data.select_dtypes(include='number')
        cat_columns = data.select_dtypes(include='object')

        describe_num = numeric_columns.describe(percentiles=[0.05, 0.95])
        median_values = numeric_columns.median()
        numeric_null_sum = numeric_columns.isnull().sum()

        unique_cats = cat_columns.nunique(dropna=True)
        cat_null_sum = cat_columns.isnull().sum()
