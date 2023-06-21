import streamlit as st
import utils
import recipy
from pathlib import Path
from streamlit_extras.switch_page_button import switch_page
from streamlit.source_util import get_pages

st.title("Find Recipes By Name")
st.subheader("What's on the menu?")

search_options = ["Tf-Idf Similarity", "Name Similarity"]
selected = st.sidebar.radio("Recipe Match Mode:", search_options)

bipartite_graph_path = st.session_state["bipartite_graph_path"]
graph = utils.get_graph(bipartite_graph_path)
recipes, tfidf, matrix = utils.get_recipe_vectorizer(bipartite_graph_path)

recipe_query = st.text_input("Write a recipe name!!")

if recipe_query:
    if search_options.index(selected) == 0:
        recipes = recipy.return_recipe_tfidf_given_query(recipe_query, tfidf, matrix, recipes)
    else:
        recipes = recipy.return_recipe_given_query(recipe_query, graph=graph)

    for recipe in recipes:
        if st.button(recipe):
            utils.visit_recipe_details(recipe)
