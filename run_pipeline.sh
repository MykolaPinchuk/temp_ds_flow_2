#!/bin/bash

# This script runs the full data science pipeline for a specified version.
# Usage: ./run_pipeline.sh [a|b]

# Exit immediately if a command exits with a non-zero status.
set -e

# Check if a version is provided
if [ -z "$1" ]; then
    echo "Error: No version specified. Usage: ./run_pipeline.sh [a|b]"
    exit 1
fi

VERSION=$1

# Validate the version
if [ "$VERSION" != "a" ] && [ "$VERSION" != "b" ]; then
    echo "Error: Invalid version. Please use 'a' or 'b'."
    exit 1
fi

echo "Running pipeline for version: $VERSION"

# Step 1: Ingest Data
echo "Step 1: Ingesting data..."
python scripts/01_ingest_data.py --dataset_version $VERSION

# Step 2: Preprocess Data
echo "Step 2: Preprocessing data..."
python scripts/02_preprocess_data.py --input_version $VERSION

# Step 3: Exploratory Data Analysis
echo "Step 3: Performing EDA..."
python scripts/03_eda.py --input_version $VERSION

# Step 4: Feature Engineering
echo "Step 4: Engineering features..."
python scripts/04_feature_engineering.py --input_version $VERSION

# Step 5: Train Models
echo "Step 5: Training models..."
python scripts/05_train_alternative_model.py --input_version $VERSION

# Step 6: Evaluate Models
echo "Step 6: Evaluating models..."
python scripts/06_evaluate_alternative_models.py --input_version $VERSION

# Step 7: Visualize Lineage
echo "Step 7: Visualizing lineage..."
python src/visualize_lineage.py

echo "Pipeline for version '$VERSION' completed successfully."
