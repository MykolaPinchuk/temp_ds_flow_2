# Data Science Project Template with Lineage Tracking

Welcome to your new Data Science project! This template is designed to help you build a robust and reproducible machine learning pipeline. The core principle is **lineage tracking**: every piece of data, every model, and every report can be traced back to the exact code and configuration that produced it.

## Philosophy

In complex data science projects, it's easy to lose track of which dataset was used to train which model, or what parameters were used for a specific experiment. This template solves that problem by enforcing a structured workflow where every execution of the pipeline is isolated in its own timestamped directory, containing all its inputs, outputs, and logs.

## Getting Started

To begin your project, you are expected to start by reading content of this directory. They serve as templates. Do not modify them here. Build in the repo root while keeping this template dir as a reference.

Scripts are copypasted from a POC project used to come up with such strcuture/workflow. Some of them may fail to run due to missing data. The objective of this template directory is to serve as a reference for a source code only.

As result of running these scripts, you may populate directories in a root of this repo with files from template pipeline. You can use them at the very beginning to understand how things work. But keep in mind that they are temporary files and should be removed to avoid confusion with the objective of the main project.

1.  **Install Dependencies**: First, ensure you have all the necessary Python packages installed. From this directory, run:

    ```bash
    pip install -r requirements.txt
    ```

2.  **Run the Pipeline**: To execute the entire data pipeline, use the provided shell script:

    ```bash
    ./run_pipeline.sh
    ```

    This script is the primary entry point for your experiments. It automatically handles the creation of a new, timestamped run directory (e.g., `../runs/a_20250705_105739/`) and then executes the Python scripts (`01_*.py`, `02_*.py`, etc.) in the correct sequence.

3.  **Customize the Scripts**: The Python scripts (`01_...` to `06_...`) are templates. You will need to modify them to implement the logic for your specific project (e.g., loading your data, applying your preprocessing steps, training your models).

    **Crucially, you must use the `ds_logger` provided in `ds_logger.py` for all logging and for saving any artifacts (datasets, models, plots).** This is the key to the lineage tracking system.

## Directory and File Breakdown

Here is a description of the files included in this template:

-   **`run_pipeline.sh`**: The main script to execute your entire workflow. It creates the necessary directory structure for a new run and then calls your Python scripts in order.

-   **`requirements.txt`**: A list of Python packages required for this project.

-   **`ds_logger.py`**: A custom logging utility that is the heart of the lineage tracking system. It provides functions to:
    -   Log messages to a file specific to the current run.
    -   Save dataframes, models, and plots along with a corresponding `.json` metadata file. This metadata file contains crucial lineage information, such as the script that generated the artifact and the source data it was derived from.

-   **`01_ingest_data.py` ... `06_evaluate_alternative_models.py`**: A series of numbered Python scripts that form the steps of your data science pipeline. You should edit these files to implement your project's logic.

-   **`visualize_lineage.py`**: A utility script to help you visualize the lineage of your project's artifacts. It scans the `runs` directory and generates a graph that shows the relationships between your data, code, and models.

### How to Visualize Lineage

After you have run the pipeline at least once, you can generate a lineage graph by running:

```bash
python visualize_lineage.py
```

This will create an `lineage.png` file in the current directory, showing how your artifacts are connected.

## The `runs` Directory

This template will create a `../runs/` directory (relative to this `template` directory) when you execute `run_pipeline.sh`. This directory is not included in the template but is the primary output location of your work. Its structure is as follows:

-   **`runs/`**
    -   **`<run_id>` (e.g., `a_20250705_105739`)**: A unique directory for each execution of the pipeline.
        -   **`data/`**: All data generated during the run.
            -   `raw/`: Raw data.
            -   `processed/`: Processed data.
            -   `metadata/`: JSON files with data lineage.
        -   **`logs/`**: Log files for each pipeline step.
        -   **`models/`**: Trained models.
            -   `metadata/`: JSON files with model lineage.
        -   **`reports/`**: Output reports and visualizations.
            -   `metadata/`: JSON files with report lineage.

By adhering to this structure, you ensure your project is organized, reproducible, and transparent.
