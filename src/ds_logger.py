import logging
import time
import json
import os
from datetime import datetime
import pandas as pd

try:
    import joblib
    _original_joblib_dump = joblib.dump
except ImportError:
    joblib = None
    _original_joblib_dump = None

try:
    import matplotlib.pyplot as plt
    _original_plt_savefig = plt.savefig
except ImportError:
    plt = None
    _original_plt_savefig = None

# Get the project root directory (which is the parent of 'src')
_project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Global state to hold logging info
_log_info = {}

# Original pandas functions
_original_to_csv = pd.DataFrame.to_csv
_original_read_csv = pd.read_csv



def _log_file_read(filepath, *args, **kwargs):
    if 'logger' in _log_info:
        _log_info['logger'].info(f"FILE_READ: {filepath}")
    return _original_read_csv(filepath, *args, **kwargs)

def _create_metadata(original_path, log_info):
    """Generates a timestamped path and creates a metadata file."""
    now = datetime.now()
    timestamp_str = now.strftime("%Y%m%d_%H%M")
    iso_timestamp = now.isoformat()

    base, ext = os.path.splitext(original_path)
    new_path = f"{base}_{timestamp_str}{ext}"

    metadata = {
        'filename': os.path.basename(new_path),
        'timestamp': iso_timestamp,
        'notebook_source': os.path.join(log_info.get('notebook_path', ''), log_info.get('notebook_name', '')),
    }

    # Determine metadata path
    data_dir = os.path.dirname(original_path)
    metadata_dir = os.path.join(data_dir, 'metadata')
    os.makedirs(metadata_dir, exist_ok=True)
    
    metadata_filename = f"{os.path.splitext(os.path.basename(new_path))[0]}.json"
    metadata_filepath = os.path.join(metadata_dir, metadata_filename)

    with open(metadata_filepath, 'w') as f:
        json.dump(metadata, f, indent=4)
    
    return new_path, metadata_filepath

def _log_file_write(df, filepath, *args, **kwargs):
    if 'logger' not in _log_info:
        return _original_to_csv(df, filepath, *args, **kwargs)

    new_filepath, _ = _create_metadata(filepath, _log_info)

    _log_info['logger'].info(f"FILE_WRITTEN: {new_filepath}")

    return _original_to_csv(df, new_filepath, *args, **kwargs)

def _log_model_save(value, filename, *args, **kwargs):
    if 'logger' not in _log_info:
        return _original_joblib_dump(value, filename, *args, **kwargs)

    new_filename, metadata_filepath = _create_metadata(filename, _log_info)

    _log_info['logger'].info(f"MODEL_SAVED: {new_filename}")
    _log_info['logger'].info(f"METADATA_WRITTEN: {metadata_filepath}")

    return _original_joblib_dump(value, new_filename, *args, **kwargs)

def _log_plot_save(fname, *args, **kwargs):
    if 'logger' not in _log_info:
        return _original_plt_savefig(fname, *args, **kwargs)

    new_fname, metadata_filepath = _create_metadata(fname, _log_info)

    _log_info['logger'].info(f"PLOT_SAVED: {new_fname}")
    _log_info['logger'].info(f"METADATA_WRITTEN: {metadata_filepath}")

    return _original_plt_savefig(new_fname, *args, **kwargs)

def start_logging(notebook_name, notebook_description):
    """Starts logging for a notebook run."""
    global _log_info
    _log_info = {
        'start_time': time.time(),
        'notebook_name': notebook_name,
        'notebook_path': 'notebooks'
    }

    # Setup logger
    log_filename = f"{os.path.splitext(notebook_name)[0]}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    log_filepath = os.path.join(_project_root, 'logs', log_filename)
    
    logger = logging.getLogger(notebook_name)
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler(log_filepath)
    formatter = logging.Formatter('%(asctime)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    _log_info['logger'] = logger

    logger.info(f"Notebook: {notebook_name}")
    logger.info(f"Description: {notebook_description}")

    # Patch pandas
    pd.read_csv = _log_file_read
    pd.DataFrame.to_csv = _log_file_write
    if joblib:
        joblib.dump = _log_model_save
    if plt:
        plt.savefig = _log_plot_save

def end_logging(results=None):
    """Ends logging for a notebook run."""
    global _log_info
    if 'logger' not in _log_info:
        print("Logging was not started.")
        return

    logger = _log_info['logger']
    end_time = time.time()
    duration = end_time - _log_info['start_time']

    logger.info(f"END_LOGGING: Notebook '{_log_info['notebook_name']}'")
    logger.info(f"RUN_DURATION: {duration:.2f} seconds")

    if results:
        logger.info(f"NOTEBOOK_RESULTS:\n{json.dumps(results, indent=4)}")

    # Add a final separator to make parsing easier
    logger.info('---')

    # Unpatch pandas and other libraries
    pd.read_csv = _original_read_csv
    pd.DataFrame.to_csv = _original_to_csv
    if joblib:
        joblib.dump = _original_joblib_dump
    if plt:
        plt.savefig = _original_plt_savefig

    # Clean up logger
    for handler in logger.handlers[:]:
        handler.close()
        logger.removeHandler(handler)
    
    _log_info = {}
