# Detailed Documentation

This document provides a detailed explanation of the Data Science Workflow POC project.

## Project Structure

The project uses a simple, hierarchical directory structure:

- `data/`: Contains all data files.
  - `raw/`: For raw, immutable data.
  - `processed/`: For cleaned, transformed, or feature-engineered data.
  - `*/metadata/`: Each data directory has a `metadata` subdirectory to store JSON files with information about each data artifact.
- `notebooks/`: Contains all Jupyter notebooks, organized by workflow steps (e.g., `01_ingest_data.ipynb`).
- `src/`: Contains Python source code.
  - `ds_logger.py`: The core logging module.
  - `visualize_lineage.py`: A script to generate the data lineage graph.
- `logs/`: Contains timestamped log files for each notebook run.
- `models/`: For trained machine learning models.
- `reports/`: For generated reports, plots, and the data lineage graph.

## Automated Logging and Lineage

The core of this workflow is the `ds_logger` module.

### How it Works

The module uses a technique called "monkey-patching" at runtime. When you call `ds_logger.start_logging()`, it replaces standard functions from libraries like `pandas`, `joblib`, and `matplotlib` with custom wrapper functions. These wrappers perform the original function's action (e.g., saving a CSV) and also log the action and create a corresponding metadata file. `ds_logger.end_logging()` restores the original functions.

### Usage

To enable logging in a notebook, you only need to add two lines of code:

1.  At the beginning of the notebook:
    ```python
    import sys
    sys.path.append('../src')
    import ds_logger

    notebook_name = '01_ingest_data.ipynb' # Should be the actual name of the notebook
    notebook_description = 'This notebook ingests the raw data.'
    ds_logger.start_logging(notebook_name, notebook_description)
    ```

2.  At the end of the notebook:
    ```python
    # You can pass a dictionary of results to be logged
    results = {'accuracy': 0.95, 'hyperparameters': {'C': 1.0, 'kernel': 'rbf'}}
    ds_logger.end_logging(results=results)
    ```

### Logged Information

For each notebook run, a log file is created in the `logs/` directory. It contains:
- Notebook name and description.
- Files read and written.
- Models and plots saved.
- Any custom results you provide.
- Total run duration.

### Metadata

For every file written by a logged notebook (datasets, models, plots), a corresponding JSON file is created in the `metadata` subdirectory of the artifact's location. This JSON contains:
- The filename of the artifact.
- A precise timestamp of its creation.
- The name of the notebook that created it.

## Data Lineage Visualization

To see how all your notebooks and data files are connected, you can generate a lineage graph.

Run the following command from the project root directory:

```bash
python src/visualize_lineage.py
```

This will parse all the log files in the `logs/` directory and generate a `pipeline_lineage.png` image in the `reports/` directory, showing the dependencies between your notebooks and data.
