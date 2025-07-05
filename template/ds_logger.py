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

# Original functions that will be patched
_original_to_csv = pd.DataFrame.to_csv
_original_read_csv = pd.read_csv


def _log_file_read(filepath, *args, **kwargs):
    """Wrapper for file read operations to log the event."""
    if 'logger' in _log_info:
        _log_info['logger'].info(f"FILE_READ: {filepath}")
    return _original_read_csv(filepath, *args, **kwargs)

def _create_metadata(original_path, log_info, model_object=None):
    """Generates a metadata file for the given path."""
    now = datetime.now()
    iso_timestamp = now.isoformat()

    metadata = {
        'filename': os.path.basename(original_path),
        'timestamp': iso_timestamp,
        'script_source': os.path.join(log_info.get('script_path', ''), log_info.get('script_name', '')),
    }

    if model_object and hasattr(model_object, 'get_params'):
        try:
            params = model_object.get_params()
            # Attempt to make parameters JSON serializable
            serializable_params = {k: str(v) for k, v in params.items()}
            metadata['hyperparameters'] = serializable_params
        except Exception as e:
            if 'logger' in _log_info:
                _log_info['logger'].warning(f"Could not serialize hyperparameters for {metadata['filename']}: {e}")

    # Determine metadata path relative to the project root
    data_dir = os.path.dirname(original_path)
    metadata_dir = os.path.join(data_dir, 'metadata')
    os.makedirs(metadata_dir, exist_ok=True)
    
    metadata_filename = f"{os.path.splitext(os.path.basename(original_path))[0]}.json"
    metadata_filepath = os.path.join(metadata_dir, metadata_filename)

    with open(metadata_filepath, 'w') as f:
        json.dump(metadata, f, indent=4)
    
    return metadata_filepath

def _log_file_write(df, filepath, *args, **kwargs):
    """Wrapper for pd.DataFrame.to_csv to log the event and create metadata."""
    if 'logger' not in _log_info:
        return _original_to_csv(df, filepath, *args, **kwargs)

    _create_metadata(filepath, _log_info)
    _log_info['logger'].info(f"FILE_WRITTEN: {filepath}")
    return _original_to_csv(df, filepath, *args, **kwargs)

def _log_model_save(value, filename, *args, **kwargs):
    """Wrapper for joblib.dump to log the event and create metadata."""
    if 'logger' not in _log_info:
        return _original_joblib_dump(value, filename, *args, **kwargs)

    metadata_filepath = _create_metadata(filename, _log_info, model_object=value)
    _log_info['logger'].info(f"MODEL_SAVED: {filename}")
    _log_info['logger'].info(f"METADATA_WRITTEN: {metadata_filepath}")
    return _original_joblib_dump(value, filename, *args, **kwargs)

def _log_plot_save(fname, *args, **kwargs):
    """Wrapper for plt.savefig to log the event and create metadata."""
    if 'logger' not in _log_info:
        return _original_plt_savefig(fname, *args, **kwargs)

    metadata_filepath = _create_metadata(fname, _log_info)
    _log_info['logger'].info(f"PLOT_SAVED: {fname}")
    _log_info['logger'].info(f"METADATA_WRITTEN: {metadata_filepath}")
    return _original_plt_savefig(fname, *args, **kwargs)

def start_logging(script_name, script_description, run_dir):
    """Starts logging for a script run."""
    global _log_info
    _log_info = {
        'start_time': time.time(),
        'script_name': script_name,
        'script_path': 'scripts',
        'run_dir': run_dir
    }

    # Setup logger
    log_filename = f"{os.path.splitext(script_name)[0]}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    log_filepath = os.path.join(run_dir, 'logs', log_filename)


    
    logger = logging.getLogger(script_name)
    logger.setLevel(logging.INFO)
    
    # Prevent duplicate handlers if logger is reused (e.g., in interactive sessions)
    if not logger.handlers:
        handler = logging.FileHandler(log_filepath)
        formatter = logging.Formatter('%(asctime)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    _log_info['logger'] = logger

    logger.info(f"Script: {script_name}")
    logger.info(f"Description: {script_description}")

    # Patch libraries
    pd.read_csv = _log_file_read
    pd.DataFrame.to_csv = _log_file_write
    if joblib:
        joblib.dump = _log_model_save
    if plt:
        plt.savefig = _log_plot_save

def end_logging(results=None):
    """Ends logging for a script run."""
    global _log_info
    if 'logger' not in _log_info:
        print("Logging was not started.")
        return

    logger = _log_info['logger']
    end_time = time.time()
    duration = end_time - _log_info['start_time']

    logger.info(f"END_LOGGING: Script '{_log_info['script_name']}'")
    logger.info(f"RUN_DURATION: {duration:.2f} seconds")

    if results:
        logger.info(f"SCRIPT_RESULTS:\n{json.dumps(results, indent=4)}")

    # Add a final separator to make parsing easier
    logger.info('---')

    # Unpatch libraries
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
