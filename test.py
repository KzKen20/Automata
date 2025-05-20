import streamlit as st
import time
from graphviz import Digraph
from collections import defaultdict
import re
import base64

# --- Define DFA ---
dfa = {
    'states': {
        'q0', 'q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'q7',
        'q8', 'q9', 'q10', 'q11', 'q12', 'q13', 'q14',
        'q15', 'q16', 'q17', 'q18', 'q19', 'q20', 'q21','q22',
        'q23', 'q24', 'q25'
    },
    'alphabet': {'0', '1'},
    'start_state': 'q0',
    'accept_states': {'q23','q24'},
    'transitions': {
        ('q0', '0'): 'q1',      # Component 1: 1*
        ('q0', '1'): 'q0',  
        ('q1', '0'): 'q2',  
        ('q1', '1'): 'q1',
        ('q2', '0'): 'q3',  
        ('q2', '1'): 'q4',  
        ('q3', '0'): 'q5',  
        ('q4', '1'): 'q5',  
        ('q4', '0'): 'q3',  
        ('q5', '1'): 'q6',  
        ('q5', '0'): 'q7',  
        ('q6', '0'): 'q8', 
        ('q8', '1'): 'q6',  
        ('q8', '0'): 'q12',  
        ('q12', '0'): 'q13',   
        ('q13', '1'): 'q19',  
        ('q13', '0'): 'q14',  
        ('q6', '1'): 'q10',  
        ('q10', '0'): 'q13',  
        ('q10', '1'): 'q14',  
        ('q7', '1'): 'q9',  
        ('q9', '0'): 'q7',  
        ('q7', '0'): 'q11',  
        ('q11', '0'): 'q14',  
        ('q9', '1'): 'q15',  
        ('q15', '1'): 'q17',
        ('q15', '0'): 'q16', 
        ('q16', '0'): 'q15',    
        ('q14', '1'): 'q17', 
        ('q14', '0'): 'q18', 
        ('q17', '0'): 'q19',     
        ('q17', '1'): 'q19',    
        ('q18', '1'): 'q19',  
        ('q18', '0'): 'q20',  
        ('q20', '1'): 'q19', 
        ('q20', '0'): 'q21', 
        ('q21', '1'): 'q19', 
        ('q21', '0'): 'q20', 
        ('q19', '1'): 'q22',
        ('q19', '0'): 'q19',
        ('q22', '0'): 'q22',
        ('q22', '1'): 'q23',
        ('q23', '0'): 'q23',
        ('q23', '1'): 'q24',
        ('q24', '1'): 'q23',
        ('q24', '0'): 'q25',
        ('q25', '0'): 'q24',
        ('q25', '1'): 'q23'





        
    }
}

dfa2 = {
    'states': {'q0', 'q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'q7', 'q8', 'q9', 'q10','q11','q12','q13','q14','q15','q16','q17','q18','q19','q20','q21','q22','T1','T2','T3'},
    'alphabet': {'a', 'b'},
    'start_state': 'q0',
    'accept_states': {'q21','q22'},
    'transitions': {
        ('q0', 'a'): 'q1',
        ('q0', 'b'): 'q2',
        ('q1', 'a'): 'q3',
        ('q2', 'b'): 'q3',

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
    # Add more if needed
}


# --- Simulate DFA ---
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

# --- Draw DFA Using Graphviz ---
def draw_dfa(dfa, current_state=None, visited=None):
    if visited is None:
        visited = set()
    dot = Digraph(strict=True)

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
            dot.node(state, label, color='orange', style='filled')
        elif state in visited:
            dot.node(state, label, color='lightblue', style='filled')
        elif state in dfa['accept_states']:
            dot.node(state, label, color='green', style='filled')
        else:
            dot.node(state, label, color='gray')

    # Group transitions
    transition_map = defaultdict(list)
    for (src, sym), dst in dfa['transitions'].items():
        transition_map[(src, dst)].append(sym)

    for (src, dst), symbols in transition_map.items():
        label = ','.join(sorted(symbols))
        dot.edge(src, dst, label=label)

    return dot

# Regex Checker for number 1
def regex_checker1(input_string):
    
    pattern = re.compile(
        r'^(1*01*01*)'                              # Component 1: 1*01*01*
        r'(11|00)'                                  # Component 2: (11+00)
        r'(10|01)*'                                 # Component 3: (10+01)*
        r'(1|0)'                                    # Component 4: (1 + 0)
        r'(11|00)'                                  # Component 5: (11 + 00)
        r'(1|0|11|00|101|111|000)'                  # Component 6: (1+0+11+00+101+111+000)
        r'(11|00)*'                                 # Component 7: (11+00)*
        r'(10*10*1)'                                # Component 8: (10*10*1)
        r'(11|00)*$'                                # Component 9: (11+00)*
    )


    if pattern.match(input_string):
        return True, "✅ Input string matches the regex."
    else:
        return False, "❌ Input string does not match the regex."

def regex_checker2(input_string):
    
    pattern2 = re.compile(
    r'^(aa|bb)'                   # Component 1: (aa + bb)
    r'(aba|bab|bbb)'              # Component 2: (aba + bab + bbb)
    r'(aa|bb)*'                   # Component 3: (aa + bb)*
    r'(ab*ab*a)'                  # Component 4: (ab*ab*a)
    r'(ab*ab*a)*'                 # Component 5: (ab*ab*a)*
    r'(bbb|aaa)'                  # Component 6: (bbb + aaa)
    r'(a|b)*$'                    # Component 7: (a + b)*
)


    if pattern2.match(input_string):
        return True, "✅ Input string matches the regex."
    else:
        return False, "❌ Input string does not match the regex."

# --- Streamlit UI ---
st.markdown("""
    <style>
            
         html, body, [class*="css"]  {
        font-size: 25px !important;
    }   
        .main {
            padding-left: 32px;
            padding-right: 32px;
        }
        .block-container {
            padding-top: 32px;
            padding-bottom: 32px;
            max-width: 1440px;
        }
            
        
    </style>
""", unsafe_allow_html=True)

st.title("DFA String Simulator")


# DFA description
st.markdown(r"""
Number 1: (1\*01\*01\*)(11|00)(10|01)\*(1|0)(11|00)(1|0|11|00|101|111|000)(11|00)\*(10\*10\*1)(11|00)\*
""")

# --- First DFA simulation ---
input_string1 = st.text_input("Input string for Number 1:")
placeholder1 = st.empty()
placeholder1.graphviz_chart(draw_dfa(dfa), use_container_width=False)

regexChecker1, simulate_button1, showCFG1, showPDA1 = st.columns(4, vertical_alignment="bottom")


checkerClicked1= regexChecker1.button("Check Regex for Number 1",use_container_width=True)

simulateClicked1 = simulate_button1.button("Simulate DFA for Number 1",use_container_width=True)

clickedCFG1 = showCFG1.button("Show CFG for Number 1",use_container_width=True)

clickedPDA1 = showPDA1.button("Show PDA for Number 1",use_container_width=True)

imagePDA1 = "PDA_1.png"



if "show_pda" not in st.session_state:
    st.session_state.show_pda = False

if clickedPDA1:
    st.session_state.show_pda = not st.session_state.show_pda  

if st.session_state.show_pda:
    # Read and encode image
    with open(imagePDA1, "rb") as img_file:
        img_base64 = base64.b64encode(img_file.read()).decode()

    st.markdown(f"""
    <div style="height:500px; width:100%; overflow:auto; border:1px solid #ccc; padding: 5px">
        <img src="data:image/png;base64,{img_base64}" style="width:100%" />
        <p style="text-align:center; margin-top:5px;">PDA for Number 1</p>
    </div>
    """, unsafe_allow_html=True)

if "show_cfg" not in st.session_state:
    st.session_state.show_cfg = False

if clickedCFG1:
    st.session_state.show_cfg = not st.session_state.show_cfg  


if st.session_state.show_cfg:
    st.info("CFG for Number 1:")
    st.code('''

S → ABCDEFGXYZ
A → H0H0H
H → 1H | Ω
B → 11 | 00 
C → 10 | 01 
D → 10D|  01D | Ω 
E → 1 | 0 
F → 11 | 00 
G → 1 | 011 | 00 | 101 | 111 | 000 
X → 11X | 00X | Ω 
Y → 1J1J1
J → OJ | Ω 
Z → 11Z | 00Z | Ω 
    ''')



if checkerClicked1:
    is_valid, message = regex_checker1(input_string1)
    if is_valid:
        st.success(message)
    else:
        st.error(message)

if simulateClicked1:
    path1 = simulate_dfa(dfa, input_string1)
    visited1 = set()

    for state in path1:
        if state is None:
            break
        visited1.add(state)
        dot = draw_dfa(dfa, current_state=state, visited=visited1)
        placeholder1.graphviz_chart(dot)
        time.sleep(0.8)

    final_state1 = path1[-1] if path1[-1] is not None else path1[-2]
    dot = draw_dfa(dfa, current_state=final_state1, visited=visited1)
    placeholder1.graphviz_chart(dot, use_container_width=True)

    if final_state1 in dfa['accept_states']:
        st.success("✅ Input 1 accepted by the DFA.")
    else:
        st.error("❌ Input 1 rejected by the DFA.")

# --- Second DFA simulation ---
st.markdown(r"""
Number 2: (aa+bb)(aba+bab+bbb)(aa+bb)\*(ab\*ab\*a)(ab\*ab\*a)\*(bbb+aaa)(a+b)\*
""")
input_string2 = st.text_input("Input string for Number 2:")
placeholder2 = st.empty()
placeholder2.graphviz_chart(draw_dfa(dfa2), use_container_width=False)


regexChecker2, simulate_button2, showCFG2, showPDA2 = st.columns(4, vertical_alignment="bottom")


checkerClicked2= regexChecker2.button("Check Regex for Number 2",use_container_width=True)

simulateClicked2 = simulate_button2.button("Simulate DFA for Number 2",use_container_width=True)

clickedCFG2 = showCFG2.button("Show CFG for Number 2",use_container_width=True)

clickedPDA2 = showPDA2.button("Show PDA for Number 2",use_container_width=True)

imagePDA1 = "PDA_2.png"



if "show_pda2" not in st.session_state:
    st.session_state.show_pda2 = False

if clickedPDA2:
    st.session_state.show_pda2 = not st.session_state.show_pda2  

if st.session_state.show_pda2:
    # Read and encode image
    with open(imagePDA1, "rb") as img_file:
        img_base64 = base64.b64encode(img_file.read()).decode()

    st.markdown(f"""
    <div style="height:500px; width:100%; overflow:auto; border:1px solid #ccc; padding: 5px">
        <img src="data:image/png;base64,{img_base64}" style="width:100%" />
        <p style="text-align:center; margin-top:5px;">PDA for Number 2</p>
    </div>
    """, unsafe_allow_html=True)

if "show_cfg2" not in st.session_state:
    st.session_state.show_cfg2 = False

if clickedCFG2:
    st.session_state.show_cfg2 = not st.session_state.show_cfg2  


if st.session_state.show_cfg2:
    st.info("CFG for Number 2:")
    st.code('''

S → ABCDEFGXYZ
A  → a a | b b
B  → a b a | b a b | b b b
C  → aC | bC | Ω  
D  → a a | b b
E  → a a E | b b E | Ω
F →  aGaGa
G →  bG | Ω
X → aHH | aHH | a | Ω
H → bHH |  Ω
Y → bbb | aaa
Z  → aZ | bZ | Ω
    ''')




if checkerClicked2:
    is_valid, message = regex_checker2(input_string2)
    if is_valid:
        st.success(message)
    else:
        st.error(message)

if simulateClicked2:
    path2 = simulate_dfa(dfa2, input_string2)
    visited2 = set()

    for state in path2:
        if state is None:
            break
        visited2.add(state)
        dot = draw_dfa(dfa2, current_state=state, visited=visited2)
        placeholder2.graphviz_chart(dot)
        time.sleep(0.8)

    final_state2 = path2[-1] if path2[-1] is not None else path2[-2]
    dot = draw_dfa(dfa2, current_state=final_state2, visited=visited2)
    placeholder2.graphviz_chart(dot, use_container_width=True)

    if final_state2 in dfa2['accept_states']:
        st.success("✅ Input 2 accepted by DFA.")
    else:
        st.error("❌ Input 2 rejected by DFA.")
