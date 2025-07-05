# Detailed Documentation

This document provides a detailed explanation of the Data Science Workflow POC project.

## Project Structure

The project uses a simple, hierarchical directory structure:

- `data/`: Contains all data files.
  - `raw/`: For raw, immutable data.
  - `processed/`: For cleaned, transformed, or feature-engineered data.
  - `*/metadata/`: Each data directory has a `metadata` subdirectory to store JSON files with information about each data artifact.
- `scripts/`: Contains Python scripts for the data science workflow, organized by workflow steps (e.g., `01_ingest_data.py`).
- `src/`: Contains Python source code.
  - `ds_logger.py`: The core logging module.
  - `visualize_lineage.py`: A script to generate the data lineage graph.
- `logs/`: Contains timestamped log files for each script run.
- `models/`: For trained machine learning models.
- `reports/`: For generated reports, plots, and the data lineage graph.

## Automated Logging and Lineage

The core of this workflow is the `ds_logger` module.

### How it Works

The module uses a technique called "monkey-patching" at runtime. When you call `ds_logger.start_logging()`, it replaces standard functions from libraries like `pandas`, `joblib`, and `matplotlib` with custom wrapper functions. These wrappers perform the original function's action (e.g., saving a CSV) and also log the action and create a corresponding metadata file. `ds_logger.end_logging()` restores the original functions.

### Usage

The workflow is executed by running the Python scripts in the `scripts/` directory in sequence from the project root. The logging is automatically handled within each script.

Here is an example of how to run the pipeline for experiment 'a':

```bash
# 1. Ingest the original data
python scripts/01a_ingest_data.py

# 2. Preprocess the data
python scripts/02_preprocess_data.py --input_version a

# 3. Perform Exploratory Data Analysis
python scripts/03_eda.py --input_version a

# 4. Engineer features
python scripts/04_feature_engineering.py --input_version a

# 5. Train models
python scripts/05_train_alternative_model.py --input_version a

# 6. Evaluate models
python scripts/06_evaluate_alternative_models.py --input_version a
```

To run the pipeline for experiment 'b' (with simulated new data), you would run:
```bash
# 1. Ingest the simulated new data
python scripts/01b_ingest_data.py

# 2. Preprocess the data
python scripts/02_preprocess_data.py --input_version b

# 3. Perform Exploratory Data Analysis
python scripts/03_eda.py --input_version b

# 4. Engineer features
python scripts/04_feature_engineering.py --input_version b

# 5. Train models
python scripts/05_train_alternative_model.py --input_version b

# 6. Evaluate models
python scripts/06_evaluate_alternative_models.py --input_version b
```

### Logged Information

For each script run, a log file is created in the `logs/` directory. It contains:
- Script name and description.
- Files read and written.
- Models and plots saved.
- Any custom results you provide.
- Total run duration.

### Metadata

For every file written by a logged script (datasets, models, plots), a corresponding JSON file is created in the `metadata` subdirectory of the artifact's location. This JSON contains:
- The filename of the artifact.
- A precise timestamp of its creation.
- The name of the script that created it.

## Data Lineage Visualization

To see how all your scripts and data files are connected, you can generate a lineage graph.

Run the following command from the project root directory:

```bash
python src/visualize_lineage.py
```

This will parse all the log files in the `logs/` directory and generate a `pipeline_lineage.png` image in the `reports/` directory, showing the dependencies between your scripts and data.