import dask.dataframe as dd
import os


def clean_data(csv_path, output_path, blocksize="256MB", sample_size=10_000_000):
    # Read CSV file in chunks
    df = dd.read_csv(csv_path, blocksize=blocksize, sample=sample_size)

    # Identify columns with missing values (using metadata from a small sample)
    missing_columns = df.columns[df.isnull().any().compute()]

    # Drop columns with missing values
    df_cleaned = df.drop(columns=missing_columns)

    # Save the cleaned data to a new CSV file
    df_cleaned.to_csv(output_path, index=False, single_file=True)


if __name__ == "__main__":
    # Define your file paths
    csv_path = "../data/sample_data.csv"  # Adjust the path to your CSV
    output_path = "../data/cleaned_sample.csv"  # Where you want the cleaned data saved
    
    # Run the cleaning process
    clean_data(csv_path, output_path, blocksize="256MB")
