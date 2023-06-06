import streamlit as st
from streamlit_extras.switch_page_button import switch_page
import utils

ingredient = st.session_state.get("ingredient_details", None)

if ingredient:
    st.title(ingredient)
    bipartite_graph_path = st.session_state["bipartite_graph_path"]
    graph = utils.get_graph(bipartite_graph_path)
    st.warning("TODO: Show information about the ingredient")
else:
    st.header("No selected ingredient")
    st.write("Wow, you are not supposed to be here. Select an ingredient from one of the other pages.")
    if st.button("Find Recipes By Ingredients"):
        switch_page("Find Recipes By Ingredients")
