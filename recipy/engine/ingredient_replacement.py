import networkx as nx
from itertools import islice


def get_node_neighbourhood(graph: nx.Graph, node: str, edges_fraction = 2) -> list[str]:
    """
    Makes a BFS from the given node, in the first step of the BFS adds the 1/<edges_fraction> of the total of nodes in that level.
    <edges_fraction> is duplicated for the consequent levels.

    :return The list of nodes found so far.
    """
    f = edges_fraction
    seen, queue1, queue2 = set([node]), [node], []
    while len(queue1) != 0 or len(queue2) != 0:
        if len(queue1) == 0: 
            queue1, queue2, f = queue2, queue1, f * 2

        c = queue1.pop()
        adj = [(v, graph[c][v]['weight']) for (_, v) in graph.edges(c)]
        adj.sort(key=lambda x: x[1], reverse=True)
        for (v, w) in adj[:len(adj) // f]:
            if not v in seen:
                seen.add(v)
                queue2.append(v)
    return list(seen)


def get_node_louvain_partition(graph: nx.Graph, node: str, resolution: int = 1.5, level: int = 1) -> list[str]:
    """
    Gets the list of nodes that fall in the same group of the given node after using the louvain_partitions
    method to get a partition of the graph.
    """

    partition = nx.community.louvain_partitions(graph, resolution=resolution)
    if level > 1: partition = next(islice(partition, level - 1))
    else: partition = next(partition)

    return list([group for group in partition if node in group][0])


def get_node_louvain_communities(graph: nx.Graph, node: str, resolution: int = 1.5, community_size_threshold: int = None) -> list[str]:
    """
    Gets the list of nodes that fall in the same community of the given node after using the louvain_communities
    method in the graph.
    """

    communities = nx.community.louvain_communities(graph, resolution=resolution)
    response = []
    for comm in communities:
        if node in comm and (community_size_threshold is None or len(comm) <= community_size_threshold):
            response.extend(comm)
    return list(set(response))


def get_percent_cuttof(arr: list[tuple[str, int]], cuttof_percent: int):
    """
    Gets the elements whose value makes at most the <cuttof_percent> of the total.
    """
    bigger = cuttof_percent > 0
    cuttof_percent= abs(cuttof_percent)

    arr.sort(key=lambda x: x[1], reverse=bigger)
    total = sum(x for (_, x) in arr)

    response, partial = [], 0
    for (x, y) in arr:
        partial += y
        if 100 * partial / total > cuttof_percent: break
        response.append(x)

    return response



def actions_similarity(actions_graph: nx.Graph, x: str, y:str):
    """
    Calculates a similarity coeficient between the given recipes according to the Jaccard index of the action verbs that are linked to them.
    """

    adjx = [(v, actions_graph[u][v]['weight']) for (u, v) in actions_graph.edges(x)]
    adjy = [(v, actions_graph[u][v]['weight']) for (u, v) in actions_graph.edges(y)]
    
    stx = set(get_percent_cuttof(adjx, 30))
    sty = set(get_percent_cuttof(adjy, 30))

    return len(stx.intersection(sty)) / len(stx.union(sty))


def get_ingredient_replacements(actions_graph: nx.Graph, ingredients_graph: nx.Graph, node: str, method):
    relevant = method(ingredients_graph, node)
    relevant.sort(key=lambda x: actions_similarity(actions_graph, x, node), reverse=True)
    return relevant[1:11]