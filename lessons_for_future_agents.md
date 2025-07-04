# Lessons for Future Agents

- **Editing Jupyter Notebooks:** Direct editing of `.ipynb` files is not supported. A reliable workaround is to convert the target notebook to a Python script (`jupyter nbconvert --to script ...`), edit the script file, and then execute the script directly (`python ...`). Converting a script back to a notebook is difficult and error-prone; executing the modified script is the most reliable method.

- **`ds_logger` Behavior:** The `ds_logger` module automatically adds a timestamp to the end of any filename being written (e.g., in `pd.to_csv`). Do not hardcode filenames when reading data that has been written by a logged process. Instead, dynamically find the latest file based on a known prefix (e.g., `iris_raw_b`) and the file's creation time.
