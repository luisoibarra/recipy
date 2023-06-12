from typing import Tuple, List
import streamlit as st
import networkx as nx
import recipy
from streamlit_extras.switch_page_button import switch_page
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import recipy

USING_TFIDF = True

@st.cache_resource(show_spinner=False)
def get_graph(path) -> nx.Graph:
    return recipy.import_graph(path)

@st.cache_resource(show_spinner=False)
def get_ingredient_vectorizer(path) -> Tuple[List[str], TfidfVectorizer, np.matrix]:
    G = get_graph(path)
    ingredients, matrix, tfidf = recipy.extract_tfidf_info(G, "ingredient")
    return [x.removesuffix("_ingredient") for x in ingredients], tfidf, matrix

@st.cache_resource(show_spinner=False)
def get_recipe_vectorizer(path) -> Tuple[List[str], TfidfVectorizer, np.matrix]:
    G = get_graph(path)
    recipes, matrix, tfidf = recipy.extract_tfidf_info(G, "recipe")
    return [x.removesuffix("_recipe") for x in recipes], tfidf, matrix

@st.cache_resource(show_spinner=False)
def get_ingredient_to_recipe_vectorizer(path) -> Tuple[List[str], TfidfVectorizer, np.matrix]:
    G = get_graph(path)
    recipes, matrix, tfidf = recipy.extract_tfidf_info(G, "recipe", represent_with_neighbors=True)
    return [x.removesuffix("_recipe") for x in recipes], tfidf, matrix


def visit_ingredient_details(ingredient):
    st.session_state["ingredient_details"] = ingredient 
    switch_page("Ingredient Details")

def visit_recipe_details(recipe):
    st.session_state["recipe_details"] = recipe
    switch_page("Recipe Details")
