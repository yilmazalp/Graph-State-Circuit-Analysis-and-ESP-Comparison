import networkx as nx
from graph_state import build_graph
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit

def graph_to_cz_gate(G: nx.Graph) -> list[tuple[int, int]]:
    return list(G.edges)

def build_circuit(G: nx.Graph):
    # create quntum circuit with 6 qubits and 2 classical bits
    qc = QuantumCircuit(G.number_of_nodes(), 2)

    # set the |+> qubits
    for vertex in G.nodes:
        qc.h(vertex)

    # construct the CZ gates
    for edge in graph_to_cz_gate(G):
        qc.cz(edge[0], edge[1])

    return qc

def schedule_cz_gate(edges: list[tuple[int, int]]) -> list[list[tuple[int, int]]]:
    scheduled_edges = []

    for edge in edges:
        placed = False

        for layer in scheduled_edges:
            # Check whether edge conflicts with ANY edge in layer.
            if all(set(edge).isdisjoint(existing_edge) for existing_edge in layer):
                layer.append(edge)
                placed = True
                break

        if not placed:
            scheduled_edges.append([edge])

    return scheduled_edges


if __name__ == '__main__':
    graph = build_graph()
    print(graph.edges)
    circuit = build_circuit(graph)
    print(schedule_cz_gate([(0, 1),  (2, 3),  (4, 5)]))
    circuit.draw('mpl')
    plt.show()