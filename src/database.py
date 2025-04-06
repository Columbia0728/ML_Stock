import pandas as pd
import psycopg2

# Define database connection
conn = psycopg2.connect(
    dbname="mydatabase",
    user="postgres",
    password="password",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

# Define CSV file path
csv_path = "../data/training.csv"
chunk_size = 5000  # Adjust based on system memory

# Read CSV in chunks
for chunk in pd.read_csv(csv_path, chunksize=chunk_size):
    ### 1. Insert Metadata (ID, "飆股")
    metadata_chunk = chunk[['ID', '飆股']]
    metadata_records = metadata_chunk.values.tolist()
    
    cur.executemany(
        "INSERT INTO metadata (ID, 飆股) VALUES (%s, %s) ON CONFLICT DO NOTHING", 
        metadata_records
    )

    ### 2. Insert Features into Multiple Feature Tables
    num_features = 10212
    features_per_table = 1598  # Avoid exceeding PostgreSQL's 1600 column limit

    for i in range(0, num_features, features_per_table):
        start = i + 1
        end = min(i + features_per_table, num_features)
        table_name = f"features_{i//features_per_table + 1}"
        
        # Select relevant columns (convert column names to string)
        feature_chunk = chunk[['ID'] + [str(j) for j in range(start, end + 1)]]
        feature_records = feature_chunk.values.tolist()

        # Prepare SQL query
        placeholders = ",".join(["%s"] * len(feature_chunk.columns))
        sql = f"INSERT INTO {table_name} VALUES ({placeholders}) ON CONFLICT DO NOTHING"
        
        # Bulk insert into feature table
        cur.executemany(sql, feature_records)

    # Commit after processing each chunk
    conn.commit()
    print(f"Inserted {chunk_size} rows...")

# Close connection
cur.close()
conn.close()
print("Data import completed successfully!")









