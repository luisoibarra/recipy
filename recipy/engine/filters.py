
def contain_filter(query: str, item: str):
    """
    Returns if `query` is inside `item`
    """
    return query in item

def equal_filter(query: str, item: str):
    """
    Returns if `query` is equal `item`
    """
    return query == item