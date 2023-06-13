from typing import List, Tuple, Callable
from nltk.metrics.distance import edit_distance
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
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
    recipe_nodes = [(len(list(graph.neighbors(recipe))), recipe)
                    for recipe in query_nodes]
    return sorted(recipe_nodes, reverse=True)[:max_amount]


def tfidf_ranking(vectorizer: TfidfVectorizer, tfidf_matrix: np.matrix, document_list: List[str], query: str, max_amount=100) -> List[Tuple[float, str]]:
    """
    Returns the ranking based on the TF-IDF algorithm

    `vectorizer`: Fitted vectorizer
    `tfidf_matrix`: Fitted matrix
    `document_list`: Original document list. In our case should be recipe names if the vector represents a recipe.
    `query`: Query to perform the ranking with
    `max_amount`: Max amount of elements return by the ranking
    """
    # Transform the query into a TF-IDF vector
    query_vector = vectorizer.transform([query])

    # Compute the cosine similarity between the query vector and each document vector
    similarity_scores = cosine_similarity(tfidf_matrix, query_vector)

    # Get the indices of the documents sorted by their similarity scores
    indices = np.argsort(similarity_scores, axis=0)[::-1].flatten()

    return [(similarity_scores[i], document_list[i]) for i in indices[:max_amount]]


def get_ingredient_cutoff(bipartite_graph: nx.Graph, ingredient_cutoff_percentage=0.9) -> List[str]:
    """
    Returns the ingredients that represents the `ingredient_cutoff_percentage` of the importance total, sorted by importance
    """
    ingredient_with_occurrence = [(len(list(bipartite_graph.neighbors(ingredient))), ingredient)
                                  for ingredient in bipartite_graph.nodes if bipartite_graph.nodes[ingredient]["type"] == "ingredient"]
    ingredient_with_occurrence = sorted(
        ingredient_with_occurrence, reverse=True)

    # Extract the ingredient names and occurrence values
    occurrences = [x[0] for x in ingredient_with_occurrence]
    ingredients = [x[1] for x in ingredient_with_occurrence]
    cumulative_occurrences = np.cumsum(occurrences)
    cutoff_index = -1
    total = cumulative_occurrences[-1]
    for i, cumsum in enumerate(cumulative_occurrences):
        if cumsum / total >= ingredient_cutoff_percentage:
            cutoff_index = i
            break

    return ingredients[:cutoff_index]


def get_recipe_cutoff(bipartite_graph: nx.Graph, recipe_cutoff_percentage=0.8) -> List[Tuple[float, str]]:
    """
    Returns the recipes that represents the `recipe_cutoff_percentage` of the importance total, sorted by importance
    """
    recipe_map = {x: "_|_".join([y.removesuffix("_ingredient") for y in bipartite_graph.neighbors(x)]) for x in bipartite_graph if bipartite_graph.nodes[x]["type"] == "recipe"}
    tfidf = TfidfVectorizer(tokenizer=lambda x: x.split("_|_"))
    # recipe_map = {x: " ".join([y.removesuffix("_ingredient") for y in bipartite_graph.neighbors(
    #     x)]) for x in bipartite_graph if bipartite_graph.nodes[x]["type"] == "recipe"}
    # tfidf = TfidfVectorizer()
    matrix = tfidf.fit_transform(recipe_map.values())

    def recipe_importance_1(i: int) -> float:
        """
        Gives an importance number to the recipe that will be used for ranking.
        """
        vector = matrix[i]
        length = vector.getnnz()  # Non zero entries
        return np.sum(vector) / length

    def recipe_importance_2(i: int) -> float:
        """
        Gives an importance number to the recipe that will be used for ranking.
        """
        from scipy.sparse.linalg import norm
        vector = matrix[i]
        return norm(vector)

    def recipe_importance_3(i: int) -> float:
        """
        Gives an importance number to the recipe that will be used for ranking.
        """
        vector = matrix[i]
        return vector.getnnz()

    recipe_importance = recipe_importance_1

    recipe_importance_list = sorted(
        [(recipe_importance(i), x) for i, x in enumerate(recipe_map)], reverse=True)

    cutoff_index = -1
    cumulative_occurrences = np.cumsum([x[0] for x in recipe_importance_list])
    total = cumulative_occurrences[-1]
    for i, cumsum in enumerate(cumulative_occurrences):
        if cumsum / total >= recipe_cutoff_percentage:
            cutoff_index = i
            break

    return recipe_importance_list[:cutoff_index]

