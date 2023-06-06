import streamlit as st
import networkx as nx
import recipy
from streamlit_extras.switch_page_button import switch_page


@st.cache_resource(show_spinner=False)
def get_graph(path) -> nx.Graph:
    return recipy.import_graph(path)


def visit_ingredient_details(ingredient):
    st.session_state["ingredient_details"] = ingredient 
    switch_page("Ingredient Details")

def visit_recipe_details(recipe):
    st.session_state["recipe_details"] = recipe
    switch_page("Recipe Details")
