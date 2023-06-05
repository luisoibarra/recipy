from typing import List, Dict, Iterable, Tuple
import networkx as nx
import random
import math


def build_recipe_graph(json: Dict, recipe_probability=1.0) -> nx.Graph:
    """
    Builds a nx Graph from the json.

    json: Json with the default schema
    recipe_probability: Probability for a recipe to be in the graph

    returns: A graph with recipe as nodes and shared ingredients as edges. 
    """
    G_json = nx.Graph()

    recipes = random.sample(list(json.keys()), math.floor(
        len(json) * recipe_probability))

    for node in json.values():
        kwargs = {}
        if "cap" in node:
            kwargs["cap"] = node['cap']
        G_json.add_node(node['nombre'], **kwargs)

    for i, recipe1 in enumerate(recipes):
        recipe1_ingredients_names_set = set(
            map(lambda x: x['nombre'], json[recipe1]['ingredientes']))
        for recipe2 in recipes[i+1:]:
            recipe2_ingredients_names = list(
                map(lambda x: x['nombre'], json[recipe2]['ingredientes']))
            common_ingredients = recipe1_ingredients_names_set.intersection(
                recipe2_ingredients_names)
            all_ingredients = recipe1_ingredients_names_set.union(
                recipe2_ingredients_names)
            if common_ingredients:
                jaccard = len(common_ingredients) / len(all_ingredients)
                G_json.add_edge(recipe1, recipe2, weight=jaccard)
    return G_json


def build_ingredient_graph(json: Dict, ingredients: Iterable[str] = None) -> Tuple[nx.Graph, nx.Graph]:
    """
    Builds a nx Graph from the json.

    json: Json with the default schema
    ingredients: Final ingredients to match

    returns: A graph with ingredients as nodes and shared recipes as edges with Jaccard similarity and pmi similarity. 
    """
    G_jaccard = nx.Graph()
    G_substitte = nx.Graph()

    if not ingredients:
        ingredients = set()
        for recipe in json:
            ingredients.update(
                list(map(lambda x: x['nombre'], json[recipe]["ingredientes"])))
    ingredients = list(ingredients)

    ingredient_dict = {x: set() for x in ingredients}
    for recipe in json:
        for ingr in list(map(lambda x: x['nombre'], json[recipe]["ingredientes"])):
            if ingr in ingredient_dict:
                ingredient_dict[ingr].add(recipe)

    for node in ingredients:
        G_jaccard.add_node(node)
        G_substitte.add_node(node)

    all_recipes = len(json)

    for i, ingredient1 in enumerate(ingredients):
        recipe1_ingredients_names_set = ingredient_dict[ingredient1]
        for ingredient2 in ingredients[i+1:]:
            recipe2_ingredients_names = ingredient_dict[ingredient2]

            common_recipes = recipe1_ingredients_names_set.intersection(
                recipe2_ingredients_names)
            all_common_recipes = recipe1_ingredients_names_set.union(
                recipe2_ingredients_names)
            if common_recipes:
                jaccard = len(common_recipes) / len(all_common_recipes)
                G_jaccard.add_edge(ingredient1, ingredient2, weight=jaccard)

                # pmi(a,b) = P(a,b)/(p(a)p(b))
                pmi = math.log((len(common_recipes) * all_recipes) / (
                    len(recipe1_ingredients_names_set) * len(recipe2_ingredients_names)))
                G_substitte.add_edge(ingredient1, ingredient2, weight=pmi)
    return G_jaccard, G_substitte


def build_ingredient_recipe_graph(json: dict, bipartite=True) -> nx.Graph:
    """
    Builds a nx Graph from the json.

    json: Json with the default schema
    bipartite: If the graph must be bipartite. Some times some recipes are used as ingredients.
    if bipartite is true the category will be enforced in the node name by appending `_recipe` or
    `_ingredient` at the end of the node name

    returns: A graph with ingredients and recipes as nodes and recipe occurrence as edges. 
    """
    G_json = nx.Graph()

    ingredients = set()
    for recipe in json:
        ingredients.update(
            list(map(lambda x: x['nombre'], json[recipe]["ingredientes"])))
    ingredients = list(ingredients)

    for node in ingredients:
        G_json.add_node(
            node + ("_ingredient" if bipartite else ""), type="ingredient")

    for node in json:
        G_json.add_node(node + ("_recipe" if bipartite else ""), type="recipe")

    for recipe in json:
        for ingredient in json[recipe]["ingredientes"]:
            G_json.add_edge(recipe + ("_recipe" if bipartite else ""),
                            ingredient["nombre"] + ("_ingredient" if bipartite else ""))

    return G_json