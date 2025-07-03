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

def _get_notebook_path():
    """Tries to get the path of the jupyter notebook."""
    try:
        import ipykernel.kernelapp
        from jupyter_core import paths
        import json
        import re

        kernel_id = re.search('kernel-(.*).json',
                            ipykernel.kernelapp.IPKernelApp.instance().connection_file).group(1)
        for p in paths.jupyter_runtime_dir():
            try:
                with open(os.path.join(p, 'nbserver-%s.json' % kernel_id)) as f:
                    return json.load(f)['notebook_dir']
            except:
                pass
    except Exception as e:
        return None
    return None

def _log_file_read(filepath, *args, **kwargs):
    if 'logger' in _log_info:
        if not _log_info.get('read_header_written'):
            _log_info['logger'].info('--- Files Read: ---')
            _log_info['read_header_written'] = True
        _log_info['logger'].info(f"- {filepath}")
    return _original_read_csv(filepath, *args, **kwargs)

def _log_file_write(df, filepath, *args, **kwargs):
    if 'logger' not in _log_info:
        return _original_to_csv(df, filepath, *args, **kwargs)

    # Generate timestamp for filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base, ext = os.path.splitext(filepath)
    new_filepath = f"{base}_{timestamp}{ext}"

    # Create metadata
    metadata = {
        'filename': os.path.basename(new_filepath),
        'timestamp': datetime.now().isoformat(),
        'notebook_path': _log_info.get('notebook_path'),
        'notebook_name': _log_info.get('notebook_name'),
    }

    # Determine metadata path
    data_dir = os.path.dirname(filepath)
    metadata_dir = os.path.join(data_dir, 'metadata')
    if not os.path.exists(metadata_dir):
        os.makedirs(metadata_dir)
    
    metadata_filename = f"{os.path.splitext(os.path.basename(new_filepath))[0]}.json"
    metadata_filepath = os.path.join(metadata_dir, metadata_filename)

    with open(metadata_filepath, 'w') as f:
        json.dump(metadata, f, indent=4)

    if not _log_info.get('write_header_written'):
        _log_info['logger'].info('--- Files Written: ---')
        _log_info['write_header_written'] = True
    _log_info['logger'].info(f"- {new_filepath}")

    return _original_to_csv(df, new_filepath, *args, **kwargs)

def _log_model_save(value, filename, *args, **kwargs):
    if 'logger' not in _log_info:
        return _original_joblib_dump(value, filename, *args, **kwargs)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base, ext = os.path.splitext(filename)
    new_filename = f"{base}_{timestamp}{ext}"

    metadata = {
        'filename': os.path.basename(new_filename),
        'timestamp': datetime.now().isoformat(),
        'notebook_path': _log_info.get('notebook_path'),
        'notebook_name': _log_info.get('notebook_name'),
    }

    model_dir = os.path.dirname(filename)
    metadata_dir = os.path.join(model_dir, 'metadata')
    if not os.path.exists(metadata_dir):
        os.makedirs(metadata_dir)
    
    metadata_filename = f"{os.path.splitext(os.path.basename(new_filename))[0]}.json"
    metadata_filepath = os.path.join(metadata_dir, metadata_filename)

    with open(metadata_filepath, 'w') as f:
        json.dump(metadata, f, indent=4)

    _log_info['logger'].info(f"MODEL_SAVED: {new_filename}")
    _log_info['logger'].info(f"METADATA_WRITTEN: {metadata_filepath}")

    return _original_joblib_dump(value, new_filename, *args, **kwargs)

def _log_plot_save(fname, *args, **kwargs):
    if 'logger' not in _log_info:
        return _original_plt_savefig(fname, *args, **kwargs)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base, ext = os.path.splitext(fname)
    new_fname = f"{base}_{timestamp}{ext}"

    metadata = {
        'filename': os.path.basename(new_fname),
        'timestamp': datetime.now().isoformat(),
        'notebook_path': _log_info.get('notebook_path'),
        'notebook_name': _log_info.get('notebook_name'),
    }

    report_dir = os.path.dirname(fname)
    metadata_dir = os.path.join(report_dir, 'metadata')
    if not os.path.exists(metadata_dir):
        os.makedirs(metadata_dir)
    
    metadata_filename = f"{os.path.splitext(os.path.basename(new_fname))[0]}.json"
    metadata_filepath = os.path.join(metadata_dir, metadata_filename)

    with open(metadata_filepath, 'w') as f:
        json.dump(metadata, f, indent=4)

    _log_info['logger'].info(f"PLOT_SAVED: {new_fname}")
    _log_info['logger'].info(f"METADATA_WRITTEN: {metadata_filepath}")

    return _original_plt_savefig(new_fname, *args, **kwargs)

def start_logging(notebook_name, notebook_description):
    """Starts logging for a notebook run."""
    global _log_info
    _log_info = {
        'start_time': time.time(),
        'notebook_name': notebook_name,
        'notebook_path': os.path.join(_get_notebook_path() or '', notebook_name)
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
        logger.info(f"RESULTS: {json.dumps(results, indent=4)}")

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
