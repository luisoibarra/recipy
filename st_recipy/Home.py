if __name__ == "__main__":
    import sys
    from pathlib import Path
    # To be able to import recipy 
    path = str(Path(__file__, "..", "..").resolve())
    if path not in sys.path:
        sys.path.insert(0, path)

from pathlib import Path
import streamlit as st
import utils

st.title("Recipe Engine")
st.subheader("Improve your cuisine by using the graph power!!")

base_path = Path(__file__, "..", "..", "recipy", "data", "graphs", "foodcom").resolve()

st.session_state["action_ingredient_graph_path"] = base_path / "ingredient_actions_graph.graphml"
st.session_state["reduced_bipartite_graph_path"] = base_path / "bipartite_recipe_ingredient_reduced_5000.graphml"
st.session_state["reduced_recipe_graph_path"] = base_path / "recipe_node_weighted_reduced_5000.graphml"
st.session_state["reduced_recipe_semantic_graph_path"] = base_path / "recipe_node_semantic_weighted_reduced_5000_sim_cutoff_0.9.graphml"
st.session_state["bipartite_graph_path"] = base_path / "bipartite_recipe_ingredient.graphml"
st.session_state["ingredient_pmi_graph_path"] = base_path / "ingredient_node_reduced_pmi_weighted.graphml"

loader = st.empty()
with st.spinner("Setting up the kitchen..."):
    loader.write("Loading cookbook...")
    bipartite_graph_path = st.session_state["bipartite_graph_path"]
    utils.get_graph(bipartite_graph_path)
    reduced_bipartite_graph_path = st.session_state["reduced_bipartite_graph_path"]
    utils.get_graph(reduced_bipartite_graph_path)
    loader.write("Getting recipes ingredients...")
    reduced_recipe_semantic_graph_path = st.session_state["reduced_recipe_semantic_graph_path"]
    utils.get_graph(reduced_recipe_semantic_graph_path)
    loader.write("Indexing recipes meaning...")
    reduced_recipe_graph_path = st.session_state["reduced_recipe_graph_path"]
    utils.get_graph(reduced_recipe_graph_path)
    loader.write("Preparing ingredients...")
    ingredient_pmi_graph_path = st.session_state["ingredient_pmi_graph_path"]
    utils.get_graph(ingredient_pmi_graph_path)
    loader.write("Matching ingredients with ingredients...")
    utils.get_ingredient_vectorizer(bipartite_graph_path)
    loader.write("Matching recipes with recipes...")
    utils.get_recipe_vectorizer(bipartite_graph_path)
    utils.get_recipe_vectorizer(reduced_bipartite_graph_path)
    loader.write("Matching recipes with ingredients...")
    utils.get_ingredient_to_recipe_vectorizer(bipartite_graph_path)
    loader.write("Reading recipe instructions")
    action_ingredient_graph_path = st.session_state["action_ingredient_graph_path"]
    utils.get_graph(action_ingredient_graph_path)
    loader.write("")

st.markdown("""
Looking for a quick and easy way to find delicious recipes that match your taste buds? 
Look no further than our amazing recipe app! With our powerful search features, you can easily 
search for recipes by name or by the ingredients you have on hand. Plus, our app goes beyond just 
finding recipes - we also help you discover new flavor combinations by suggesting ingredients that 
pair well together. And if you're ever in a pinch and need to substitute an ingredient, our app has 
got you covered with our handy substitution feature. So why wait? Prepare to start 
cooking up a storm!
""")
