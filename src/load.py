import pandas as pd
import sqlite3

# -----------------------------
# 1. Read cleaned data
# -----------------------------

df = pd.read_csv("../data/cleaned_sales.csv")

print(f"Loaded {len(df)} cleaned records from CSV")


# -----------------------------
# 2. Connect to SQLite database
# -----------------------------

connection = sqlite3.connect("../ecommerce.db")

print("Connected to SQLite database")


# -----------------------------
# 3. Load data into sales table
# -----------------------------

df.to_sql(
    "sales",
    connection,
    if_exists="replace",
    index=False
)

print("Data loaded into 'sales' table")


# -----------------------------
# 4. Verify the loaded data
# -----------------------------

cursor = connection.cursor()

cursor.execute("SELECT COUNT(*) FROM sales")

count = cursor.fetchone()[0]

print(f"Records in database: {count}")


# -----------------------------
# 5. Close connection
# -----------------------------

connection.close()

print("Database connection closed")