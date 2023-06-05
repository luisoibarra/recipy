import nltk
from typing import List, Tuple


def extract_ingredients_with_modifiers_nltk_grammar(ingredient: str) -> List[Tuple[str, str]]:
    """
    Given an ingredient description extract all ingredients with its modifier.
    This implementation works by extracting all groups of adjacent adjectives and nouns
    as a single ingredient and then converting to singular all its terms. 

    ingredient: Must be a short description of ingredients.

    ## Examples:
    - normalize("the prepared pizza crust") => [('pizza crust', 'prepared')]
    - normalize("salt and pepper") => [('salt', ''), ('pepper', '')]
    - normalize("finely chopped onion") => [('onion', '')]
    - normalize("diced tomatoes") => [('tomato', '')]
    - normalize("tomato paste") => [('tomato paste', '')]
    - normalize("apple cider vinegar") => [('apple cider vinegar', '')]
    - normalize("fresh cilantro leaves") => [('cilantro leaf', 'fresh')]
    - normalize("black pepper") => [('pepper', 'black')]
    """

    simple_grammar = \
    """
    I: {<ADJ>*<NOUN>+}
    """

    parser = nltk.RegexpParser(simple_grammar)
    lemmatizer = nltk.WordNetLemmatizer()

    def filter_tree(tree, tag):
        try:
            if tree.label() == tag:
                return [[x for x in tree]]
        except:
            return []
        current = []
        for node in tree:
            filtered_nodes = filter_tree(node, tag)
            current.extend(filtered_nodes)
        return current

    def reassemble_ingredient(parsed: List[Tuple[str, str]]) -> str:
        return " ".join([lemmatizer.lemmatize(x, pos="n") for x, y in parsed if y == "NOUN"])

    def get_modifiers(parsed: List[Tuple[str, str]]) -> str:
        return " ".join([lemmatizer.lemmatize(x, pos="a") for x, y in parsed if y == "ADJ"])

    pos = nltk.pos_tag([x.lower() for x in ingredient.split()], tagset="universal")
    result = parser.parse(pos)
    result = filter_tree(result, "I")
    if result:
        return list(zip(map(reassemble_ingredient, result), map(get_modifiers, result)))
    else:
        return [(ingredient, "")]