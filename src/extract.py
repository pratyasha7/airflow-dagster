from pathlib import Path
import pandas as pd


def extract_data(file_path):
    """Read raw sales data from a CSV file."""
    df = pd.read_csv(file_path)

    print(f"Extracted {len(df)} records")
    print(f"Columns: {list(df.columns)}")

    return df


if __name__ == "__main__":
    # Resolves paths relative to this script's directory: src/ -> ../data/
    base_dir = Path(__file__).resolve().parent
    file_path = base_dir.parent / "data" / "sales.csv"

    df = extract_data(file_path)

    print("\nFirst 5 records:")
    print(df.head())