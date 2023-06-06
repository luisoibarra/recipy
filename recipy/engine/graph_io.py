import networkx as nx
from pathlib import Path

def import_graph(path: Path) -> nx.Graph:
    if path.name.endswith(".graphml"):
        return nx.read_graphml(path)
    raise ValueError(f"Path must end with .graphml")

def export_graph(graph: nx.Graph, path: Path):
    if path.name.endswith(".graphml"):
        return nx.write_graphml(graph, path)
    raise ValueError(f"Path must end with .graphml")
