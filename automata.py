import streamlit as st
import time
from graphviz import Digraph
from collections import defaultdict

# --- Define DFA ---
dfa = {
    'states': {'q0', 'q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'q7', 'q8', 'q9', 'q10','q11','q12','q13','q14','q15','q16','q17','q18','q19','q20','q21','q22','T1','T2','T3'},
    'alphabet': {'a', 'b'},
    'start_state': 'q0',
    'accept_states': {'q21','q22'},
    'transitions': {
        ('q0', 'a'): 'q1',
        ('q0', 'b'): 'q2',
        ('q1', 'a'): 'q3',
        ('q2', 'b'): 'q3',
        ('q0', 'a'): 'q1',
        ('q3', 'a'): 'q4',
        ('q3', 'b'): 'q5',
        ('q4', 'b'): 'q6',
        ('q5', 'a'): 'q7',
        ('q5', 'b'): 'q7',
        ('q6', 'b'): 'q7',
        ('q7', 'a'): 'q6',
        ('q6', 'a'): 'q8',
        ('q7', 'b'): 'q8',
        ('q8', 'a'): 'q9',
        ('q8', 'b'): 'q10',
        ('q9', 'b'): 'q10',
        ('q10', 'a'): 'q9',
        ('q9', 'a'): 'q11',
        ('q10', 'b'): 'q11',
        ('q11', 'b'): 'q10',
        ('q11', 'a'): 'q12',
        ('q12', 'b'): 'q12',
        ('q12', 'a'): 'q13',
        ('q13', 'b'): 'q13',
        ('q13', 'a'): 'q14',
        ('q14', 'a'): 'q15',
        ('q14', 'a'): 'q15',
        ('q15', 'b'): 'q16',
        ('q15', 'a'): 'q18',
        ('q18', 'b'): 'q19',
        ('q19', 'b'): 'q19',
        ('q19', 'a'): 'q14',
        ('q16', 'a'): 'q13',
        ('q16', 'b'): 'q16',
        ('q14', 'b'): 'q17',
        ('q17', 'b'): 'q20',
        ('q17', 'a'): 'q12',
        ('q20', 'a'): 'q12',
        ('q20', 'b'): 'q21',
        ('q18', 'a'): 'q22',
        ('q22', 'a'): 'q22',
        ('q22', 'b'): 'q22',
        ('q21', 'a'): 'q21',
        ('q21', 'b'): 'q21',
        ('q1', 'b'): 'T1',
        ('q2', 'a'): 'T2',
        ('q4', 'a'): 'T3',


        

    }
}


state_labels = {
    'T1': 'T',
    'T2': 'T',
    'T3': 'T',
    'T4': 'T',
    'T5': 'T',
    'T6': 'T',
    'T7': 'T',
    'q23': '+',
    'q24': '+',
    'q25': '+',
    'q0': '-',
    
}

#Simulate DFA 
def simulate_dfa(dfa, input_string):
    current_state = dfa['start_state']
    path = [current_state]

    for symbol in input_string:
        key = (current_state, symbol)
        if key not in dfa['transitions']:
            path.append(None)
            break
        current_state = dfa['transitions'][key]
        path.append(current_state)

    return path

# Draw DFA Using Graphviz 
def draw_dfa(current_state=None, visited=set()):
    dot = Digraph(strict=True)
    
    # Set large display size
    desired_height_px = 3000
    aspect_ratio = 20 / 27
    desired_width_px = desired_height_px * aspect_ratio
    width_in_inches = desired_width_px / 96
    height_in_inches = desired_height_px / 96
    dot.attr(rankdir='LR', size=f'{width_in_inches},{height_in_inches}')

    # Render nodes
    for state in dfa['states']:
        label = state_labels.get(state, state)
        if state == current_state:
            dot.node(state, color='orange', style='filled')
        elif state in visited:
            dot.node(state, color='lightblue', style='filled')
        elif state in dfa['accept_states']:
            dot.node(state, color='green', style='filled')
        else:
            dot.node(state, color='gray')

    # Group transitions with same source and destination
    transition_map = defaultdict(list)
    for (src, sym), dst in dfa['transitions'].items():
        transition_map[(src, dst)].append(sym)

    for (src, dst), symbols in transition_map.items():
        label = ','.join(sorted(symbols))
        dot.edge(src, dst, label=label)

    return dot

# --- Streamlit UI ---
st.title("DFA String Simulator")

st.markdown(
    """
    <style>
    .graphviz-container img {
        width: 2222px !important;
        height: 3000px !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

input_string = st.text_input("Enter input string:")

placeholder = st.empty()
initial_dfa = draw_dfa()
placeholder.graphviz_chart(initial_dfa, use_container_width=False)

st.markdown(r"Number 1: (aa+bb)(aba+bab+bbb)(aa+bb)\*(ab\*ab\*a)(ab\*ab\*a)\*(bbb+aaa)(a+b)\*")

if st.button("Simulate"):
    path = simulate_dfa(dfa, input_string)
    visited = set()

    for i, state in enumerate(path):
        if state is None:
            break
        visited.add(state)
        dot = draw_dfa(current_state=state, visited=visited)
        placeholder.graphviz_chart(dot)
        time.sleep(0.8)

    final_state = path[-1] if path[-1] is not None else path[-2]
    dot = draw_dfa(current_state=state, visited=visited)
    placeholder.graphviz_chart(dot, use_container_width=True)

    if final_state in dfa['accept_states']:
        st.success("✅ Input accepted by the DFA.")
    else:
        st.error("❌ Input rejected by the DFA.")