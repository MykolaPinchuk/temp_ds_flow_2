import os
import re
import textwrap
from graphviz import Digraph

def parse_logs_for_lineage(log_dir):
    edges = set()
    log_files = [os.path.join(log_dir, f) for f in os.listdir(log_dir) if f.endswith('.log')]

    for log_file_path in log_files:
        log_filename = os.path.basename(log_file_path)
        
        # Extract notebook basename from log filename, e.g., '01_ingest_data' from '01_ingest_data_20250703_162918.log'
        match = re.match(r'(.+)_(\d{8}_\d{6})\.log$', log_filename)
        if not match:
            continue
        
        notebook_basename = match.group(1)
        notebook_name = f"{notebook_basename}.ipynb"

        with open(log_file_path, 'r') as f:
            content = f.read()

        # Find all files read
        files_read = re.findall(r'FILE_READ: (.*)', content)
        for filepath in files_read:
            edges.add((os.path.basename(filepath.strip()), notebook_name))

        # Find all files written
        files_written = re.findall(r'FILE_WRITTEN: (.*)', content)
        for filepath in files_written:
            edges.add((notebook_name, os.path.basename(filepath.strip())))

    print("Found the following connections:")
    for start, end in sorted(list(edges)):
        print(f"  {start} -> {end}")

    return edges

def visualize_lineage(edges, output_path):
    dot = Digraph(comment='Data Science Pipeline', graph_attr={'rankdir': 'LR'})
    nodes = set()
    for start, end in edges:
        nodes.add(start)
        nodes.add(end)

    for node in nodes:
        # Wrap node labels for better readability
        label = '\n'.join(textwrap.wrap(node, width=30))
        if '.ipynb' in node:
            dot.node(node, label=label, shape='box', style='rounded,filled', fillcolor='lightblue')
        else:
            dot.node(node, label=label, shape='ellipse', style='filled', fillcolor='lightgrey')

    for start, end in edges:
        dot.edge(start, end)

    try:
        dot.render(output_path, format='png', cleanup=True)
        print(f'Lineage graph saved to {output_path}.png')
    except Exception as e:
        print(f'Error rendering graph: {e}')
        print("Please ensure that Graphviz is installed and in your system's PATH.")

if __name__ == '__main__':
    # Correctly set paths relative to the script location in src/
    log_directory = os.path.join(os.path.dirname(__file__), '..', 'logs')
    reports_directory = os.path.join(os.path.dirname(__file__), '..', 'reports')
    os.makedirs(reports_directory, exist_ok=True)
    graph_output_path = os.path.join(reports_directory, 'pipeline_lineage')

    lineage_edges = parse_logs_for_lineage(log_directory)
    visualize_lineage(lineage_edges, graph_output_path)
