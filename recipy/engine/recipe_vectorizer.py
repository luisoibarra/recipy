from typing import Dict, List
from typing import List, Dict, Tuple
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer


def get_recipe_tf_idf_vectors(json_graph: Dict) -> Tuple[Dict[str, List[int]], np.matrix, TfidfVectorizer]:
    """
    Given a graph in json format, returns a dictionary with the vector representation for all recipes.
    """
    def extract_recipe_info(recipe: Dict) -> List[str]:
        return [x["nombre"] for x in recipe["ingredientes"]]
    
    estimator = TfidfVectorizer()
    recipes = [" ".join(extract_recipe_info(recipe)) for _, recipe in json_graph.items()]
    tfidf = estimator.fit_transform(recipes)
    return {x: tfidf[i] for i, x in enumerate(json_graph)}, tfidf, estimator
