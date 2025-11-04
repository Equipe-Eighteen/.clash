import string
from automata.fa.nfa import NFA
from automata.fa.dfa import DFA
from lib.lexer.tables import KEYWORDS_TABLE, OPERATORS_TABLE, PUNCTUATION_TABLE

def nfa_whitespace_comments() -> NFA:
    states = {"q0"}
    transitions: dict[str, dict[str, set[str]]] = {}
    final_states: set[str] = set()

    # --- Whitespace ---
    ws_chars = [' ', '\t', '\r', '\n']
    states.add("ws")
    for c in ws_chars:
        transitions.setdefault("q0", {}).setdefault(c, set()).add("ws")
        transitions.setdefault("ws", {}).setdefault(c, set()).add("ws")
    final_states.add("ws")

    # --- Line Comment: // ... ---
    states.update(["slash1", "line_comment"])
    transitions.setdefault("q0", {}).setdefault("/", set()).add("slash1")
    transitions.setdefault("slash1", {}).setdefault("/", set()).add("line_comment")

    for c in ((set(map(chr, range(32, 127))) | {'\t', '\r'}) - {'\n'}):
        transitions.setdefault("line_comment", {}).setdefault(c, set()).add("line_comment")

    transitions.setdefault("line_comment", {}).setdefault('\n', set()).add("ws")
    final_states.add("line_comment")

    # --- Line Comment: # ... ---
    # states.add("line_comment")
    # transitions.setdefault("q0", {}).setdefault("#", set()).add("line_comment")

    # for c in ((set(map(chr, range(32, 127))) | {'\t', '\r'}) - {'\n'}):
    #     transitions.setdefault("line_comment", {}).setdefault(c, set()).add("line_comment")

    # transitions.setdefault("line_comment", {}).setdefault('\n', set()).add("ws")
    # final_states.add("line_comment")

    input_symbols = set(map(chr, range(32, 127))) | {'\n', '\t', '\r'}

    return NFA(
        states=states,
        input_symbols=input_symbols,
        transitions=transitions,
        initial_state="q0",
        final_states=final_states
    )

def nfa_keywords() -> NFA:
    states = {"q0"}
    transitions: dict[str, dict[str, set[str]]] = {}
    final_states: set[str] = set()

    for _, kw in enumerate(sorted(KEYWORDS_TABLE.keys())):
        current = "q0"
        for j, char in enumerate(kw):
            next_state = f"q_{kw}_{j+1}"
            states.add(next_state)
            transitions.setdefault(current, {}).setdefault(char, set()).add(next_state)
            current = next_state
        final_states.add(current)

    input_symbols = set(char for kw in KEYWORDS_TABLE.keys() for char in kw)

    return NFA(
        states=states,
        input_symbols=input_symbols,
        transitions=transitions,
        initial_state="q0",
        final_states=final_states
    )

def nfa_operators() -> NFA:
    states = {"q0"}
    transitions: dict[str, dict[str, set[str]]] = {}
    final_states: set[str] = set()
    
    for i, op in enumerate(sorted(OPERATORS_TABLE.keys(), key=lambda x: -len(x))):
        current = "q0"
        for j, char in enumerate(op):
            next_state = f"q_{i}_{j+1}"
            states.add(next_state)
            transitions.setdefault(current, {}).setdefault(char, set()).add(next_state)
            current = next_state
        final_states.add(current)
    
    return NFA(
        states=states,
        input_symbols=set(char for op in OPERATORS_TABLE.keys() for char in op),
        transitions=transitions,
        initial_state="q0",
        final_states=final_states
    )

def nfa_punctuation() -> NFA:
    states = {"q0"}
    transitions: dict[str, dict[str, set[str]]] = {}
    final_states: set[str] = set()
    
    for i, p in enumerate(PUNCTUATION_TABLE.keys()):
        current = "q0"
        next_state = f"q_{i}_1"
        states.add(next_state)
        transitions.setdefault(current, {}).setdefault(p, set()).add(next_state)
        final_states.add(next_state)
    
    return NFA(
        states=states,
        input_symbols=set(PUNCTUATION_TABLE.keys()),
        transitions=transitions,
        initial_state="q0",
        final_states=final_states
    )


def nfa_literals() -> NFA:
    letters: str = string.ascii_letters + "_"
    digits: str = string.digits

    states = {"q0"}
    transitions: dict[str, dict[str, set[str]]] = {}
    final_states: set[str] = set()
    
    # --- Identifiers: [a-zA-Z_][a-zA-Z0-9_]* ---
    states.add("id1")
    for c in letters:
        transitions.setdefault("q0", {}).setdefault(c, set()).add("id1")
        transitions.setdefault("id1", {}).setdefault(c, set()).add("id1")
    for c in digits:
        transitions.setdefault("id1", {}).setdefault(c, set()).add("id1")
    final_states.add("id1")
    
    # --- Integers and Floats ---
    states.add("int")
    for c in digits:
        transitions.setdefault("q0", {}).setdefault(c, set()).add("int")
        transitions.setdefault("int", {}).setdefault(c, set()).add("int")
    
    # float
    states.add("dot")
    states.add("frac")
    transitions.setdefault("int", {}).setdefault(".", set()).add("dot")
    for c in digits:
        transitions.setdefault("dot", {}).setdefault(c, set()).add("frac")
        transitions.setdefault("frac", {}).setdefault(c, set()).add("frac")
    final_states.add("int")
    final_states.add("frac")
    
    # --- Strings ---
    states.add("str_start")
    states.add("str_body")
    states.add("str_end")
    transitions.setdefault("q0", {}).setdefault('"', set()).add("str_start")
    
    string_body_chars = set(map(chr, range(32, 127))) - {'"'}

    for c in string_body_chars:
        transitions.setdefault("str_start", {}).setdefault(c, set()).add("str_body")
        transitions.setdefault("str_body", {}).setdefault(c, set()).add("str_body")

    transitions.setdefault("str_start", {}).setdefault('"', set()).add("str_end")
    transitions.setdefault("str_body", {}).setdefault('"', set()).add("str_end")

    final_states.add("str_end")
    
    input_symbols = set(letters) | set(digits) | set(map(chr, range(32, 127))) | {'"', '.'}

    return NFA(
        states=states,
        input_symbols=input_symbols,
        transitions=transitions,
        initial_state="q0",
        final_states=final_states
    )

def nfa_final() -> NFA:
    nfas = [
        nfa_whitespace_comments(),
        nfa_keywords(),
        nfa_operators(),
        nfa_punctuation(),
        nfa_literals(),
    ]

    states = {"q_init"}
    transitions: dict[str, dict[str, set[str]]] = {}
    final_states: set[str] = set()
    
    for idx, nfa in enumerate(nfas):
        state_map = {s: f"{s}_{idx}" for s in nfa.states}
        
        states.update(state_map.values())
        
        for s, trans in nfa.transitions.items():
            for symbol, targets in trans.items():
                transitions.setdefault(state_map[s], {}).setdefault(symbol, set()).update(
                    state_map[t] for t in targets
                )
        
        transitions.setdefault("q_init", {}).setdefault("", set()).add(state_map[nfa.initial_state])
        
        final_states.update(state_map[s] for s in nfa.final_states)
    
    input_symbols: set[str] = set[str]().union(*(nfa.input_symbols for nfa in nfas))
    
    return NFA(
        states=states,
        input_symbols=input_symbols,
        transitions=transitions,
        initial_state="q_init",
        final_states=final_states
    )

nfa = nfa_final()
dfa = DFA.from_nfa(nfa)
