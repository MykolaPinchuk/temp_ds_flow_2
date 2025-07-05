import sys
import os
import pandas as pd
import joblib
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import seaborn as sns
import matplotlib.pyplot as plt
import argparse
import json

# Add src to path to be able to import ds_logger
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from ds_logger import start_logging, end_logging

def main(input_version, run_dir):
    """Main function to evaluate multiple models."""
    script_name = f'06_evaluate_hyperparameter_models_{input_version}.py'
    script_description = f"Evaluates multiple models for data version {input_version}."
    start_logging(script_name=script_name, script_description=script_description, run_dir=run_dir)

    # Load the test set
    X_test_path = os.path.join(run_dir, 'data', 'processed', f'X_test_{input_version}.csv')
    y_test_path = os.path.join(run_dir, 'data', 'processed', f'y_test_{input_version}.csv')
    X_test = pd.read_csv(X_test_path)
    y_test = pd.read_csv(y_test_path)

    model_names = ['rf_simple', 'rf_medium', 'rf_complex', 'xgb_simple', 'xgb_complex']
    models = {}
    for model_name in model_names:
        model_path = os.path.join(run_dir, 'models', f'iris_{model_name}_{input_version}.joblib')
        models[model_name] = joblib.load(model_path)

    print(f"--- Model Evaluation Metrics ---")
    print(f"X_test shape: {X_test.shape}")
    print(f"y_test shape: {y_test.shape}")
    print(f"--------------------------------")

    results = {
        'evaluation_metrics': {},
        'test_data_shape': {
            'X_test': X_test.shape,
            'y_test': y_test.shape
        }
    }

    # Generate and save classification reports
    report_path = os.path.join(run_dir, 'reports', f'classification_reports_{input_version}.txt')
    with open(report_path, 'w') as f:
        for model_name, model in models.items():
            preds = model.predict(X_test)
            accuracy = accuracy_score(y_test, preds)
            report = classification_report(y_test, preds)
            cm = confusion_matrix(y_test, preds)

            results['evaluation_metrics'][model_name] = {
                'accuracy': accuracy,
                'classification_report': classification_report(y_test, preds, output_dict=True),
                'confusion_matrix': cm.tolist()
            }

            print(f"{model_name} Accuracy: {accuracy:.4f}")
            print(f"{model_name} Classification Report:")
            print(report)
            print(f"--------------------------------")

            f.write(f'{model_name} Classification Report:\n')
            f.write(report)
            f.write('\n\n')

    # Generate and save confusion matrix plots
    num_models = len(models)
    plt.figure(figsize=(6 * num_models, 5))
    for i, (model_name, model) in enumerate(models.items()):
        plt.subplot(1, num_models, i + 1)
        cm = results['evaluation_metrics'][model_name]['confusion_matrix']
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
        plt.title(f'{model_name} Confusion Matrix')
        plt.ylabel('Actual')
        plt.xlabel('Predicted')

    plot_path = os.path.join(run_dir, 'reports', f'confusion_matrices_{input_version}.png')
    plt.savefig(plot_path)
    plt.close()

    end_logging(results=results)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Evaluate multiple models.')
    parser.add_argument('--input_version', type=str, required=True, choices=['a', 'b', 'c', 'd', 'e'],
                        help="Version of the models and data to use.")
    parser.add_argument('--run_dir', type=str, required=True, help='The directory for this run.')
    args = parser.parse_args()
    main(args.input_version, args.run_dir)
