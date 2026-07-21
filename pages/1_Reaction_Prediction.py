import streamlit as st
from rdkit import Chem
from rdkit.Chem import Draw
from rdkit.Chem import rdChemReactions
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors
import io

st.set_page_config(page_title="Reaction Prediction", layout="wide")

st.title("🧪 Organic Reaction Prediction")

st.write(
"""
Predict products of common organic reactions.

Enter the reactants as SMILES strings.
"""
)

# -----------------------------
# Reaction Database
# -----------------------------

REACTIONS = {

    "Esterification":{

        "smarts":"[CX3:1](=[O:2])[OH].[OX2H:3]>>[CX3:1](=[O:2])[O:3]",

        "reactants":["CC(=O)O","CCO"]

    },

    "Amide Formation":{

        "smarts":"[CX3:1](=[O:2])[OH].[NX3H2:3]>>[CX3:1](=[O:2])[N:3]",

        "reactants":["CC(=O)O","CN"]

    },

    "SN2 Reaction":{

        "smarts":"[C:1][Br].[O-:2]>>[C:1][O:2]",

        "reactants":["CCBr","[OH-]"]

    }

}

# -----------------------------
# Select Reaction
# -----------------------------

reaction_name = st.selectbox(

    "Choose Reaction",

    list(REACTIONS.keys())

)

reaction = REACTIONS[reaction_name]

# -----------------------------
# Input Reactants
# -----------------------------

col1,col2 = st.columns(2)

with col1:

    react1 = st.text_input(

        "Reactant 1",

        reaction["reactants"][0]

    )

with col2:

    react2 = st.text_input(

        "Reactant 2",

        reaction["reactants"][1]

    )

# -----------------------------
# Convert Molecules
# -----------------------------

mol1 = Chem.MolFromSmiles(react1)

mol2 = Chem.MolFromSmiles(react2)

def mol_image(mol):

    img = Draw.MolToImage(mol,size=(300,300))

    buf=io.BytesIO()

    img.save(buf,format="PNG")

    return buf.getvalue()

# -----------------------------
# Display Reactants
# -----------------------------

st.markdown("## Reactants")

c1,c2 = st.columns(2)

with c1:

    if mol1:

        st.image(mol_image(mol1))

        st.write("Formula :",rdMolDescriptors.CalcMolFormula(mol1))

        st.write("Molecular Weight :",round(Descriptors.MolWt(mol1),2))

    else:

        st.error("Invalid Reactant 1")

with c2:

    if mol2:

        st.image(mol_image(mol2))

        st.write("Formula :",rdMolDescriptors.CalcMolFormula(mol2))

        st.write("Molecular Weight :",round(Descriptors.MolWt(mol2),2))

    else:

        st.error("Invalid Reactant 2")

# -----------------------------
# Predict Product
# -----------------------------

if st.button("Predict Product"):

    if mol1 and mol2:

        try:

            rxn = rdChemReactions.ReactionFromSmarts(

                reaction["smarts"]

            )

            products = rxn.RunReactants(

                (mol1,mol2)

            )

            if len(products)==0:

                st.warning("No product predicted.")

            else:

                st.success("Reaction Successful")

                st.markdown("## Predicted Products")

                unique=[]

                for prod in products:

                    p=prod[0]

                    Chem.SanitizeMol(p)

                    smi=Chem.MolToSmiles(p)

                    if smi not in unique:

                        unique.append(smi)

                        st.image(

                            mol_image(p),

                            width=300

                        )

                        st.code(smi)

                        st.write(

                            "Formula :",

                            rdMolDescriptors.CalcMolFormula(p)

                        )

                        st.write(

                            "Molecular Weight :",

                            round(

                                Descriptors.MolWt(p),

                                2

                            )

                        )

        except Exception as e:

            st.error(str(e))

    else:

        st.error("Please enter valid reactants.")
