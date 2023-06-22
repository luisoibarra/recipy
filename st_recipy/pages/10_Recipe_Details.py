import streamlit as st
from streamlit_extras.switch_page_button import switch_page
import utils

recipe = st.session_state.get("recipe_details", None)

if recipe:
    st.title(recipe)
    bipartite_graph_path = st.session_state["bipartite_graph_path"]
    graph = utils.get_graph(bipartite_graph_path)
    st.warning("TODO: Show information about the recipe")
else:
    st.header("No selected recipe")
    st.write("Wow, you are not supposed to be here. Select a recipe from one of the other pages.")
    if st.button("Find Recipes By Name"):
        switch_page("Find Recipes By Name")
