import dask.dataframe as dd

def sample(csv_path, output_path, n=10000, blocksize="256MB", sample_size=10_000_000):
    # Read only the first 1000 rows
    df = dd.read_csv(csv_path, blocksize=blocksize, sample=sample_size).head(n)

    # Convert to Dask DataFrame for saving
    df_sampled = dd.from_pandas(df, npartitions=1)

    # Save as a single CSV file
    df_sampled.to_csv(output_path, index=False, single_file=True)
    print(f"Saved top {n} rows to {output_path}")

if __name__ == "__main__":
    csv_path = "../data/training.csv"
    output_path = "../data/sample_data.csv"
    target_col = "飆股"  # Ensure this matches the column name in your dataset

    # Run optimized sampling
    sample(csv_path, output_path, n=10000)



