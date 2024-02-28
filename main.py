from automata.fa.dfa import DFA

dfa = DFA(
    states={'q0', 'q1', 'q2', 'q3', 'q4', 'qe'},
    input_symbols={'r', 'o', 'm', 'n', 'R', 'O', 'M', 'N'},
    transitions={
        'q0': {'r': 'q1', 'R': 'q1', 'o': 'qe', 'm': 'qe', 'n': 'qe', 'O': 'qe', 'M': 'qe', 'N': 'qe'},
        'q1': {'o': 'q2', 'O': 'q2', 'r': 'q1', 'R': 'q1', 'm': 'qe', 'n': 'qe', 'M': 'qe', 'N': 'qe'},
        'q2': {'m': 'q3', 'M': 'q3', 'o': 'q2', 'O': 'q2', 'r': 'qe', 'n': 'qe', 'R': 'qe', 'N': 'qe'},
        'q3': {'n': 'q4', 'N': 'q4', 'm': 'qe', 'M': 'qe', 'r': 'qe', 'o': 'qe', 'R': 'qe', 'O': 'qe'},
        'q4': {'n': 'qe', 'N': 'qe', 'r': 'qe', 'o': 'qe', 'm': 'qe', 'R': 'qe', 'O': 'qe', 'M': 'qe'},
        'qe': {'r': 'qe', 'o': 'qe', 'm': 'qe', 'n': 'qe', 'R': 'qe', 'O': 'qe', 'M': 'qe', 'N': 'qe'}
    },
    initial_state='q0',
    final_states={'q1', 'q2', 'q3', 'q4'}
)

def es_valida(cadena):
    try:
        dfa.read_input(cadena)
        return True
    except:
        return False