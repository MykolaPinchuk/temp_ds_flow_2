import sys
import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib
import argparse

# Add src to path to be able to import ds_logger
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from ds_logger import start_logging, end_logging

def main(input_version, run_dir):
    """Main function to train and evaluate models."""
    script_name = f'05_train_alternative_model_{input_version}.py'
    script_description = f"Trains and compares Logistic Regression and Random Forest models on data version {input_version}."
    start_logging(script_name=script_name, script_description=script_description, run_dir=run_dir)

    # Load feature-engineered data
    features_path = os.path.join(run_dir, 'data', 'processed', f'iris_features_{input_version}.csv')
    df = pd.read_csv(features_path)

    # Prepare data for modeling
    X = df.drop('target', axis=1)
    y = df['target']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Save the test set for consistent evaluation
    X_test_path = os.path.join(run_dir, 'data', 'processed', f'X_test_{input_version}.csv')
    y_test_path = os.path.join(run_dir, 'data', 'processed', f'y_test_{input_version}.csv')
    X_test.to_csv(X_test_path, index=False)
    y_test.to_csv(y_test_path, index=False)

    # Train and evaluate Logistic Regression
    lr_model = LogisticRegression(max_iter=1000)
    lr_model.fit(X_train, y_train)
    lr_preds = lr_model.predict(X_test)
    lr_accuracy = accuracy_score(y_test, lr_preds)
    lr_model_path = os.path.join(run_dir, 'models', f'iris_log_reg_{input_version}.joblib')
    joblib.dump(lr_model, lr_model_path)

    # Train and evaluate Random Forest
    rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
    rf_model.fit(X_train, y_train)
    rf_preds = rf_model.predict(X_test)
    rf_accuracy = accuracy_score(y_test, rf_preds)
    rf_model_path = os.path.join(run_dir, 'models', f'iris_random_forest_{input_version}.joblib')
    joblib.dump(rf_model, rf_model_path)

    results = {
        'logistic_regression': {
            'hyperparameters': lr_model.get_params(),
            'accuracy': lr_accuracy
        },
        'random_forest': {
            'hyperparameters': rf_model.get_params(),
            'accuracy': rf_accuracy
        }
    }
    end_logging(results=results)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Train models on Iris data.')
    parser.add_argument('--input_version', type=str, required=True, choices=['a', 'b'],
                        help="Version of the feature data to use ('a' or 'b')")
    parser.add_argument('--run_dir', type=str, required=True, help='The directory for this run.')
    args = parser.parse_args()
    main(args.input_version, args.run_dir)
