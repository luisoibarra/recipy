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

st.session_state["bipartite_graph_path"] = base_path / "bipartite_recipe_ingredient.graphml"
st.session_state["ingredient_pmi_graph_path"] = base_path / "ingredient_node_reduced_pmi_weighted.graphml"

loader = st.empty()
with st.spinner("Setting up the kitchen..."):
    loader.write("Loading cookbook...")
    bipartite_graph_path = st.session_state["bipartite_graph_path"]
    utils.get_graph(bipartite_graph_path)
    loader.write("Preparing ingredients...")
    ingredient_pmi_graph_path = st.session_state["ingredient_pmi_graph_path"]
    utils.get_graph(ingredient_pmi_graph_path)
    loader.write("Matching ingredients with ingredients...")
    utils.get_ingredient_vectorizer(bipartite_graph_path)
    loader.write("Matching recipes with recipes...")
    utils.get_recipe_vectorizer(bipartite_graph_path)
    loader.write("Matching recipes with ingredients...")
    utils.get_ingredient_to_recipe_vectorizer(bipartite_graph_path)
    loader.write("")

# TODO Change some of the text to actually the features present on the application
st.markdown("""
Are you tired of sifting through countless recipes online, only to find that you don't have the right ingredients 
or that the recipe doesn't suit your dietary restrictions? Or maybe you're a food blogger or nutritionist looking 
for a way to analyze recipes and ingredients in a more efficient and systematic manner. Well, look no further!

Introducing a revolutionary application that uses graph theory to analyze recipes and ingredients. This cutting-edge 
technology allows users to input recipes and ingredients, and then generates a visual representation of the relationships 
between them. By analyzing the graph, users can quickly identify which ingredients are essential, which can be substituted, 
and which should be avoided altogether.

But that's not all. This application also incorporates dietary restrictions and preferences, allowing users to filter out 
ingredients that they cannot or do not want to consume. And for food bloggers and nutritionists, the graph can be used to 
identify patterns and trends in recipe ingredients, such as which ingredients are most commonly used together or which 
recipes are most popular among certain demographics.

So whether you're a home cook looking to simplify your recipe search or a food industry professional in need of data-driven 
insights, this application is sure to revolutionize the way you approach recipe analysis.
""")
