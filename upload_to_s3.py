import os
import boto3
import snowflake.connector

# Configuration
bucket_name = "snowflake-bronze-raw-data"
s3_prefix = "bronze"
data_folder = "data"
files = ["transactions.csv", "inventory.csv", "stores.csv", "products.csv", "customers.csv"]

# Upload files to S3
s3 = boto3.client("s3")
for file_name in files:
    s3_path = f"{s3_prefix}/{file_name}"
    local_path = os.path.join(data_folder, file_name)
    s3.upload_file(local_path, bucket_name, s3_path)
    print(f"Uploaded {file_name} to s3://{bucket_name}/{s3_path}")

# Connect to Snowflake
conn = snowflake.connector.connect(
    user=os.getenv("SNOWFLAKE_USER"),
    password=os.getenv("SNOWFLAKE_PASSWORD"),
    role=os.getenv("SNOWFLAKE_ROLE"),
    warehouse="DATAOPS_WH",
    database="DATAOPS_DB",
    schema="BRONZE",
    account=os.getenv("SNOWFLAKE_ACCOUNT_NAME"),
    organization=os.getenv("SNOWFLAKE_ORGANIZATION_NAME"),
    host=f"{os.getenv('SNOWFLAKE_ORGANIZATION_NAME')}-{os.getenv('SNOWFLAKE_ACCOUNT_NAME')}.snowflakecomputing.com"
)

cur = conn.cursor()

# Create tables and load data
table_schemas = {
    "transactions": "transaction_id INT, customer_id INT, product_id INT, store_id INT, quantity INT, total_price FLOAT, transaction_date DATE",
    "inventory": "inventory_id INT, store_id INT, product_id INT, quantity_available INT",
    "stores": "store_id INT, store_name STRING, city STRING, state STRING, country STRING",
    "products": "product_id INT, product_name STRING, category STRING, price FLOAT",
    "customer": "customer_id INT, name STRING, email STRING, age INT, signup_date DATE"
}

for name, schema in table_schemas.items():
    table_name = name.lower()
    file_name = f"{table_name}.csv"
    stage_path = f"@bronze_stage/{file_name}"

    cur.execute(f"""
    COPY INTO {table_name}
    FROM {stage_path}
    FILE_FORMAT = (
        TYPE = CSV
        FIELD_OPTIONALLY_ENCLOSED_BY = '"'
        SKIP_HEADER = 1
        ERROR_ON_COLUMN_COUNT_MISMATCH = FALSE
        TRIM_SPACE = TRUE
    )
    ON_ERROR = 'CONTINUE';
""")
print(f"Table '{table_name}' created and data loaded.")


cur.close()
conn.close()
