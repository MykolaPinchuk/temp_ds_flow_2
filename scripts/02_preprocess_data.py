import sys
import os
import pandas as pd
import argparse

# Add src to path to be able to import ds_logger
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from ds_logger import start_logging, end_logging

def main(input_version, run_dir):
    """Main function to preprocess data."""
    script_name = f'02_preprocess_data_{input_version}.py'
    script_description = f"Cleans and preprocesses the raw Iris data for version {input_version}."
    start_logging(script_name=script_name, script_description=script_description, run_dir=run_dir)

    # Load raw data
    raw_data_path = os.path.join(run_dir, 'data', 'raw', f'iris_raw_{input_version}.csv')
    df = pd.read_csv(raw_data_path)
    df_initial_shape = df.shape
    df_initial_columns = df.columns.tolist()

    # Clean column names
    df.columns = df.columns.str.replace(' (cm)', '', regex=False).str.replace(' ', '_')

    print(f"--- Data Preprocessing Metrics ---")
    print(f"Initial DataFrame shape: {df_initial_shape}")
    print(f"Initial DataFrame columns: {df_initial_columns}")
    print(f"Processed DataFrame shape: {df.shape}")
    print(f"Processed DataFrame columns: {df.columns.tolist()}")
    print(f"----------------------------------")

    # Save processed data
    processed_data_path = os.path.join(run_dir, 'data', 'processed', f'iris_processed_{input_version}.csv')
    df.to_csv(processed_data_path, index=False)

    results = {
        'processed_rows': len(df),
        'initial_df_shape': df_initial_shape,
        'initial_df_columns': df_initial_columns,
        'processed_df_shape': df.shape,
        'processed_df_columns': df.columns.tolist()
    }
    end_logging(results=results)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Preprocess Iris data.')
    parser.add_argument('--input_version', type=str, required=True, choices=['a', 'b'],
                        help="Version of the raw data to process ('a' or 'b')")
    parser.add_argument('--run_dir', type=str, required=True, help='The directory for this run.')
    args = parser.parse_args()
    main(args.input_version, args.run_dir)
