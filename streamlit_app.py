import streamlit as st
from lab02 import show_lab02, show_lab02_part2
from lab03 import show_lab03
from lab04 import show_lab04

# Set page config once
st.set_page_config(page_title="Bayesian DS Labs", layout="wide")

# --- CUSTOM CSS FOR THE PREMIUM WIDGET LOOK ---
st.markdown("""
    <style>
    /* Global Background and Sidebar */
    .stApp { background-color: #fcfcfc; }
    [data-testid="stSidebar"] { background-color: #ffffff; border-right: 1px solid #eee; }
    
    /* REMOVE ALL NATIVE RADIO BUTTONS AND HEADERS */
    div[role="radiogroup"] > label > div:first-child { display: none !important; }
    div[role="radiogroup"] { gap: 0.8rem; }
    
    /* STYLING ITEMS AS CARDS (Matching Screenshot 3:03 AM) */
    div[role="radiogroup"] label {
        background-color: #ffffff;
        border: 1px solid #f0f0f0;
        border-radius: 12px;
        padding: 18px 16px !important;
        cursor: pointer;
        transition: all 0.2s ease-in-out;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
    }
    
    div[role="radiogroup"] label:hover {
        border-color: #e0e0e0;
        background-color: #fafafa;
        transform: translateY(-1px);
    }
    
    /* ACTIVE STATE (Matching Screenshot 3:01 AM) */
    div[role="radiogroup"] label[data-selected="true"] {
        background-color: #f8f9fb !important;
        border-color: #1a73e8 !important;
        box-shadow: 0 4px 12px rgba(26, 115, 232, 0.08);
    }
    
    /* Typography within the Widgets */
    div[role="radiogroup"] label p {
        font-size: 15px !important;
        font-weight: 500 !important;
        color: #3c4043 !important;
    }
    </style>
    """, unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### Laboratory Assignments")
    
    # This is the ONLY selection widget
    selection = st.radio(
        "Navigation",
        ["🏥 Lab 02: Clinical Decisions", "🎲 Lab 03: Random Variables","📈 Lab 04: Predictive Thinking"],
        label_visibility="collapsed"
    )
    

# ROUTING LOGIC
if selection == "🏥 Lab 02: Clinical Decisions":
    show_lab02()
    st.divider()
    show_lab02_part2()
elif selection == "🎲 Lab 03: Random Variables":
    show_lab03()
elif selection == "📈 Lab 04: Predictive Thinking":
    # Lab 04 covers priors as pseudo-data and posterior predictive distributions [cite: 146, 148]
    show_lab04()