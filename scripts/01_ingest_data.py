import sys
import os
import pandas as pd
from sklearn.datasets import load_iris
import argparse

# Add src to path to be able to import ds_logger
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from ds_logger import start_logging, end_logging

def main(dataset_version):
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
    
    start_logging(script_name=script_name, script_description=script_description)

    # Save raw data
    raw_data_path = f'data/raw/iris_raw_{dataset_version}.csv'
    os.makedirs(os.path.dirname(raw_data_path), exist_ok=True)
    df.to_csv(raw_data_path, index=False)

    end_logging(results={'rows_ingested': len(df)})

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Ingest Iris data for a specific experiment version.')
    parser.add_argument('--dataset_version', type=str, required=True, choices=['a', 'b'],
                        help="Version of the dataset to generate ('a' for original, 'b' for simulated')")
    args = parser.parse_args()
    main(args.dataset_version)
