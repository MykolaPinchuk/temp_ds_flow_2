import sys
import os
import pandas as pd
import argparse

# Add src to path to be able to import ds_logger
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from ds_logger import start_logging, end_logging

def main(input_version):
    """Main function to preprocess data."""
    script_name = f'02_preprocess_data_{input_version}.py'
    script_description = f"Cleans and preprocesses the raw Iris data for version {input_version}."
    start_logging(script_name=script_name, script_description=script_description)

    # Load raw data
    raw_data_path = f'data/raw/iris_raw_{input_version}.csv'
    df = pd.read_csv(raw_data_path)

    # Clean column names
    df.columns = df.columns.str.replace(' (cm)', '', regex=False).str.replace(' ', '_')

    # Save processed data
    processed_data_path = f'data/processed/iris_processed_{input_version}.csv'
    os.makedirs(os.path.dirname(processed_data_path), exist_ok=True)
    df.to_csv(processed_data_path, index=False)

    end_logging(results={'processed_rows': len(df), 'processed_columns': list(df.columns)})

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Preprocess Iris data.')
    parser.add_argument('--input_version', type=str, required=True, choices=['a', 'b'],
                        help="Version of the raw data to process ('a' or 'b')")
    args = parser.parse_args()
    main(args.input_version)
