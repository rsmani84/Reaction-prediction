import streamlit as st
from rdkit import Chem
from rdkit.Chem import rdChemReactions, Draw, Descriptors
from mendeleev import element
import io

st.set_page_config(page_title="Advanced Organic Lab", layout="wide")
st.title("🧪 Organic Synthesis Lab with Thermodynamic Analytics")
st.write("Simulate multi-component organic reactions and evaluate thermal feasibility ($\Delta G$, $\Delta H$).")

# Reaction templates with foundational group-contribution enthalpy changes (approx kJ/mol)
REACTION_TEMPLATES = {
    "Esterification (Acid + Alcohol -> Ester)": {
        "smarts": "[CX3:1](=[O:2])[OH:3].[CX4:4][OH:5] >> [CX3:1](=[O:2])[O:5][CX4:4]",
        "num_reactants": 2,
        "defaults": ["CC(=O)O", "CCO"],
        "base_dh": -15.0,  # Slightly exothermic
        "base_ds": -0.01   # Loss of rotational/translational degrees of freedom
    },
    "Grignard Reaction (Ketone/Aldehyde + Grignard -> Alcohol)": {
        "smarts": "[CX3:1]=[O:2].[CX4:3][Mg][Cl,Br,I:4] >> [CX4:3][CX4:1]([O-:2])",
        "num_reactants": 2,
        "defaults": ["CC(=O)C", "CC[Mg]Br"],
        "base_dh": -120.0, # Highly exothermic
        "base_ds": -0.08
    },
    "Amide Coupling (Acid + Amine -> Amide)": {
        "smarts": "[CX3:1](=[O:2])[OH:3].[NX3:4] >> [CX3:1](=[O:2])[NX3:4]",
        "num_reactants": 2,
        "defaults": ["CC(=O)O", "CCN"],
        "base_dh": -25.0,
        "base_ds": -0.01
    }
}

# --- Sidebar Controls ---
st.sidebar.header("🔬 Lab Configuration")
reaction_name = st.sidebar.selectbox("Choose Reaction Type", list(REACTION_TEMPLATES.keys()))
selected_rxn = REACTION_TEMPLATES[reaction_name]

st.sidebar.subheader("🌡️ Environment Conditions")
# Temperature slider converting Celsius to Kelvin internally
temp_c = st.sidebar.slider("Reaction Temperature (°C)", min_value=-50, max_value=300, value=25)
temp_k = temp_c + 273.15

# --- Helper Functions ---
def mol_to_image_bytes(mol):
    if mol is None: return None
    img = Draw.MolToImage(mol, size=(250, 250))
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()

# --- Reactants Section ---
st.subheader("1. Enter Reactants (SMILES)")
cols = st.columns(selected_rxn["num_reactants"])
reactant_mols = []
invalid_smiles = False

for i in range(selected_rxn["num_reactants"]):
    with cols[i]:
        default_smiles = selected_rxn["defaults"][i]
        smiles_input = st.text_input(f"Reactant {i+1}", value=default_smiles, key=f"react_{i}")
        
        mol = Chem.MolFromSmiles(smiles_input)
        if mol:
            reactant_mols.append(mol)
            # Property generation using RDKit Descriptors
            mw = Descriptors.MolWt(mol)
            formula = Descriptors.MolecularFormula(mol)
            
            st.markdown(f"**Formula:** ${formula}$")
            st.markdown(f"**Mass:** {mw:.2f} g/mol")
            st.image(mol_to_image_bytes(mol), caption=f"Reactant {i+1}")
        else:
            st.error("Invalid SMILES notation string.")
            invalid_smiles = True

# --- Simulation Engine ---
st.subheader("2. Synthesis and Feasibility Analysis")

if st.button("⚡ Run Chemical Analysis") and not invalid_smiles:
    try:
        rxn = rdChemReactions.ReactionFromSmarts(selected_rxn["smarts"])
        product_tuples = rxn.RunReactants(tuple(reactant_mols))
        
        if product_tuples:
            unique_products = {}
            for prod_tuple in product_tuples:
                for prod in prod_tuple:
                    try:
                        Chem.SanitizeMol(prod)
                        smiles = Chem.MolToSmiles(prod)
                        if smiles not in unique_products:
                            unique_products[smiles] = prod
                    except:
                        continue
            
            if unique_products:
                # Render predicted product cards
                p_cols = st.columns(len(unique_products))
                for idx, (smiles, prod_mol) in enumerate(unique_products.items()):
                    with p_cols[idx]:
                        st.success(f"Predicted Product")
                        st.code(f"SMILES: {smiles}")
                        
                        p_mw = Descriptors.MolWt(prod_mol)
                        p_form = Descriptors.MolecularFormula(prod_mol)
                        st.markdown(f"**Formula:** ${p_form}$")
                        st.markdown(f"**Mass:** {p_mw:.2f} g/mol")
                        st.image(mol_to_image_bytes(prod_mol))

                # --- Thermodynamics Computation Engine ---
                st.markdown("---")
                st.subheader("📊 Thermodynamics & Feasibility Diagnostics")
                
                # Base heuristic values loaded from configuration
                dH = selected_rxn["base_dh"]
                dS = selected_rxn["base_ds"]
                
                # Gibbs Free Energy calculation: dG = dH - T*dS
                dG = dH - (temp_k * dS)
                
                metric_col1, metric_col2, metric_col3 = st.columns(3)
                metric_col1.metric("Enthalpy ($\Delta H$)", f"{dH:.1f} kJ/mol")
                metric_col2.metric("Entropy ($\Delta S$)", f"{dS*1000:.1f} J/(mol·K)")
                metric_col3.metric("Gibbs Free Energy ($\Delta G$)", f"{dG:.1f} kJ/mol")
                
                # Feasibility Evaluation Logic
                if dG < 0:
                    st.balloons()
                    st.success(f"✅ **Reaction Spontaneous and Feasible!** At {temp_c}°C ({temp_k:.1f} K), $\Delta G$ is negative ({dG:.1f} kJ/mol). The forward reaction will happen without external energy intervention.")
                else:
                    st.error(f"❌ **Reaction Non-Spontaneous!** At {temp_c}°C ({temp_k:.1f} K), $\Delta G$ is positive ({dG:.1f} kJ/mol). The synthesis requires heat addition, a catalyst, or a coupling setup to proceed.")
                    
                # Kinetic insight
                if temp_c < 20:
                    st.warning("⚠️ **Kinetic Notice:** Low working temperature profile detected. Even if thermodynamically feasible, reaction velocity may be severely restricted.")
            else:
                st.error("The simulation could not yield any chemically stable molecules.")
        else:
            st.warning("No reaction occurred! Check if your reactant molecules contain the functional groups required for this reaction.")
            
    except Exception as e:
        st.error(f"Execution Error: {str(e)}")
