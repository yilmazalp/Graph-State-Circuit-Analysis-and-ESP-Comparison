def pauli_weight(pauli_string: str) -> int:
    valid_symbols = {"I", "X", "Y", "Z"}

    if not pauli_string:
        raise ValueError("The Pauli string cannot be empty.")

    if any(symbol not in valid_symbols for symbol in pauli_string):
        raise ValueError("A Pauli string may contain only I, X, Y, and Z.")

    return sum(symbol != "I" for symbol in pauli_string)

def minimum_pauli_weight(pauli_string: list[str]) -> int:
    return min(pauli_weight(_pauli_) for _pauli_ in pauli_string)