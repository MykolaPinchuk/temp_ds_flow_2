import os
import re
import textwrap
from graphviz import Digraph

def parse_logs_for_lineage(log_dir):
    """Parses log files to extract file dependencies for lineage."""
    edges = set()
    log_files = [os.path.join(log_dir, f) for f in os.listdir(log_dir) if f.endswith('.log')]

    for log_file_path in log_files:
        with open(log_file_path, 'r') as f:
            content = f.read()

        # Find the source script name from the log content
        script_match = re.search(r'Script: (.*)', content)
        if not script_match:
            continue
        
        script_name = script_match.group(1).strip()
        # We only want the basename for the graph
        script_name = os.path.basename(script_name)

        # Find all files read
        files_read = re.findall(r'FILE_READ: (.*)', content)
        for filepath in files_read:
            # Use basename for data files as well
            edges.add((os.path.basename(filepath.strip()), script_name))

        # Find all files written
        files_written = re.findall(r'FILE_WRITTEN: (.*)', content)
        for filepath in files_written:
            edges.add((script_name, os.path.basename(filepath.strip())))

    print("Found the following connections:")
    for start, end in sorted(list(edges)):
        print(f"  {start} -> {end}")

    return edges

def visualize_lineage(edges, output_path):
    """Generates a lineage graph from the given edges."""
    dot = Digraph(comment='Data Science Pipeline', graph_attr={'rankdir': 'LR'})
    nodes = set()
    for start, end in edges:
        nodes.add(start)
        nodes.add(end)

    for node in sorted(list(nodes)):
        # Wrap node labels for better readability
        label = '\n'.join(textwrap.wrap(node.replace('_', ' '), width=30))
        if '.py' in node:
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
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    log_directory = os.path.join(project_root, 'logs')
    reports_directory = os.path.join(project_root, 'reports')
    os.makedirs(reports_directory, exist_ok=True)
    graph_output_path = os.path.join(reports_directory, 'pipeline_lineage')

    if os.path.exists(log_directory):
        lineage_edges = parse_logs_for_lineage(log_directory)
        visualize_lineage(lineage_edges, graph_output_path)
    else:
        print(f"Log directory not found at {log_directory}")
