from pathlib import Path
import pandas as pd


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    initial_count = len(df)

    # 1. Deduplicate by order_id
    df = df.drop_duplicates(subset=["order_id"], keep="first")
    print(f"Removed duplicates: {initial_count - len(df)} row(s)")

    # 2. Filter invalid quantities (quantity > 0)
    valid_qty_count = len(df)
    df = df[df["quantity"] > 0]
    print(f"Removed invalid quantities: {valid_qty_count - len(df)} row(s)")

    # 3. Impute missing categories
    category_reference = (
        df.dropna(subset=["category"])
        .drop_duplicates(subset=["product"])
        .set_index("product")["category"]
    )
    df["category"] = df["category"].fillna(df["product"].map(category_reference))

    # 4. Impute missing prices
    price_reference = (
        df.dropna(subset=["price"]).groupby("product")["price"].first()
    )
    df["price"] = df["price"].fillna(df["product"].map(price_reference))

    # 5. Normalize dates to YYYY-MM-DD
    df["order_date"] = pd.to_datetime(
        df["order_date"], format="mixed", errors="coerce"
    ).dt.strftime("%Y-%m-%d")

    # 6. Calculate total amount
    df["total_amount"] = df["quantity"] * df["price"]

    print(f"Cleaned dataset records: {len(df)}")
    return df


if __name__ == "__main__":
    base_dir = Path(__file__).resolve().parent
    file_path = base_dir.parent / "data" / "sales.csv"

    # Reuse extract
    from extract import extract_data

    raw_df = extract_data(file_path)
    cleaned_df = clean_data(raw_df)

    print("\nCleaned sample:")
    print(cleaned_df.head())
    print("\nRemaining null values:")
    print(cleaned_df.isnull().sum())

    # Save to data/cleaned_sales.csv using cleaned_df
    output_path = base_dir.parent / "data" / "cleaned_sales.csv"
    cleaned_df.to_csv(output_path, index=False)
    print(f"\nCleaned data saved to: {output_path}")