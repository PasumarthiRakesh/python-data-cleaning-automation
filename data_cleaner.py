import pandas as pd
import os
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(
    filename="process.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def load_csv(file_path):
    if not os.path.exists(file_path):
        logging.error("Input file does not exist.")
        raise FileNotFoundError("CSV file not found.")
    
    logging.info("Loading CSV file...")
    return pd.read_csv(file_path)

def clean_data(df):
    logging.info("Cleaning data...")

    # Remove duplicates
    df = df.drop_duplicates()

    # Fill missing numerical columns with mean
    for col in df.select_dtypes(include="number").columns:
        df[col] = df[col].fillna(df[col].mean())

    # Fill missing text columns with "Unknown"
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].fillna("Unknown")

    return df

def save_cleaned_data(df, output_file):
    df.to_csv(output_file, index=False)
    logging.info(f"Cleaned file saved as {output_file}")

def generate_report(df):
    report = {
        "total_rows": len(df),
        "total_columns": len(df.columns),
        "missing_values": df.isnull().sum().to_dict(),
        "numerical_summary": df.describe().to_dict()
    }

    with open("report.txt", "w") as f:
        f.write(str(report))

    logging.info("Generated summary report.")

def main():
    input_file = "input.csv"
    output_file = f"cleaned_{datetime.now().strftime('%Y%m%d_%H%M')}.csv"

    df = load_csv(input_file)
    cleaned_df = clean_data(df)
    save_cleaned_data(cleaned_df, output_file)
    generate_report(cleaned_df)

    logging.info("Data cleaning automation completed successfully.")

if __name__ == "__main__":
    main()
