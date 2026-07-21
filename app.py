import streamlit as st
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Draw

st.set_page_config(page_title="Organic Reaction Prediction", page_icon="🧪")

st.title("🧪 Organic Reaction Prediction")
st.write("Predict products of common organic reactions.")
st.write("Enter the reactants as SMILES strings.")

# Reaction Definitions using SMARTS patterns
REACTIONS = {
    "Esterification": {
        "smarts": "[CX3(=O):1][OX2H:2].[OX2H:3][CX4:4]>>[CX3(=O):1][O:3][CX4:4].[OH2:2]",
        "num_reactants": 2,
        "labels": ["Carboxylic Acid SMILES", "Alcohol SMILES"],
        "defaults": ["CC(=O)O", "CCO"],
    },
    "Amide Formation": {
        "smarts": "[CX3(=O):1][OX2H:2].[NX3;H2,H1:3]>>[CX3(=O):1][N:3].[OH2:2]",
        "num_reactants": 2,
        "labels": ["Carboxylic Acid SMILES", "Amine SMILES"],
        "defaults": ["CC(=O)O", "CCN"],
    },
    "SN2 Reaction": {
        "smarts": "[CX4:1][Cl,Br,I:2].[NX3,OX2H,SX2H:-1,H0:3]>>[CX4:1][N,O,S:3].[Cl,Br,I:2]",
        "num_reactants": 2,
        "labels": ["Alkyl Halide SMILES", "Nucleophile SMILES"],
        "defaults": ["CCBr", "C[O-]"],
    },
    "Diels-Alder Reaction": {
        "smarts": "[C:1]=[C:2]-[C:3]=[C:4].[C:5]=[C:6]>>[C:1]1[C:2]=[C:3][C:4][C:6][C:5]1",
        "num_reactants": 2,
        "labels": ["Diene SMILES", "Dienophile SMILES"],
        "defaults": ["C=CC=C", "C=CC(=O)OC"],
    },
    "Friedel-Crafts Acylation": {
        "smarts": "[c:1][H:2].[CX3(=O):3][Cl:4]>>[c:1][CX3(=O):3].[H][Cl:4]",
        "num_reactants": 2,
        "labels": ["Aromatic Ring SMILES", "Acyl Chloride SMILES"],
        "defaults": ["c1ccccc1", "CC(=O)Cl"],
    },
    "Grignard Reaction": {
        "smarts": "[CX3:1]=[O:2].[C:3][Mg][Br,Cl,I:4]>>[CX4:1]([O:2][H])[C:3]",
        "num_reactants": 2,
        "labels": ["Carbonyl (Aldehyde/Ketone) SMILES", "Grignard Reagent SMILES"],
        "defaults": ["CC(=O)C", "C[Mg]Br"],
    },
    "Aldol Condensation": {
        "smarts": "[CX3H1:1](=O)[CH2:2].[CX3H1:3](=O)>>[CX3H1:1](=O)[CH1:2]=[CH1:3]",
        "num_reactants": 2,
        "labels": ["Enolizable Aldehyde SMILES", "Electrophilic Aldehyde SMILES"],
        "defaults": ["CC=O", "CC=O"],
    },
    "Alkene Hydrogenation": {
        "smarts": "[C:1]=[C:2]>>[C:1][C:2]",
        "num_reactants": 1,
        "labels": ["Alkene SMILES"],
        "defaults": ["CC=CC"],
    },
}

# Selectbox for reaction type
reaction_name = st.selectbox("Choose Reaction", list(REACTIONS.keys()))
selected_rxn = REACTIONS[reaction_name]

# Render reactant input fields dynamically
reactant_inputs = []
for i in range(selected_rxn["num_reactants"]):
    label = selected_rxn["labels"][i]
    default_val = selected_rxn["defaults"][i]
    val = st.text_input(label, value=default_val, key=f"input_{reaction_name}_{i}")
    reactant_inputs.append(val)

# Run prediction
if st.button("Predict Products"):
    try:
        # Parse inputs into RDKit molecules
        mols = [Chem.MolFromSmiles(smi) for smi in reactant_inputs if smi.strip()]

        if len(mols) != selected_rxn["num_reactants"] or any(m is None for m in mols):
            st.error("Please enter valid SMILES strings for all inputs.")
        else:
            rxn = AllChem.ReactionFromSmarts(selected_rxn["smarts"])
            products = rxn.RunReactants(tuple(mols))

            if not products:
                st.warning("No product formed. Check if the reactants match the expected functional groups.")
            else:
                st.subheader("Predicted Product(s):")
                
                # Extract unique products
                unique_smiles = set()
                for prod_tuple in products:
                    for prod in prod_tuple:
                        Chem.SanitizeMol(prod)
                        unique_smiles.add(Chem.MolToSmiles(prod))

                for smi in unique_smiles:
                    st.code(smi, language="text")
                    
                    # Render 2D image of product
                    mol = Chem.MolFromSmiles(smi)
                    if mol:
                        img = Draw.MolToImage(mol)
                        st.image(img, caption=f"SMILES: {smi}")

    except Exception as e:
        st.error(f"Error predicting products: {str(e)}")
