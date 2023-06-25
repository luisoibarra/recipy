from typing import List
import streamlit as st
import recipy
import utils
from pathlib import Path


st.title("Find Recipes By Ingredients")
st.subheader("What can I prepare with these ingredients??")

if "selected_ingredients" not in st.session_state:
    st.session_state["selected_ingredients"] = []
saved_ingredients: List[str] = st.session_state["selected_ingredients"]

bipartite_graph_path = st.session_state["bipartite_graph_path"]
graph = utils.get_graph(bipartite_graph_path)

search_options = ["Tf-Idf Similarity", "Name Similarity"]
selected = st.sidebar.radio("Ingredient Match Mode:", search_options)

recipe_search_options = ["Ingredient Intersection", "Tf-Idf Ingredient Similarity"]
recipe_selected = st.sidebar.radio("Recipe Match Mode:", recipe_search_options)


ingredients, tfidf, matrix = utils.get_ingredient_vectorizer(bipartite_graph_path)
recipes_list, recipe_tfidf, recipe_matrix = utils.get_ingredient_to_recipe_vectorizer(bipartite_graph_path)

ingredient_query = st.text_input("Search ingredients to add to the basket!!")

if ingredient_query:
    if search_options.index(selected) == 0:
        all_ingredients = recipy.return_ingredient_tfidf_given_query(ingredient_query, tfidf, matrix, ingredients)
    else:
        all_ingredients = recipy.return_ingredient_graph_ingredient_given_query(
            ingredient_query, graph)
    selected_ingredients = st.multiselect(
        "Select your ingredients!!", all_ingredients)
    if selected_ingredients:
        st.button("Add to basket", on_click=lambda: saved_ingredients.extend(
            set(selected_ingredients).difference(saved_ingredients)))


st.subheader("Basket:")
for ingredient in saved_ingredients:
    col1, col2 = st.columns(2)
    if col1.button(ingredient):
        utils.visit_ingredient_details(ingredient)
    col2.button("Remove", key=f"add_{ingredient}_ingredient", on_click=lambda: saved_ingredients.remove(ingredient))

if saved_ingredients:
    st.subheader("Recipes:")
    if recipe_search_options.index(recipe_selected) == 1:
        recipes = recipy.return_recipe_tfidf_given_query(" ".join(saved_ingredients), recipe_tfidf, recipe_matrix, recipes_list)
    else:
        recipes = recipy.return_available_recipes_given_ingredients(
            saved_ingredients, graph, True)
    for recipe in recipes:
        if st.button(recipe):
            utils.visit_recipe_details(recipe)
