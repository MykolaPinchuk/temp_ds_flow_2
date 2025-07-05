import sys
import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import argparse

# Add src to path to be able to import ds_logger
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from ds_logger import start_logging, end_logging

def main(input_version):
    """Main function to perform EDA."""
    script_name = f'03_eda_{input_version}.py'
    script_description = f"Performs EDA on the processed Iris data ({input_version}) and saves a pairplot."
    start_logging(script_name=script_name, script_description=script_description)

    # Load processed data
    processed_data_path = f'data/processed/iris_processed_{input_version}.csv'
    df = pd.read_csv(processed_data_path)

    # Generate pairplot
    sns.pairplot(df, hue='target')

    # Save plot
    plot_path = f'reports/iris_pairplot_{input_version}.png'
    os.makedirs(os.path.dirname(plot_path), exist_ok=True)
    plt.savefig(plot_path)

    end_logging(results={'plot_generated': os.path.basename(plot_path)})

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Perform EDA on Iris data.')
    parser.add_argument('--input_version', type=str, required=True, choices=['a', 'b'],
                        help="Version of the processed data to use ('a' or 'b')")
    args = parser.parse_args()
    main(args.input_version)
