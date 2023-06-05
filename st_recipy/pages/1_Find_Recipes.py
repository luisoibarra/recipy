import streamlit as st
import utils
import recipy
from pathlib import Path
from streamlit_extras.switch_page_button import switch_page
from streamlit.source_util import get_pages

st.title("Find Recipes")
st.subheader("What's on the menu?")

bipartite_graph_path = st.session_state["bipartite_graph_path"]
graph = utils.get_graph(bipartite_graph_path)

recipe_query = st.text_input("Write a recipe name!!")

if recipe_query:
    recipes = recipy.return_recipe_given_query(recipe_query, graph=graph)

    for recipe in recipes:
        if st.button(recipe):
            utils.visit_recipe_details(recipe)
