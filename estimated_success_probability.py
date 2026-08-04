import math
from graph_state import build_graph
import pandas as pd
import networkx as nx
from AME_circuit import schedule_cz_gate

def calculate_esp(gate_fidelities: list[float], circuit_time: float, coherence_time: float) -> float:
    return math.prod(gate_fidelities) * math.exp(-circuit_time / coherence_time)

def calculate_scheduled_esp(gate_fidelities: list[float], scheduled_time: float, coherence_time: float) -> float:
    return math.prod(gate_fidelities) * math.exp(-scheduled_time / coherence_time)

def create_test_graphs(number_of_qubits: int) -> dict[str, nx.Graph]:
    return {
        "path": nx.path_graph(number_of_qubits),
        "cycle": nx.cycle_graph(number_of_qubits),
        "star": nx.star_graph(number_of_qubits - 1),
        "complete": nx.complete_graph(number_of_qubits),
        "grid_2x3": nx.convert_node_labels_to_integers(
            nx.grid_2d_graph(2, 3)
        ),
        "ame_6_2": build_graph(),
    }

def analyze_graph_state(
    name: str,
    graph: nx.Graph,
    single_qubit_fidelity: float,
    two_qubit_fidelity: float,
    single_qubit_duration: float,
    two_qubit_duration: float,
    coherence_time: float,
) -> dict:

    number_of_h_gates = graph.number_of_nodes()
    number_of_cz_gates = graph.number_of_edges()

    gate_fidelities = ([single_qubit_fidelity] * number_of_h_gates + [two_qubit_fidelity] * number_of_cz_gates)
    circuit_time = number_of_h_gates*single_qubit_duration + number_of_cz_gates*two_qubit_duration
    cz_depth = len(schedule_cz_gate(list(graph.edges)))
    scheduled_time = single_qubit_duration + cz_depth * two_qubit_duration

    return {
        "name": name,
        "vertices": graph.number_of_nodes(),
        "edges": graph.number_of_edges(),
        "maximum_degree": max(degree for _, degree in graph.degree()),
        "diameter": nx.diameter(graph),
        "cz_depth": cz_depth,
        "sequential_time": circuit_time,
        "scheduled_time": scheduled_time,
        "sequential_esp": calculate_esp(gate_fidelities, circuit_time, coherence_time),
        "scheduled_esp":  calculate_scheduled_esp(gate_fidelities, scheduled_time, coherence_time),
    }


if __name__ == '__main__':

    results = []

    for name, graph in create_test_graphs(6).items():
        results.append(
            analyze_graph_state(
                name=name,
                graph=graph,
                single_qubit_fidelity=0.9999,
                two_qubit_fidelity=0.999,
                single_qubit_duration=100e-9,
                two_qubit_duration=150e-9,
                coherence_time=20e-6
            )
        )


    results_table = pd.DataFrame(results)

    results_table["sequential_time_"] = (results_table["sequential_time"] * 1e6)

    results_table["scheduled_time_"] = (results_table["scheduled_time"] * 1e6)

    results_table = results_table.drop(columns=["sequential_time", "scheduled_time"])

    results_table = results_table[
        [
            "name",
            "vertices",
            "edges",
            "maximum_degree",
            "diameter",
            "cz_depth",
            "sequential_time_",
            "scheduled_time_",
            "sequential_esp",
            "scheduled_esp",
        ]
    ]

    print(
        results_table.to_string(
            index=False,
            formatters={
                "sequential_time_": lambda x: f"{x:.3f}",
                "scheduled_time_": lambda x: f"{x:.3f}",
                "sequential_esp": lambda x: f"{x:.6f}",
                "scheduled_esp": lambda x: f"{x:.6f}",
            },
        )
    )
