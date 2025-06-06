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
        ('q12', '1'): 'q13',
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
    'states': {
        'q0', 'q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'q7', 'q8', 'q9', 'q10',
        'q11', 'q12', 'q13', 'q14', 'q15','q16', 'q18', 'q19', 'q20',
        'T1', 'T2', 'T3'
    },
    'alphabet': {'a', 'b'},
    'start_state': 'q0',
    'accept_states': {'q19', 'q20'},
    'transitions': {
        # Component 1: (aa|bb)
        ('q0', 'a'): 'q1',
        ('q0', 'b'): 'q2',
        ('q1', 'b'): 'T1',
        ('q2', 'a'): 'T2',
        ('q1', 'a'): 'q3',
        ('q2', 'b'): 'q3',
        ('q3', 'a'): 'q4',
        ('q4', 'b'): 'q6',
        ('q4', 'a'): 'T3',
        ('q3', 'b'): 'q5',
        ('q5', 'a'): 'q7',
        ('q5', 'b'): 'q7',
        ('q6', 'b'): 'q7',
        ('q7', 'a'): 'q6',
        ('q6', 'a'): 'q8',
        ('q7', 'b'): 'q8',
        ('q8', 'a'): 'q9',
        ('q8', 'b'): 'q10',
        ('q9', 'b'): 'q9',
        
        ('q9', 'a'): 'q11',
        ('q10', 'b'): 'q11',
        ('q11', 'b'): 'q11',
        ('q11', 'a'): 'q12',
        ('q12', 'a'): 'q13',
        ('q13', 'b'): 'q14',
        ('q14', 'b'): 'q14',
        ('q14', 'a'): 'q11',
        ('q12', 'b'): 'q15',
        ('q15', 'a'): 'q12',
        ('q15', 'b'): 'q18',
        ('q18', 'a'): 'q12',
        ('q13', 'a'): 'q16',
        ('q16', 'b'): 'q17',
        ('q17', 'a'): 'q12',

        ('q16', 'a'): 'q19',
        ('q18', 'b'): 'q20',
        ('q19', 'a'): 'q19',
        ('q19', 'b'): 'q19',
        ('q20', 'a'): 'q20',
        ('q20', 'b'): 'q20',





        
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
    'q19': '+',
    'q20': '+',
    
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

# --- Helper function for multi-line input processing ---
def process_multiline_inputs(input_text, regex_checker, dfa, placeholder, simulate=False):
    results = []
    input_lines = [line.strip() for line in input_text.split('\n') if line.strip()]
    for idx, input_str in enumerate(input_lines, 1):
        result = {'input': input_str}
        is_valid, message = regex_checker(input_str)
        result['regex'] = (is_valid, message)
        if simulate:
            path = simulate_dfa(dfa, input_str)
            visited = set()
            for state in path:
                if state is None:
                    break
                visited.add(state)
                dot = draw_dfa(dfa, current_state=state, visited=visited)
                placeholder.graphviz_chart(dot, use_container_width=True)
                time.sleep(0.8)
            final_state = path[-1] if path[-1] is not None else path[-2]
            dot = draw_dfa(dfa, current_state=final_state, visited=visited)
            placeholder.graphviz_chart(dot, use_container_width=True)
            result['dfa'] = (final_state in dfa['accept_states'])
        results.append(result)
    return results

# --- Streamlit UI with completely redesigned interface ---
st.set_page_config(layout="wide", page_title="DFA String Simulator")

st.markdown("""
    <style>
        /* Reset and base styling */
        html, body, [class*="css"] {
            font-family: 'Segoe UI', Arial, sans-serif;
        }
       
            
       
            
         html, body, .stApp {
         background: linear-gradient(135deg, #141e30 0%, #243b55 100%);
            background-attachment: fixed;
            padding: 20% !important;
            margin: 0 !important;
            width: 100% !important;
            max-width: 100% !important;
}
        
        /* Remove default Streamlit container padding */
        .block-container {
            padding: 1rem 1rem 10rem 1rem !important;
            max-width: 1200px !important;
            margin: 0 auto;
        }
        
        /* Hide Streamlit branding */
        #MainMenu, footer, header {
            visibility: hidden;
        }
        
        /* App title and header */
        .app-header {
            background: #4662D7;
            padding: 220px 220px;
            border-radius: 10px;
            color: white;
            margin-bottom: 20px;
            text-align: center;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        
        .app-title {
            color: white;
            font-size: 36px;
            font-weight: 600;
            margin: 30px 0;
            text-align: center;
        }
        
        /* Navigation */
        .nav-container {
            background: rgba(70, 98, 215, 0.9);
            padding: 10px 20px;
            border-radius: 10px;
            margin-bottom: 30px;
        }
        
        .nav-link {
            display: inline-block;
            color: white;
            padding: 8px 16px;
            text-decoration: none;
            border-radius: 5px;
            margin-right: 10px;
            font-weight: 500;
        }
        
        .nav-link.active {
            background: rgba(255, 255, 255, 0.2);
        }
        
        
        

            
            
        
        /* Input styling */
        .stTextInput > div > div > input {
            border-radius: 5px;
            border: 1px solid #E0E0E0;
            padding: 10px;
            font-size: 16px;
        }
        
        /* Textarea styling */
        textarea {
            border-radius: 5px !important;
            border: 1px solid #E0E0E0 !important;
            min-height: 120px !important;
        }
        
        /* Button styling */
        .primary-button {
            background: #0D6EFD;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 50px;
            font-weight: 500;
            cursor: pointer;
            display: inline-block;
            text-align: center;
            margin: 5px;
            min-width: 150px;
        }
        
        .secondary-button {
            background: #6C757D;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 50px;
            font-weight: 500;
            cursor: pointer;
            display: inline-block;
            text-align: center;
            margin: 5px;
            min-width: 120px;
        }
        
        /* Alert box styling */
        .info-box {
            background: #d1ecf1;
            color: #0c5460;
            padding: 15px;
            border-radius: 5px;
            margin: 10px 0;
        }
        
        /* Regex display */
        .regex-display {
            font-family: 'Courier New', monospace;
            background: #f8f9fa;
            padding: 12px;
            border-radius: 5px;
            margin: 10px 0;
            border-left: 4px solid #4662D7;
        }
        
        /* Graphviz chart container */
        .graph-container {
            background: white;
            border-radius: 5px;
            padding: 15px;
            margin: 15px 0;
            overflow: auto;
            max-height: 500px;
            border: 1px solid #E0E0E0;
        }
        
        /* Results section */
        .results-section {
            margin-top: 20px;
        }
        
        /* Success/Error messages */
        .success-message {
            background-color: #d4edda;
            color: #155724;
            padding: 12px;
            border-radius: 5px;
            margin: 10px 0;
        }
        
        .error-message {
            background-color: #f8d7da;
            color: #721c24;
            padding: 12px;
            border-radius: 5px;
            margin: 10px 0;
        }
        
        /* Button container */
        .button-container {
            display: flex;
            justify-content: center;
            margin: 20px 0;
            gap: 10px;
        }
        
        /* Center content */
        .center {
            display: flex;
            justify-content: center;
        }
        
        /* Hide default Streamlit spinner */
        .stSpinner {
            display: none !important;
        }
            
            
    </style>
""", unsafe_allow_html=True)



# Custom navigation and header
st.markdown("""
<div class="nav-container">
    <span class="nav-link active">Automata Theory</span>
    <span class="nav-link">Home</span>
    <span class="nav-link">DFA #1</span>
    <span class="nav-link">DFA #2</span>
</div>
<h1 class="app-title">DFA String Simulator</h1>
""", unsafe_allow_html=True)

# DFA #1 section

st.markdown('<div class="section-header">DFA #1</div>', unsafe_allow_html=True)
st.markdown('<div class="regex-display" style="color: black;">Number 1: (1*01*01*)(11|00)(10|01)*(1|0)(11|00)(1|0|11|00|101|111|000)(11|00)*(10*10*1)(11|00)*</div>', unsafe_allow_html=True)

# Input area
input_string1 = st.text_area("Enter string for DFA #1 analysis:", placeholder="Type or paste a string here to test against DFA #1...", height=100)

# Button container

col1, col2, col3, col4 = st.columns([1,1,1,1])
checkerClicked1 = col1.button("Check Regex", key="check_regex1", use_container_width=True)
simulateClicked1 = col2.button("Simulate DFA", key="simulate_dfa1", use_container_width=True)
clickedCFG1 = col3.button("Show CFG", key="show_cfg1", use_container_width=True)
clickedPDA1 = col4.button("Show PDA", key="show_pda1", use_container_width=True)


# Graph display container

placeholder1 = st.empty()
placeholder1.graphviz_chart(draw_dfa(dfa), use_container_width=True)

# PDA and CFG sections
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
    <div class="graph-container">
        <img src="data:image/png;base64,{img_base64}" style="width:100%" />
        <p style="text-align:center; margin-top:10px; font-weight:500;">PDA for Number 1</p>
    </div>
    """, unsafe_allow_html=True)

if "show_cfg" not in st.session_state:
    st.session_state.show_cfg = False

if clickedCFG1:
    st.session_state.show_cfg = not st.session_state.show_cfg  

if st.session_state.show_cfg:
    st.markdown('<div class="info-box">', unsafe_allow_html=True)
    st.markdown('<strong>CFG for Number 1:</strong>', unsafe_allow_html=True)
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
    st.markdown('</div>', unsafe_allow_html=True)

# Results section
st.markdown('<div class="results-section">', unsafe_allow_html=True)
if checkerClicked1:
    results = process_multiline_inputs(input_string1, regex_checker1, dfa, placeholder1, simulate=False)
    for res in results:
        if res['regex'][0]:
            st.markdown(f'<div class="success-message">[Input: <b>{res["input"]}</b>] {res["regex"][1]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="error-message">[Input: <b>{res["input"]}</b>] {res["regex"][1]}</div>', unsafe_allow_html=True)

if simulateClicked1:
    results = process_multiline_inputs(input_string1, regex_checker1, dfa, placeholder1, simulate=True)
    for res in results:
        if 'dfa' in res:
            if res['dfa']:
                st.markdown(f'<div class="success-message">✅ Input <b>{res["input"]}</b> accepted by DFA #1.</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="error-message">❌ Input <b>{res["input"]}</b> rejected by DFA #1.</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)  # Close results section

st.markdown('</div>', unsafe_allow_html=True)  # Close DFA #1 section

# DFA #2 section

st.markdown('<div class="section-header">DFA #2</div>', unsafe_allow_html=True)
st.markdown('<div class="regex-display" style="color: black;">Number 2: (aa+bb)(aba+bab+bbb)(aa+bb)*(ab*ab*a)(ab*ab*a)*(bbb+aaa)(a+b)*</div>', unsafe_allow_html=True)

# Input area
input_string2 = st.text_area("Enter string for DFA #2 analysis:", placeholder="Type or paste a string here to test against DFA #2...", height=100)

# Button container

col1, col2, col3, col4 = st.columns([1,1,1,1])
checkerClicked2 = col1.button("Check Regex", key="check_regex2", use_container_width=True)
simulateClicked2 = col2.button("Simulate DFA", key="simulate_dfa2", use_container_width=True)
clickedCFG2 = col3.button("Show CFG", key="show_cfg2", use_container_width=True)
clickedPDA2 = col4.button("Show PDA", key="show_pda2", use_container_width=True)


# Graph display container

placeholder2 = st.empty()
placeholder2.graphviz_chart(draw_dfa(dfa2), use_container_width=True)


# PDA and CFG sections

imagePDA2 = "PDA_2.png"

if "show_pda" not in st.session_state:
    st.session_state.show_pda = False

if clickedPDA2:
    st.session_state.show_pda = not st.session_state.show_pda  

if st.session_state.show_pda:
    # Read and encode image
    with open(imagePDA2, "rb") as img_file:
        img_base64 = base64.b64encode(img_file.read()).decode()

    st.markdown(f"""
    <div class="graph-container">
        <img src="data:image/png;base64,{img_base64}" style="width:100%" />
        <p style="text-align:center; margin-top:10px; font-weight:500;">PDA for Number 2</p>
    </div>
    """, unsafe_allow_html=True)

if "show_cfg" not in st.session_state:
    st.session_state.show_cfg = False

if clickedCFG2:
    st.session_state.show_cfg = not st.session_state.show_cfg 

if st.session_state.show_cfg:
    st.markdown('<div class="info-box">', unsafe_allow_html=True)
    st.markdown('<strong>CFG for Number 2:</strong>', unsafe_allow_html=True)
    st.code('''
S → ABCDEFGXYZ
A  → a a | b b
B  → a b a | b a b | b b b
C  → aC | bC | Ω  
D  → a a | b b
E  → a a E | b b E | Ω
F →  aGaGa
G →  bG | Ω
X → aH | aH | a | Ω
H → bH |  Ω
Y → bbb | aaa
Z  → aZ | bZ | Ω
    ''')
    st.markdown('</div>', unsafe_allow_html=True)

# Results section
st.markdown('<div class="results-section">', unsafe_allow_html=True)
if checkerClicked2:
    results = process_multiline_inputs(input_string2, regex_checker2, dfa2, placeholder2, simulate=False)
    for res in results:
        if res['regex'][0]:
            st.markdown(f'<div class="success-message">[Input: <b>{res["input"]}</b>] {res["regex"][1]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="error-message">[Input: <b>{res["input"]}</b>] {res["regex"][1]}</div>', unsafe_allow_html=True)

if simulateClicked2:
    results = process_multiline_inputs(input_string2, regex_checker2, dfa2, placeholder2, simulate=True)
    for res in results:
        if 'dfa' in res:
            if res['dfa']:
                st.markdown(f'<div class="success-message">✅ Input <b>{res["input"]}</b> accepted by DFA #2.</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="error-message">❌ Input <b>{res["input"]}</b> rejected by DFA #2.</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)  # Close results section

st.markdown('</div>', unsafe_allow_html=True)  # Close DFA #2 section

# Example Strings Section
st.markdown('<div class="content-section">', unsafe_allow_html=True)
st.markdown('<div class="section-header">Example Strings</div>', unsafe_allow_html=True)
st.markdown('<p>Click on any example to use it:</p>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown('<strong>Examples for DFA #1:</strong>', unsafe_allow_html=True)
    example1_1 = st.button("Example 1: 10001011001001", key="example1_1")
    example1_2 = st.button("Example 2: 11001010111011", key="example1_2")
    
with col2:
    st.markdown('<strong>Examples for DFA #2:</strong>', unsafe_allow_html=True)
    example2_1 = st.button("Example 1: aababaababaabbbaaaa", key="example2_1")
    example2_2 = st.button("Example 2: bbbabaaaaababbaaa", key="example2_2")

st.markdown('</div>', unsafe_allow_html=True)  # Close example section
