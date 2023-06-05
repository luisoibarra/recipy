from typing import List, Tuple
from nltk.metrics.distance import edit_distance
import networkx as nx

NodeType = object

def levenshtein_ranking(query: str, items: List[str], max_amount=100) -> List[Tuple[float, str]]:
    """
    Given a `query` and a list of `items` return the ranked list by the Levenshtein distance 
    between the query and the items.

    query: Query to rank with
    items: Items to rank with
    max_amount: Max amount of items returned in the ranking

    returns: A ranked list containing tuples with the distance and the item.
    """

    ranked_list = []

    # Ranking by Levenshtein distance
    for ingredient in items:
        ranked_list.append((edit_distance(ingredient, query), ingredient))

    return [x for x in sorted(ranked_list)][:max_amount]

def degree_ranking(graph: nx.Graph, query_nodes: List[NodeType] = None, max_amount=100) -> List[Tuple[float, NodeType]]:
    """
    Given a `graph` and a list of `query_nodes` return the ranked list by the degree amount 
    between the query nodes in the graph.

    graph: The graph to perform the query
    query_nodes: Nodes to check for degree amount
    max_amount: Max amount of items returned in the ranking

    returns: A ranked list containing tuples with the distance and the item.
    """
    if not query_nodes:
        query_nodes = graph.nodes
    recipe_nodes = [(len(list(graph.neighbors(recipe))), recipe) for recipe in query_nodes]
    return sorted(recipe_nodes, reverse=True)
