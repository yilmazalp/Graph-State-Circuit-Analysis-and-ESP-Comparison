import networkx as nx
from generating_all_AME_stabilizers import generators
import matplotlib.pyplot as plt

def detection_z_locations(pauli_string: str):
    adjacency_list = []
    for pauli,index in zip(pauli_string, range(len(pauli_string))):
        if pauli == "Z":
            adjacency_list.append(index)
    return adjacency_list

def extract_adjacency(generator: list[str]):
    adjacency_dict = {}
    for item, index in zip(generator, range(len(generator))):
        adjacency_dict[index] = detection_z_locations(item)

    return adjacency_dict

def check_symmetry(matrix: dict) -> bool:
    for _key_ in matrix.keys():
        for _value_ in matrix[_key_]:
            if _key_ not in matrix[_value_]:
                return False
    return True

def build_graph():
    # initialize the graph
    G = nx.Graph()

    # construct adjacency dictionary
    adjacency = extract_adjacency(generators)

    # prepare vertices
    vertices = adjacency.keys()
    G.add_nodes_from(vertices)

    for vertex in vertices:
        # build edges
        edge = []
        [edge.append((vertex, _value_)) for _value_ in adjacency[vertex]]
        G.add_edges_from(edge)

    return G

def draw_graph(G: nx.Graph) -> None:
    nx.draw_networkx(G)
    plt.show()


def validate_graph_generator(generator_list:list[str]) -> bool:

    # check all strings have same length or not
    for j in range(len(generator_list)):
        for k in range(j, len(generator_list)):
            if len(generator_list[j]) != len(generator_list[k]):
                return False

    # each string should contain exactly one X
    for generator in generator_list:
        if generator.count("X") != 1:
            return False

    # generator i should have X in the position i
    for j in range(len(generator_list)):
        if generator_list[j].index("X") != j:
            return False

    # all non-identity elements should have X or Z
    for generator in generator_list:
        if any(symbol not in {"I", "Z", "X"} for symbol in generator):
            return False

    # graph should have symmetry
    if not check_symmetry(extract_adjacency(generator_list)):
        return False

    # no vertex is adjacent to itself
    for _key_ in extract_adjacency(generator_list):
        if _key_ in extract_adjacency(generator_list)[_key_]:
            return False

    return True


def graph_to_generators(G: nx.Graph) -> list[str]:
    vertex_list = G.nodes
    generators = []


    for vertex in vertex_list:

        generator = list("I"*len(vertex_list))
        generator[vertex] = "X"

        for neighbor in G.neighbors(vertex):
            generator[neighbor] = "Z"

        generators.append("".join(generator))

    return generators

if __name__== '__main__':
    print(f"check whether is a generator: {validate_graph_generator(generators)}")
    print(f"adjacency dictionary: {extract_adjacency(generators)}")
    print(f"has the adjacency matrix symmetry: {check_symmetry(extract_adjacency(generators))}")

    graph = build_graph()
    draw_graph(graph)
    print(f"the set of generators: {graph_to_generators(graph)}")

    # the number of vertices of the graph
    print(f"the number of vertices of the graph: {graph.number_of_nodes()}")
    # the number of edges of the graph
    print(f"the number of edges of the graph: {graph.number_of_edges()}")
    # degrees of each vertices
    print(f"degrees of each vertices: {dict(graph.degree())}")
    # is the graph connected
    print(f"is the graph connected: {nx.is_connected(graph)}")
    # maximum shortest-path distance
    print(f"maximum shortest-path distance: {nx.diameter(graph)}")
    # average shortest-path distance
    print(f"average shortest-path distance: {nx.average_shortest_path_length(graph)}")
    # is the graph bipartite
    print(f"is the graph bipartite: {nx.is_bipartite(graph)}")
    # is the graph Eulerian
    print(f"is the graph eulerian: {nx.is_eulerian(graph)}")