import os
import re
from graphviz import Digraph

def parse_logs_for_lineage(log_dir):
    edges = set()
    log_files = [os.path.join(log_dir, f) for f in os.listdir(log_dir) if f.endswith('.log')]

    for log_file in log_files:
        with open(log_file, 'r') as f:
            lines = f.readlines()

        notebook_name = None
        in_read_block = False
        in_written_block = False

        for line in lines:
            # Strip the logger's timestamp and prefix
            clean_line = re.sub(r'^.*?- ', '', line).strip()

            # First, find the notebook name for this log file
            if not notebook_name:
                match = re.match(r'Notebook: (.*)', clean_line)
                if match:
                    notebook_name = os.path.basename(match.group(1).strip())
                continue # Continue to the next line to start processing

            # State transitions to enter a block
            if clean_line == '--- Files Read: ---':
                in_read_block = True
                in_written_block = False
                continue
            elif clean_line == '--- Files Written: ---':
                in_written_block = True
                in_read_block = False
                continue

            # Process lines if we are inside a block
            if in_read_block or in_written_block:
                # If the line starts with '-', it's a file path
                if clean_line.startswith('- '):
                    filepath = os.path.basename(clean_line.lstrip('- ').strip())
                    if filepath:
                        if in_read_block:
                            edges.add((filepath, notebook_name))
                        elif in_written_block:
                            edges.add((notebook_name, filepath))
                # If it's any other line, we've exited the block
                else:
                    in_read_block = False
                    in_written_block = False

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
