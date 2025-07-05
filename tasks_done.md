# Tasks Completed

- **Refactor 1: Convert Notebooks to Scripts:**
  - Converted all Jupyter notebooks from the `notebooks/` directory into Python scripts located in the new `scripts/` directory.
  - Each script now uses `argparse` to handle parameters (like data versioning), making them executable from the command line.
  - Removed the now-obsolete `notebooks/` directory.
  - Updated `DOCUMENTATION.md` to reflect the new script-based workflow, including updated project structure and usage examples.

- **Fix `06_evaluate_alternative_models.ipynb`:** The notebook was failing due to a `FileNotFoundError` caused by hardcoded model filenames. The notebook has been updated to dynamically find the latest saved models for both logistic regression and random forest, ensuring it always uses the most recent versions.
- **Simulate New Data (Example 2):** Refactored the data ingestion step to support experimentation. The original ingestion logic was preserved in `01a_ingest_data.ipynb`, and a new experiment simulating a 50% increase in data was created in `01b_ingest_data.ipynb`. The downstream pipeline was updated to process the data from experiment 'B', and the full pipeline was executed successfully. The lineage graph was updated to show both experimental branches.
