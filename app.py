import streamlit as st

st.set_page_config(
    page_title="Organic Synthesis Virtual Laboratory",
    page_icon="🧪",
    layout="wide"
)

st.title("🧪 Organic Synthesis Virtual Laboratory")

st.markdown("""
Welcome to the **Organic Synthesis Virtual Laboratory**.

This virtual laboratory allows students to:

- Predict organic reactions
- Visualize reactants and products
- Calculate molecular properties
- Evaluate thermodynamic feasibility
- Learn reaction mechanisms
- Practice through quizzes

Use the navigation menu on the left to begin.
""")

st.image(
    "https://upload.wikimedia.org/wikipedia/commons/thumb/8/87/Chemical_reaction.svg/1024px-Chemical_reaction.svg.png",
    width=700
)

st.info("Select a module from the left sidebar.")

from utils.thermo import gibbs_energy
from utils.thermo import spontaneity

temperature = st.slider(
    "Temperature (°C)",
    0,
    200,
    25
)

dH = -25.4

dS = -42.5

dG = gibbs_energy(
    dH,
    dS,
    temperature
)

st.metric("ΔH",f"{dH} kJ/mol")

st.metric("ΔS",f"{dS} J/mol.K")

st.metric("ΔG",f"{dG} kJ/mol")

st.success(spontaneity(dG))
