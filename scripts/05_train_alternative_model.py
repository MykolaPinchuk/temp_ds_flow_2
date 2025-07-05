import sys
import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score
import joblib
import argparse

# Add src to path to be able to import ds_logger
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from ds_logger import start_logging, end_logging

def main(input_version, run_dir):
    """Main function to train and evaluate models with hyperparameter tuning."""
    script_name = f'05_train_hyperparameter_models_{input_version}.py'
    script_description = f"Trains multiple RF and XGBoost models with different hyperparameters on data version {input_version}."
    start_logging(script_name=script_name, script_description=script_description, run_dir=run_dir)

    # Load feature-engineered data
    features_path = os.path.join(run_dir, 'data', 'processed', f'iris_features_{input_version}.csv')
    df = pd.read_csv(features_path)

    # Prepare data for modeling
    X = df.drop('target', axis=1)
    y = df['target']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=24)

    print(f"--- Data Splitting Metrics ---")
    print(f"Input DataFrame shape: {df.shape}")
    print(f"X_train shape: {X_train.shape}")
    print(f"X_test shape: {X_test.shape}")
    print(f"y_train shape: {y_train.shape}")
    print(f"y_test shape: {y_test.shape}")
    print(f"------------------------------")

    # Save the test set for consistent evaluation
    X_test_path = os.path.join(run_dir, 'data', 'processed', f'X_test_{input_version}.csv')
    y_test_path = os.path.join(run_dir, 'data', 'processed', f'y_test_{input_version}.csv')
    X_test.to_csv(X_test_path, index=False)
    y_test.to_csv(y_test_path, index=False)

    # Define models and hyperparameters
    # Define models and a wider range of hyperparameters to test sensitivity
    models_to_train = {
        'rf_simple': RandomForestClassifier(n_estimators=10, max_depth=2, random_state=42),
        'rf_medium': RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42),
        'rf_complex': RandomForestClassifier(n_estimators=300, max_depth=None, min_samples_leaf=1, random_state=42),
        'xgb_simple': XGBClassifier(n_estimators=50, max_depth=2, learning_rate=0.5, use_label_encoder=False, eval_metric='mlogloss', random_state=42),
        'xgb_complex': XGBClassifier(n_estimators=200, max_depth=6, learning_rate=0.05, use_label_encoder=False, eval_metric='mlogloss', random_state=42),
    }

    results = {
        'data_shapes': {
            'input_df': df.shape,
            'X_train': X_train.shape,
            'X_test': X_test.shape,
            'y_train': y_train.shape,
            'y_test': y_test.shape,
        },
        'model_performance': {}
    }

    print(f"--- Model Training and Performance ---")
    for model_name, model in models_to_train.items():
        print(f"Training {model_name}...")
        model.fit(X_train, y_train)
        
        preds = model.predict(X_test)
        accuracy = accuracy_score(y_test, preds)
        
        model_path = os.path.join(run_dir, 'models', f'iris_{model_name}_{input_version}.joblib')
        joblib.dump(model, model_path)
        
        results['model_performance'][model_name] = {
            'accuracy': accuracy,
            'hyperparameters': {k: str(v) for k, v in model.get_params().items()}
        }
        print(f"{model_name} Accuracy: {accuracy:.4f}")
    print(f"--------------------------------------")

    end_logging(results=results)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Train models with different hyperparameters.')
    parser.add_argument('--input_version', type=str, required=True, choices=['a', 'b', 'c', 'd', 'e'],
                        help="Version of the feature data to use.")
    parser.add_argument('--run_dir', type=str, required=True, help='The directory for this run.')
    args = parser.parse_args()
    main(args.input_version, args.run_dir)
