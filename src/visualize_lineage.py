import os
import re
from graphviz import Digraph

def parse_logs_for_lineage(log_dir):
    edges = set()
    log_files = [os.path.join(log_dir, f) for f in os.listdir(log_dir) if f.endswith('.log')]

    for log_file in log_files:
        with open(log_file, 'r') as f:
            content = f.read()

        # Find the notebook name for this log file
        notebook_match = re.search(r'Notebook: (.*)', content)
        if not notebook_match:
            continue
        notebook_name = os.path.basename(notebook_match.group(1).strip())

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
        if '.ipynb' in node:
            dot.node(node, shape='box', style='rounded,filled', fillcolor='lightblue')
        else:
            dot.node(node, shape='ellipse', style='filled', fillcolor='lightgrey')

    for start, end in edges:
        dot.edge(start, end)

    try:
        dot.render(output_path, format='png', cleanup=True)
        print(f'Lineage graph saved to {output_path}.png')
    except Exception as e:
        print(f'Error rendering graph: {e}')
        print('Please ensure that Graphviz is installed and in your system\'s PATH.')

if __name__ == '__main__':
    # Correctly set paths relative to the script location in src/
    log_directory = os.path.join(os.path.dirname(__file__), '..', 'logs')
    reports_directory = os.path.join(os.path.dirname(__file__), '..', 'reports')
    os.makedirs(reports_directory, exist_ok=True)
    graph_output_path = os.path.join(reports_directory, 'pipeline_lineage')

    lineage_edges = parse_logs_for_lineage(log_directory)
    visualize_lineage(lineage_edges, graph_output_path)
