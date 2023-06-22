from typing import List
from .filters import equal_filter
import networkx as nx


def return_most_similar_recipes(recipe_node_query: str, recipe_graph: nx.Graph, max_amount: int = 100) -> List[str]:
    """
    Returns the most similar recipes matching `recipe_node_query` by the node's weight.
    """
    to_rank = []
    for recipe in recipe_graph.nodes:
        if equal_filter(recipe_node_query, recipe):
            neighbors = recipe_graph.neighbors(recipe)
            for neighbor in neighbors:
                to_rank.append((recipe_graph[recipe][neighbor]["weight"], neighbor))
            break

    to_rank.sort(reverse=True)
    return [x[1] for x in to_rank[:max_amount]]

