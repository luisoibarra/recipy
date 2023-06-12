from typing import List
from .filters import equal_filter, contain_filter
from .ranking import levenshtein_ranking
import networkx as nx


def return_most_similar_ingredients(ingredient_query: str, ingredient_graph: nx.Graph, max_amount: int = 100) -> List[str]:
    """
    Returns the most similar ingredients matching `ingredient_query` by the node's weight.
    """
    to_rank = []
    for ingredient in ingredient_graph.nodes:
        if equal_filter(ingredient_query, ingredient):
            # TODO maybe the k-clique is a better approach
            neighbors = ingredient_graph.neighbors(ingredient)
            for neighbor in neighbors:
                to_rank.append((ingredient_graph[ingredient][neighbor]["weight"], neighbor))
            break

    to_rank.sort(reverse=True)
    return [x[1] for x in to_rank[:max_amount]]



def return_ingredient_graph_ingredient_given_query(ingredient_query: str, graph: nx.Graph, max_amount: int = 100) -> List[str]:
    """
    Returns a ranked list with the ingredients that matches the query in the graph.
    """
    filtered_list = []

    bipartite = "type" in graph.nodes[next(iter(graph.nodes))]

    # Filter
    for ingredient in [x for x in graph.nodes if not bipartite or graph.nodes[x]["type"] == "ingredient"]:
        if contain_filter(ingredient_query, ingredient):
            filtered_list.append(ingredient)

    ranked_list = levenshtein_ranking(ingredient_query, [
        x.removesuffix("_ingredient") for x in filtered_list], max_amount=max_amount)

    return [x[1] for x in ranked_list]
