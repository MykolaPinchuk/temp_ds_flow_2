# Tasks Completed

- **Fix `06_evaluate_alternative_models.ipynb`:** The notebook was failing due to a `FileNotFoundError` caused by hardcoded model filenames. The notebook has been updated to dynamically find the latest saved models for both logistic regression and random forest, ensuring it always uses the most recent versions.
- **Simulate New Data (Example 2):** Refactored the data ingestion step to support experimentation. The original ingestion logic was preserved in `01a_ingest_data.ipynb`, and a new experiment simulating a 50% increase in data was created in `01b_ingest_data.ipynb`. The downstream pipeline was updated to process the data from experiment 'B', and the full pipeline was executed successfully. The lineage graph was updated to show both experimental branches.
