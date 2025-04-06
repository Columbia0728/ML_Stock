import os
import zipfile
from abc import ABC, abstractmethod

import dask.dataframe as dd
import pandas as pd


# Define an abstract class for Data Ingestor
class DataIngestor(ABC):
    @abstractmethod
    def ingest(self, file_path: str, save_dir: str = "../data") -> dd.DataFrame:
        """Abstract method to ingest data from a given file."""
        pass


# Implement a concrete class for ZIP Ingestion
class ZipDataIngestor(DataIngestor):
    def ingest(self, file_path: str, save_dir: str = "../data") -> dd.DataFrame:
        """Extracts a .zip file and returns the content as a Dask or Pandas DataFrame."""
        if not file_path.endswith(".zip"):
            raise ValueError("The provided file is not a .zip file.")

        os.makedirs(save_dir, exist_ok=True)  # Ensure save directory exists

        with zipfile.ZipFile(file_path, "r") as zip_ref:
            csv_files = [f for f in zip_ref.namelist() if f.endswith(".csv")]

            if len(csv_files) == 0:
                raise FileNotFoundError("No CSV file found in the ZIP archive.")
            if len(csv_files) > 1:
                raise ValueError("Multiple CSV files found. Please specify which one to use.")

            # Extract only the required CSV file
            csv_filename = csv_files[0]
            csv_file_path = os.path.join(save_dir, csv_filename)

            if not os.path.exists(csv_file_path):  # Avoid re-extracting
                zip_ref.extract(csv_filename, save_dir)

        print(f"✅ CSV extracted and saved at: {csv_file_path}")

        # Check file size to decide whether to use Dask or Pandas
        file_size = os.path.getsize(csv_file_path)

        if file_size < 50 * 1024 * 1024:  # If < 50MB, use Pandas for speed
            print("⚡ Small file detected, using Pandas...")
            return pd.read_csv(csv_file_path)

        print("📊 Large file detected, using Dask...")
        
        # Increase `sample` size to avoid errors
        df = dd.read_csv(csv_file_path, blocksize="256MB", sample=10_000_000)

        return df


# Implement a Factory to create DataIngestors
class DataIngestorFactory:
    @staticmethod
    def get_data_ingestor(file_extension: str) -> DataIngestor:
        """Returns the appropriate DataIngestor based on file extension."""
        if file_extension == ".zip":
            return ZipDataIngestor()
        else:
            raise ValueError(f"No ingestor available for file extension: {file_extension}")


if __name__ == "__main__":
    file_path = "../zip data/38_Training_Data_Set_V2.zip"  # Relative from ML_comp/src

    # Determine the file extension
    file_extension = os.path.splitext(file_path)[1]

    # Get the appropriate DataIngestor
    data_ingestor = DataIngestorFactory.get_data_ingestor(file_extension)

    # Ingest the data
    df = data_ingestor.ingest(file_path)

    # Display the first few rows without loading everything into memory
    print(df.head())  

