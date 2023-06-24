import streamlit as st
import utils
import recipy

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
ingredients, tfidf, matrix = utils.get_ingredient_vectorizer(action_ingredient_graph_path)

if ingredient_query:
    all_ingredients = recipy.return_ingredient_tfidf_given_query(ingredient_query, tfidf, matrix, ingredients)
    selected_ingredient = st.selectbox("Select your ingredient!", all_ingredients)

    print(selected_ingredient)
    
    if selected_ingredient:
        replacements = recipy.get_ingredient_replacements(action_ingredient_graph, ingredient_graph, selected_ingredient, recipy.get_node_louvain_partition)

        if len(replacements) > 0:
            st.subheader(f"Here is a list of some possible replacements for {selected_ingredient}:")
            for e in replacements:
                st.write(f"- {e}")
        else :
            st.subheader(f"We could not find a substitute for {selected_ingredient}")

        

