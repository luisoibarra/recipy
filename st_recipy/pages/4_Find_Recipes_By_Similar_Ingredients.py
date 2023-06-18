import streamlit as st
import utils
import recipy

st.title("Find Recipes With Similar Ingredients")
st.subheader("What can I make with the ingredients of this recipe?")

search_options = ["Name Similarity", "Tf-Idf Similarity"]
selected = st.sidebar.radio("Recipe Match Mode:", search_options)

bipartite_graph_path = st.session_state["reduced_bipartite_graph_path"]
recipe_graph_path = st.session_state["reduced_recipe_graph_path"]
graph = utils.get_graph(bipartite_graph_path)
recipe_graph = utils.get_graph(recipe_graph_path)
recipes, tfidf, matrix = utils.get_recipe_vectorizer(bipartite_graph_path)

recipe_query = st.text_input("Write a recipe name!!")

if recipe_query:
    if search_options.index(selected) == 1:
        recipes = recipy.return_recipe_tfidf_given_query(recipe_query, tfidf, matrix, recipes)
    else:
        recipes = recipy.return_recipe_given_query(recipe_query, graph=graph)

    for recipe in recipes:
        if st.button(recipe):
            similar_recipes = recipy.return_most_similar_recipes(recipe, recipe_graph)
            for similar in similar_recipes:
                col1, col2 = st.columns(2)
                with col2:
                    if st.button(similar, key=f"similar_{similar}"):
                        utils.visit_recipe_details(similar)