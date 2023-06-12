import networkx as nx
from typing import List
from sklearn.feature_extraction.text import TfidfVectorizer

import numpy as np
from .ranking import levenshtein_ranking, degree_ranking, tfidf_ranking
from .filters import contain_filter

def return_ingredient_tfidf_given_query(ingredient_query: str, vectorizer: TfidfVectorizer, tfidf_matrix: np.matrix, ingredient_list: List[str], max_amount: int = 100) -> List[str]:
    """
    Returns a ranked list with the ingredients that matches the query in the graph.
    """

    ranked_list = tfidf_ranking(vectorizer, tfidf_matrix, ingredient_list, ingredient_query, max_amount)

    return [x[1] for x in ranked_list]


def return_recipe_tfidf_given_query(recipe_query: str, vectorizer: TfidfVectorizer, tfidf_matrix: np.matrix, recipe_list: List[str], max_amount: int = 100) -> List[str]:
    """
    Returns a ranked list with the recipes that matches the query in the graph.
    """

    ranked_list = tfidf_ranking(vectorizer, tfidf_matrix, recipe_list, recipe_query, max_amount)

    return [x[1] for x in ranked_list]


def return_ingredient_given_query(ingredient_query: str, graph: nx.Graph, max_amount: int = 100) -> List[str]:
    """
    Returns a ranked list with the ingredients that matches the query in the graph.
    """
    ingredient_nodes: List[str] = [
        x for x in graph.nodes if graph.nodes[x]["type"] == "ingredient"]
    filtered_list = []

    # Filter
    for ingredient in ingredient_nodes:
        if contain_filter(ingredient_query, ingredient):
            filtered_list.append(ingredient)

    ranked_list = levenshtein_ranking(ingredient_query, [
        x.removesuffix("_ingredient") for x in filtered_list], max_amount=max_amount)

    return [x[1] for x in ranked_list]


def return_recipe_given_query(recipe_query: str, graph: nx.Graph, max_amount: int = 100) -> List[str]:
    """
    Returns a ranked list of the recipes matching the `recipe_query`
    """
    recipe_nodes: List[str] = [
        x for x in graph.nodes if graph.nodes[x]["type"] == "recipe"]
    filtered_list = []

    # Filter
    for recipe in recipe_nodes:
        if contain_filter(recipe_query, recipe):
            filtered_list.append(recipe)

    # Ranking
    ranked_list = levenshtein_ranking(recipe_query, [
        x.removesuffix("_recipe") for x in filtered_list], max_amount=max_amount)

    return [x[1] for x in ranked_list]


def return_available_recipes_given_ingredients(ingredients_query: List[str], graph: nx.Graph, exact_ingredient_match: bool = False, max_amount: int = 100) -> List[str]:
    """
    Returns the recipes that can be made with any of the given ingredients.
    """
    ingredients_query = [x + "_ingredient" for x in ingredients_query]

    ingredient_nodes: List[str] = [
        x for x in graph.nodes if graph.nodes[x]["type"] == "ingredient"]
    ingredient_nodes = set(ingredient_nodes).intersection(ingredients_query)

    recipe_nodes = set(
        recipe for ingredient in ingredient_nodes for recipe in graph[ingredient])

    subgraph: nx.Graph = graph.subgraph(recipe_nodes.union(ingredient_nodes))

    # Ranking by degree
    recipe_nodes = [
        recipe for recipe in subgraph.nodes if subgraph.nodes[recipe]["type"] == "recipe"]
    ranked_list = degree_ranking(
        subgraph, query_nodes=recipe_nodes, max_amount=len(subgraph))

    return [x[1].removesuffix("_recipe") for x in ranked_list if not exact_ingredient_match or x[0] == len(ingredient_nodes)][:max_amount]


def return_ingredients_given_recipe(recipe_query: str, graph: nx.Graph) -> List[str]:
    return [x.removesuffix("_ingredient") for x in graph.neighbors(recipe_query + "_recipe")]
