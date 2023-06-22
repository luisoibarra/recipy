import streamlit as st
import utils
import recipy

search_options = ["Tf-Idf Similarity", "Name Similarity"]
selected = st.sidebar.radio("Recipe Match Mode:", search_options)

similarity_options = ["Ingredients", "Semantic"]
similarity_selected = st.sidebar.radio(
    "Recipe Similarity Mode:", similarity_options)

st.title("Find Recipes By Similarity")
if similarity_selected == similarity_options[0]:
    st.subheader("What can I make with the ingredients of this recipe?")
else:
    st.subheader("What can I make with similar steps of this recipe?")

bipartite_graph_path = st.session_state["reduced_bipartite_graph_path"]
recipe_graph_path = st.session_state["reduced_recipe_graph_path"]
semantic_recipe_graph_path = st.session_state["reduced_recipe_semantic_graph_path"]
graph = utils.get_graph(bipartite_graph_path)
recipe_graph = utils.get_graph(recipe_graph_path)
semantic_recipe_graph = utils.get_graph(semantic_recipe_graph_path)
recipes, tfidf, matrix = utils.get_recipe_vectorizer(bipartite_graph_path)

recipe_query = st.text_input("Write a recipe name!!")

if recipe_query:
    if search_options.index(selected) == 0:
        recipes = recipy.return_recipe_tfidf_given_query(
            recipe_query, tfidf, matrix, recipes)
    else:
        recipes = recipy.return_recipe_given_query(recipe_query, graph=graph)

    for recipe in recipes:
        if st.button(recipe):
            similar_recipes = recipy.return_most_similar_recipes(
                recipe, recipe_graph if similarity_options.index(similarity_selected) == 0 else semantic_recipe_graph)
            for similar in similar_recipes:
                col1, col2 = st.columns(2)
                with col2:
                    if st.button(similar, key=f"similar_{similar}"):
                        utils.visit_recipe_details(similar)
