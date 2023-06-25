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

all_ingredients = [x for x in action_ingredient_graph if action_ingredient_graph.nodes[x]["type"] == "ingredient"]
selected_ingredient = st.selectbox("Select your ingredient!", all_ingredients)

if selected_ingredient:
    print(selected_ingredient)
    replacements = recipy.get_ingredient_replacements(action_ingredient_graph, ingredient_graph, selected_ingredient, recipy.get_node_louvain_partition)

    if len(replacements) > 0:
        st.subheader(f"Here is a list of some possible replacements for {selected_ingredient}:")
        for e in replacements:
            st.write(f"- {e}")
    else :
        st.subheader(f"We could not find a substitute for {selected_ingredient}")