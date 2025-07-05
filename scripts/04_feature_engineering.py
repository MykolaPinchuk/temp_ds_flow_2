import sys
import os
import pandas as pd
import argparse

# Add src to path to be able to import ds_logger
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from ds_logger import start_logging, end_logging

def main(input_version, run_dir):
    """Main function for feature engineering."""
    script_name = f'04_feature_engineering_{input_version}.py'
    script_description = f"Creates a new feature, 'sepal_area', from the processed Iris data ({input_version})."
    start_logging(script_name=script_name, script_description=script_description, run_dir=run_dir)

    # Load processed data
    processed_data_path = os.path.join(run_dir, 'data', 'processed', f'iris_processed_{input_version}.csv')
    df = pd.read_csv(processed_data_path)

    # Create new feature
    df['sepal_area'] = df['sepal_length'] * df['sepal_width']

    # Save feature-engineered data
    features_path = os.path.join(run_dir, 'data', 'processed', f'iris_features_{input_version}.csv')
    df.to_csv(features_path, index=False)

    end_logging(results={'features_created': ['sepal_area']})

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Perform feature engineering on Iris data.')
    parser.add_argument('--input_version', type=str, required=True, choices=['a', 'b'],
                        help="Version of the processed data to use ('a' or 'b')")
    parser.add_argument('--run_dir', type=str, required=True, help='The directory for this run.')
    args = parser.parse_args()
    main(args.input_version, args.run_dir)
