import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import sys
import os
from sklearn.preprocessing import LabelEncoder

def analyze_write_data(input_path, output_path, image_dir_path):
    if os.path.dirname(output_path):
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
    os.makedirs(image_dir_path, exist_ok=True)
    with open(output_path, 'w') as file:
        data = pd.read_csv(input_path)

        numeric_columns = data.select_dtypes(include='number')
        cat_columns = data.select_dtypes(include='object')

        describe_num = numeric_columns.describe(percentiles=[0.05, 0.95])
        median_values = numeric_columns.median()
        numeric_null_sum = numeric_columns.isnull().sum()

        stats_df = describe_num.T
        stats_df['Median'] = median_values
        stats_df['Null Values Count'] = numeric_null_sum
        stats_df.to_csv(file)

        unique_vals = cat_columns.nunique(dropna=True)
        cat_null_sum = cat_columns.isnull().sum()
        cat_df = pd.DataFrame(unique_vals, columns=['Unique val count'])
        cat_df['Null count'] = cat_null_sum
        cat_df.to_csv(file, mode='a')

        file.write('\nCategorical Column Proportions\n')

        for col in cat_columns:
            category_proportions = cat_columns[col].value_counts(normalize=True).reset_index()
            category_proportions.columns = [col, 'Proportion']

            category_proportions.to_csv(file, index=False, mode='a')

            file.write('\n')

        i=0
        subdir_path = os.path.join(image_dir_path, 'Boxplots')
        os.makedirs(subdir_path, exist_ok=True)
        for col in numeric_columns:
            output_image_path = os.path.join(subdir_path, f'Boxplot_{i}.png')
            i+=1
            sns.boxplot(data=numeric_columns, y=numeric_columns[col])
            plt.savefig(output_image_path, dpi=300, bbox_inches='tight')
            plt.close()

        i = 0
        subdir_path = os.path.join(image_dir_path, 'Violinplots')
        os.makedirs(subdir_path, exist_ok=True)
        for col in numeric_columns:
            output_image_path = os.path.join(subdir_path, f'Violinplot_{i}.png')
            i += 1
            sns.violinplot(data=numeric_columns, y=numeric_columns[col])
            plt.savefig(output_image_path, dpi=300, bbox_inches='tight')
            plt.close()

        i = 0
        subdir_path = os.path.join(image_dir_path, 'Barplots')
        os.makedirs(subdir_path, exist_ok=True)
        for col in numeric_columns:
            output_image_path = os.path.join(subdir_path, f'Barplot_{i}.png')
            i += 1
            sns.barplot(data=numeric_columns, y=numeric_columns[col])
            plt.savefig(output_image_path, dpi=300, bbox_inches='tight')
            plt.close()

        i = 0
        subdir_path = os.path.join(image_dir_path, 'Histograms')
        os.makedirs(subdir_path, exist_ok=True)
        for col in numeric_columns:
            output_image_path = os.path.join(subdir_path, f'Histogram_{i}.png')
            i += 1
            sns.histplot(data=numeric_columns[col], bins=10)
            plt.savefig(output_image_path, dpi=300, bbox_inches='tight')
            plt.close()

        i = 0
        subdir_path = os.path.join(image_dir_path, 'Histograms_gender')
        os.makedirs(subdir_path, exist_ok=True)
        for col in numeric_columns:
            output_image_path = os.path.join(subdir_path, f'Histogram_gender_{i}.png')
            i += 1
            sns.histplot(data=data, bins=10, x=col, hue='Gender')
            plt.savefig(output_image_path, dpi=300, bbox_inches='tight')
            plt.close()

        output_image_path = os.path.join(image_dir_path, f'Correlation_heatmap.png')
        plt.figure(figsize=(10, 8))
        num_corr_matrix = numeric_columns.corr()
        sns.heatmap(num_corr_matrix, annot=True)

        plt.savefig(output_image_path, dpi=300, bbox_inches='tight')
        plt.close()

        subdir_path = os.path.join(image_dir_path, 'Correlations')
        os.makedirs(subdir_path, exist_ok=True)
        corr_df = pd.DataFrame(num_corr_matrix)
        for col1 in numeric_columns:
            for col2 in numeric_columns:
                if col1 != col2:
                    if abs(corr_df[col1][col2]) >= 0.2:
                        output_image_path = os.path.join(subdir_path, f'Relation_{col1}_{col2}.png')
                        sns.regplot(x=data[col1], y=data[col2])
                        plt.savefig(output_image_path, dpi=300, bbox_inches='tight')
                        plt.close()

        le = LabelEncoder()
        numeric_columns['encoded_target'] = le.fit_transform(data['NObeyesdad'])
        num_corr_matrix = numeric_columns.corr()
        corr_df = pd.DataFrame(num_corr_matrix)
        corrs_encoded_target = corr_df.sort_values('encoded_target', axis=0, ascending=False)
        corrs_encoded_target.to_csv(file, mode='a')

        output_image_path = os.path.join(image_dir_path, f'Heatmap_with_encoded_target.png')
        plt.figure(figsize=(10, 8))
        sns.heatmap(num_corr_matrix, annot=True)
        plt.savefig(output_image_path, dpi=300, bbox_inches='tight')
        plt.close()


def main():
    analyze_write_data("ObesityDataSet_raw_and_data_sinthetic.csv", "Output.csv", "Images")

if __name__ == "__main__":
    main()