# Graph-State Circuit Analysis and ESP Comparison
This project studies quantum circuits preparing several six-qubit graph states and compares their estimated success probability (ESP) under a simplified hardware model.

The main example is the AME(6,2) graph-state circuit considered in the paper "Near-Term Spin-Qubit Architecture Design via Multipartite Maximally-Entangled States."

For each graph, the project computes:

- number of vertices,
- number of edges,
- maximum degree,
- graph diameter,
- CZ-gate depth,
- sequential circuit duration,
- scheduled circuit duration,
- sequential Expected Success Probability,
- scheduled Expected Success Probability.

## Graph states

Let $G=(V,E)$ be a simple graph with $n=|V|$ vertices. A graph state is prepared by initializing every qubit in the state

 $$|+\rangle = \frac{|0\rangle+|1\rangle}{\sqrt{2}}$$

and then applying one controlled-Z gate for every edge of the graph:

$$
|G\rangle =\prod_{(i,j)\in E} CZ_{ij}|+\rangle^{\otimes n}$$

- every vertex corresponds to a qubit,
- every edge corresponds to a CZ gate.

## Absolutely maximally entangled states

An absolutely maximally entangled state AME(n,d) is an $n$-party quantum state with local dimension $d$ such that every reduction to at most half of the parties is maximally mixed.

For an AME(6,2) state, $1$-, $2$-, or $3$-qubit reduced states are maximally mixed.

Equivalently, for every subsystem $A$ such that  $|A|\leq \frac{6}{2}=3$,

$$\rho_A = {Tr}_{\bar A} \left(|\psi\rangle\langle\psi|\right)=\frac{I_{2^{|A|}}}{2^{|A|}}$$

This property means that the quantum information is distributed across the full multipartite system equally rather than being localized in a small subsystem.

The AME(6,2) state used in this project admits a graph-state representation. Its corresponding graph contains six vertices and nine edges.

## Expected Success Probability

Expected Success Probability (ESP) is an estimate of the probability that a circuit is executed successfully under a simplified model.

The modified ESP used in this project is

$$ESP =\left(\prod_i F_i\right)e^{-t/T_2}$$

where:

- $F_i$: the fidelity of gate $i$
- $t$  : total circuit duration
- $T_2$: the coherence time

The model contains two sources of degradation:

1. Gate errors: every additional gate contributes another fidelity factor smaller than one. it leads to lower ESP values.

2. Decoherence: longer circuit duration reduces ESP through the decoherence factor $e^{-t/T_2}$

## Hardware parameters

The parameters of physical device are assumed as follows:

| Parameter | Value |
|---|---:|
| Single-qubit fidelity | 0.9999 |
| Two-qubit fidelity | 0.999 |
| Single-qubit duration | 100 ns |
| Two-qubit duration | 150 ns |
| Coherence time $T_2$ | 20 μs |

These values are simplified hardware assumptions inspired by the parameter model used in the reference paper.

## Circuit timing models

Two timing models are compared.

### Sequential model

All gates are assumed to execute one after another:

$$t_{\mathrm{seq}}=n_H t_H + n_{CZ}t_{CZ}$$

where: 

* $n_H$ : the number of Hadamard gates
* $t_H$: single-qubit duration
* $n_{CZ}$: the number of CZ gates
* $t_{CZ}$: two-qubit duration

### Scheduled model

All Hadamard gates are assumed to execute in one parallel layer, while CZ gates are grouped into layers. Two CZ gates may appear in the same layer only if they act on disjoint sets of qubits.

The scheduled duration is

$$t_{\mathrm{sched}}=t_H + d_{CZ}t_{CZ}$$

where $d_{CZ}$ is the number of CZ layers

## Comparing graphs

The following six-qubit graphs are compared:

- path graph $P_6$,
- cycle graph $C_6$,
- star graph $S_6$,
- complete graph $K_6$,
- $2\times3$ grid graph,
- AME(6,2) graph.

At the end of the experiments, the following results are obtained: 

| Graph | Vertices | Edges | Max degree | Diameter | CZ depth | Sequential time (μs) | Scheduled time (μs) | Sequential ESP | Scheduled ESP |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Path | 6 | 5 | 2 | 5 | 2 | 1.350 | 0.400 | 0.929506 | 0.974722 |
| Cycle | 6 | 6 | 2 | 3 | 2 | 1.500 | 0.400 | 0.921638 | 0.973748 |
| Star | 6 | 5 | 5 | 2 | 5 | 1.350 | 0.850 | 0.929506 | 0.953036 |
| Complete | 6 | 15 | 5 | 1 | 7 | 2.850 | 1.150 | 0.853758 | 0.929501 |
| Grid $2\times3$ | 6 | 7 | 3 | 3 | 3 | 1.650 | 0.550 | 0.913837 | 0.965505 |
| AME(6,2) | 6 | 9 | 3 | 2 | 4 | 1.950 | 0.700 | 0.898432 | 0.956376 |

## Discussion

Under the sequential model, ESP decreases mainly with the number of edges because every graph edge introduces one additional CZ gate.

The complete graph has the lowest sequential ESP because it contains 15 edges and therefore requires the largest number of two-qubit gates.

However, edge count alone does not determine the scheduled ESP.

The path and star graphs both contain five edges and therefore have the same sequential ESP. Their scheduled ESP values differ because their CZ depths are different:

- path: CZ depth 2,
- star: CZ depth 5.

The star graph cannot exploit CZ parallelism because all edges share the central vertex.

The path graph contains several disjoint edges and can therefore be scheduled using fewer layers.

This shows that graph structure affects circuit execution through two different quantities:

- edge count determines the gate-fidelity penalty,
- edge overlap determines the scheduling and decoherence penalty.

ESP does not say everything about multipartite entanglement. A graph state with a larger ESP is not necessarily more entangled or more useful than a graph state with a lower ESP.

For example, the AME(6,2) graph has a lower ESP than the path graph under the assumed hardware model, but it satisfies a much stronger multipartite-entanglement property.

Therefore, the results should be interpreted as a comparison of preparation cost, not as a ranking of entanglement quality.

## Future work

Possible extensions include:

- comparison under different hardware fidelities,
- noisy circuit simulation,
- reduced-density-matrix calculations,
- verification of $k$-uniformity,
- shuttle-count and routing-overhead analysis,
- comparison of graph and higher-order representations such as simplicial complexes, hypergraphs, combinatorial complexes etc.
