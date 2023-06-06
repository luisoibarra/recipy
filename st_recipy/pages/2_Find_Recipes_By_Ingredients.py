from typing import List
import streamlit as st
import recipy
import utils
from pathlib import Path


st.title("Find Recipes By Ingredients")
st.subheader("What can I prepare with these ingredients??")

if "selected_ingredients" not in st.session_state:
    st.session_state["selected_ingredients"] = []
ingredients: List[str] = st.session_state["selected_ingredients"]

bipartite_graph_path = st.session_state["bipartite_graph_path"]
graph = utils.get_graph(bipartite_graph_path)

ingredient_query = st.text_input("Search ingredients to add to the basket!!")

if ingredient_query:
    all_ingredients = recipy.return_ingredient_given_query(
        ingredient_query, graph)
    selected_ingredients = st.multiselect(
        "Select your ingredients!!", all_ingredients)
    if selected_ingredients:
        st.button("Add to basket", on_click=lambda: ingredients.extend(
            set(selected_ingredients).difference(ingredients)))


st.subheader("Basket:")
for ingredient in ingredients:
    col1, col2 = st.columns(2)
    if col1.button(ingredient):
        utils.visit_ingredient_details(ingredient)
    col2.button("Remove", key=f"add_{ingredient}_ingredient", on_click=lambda: ingredients.remove(ingredient))

if ingredients:
    st.subheader("Recipes:")
    recipes = recipy.return_available_recipes_given_ingredients(
        ingredients, graph, True)
    for recipe in recipes:
        if st.button(recipe):
            utils.visit_recipe_details(recipe)
