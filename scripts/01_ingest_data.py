import sys
import os
import pandas as pd
from sklearn.datasets import load_iris
import argparse

# Add src to path to be able to import ds_logger
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from ds_logger import start_logging, end_logging

def main(dataset_version, run_dir):
    """Main function to ingest data based on version."""
    script_name = f'01_ingest_data_{dataset_version}.py'
    
    if dataset_version == 'a':
        script_description = "Loads the original Iris dataset and saves it to the raw data directory for experiment A."
        iris = load_iris()
        df = pd.DataFrame(data=iris.data, columns=iris.feature_names)
        df['target'] = iris.target
    elif dataset_version == 'b':
        script_description = "Loads and simulates a 50% increase in the Iris dataset for experiment B."
        iris = load_iris()
        df = pd.DataFrame(data=iris.data, columns=iris.feature_names)
        df['target'] = iris.target
        # Simulate 50% more data
        df_sim = df.sample(frac=0.5, random_state=42)
        df = pd.concat([df, df_sim], ignore_index=True)
    
    start_logging(script_name=script_name, script_description=script_description, run_dir=run_dir)

    print(f"--- Data Ingestion Metrics ---")
    print(f"DataFrame shape: {df.shape}")
    print(f"DataFrame columns: {df.columns.tolist()}")
    print(f"------------------------------")

    # Save raw data
    raw_data_path = os.path.join(run_dir, 'data', 'raw', f'iris_raw_{dataset_version}.csv')
    df.to_csv(raw_data_path, index=False)

    results = {
        'rows_ingested': len(df),
        'df_shape': df.shape,
        'df_columns': df.columns.tolist()
    }
    end_logging(results=results)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Ingest Iris data for a specific experiment version.')
    parser.add_argument('--dataset_version', type=str, required=True, choices=['a', 'b'],
                        help="Version of the dataset to generate ('a' for original, 'b' for simulated')")
    parser.add_argument('--run_dir', type=str, required=True, help='The directory for this run.')
    args = parser.parse_args()
    main(args.dataset_version, args.run_dir)
