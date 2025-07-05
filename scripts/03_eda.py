import sys
import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import argparse

# Add src to path to be able to import ds_logger
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from ds_logger import start_logging, end_logging

def main(input_version, run_dir):
    """Main function to perform EDA."""
    script_name = f'03_eda_{input_version}.py'
    script_description = f"Performs EDA on the processed Iris data ({input_version}) and saves a pairplot."
    start_logging(script_name=script_name, script_description=script_description, run_dir=run_dir)

    # Load processed data
    processed_data_path = os.path.join(run_dir, 'data', 'processed', f'iris_processed_{input_version}.csv')
    df = pd.read_csv(processed_data_path)

    print(f"--- EDA Metrics ---")
    print(f"DataFrame shape: {df.shape}")
    print(f"DataFrame columns: {df.columns.tolist()}")
    print(f"---------------------")

    # Generate pairplot
    sns.pairplot(df, hue='target')

    # Save plot
    plot_path = os.path.join(run_dir, 'reports', f'iris_pairplot_{input_version}.png')
    plt.savefig(plot_path)

    results = {
        'plot_generated': os.path.basename(plot_path),
        'df_shape': df.shape,
        'df_columns': df.columns.tolist()
    }
    end_logging(results=results)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Perform EDA on Iris data.')
    parser.add_argument('--input_version', type=str, required=True, choices=['a', 'b'],
                        help="Version of the processed data to use ('a' or 'b')")
    parser.add_argument('--run_dir', type=str, required=True, help='The directory for this run.')
    args = parser.parse_args()
    main(args.input_version, args.run_dir)
