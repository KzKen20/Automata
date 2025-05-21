import streamlit as st
import time
from graphviz import Digraph
from collections import defaultdict
import re
import base64

# --- Define DFA --- (existing code remains the same)
# ... (keep all your DFA definitions and functions)

# --- Streamlit UI with enhanced background styling ---
st.markdown("""
    <style>
        /* Base Styling */
        html, body, [class*="css"] {
            font-size: 22px !important;
            font-family: 'Roboto', sans-serif;
        }
        
        /* Enhanced Background Styling */
        .main {
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            background-attachment: fixed;
            padding-left: 32px;
            padding-right: 32px;
        }
        
        .block-container {
            padding-top: 32px;
            padding-bottom: 32px;
            max-width: 1440px;
        }
        
        /* Headers */
        h1 {
            color: #1e3a8a;
            font-weight: 700;
            margin-bottom: 30px;
            padding: 15px 20px;
            border-radius: 10px;
            background: linear-gradient(to right, #1e3a8a, #3b82f6);
            color: white;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            text-align: center;
        }
        
        h2, h3 {
            color: #1e3a8a;
            font-weight: 600;
            margin-bottom: 15px;
        }
        
        /* Section styling */
        .section {
            background: white;
            border-radius: 12px;
            padding: 25px;
            box-shadow: 0 6px 18px rgba(0, 0, 0, 0.1);
            margin-bottom: 30px;
            border: 1px solid rgba(255, 255, 255, 0.3);
            background-image: linear-gradient(120deg, rgba(255,255,255,0.8) 0%, rgba(245,247,250,0.8) 100%);
        }
        
        /* Input fields */
        .stTextInput > div > div > input {
            border-radius: 8px;
            border: 2px solid #e2e8f0;
            padding: 10px 15px;
            background-color: rgba(255, 255, 255, 0.9);
            transition: all 0.3s ease;
        }
        
        .stTextInput > div > div > input:focus {
            border-color: #3b82f6;
            box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.2);
        }
        
        /* Buttons */
        .stButton > button {
            border-radius: 8px;
            font-weight: 600;
            background: linear-gradient(to right, #1e40af, #3b82f6);
            color: white;
            border: none;
            padding: 10px 20px;
            transition: all 0.3s ease;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        
        .stButton > button:hover {
            background: linear-gradient(to right, #1e4bd8, #60a5fa);
            box-shadow: 0 6px 10px rgba(0, 0, 0, 0.15);
            transform: translateY(-2px);
        }
        
        /* Success/Error messages */
        .stSuccess {
            background-color: #d1fae5;
            color: #065f46;
            padding: 16px;
            border-radius: 8px;
            border-left: 5px solid #10b981;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        }
        
        .stError {
            background-color: #fee2e2;
            color: #991b1b;
            padding: 16px;
            border-radius: 8px;
            border-left: 5px solid #ef4444;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        }
        
        /* Code blocks */
        .stCodeBlock {
            background-color: #f8fafc;
            border-radius: 8px;
            border: 1px solid #e2e8f0;
            box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.05);
        }
        
        /* Graphs and visualizations */
        .graphviz-chart {
            border: 1px solid #e2e8f0;
            border-radius: 10px;
            padding: 15px;
            background: rgba(255, 255, 255, 0.8);
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
        }
        
        /* Regex displays */
        .regex-display {
            font-family: 'Courier New', monospace;
            background: linear-gradient(to right, #f1f5f9, #e2e8f0);
            padding: 15px;
            border-radius: 8px;
            margin: 10px 0;
            font-weight: 500;
            border-left: 5px solid #3b82f6;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
        }
        
        /* Image containers */
        .img-container {
            background: rgba(255, 255, 255, 0.9);
            border: 1px solid #e2e8f0;
            border-radius: 10px;
            padding: 15px;
            margin: 15px 0;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05);
        }
        
        /* Additional styles for the background texture */
        .main::before {
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-image: url("data:image/svg+xml,%3Csvg width='100' height='100' viewBox='0 0 100 100' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M11 18c3.866 0 7-3.134 7-7s-3.134-7-7-7-7 3.134-7 7 3.134 7 7 7zm48 25c3.866 0 7-3.134 7-7s-3.134-7-7-7-7 3.134-7 7 3.134 7 7 7zm-43-7c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zm63 31c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zM34 90c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zm56-76c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zM12 86c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm28-65c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm23-11c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm-6 60c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm29 22c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zM32 63c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm57-13c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm-9-21c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM60 91c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM35 41c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM12 60c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2z' fill='%231e3a8a' fill-opacity='0.03' fill-rule='evenodd'/%3E%3C/svg%3E");
            pointer-events: none;
            z-index: -1;
        }
    </style>
""", unsafe_allow_html=True)

st.title("DFA String Simulator")

# Use CSS classes with HTML wrappers for better styling
st.markdown('<div class="section">', unsafe_allow_html=True)
st.markdown('<h2>DFA #1</h2>', unsafe_allow_html=True)
st.markdown('<div class="regex-display">Number 1: (1*01*01*)(11|00)(10|01)*(1|0)(11|00)(1|0|11|00|101|111|000)(11|00)*(10*10*1)(11|00)*</div>', unsafe_allow_html=True)

# --- First DFA simulation ---
input_string1 = st.text_input("Input string for Number 1:")
placeholder1 = st.empty()
placeholder1.markdown('<div class="graphviz-chart">', unsafe_allow_html=True)
placeholder1.graphviz_chart(draw_dfa(dfa), use_container_width=False)
placeholder1.markdown('</div>', unsafe_allow_html=True)

regexChecker1, simulate_button1, showCFG1, showPDA1 = st.columns(4, vertical_alignment="bottom")

checkerClicked1= regexChecker1.button("Check Regex", use_container_width=True)
simulateClicked1 = simulate_button1.button("Simulate DFA", use_container_width=True)
clickedCFG1 = showCFG1.button("Show CFG", use_container_width=True)
clickedPDA1 = showPDA1.button("Show PDA", use_container_width=True)

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
    <div class="img-container" style="height:500px; width:100%; overflow:auto; padding: 10px">
        <img src="data:image/png;base64,{img_base64}" style="width:100%" />
        <p style="text-align:center; margin-top:10px; font-weight:500;">PDA for Number 1</p>
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
        placeholder1.markdown('<div class="graphviz-chart">', unsafe_allow_html=True)
        placeholder1.graphviz_chart(dot)
        placeholder1.markdown('</div>', unsafe_allow_html=True)
        time.sleep(0.8)

    final_state1 = path1[-1] if path1[-1] is not None else path1[-2]
    dot = draw_dfa(dfa, current_state=final_state1, visited=visited1)
    placeholder1.markdown('<div class="graphviz-chart">', unsafe_allow_html=True)
    placeholder1.graphviz_chart(dot, use_container_width=True)
    placeholder1.markdown('</div>', unsafe_allow_html=True)

    if final_state1 in dfa['accept_states']:
        st.success("✅ Input 1 accepted by the DFA.")
    else:
        st.error("❌ Input 1 rejected by the DFA.")

st.markdown('</div>', unsafe_allow_html=True)  # Close the section div

# Start DFA 2 section
st.markdown('<div class="section">', unsafe_allow_html=True)
st.markdown('<h2>DFA #2</h2>', unsafe_allow_html=True)
st.markdown('<div class="regex-display">Number 2: (aa+bb)(aba+bab+bbb)(aa+bb)*(ab*ab*a)(ab*ab*a)*(bbb+aaa)(a+b)*</div>', unsafe_allow_html=True)

input_string2 = st.text_input("Input string for Number 2:")
placeholder2 = st.empty()
placeholder2.markdown('<div class="graphviz-chart">', unsafe_allow_html=True)
placeholder2.graphviz_chart(draw_dfa(dfa2), use_container_width=False)
placeholder2.markdown('</div>', unsafe_allow_html=True)

regexChecker2, simulate_button2, showCFG2, showPDA2 = st.columns(4, vertical_alignment="bottom")

checkerClicked2= regexChecker2.button("Check Regex", use_container_width=True)
simulateClicked2 = simulate_button2.button("Simulate DFA", use_container_width=True)
clickedCFG2 = showCFG2.button("Show CFG", use_container_width=True)
clickedPDA2 = showPDA2.button("Show PDA", use_container_width=True)

imagePDA2 = "PDA_2.png"

if "show_pda2" not in st.session_state:
    st.session_state.show_pda2 = False

if clickedPDA2:
    st.session_state.show_pda2 = not st.session_state.show_pda2  

if st.session_state.show_pda2:
    # Read and encode image
    with open(imagePDA2, "rb") as img_file:
        img_base64 = base64.b64encode(img_file.read()).decode()

    st.markdown(f"""
    <div class="img-container" style="height:500px; width:100%; overflow:auto; padding: 10px">
        <img src="data:image/png;base64,{img_base64}" style="width:100%" />
        <p style="text-align:center; margin-top:10px; font-weight:500;">PDA for Number 2</p>
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
        placeholder2.markdown('<div class="graphviz-chart">', unsafe_allow_html=True)
        placeholder2.graphviz_chart(dot)
        placeholder2.markdown('</div>', unsafe_allow_html=True)
        time.sleep(0.8)

    final_state2 = path2[-1] if path2[-1] is not None else path2[-2]
    dot = draw_dfa(dfa2, current_state=final_state2, visited=visited2)
    placeholder2.markdown('<div class="graphviz-chart">', unsafe_allow_html=True)
    placeholder2.graphviz_chart(dot, use_container_width=True)
    placeholder2.markdown('</div>', unsafe_allow_html=True)

    if final_state2 in dfa2['accept_states']:
        st.success("✅ Input 2 accepted by DFA.")
    else:
        st.error("❌ Input 2 rejected by DFA.")

st.markdown('</div>', unsafe_allow_html=True)  # Close the section div

# Optional: Add footer
st.markdown("""
<div style="text-align: center; margin-top: 30px; padding: 20px; color: #64748b; font-size: 0.8em;">
    DFA String Simulator © 2025
</div>
""", unsafe_allow_html=True)