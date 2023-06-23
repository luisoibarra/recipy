from recipy.engine.ingredient_replacement import get_node_louvain_partition
import streamlit as st
import utils
import recipy
from pathlib import Path
from streamlit_extras.switch_page_button import switch_page
from streamlit.source_util import get_pages

st.title("Replace Ingredient")
st.subheader("How can I replace this ingredient?")

if "selected_ingredient" not in st.session_state:
    st.session_state["selected_ingredient"] = []
selected_ingredient: list[str] = st.session_state["selected_ingredient"]

bipartite_graph_path = st.session_state["bipartite_graph_path"]

ingredient_graph_path = st.session_state["ingredient_pmi_graph_path"]
action_ingredient_graph_path = st.session_state["action_ingredient_graph_path"]
ingredient_graph = utils.get_graph(ingredient_graph_path)
action_ingredient_graph = utils.get_graph(action_ingredient_graph_path)

ingredient_query = st.text_input("Ingredient to replace")
ingredients, tfidf, matrix = utils.get_ingredient_vectorizer(bipartite_graph_path)

if ingredient_query:
    all_ingredients = recipy.return_ingredient_tfidf_given_query(ingredient_query, tfidf, matrix, ingredients)
    selected_ingredient = st.selectbox("Select your ingredient!", all_ingredients)
    
    if selected_ingredient:
        st.subheader(f"Here is a list of some possible replacements for {selected_ingredient}:")
        replacements = recipy.get_ingredient_replacements(action_ingredient_graph, ingredient_graph, selected_ingredient, recipy.get_node_louvain_partition)
        for e in replacements:
            st.write(f"- {e}")

        

