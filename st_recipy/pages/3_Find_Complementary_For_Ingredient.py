import streamlit as st
import utils
import recipy

st.title("Find complementary for ingredient")
st.subheader("I have this ingredient, with which other ingredient can be mixed??")

ingredient_pmi_graph_path = st.session_state["ingredient_pmi_graph_path"]
graph = utils.get_graph(ingredient_pmi_graph_path)

ingredient_query = st.text_input("Search ingredient to complement!!")

if ingredient_query:
    all_ingredients = recipy.return_ingredient_graph_ingredient_given_query(
        ingredient_query, graph)
    for ingredient in all_ingredients:
        if st.button(ingredient):
            similar_ingredients = recipy.return_most_similar_ingredients(ingredient, graph)
            col1, col2 = st.columns(2)
            for similar_ingredient in similar_ingredients:
                if col2.button(similar_ingredient, key=f"similar_ingredient_{similar_ingredient}"):
                    utils.visit_ingredient_details(similar_ingredient)

