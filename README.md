# Data Science Workflow POC

This repository is a proof-of-concept for a structured data science workflow. It aims to address common pain points like messy codebases and lack of data lineage by providing a simple, convention-based framework for organizing and tracking data science projects.

## Key Features

- **Standardized Project Structure**: A simple layout with `data`, `notebooks`, `src`, `logs`, and `reports` directories.
- **Automated Logging**: Automatically track files read/written, models saved, and plots created within Jupyter notebooks.
- **Data Lineage**: Automatically generate metadata for all artifacts and visualize the entire pipeline as a dependency graph.
- **Minimal Code Changes**: Designed to integrate into existing notebook-based workflows with minimal modifications.

## Human notes
LLM agents cannot handle jupyter notebooks well. Thus, this codebase minimizes notebook usage.

Run the whole pipeline with `bash run_pipeline.sh b`.

For detailed usage and explanation of the components, please see `DOCUMENTATION.md`.