#!/bin/bash

# This script runs the full data science pipeline for a specified version.
# It creates a self-contained directory for each run to store all outputs.
# Usage: ./run_pipeline.sh [a|b|c|d|e]

# Exit immediately if a command exits with a non-zero status.
set -e

# Check if a version is provided
if [ -z "$1" ]; then
    echo "Error: No version specified. Usage: ./run_pipeline.sh [a|b|c|d|e]"
    exit 1
fi

VERSION=$1

# Validate the version
if [ "$VERSION" != "a" ] && [ "$VERSION" != "b" ] && [ "$VERSION" != "c" ] && [ "$VERSION" != "d" ] && [ "$VERSION" != "e" ]; then
    echo "Error: Invalid version. Please use 'a', 'b', 'c', 'd', or 'e'."
    exit 1
fi

# Create a unique directory for this run
RUN_ID=$(date +%Y%m%d_%H%M%S)
RUN_DIR="runs/${VERSION}_${RUN_ID}"
echo "Creating new run directory: $RUN_DIR"
mkdir -p "$RUN_DIR/data/raw"
mkdir -p "$RUN_DIR/data/processed"
mkdir -p "$RUN_DIR/models"
mkdir -p "$RUN_DIR/reports"
mkdir -p "$RUN_DIR/logs"

echo "Running pipeline for version: $VERSION in directory: $RUN_DIR"

# Step 1: Ingest Data
echo "Step 1: Ingesting data..."
python scripts/01_ingest_data.py --dataset_version $VERSION --run_dir $RUN_DIR

# Step 2: Preprocess Data
echo "Step 2: Preprocessing data..."
python scripts/02_preprocess_data.py --input_version $VERSION --run_dir $RUN_DIR

# Step 3: Exploratory Data Analysis
echo "Step 3: Performing EDA..."
python scripts/03_eda.py --input_version $VERSION --run_dir $RUN_DIR

# Step 4: Feature Engineering
echo "Step 4: Engineering features..."
python scripts/04_feature_engineering.py --input_version $VERSION --run_dir $RUN_DIR

# Step 5: Train Models
echo "Step 5: Training models..."
python scripts/05_train_alternative_model.py --input_version $VERSION --run_dir $RUN_DIR

# Step 6: Evaluate Models
echo "Step 6: Evaluating models..."
python scripts/06_evaluate_alternative_models.py --input_version $VERSION --run_dir $RUN_DIR

# Step 7: Visualize Lineage (after the pipeline run)
echo "Step 7: Visualizing lineage for all runs..."
python src/visualize_lineage.py

echo "Pipeline for version '$VERSION' completed successfully in '$RUN_DIR'."
