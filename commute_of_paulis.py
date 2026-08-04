def commute_paulis(pauli_a: str, pauli_b: str) -> bool:
    symbols = {"X", "Z", "Y"}

    if not pauli_a or not pauli_b:
        raise ValueError("The Pauli string cannot be empty.")

    if len(pauli_a) != len(pauli_b):
        raise ValueError("The Pauli strings must have the same length.")

    commute_number = sum(symbol_a != symbol_b and symbol_a in symbols and symbol_b in symbols
                         for symbol_a, symbol_b in zip(pauli_a, pauli_b))

    return commute_number % 2 == 0

stabilizers = [
    "XZIIZZ",
    "ZXZZII",
    "IZXZIZ",
    "IZZXZI",
    "ZIIZXZ",
    "ZIZIZX",
]

for i in range(0, len(stabilizers)):
    for j in range(i+1, len(stabilizers)):
        if commute_paulis(stabilizers[i], stabilizers[j]):
            print(f"{stabilizers[i]} commutes with {stabilizers[j]}")
        else:
            print(f"{stabilizers[i]} anticommutes with {stabilizers[j]}")

