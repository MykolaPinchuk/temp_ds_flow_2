import sys
import os
import pandas as pd
import joblib
from sklearn.metrics import accuracy_score, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt
import argparse

# Add src to path to be able to import ds_logger
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from ds_logger import start_logging, end_logging

def main(input_version):
    """Main function to evaluate models."""
    script_name = f'06_evaluate_alternative_models_{input_version}.py'
    script_description = f"Evaluates and compares the trained models for data version {input_version}."
    start_logging(script_name=script_name, script_description=script_description)

    # Load Models
    lr_model_path = f'models/iris_log_reg_{input_version}.joblib'
    rf_model_path = f'models/iris_random_forest_{input_version}.joblib'
    lr_model = joblib.load(lr_model_path)
    rf_model = joblib.load(rf_model_path)

    # Load feature-engineered data
    features_path = f'data/processed/iris_features_{input_version}.csv'
    df = pd.read_csv(features_path)

    # Load the test set for consistent evaluation
    X_test_path = f'data/processed/X_test_{input_version}.csv'
    y_test_path = f'data/processed/y_test_{input_version}.csv'
    X_test = pd.read_csv(X_test_path)
    y_test = pd.read_csv(y_test_path)

    # Evaluate Logistic Regression
    lr_preds = lr_model.predict(X_test)
    lr_accuracy = accuracy_score(y_test, lr_preds)
    lr_cm = confusion_matrix(y_test, lr_preds)

    # Evaluate Random Forest
    rf_preds = rf_model.predict(X_test)
    rf_accuracy = accuracy_score(y_test, rf_preds)
    rf_cm = confusion_matrix(y_test, rf_preds)

    # Generate and save confusion matrix plots
    plt.figure(figsize=(16, 6))

    plt.subplot(1, 2, 1)
    sns.heatmap(lr_cm, annot=True, fmt='d', cmap='Blues')
    plt.title('Logistic Regression Confusion Matrix')
    plt.ylabel('Actual')
    plt.xlabel('Predicted')

    plt.subplot(1, 2, 2)
    sns.heatmap(rf_cm, annot=True, fmt='d', cmap='Greens')
    plt.title('Random Forest Confusion Matrix')
    plt.ylabel('Actual')
    plt.xlabel('Predicted')

    plot_path = f'reports/confusion_matrices_{input_version}.png'
    os.makedirs(os.path.dirname(plot_path), exist_ok=True)
    plt.savefig(plot_path)

    results = {
        'logistic_regression_accuracy': lr_accuracy,
        'random_forest_accuracy': rf_accuracy
    }
    end_logging(results=results)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Evaluate models on Iris data.')
    parser.add_argument('--input_version', type=str, required=True, choices=['a', 'b'],
                        help="Version of the models and data to use ('a' or 'b')")
    args = parser.parse_args()
    main(args.input_version)
