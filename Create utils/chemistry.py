from rdkit import Chem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors
def load_molecule(smiles):
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None
    Chem.SanitizeMol(mol)
    return mol
def molecular_formula(mol):
    return rdMolDescriptors.CalcMolFormula(mol)
def molecular_weight(mol):
    return Descriptors.MolWt(mol)
def logP(mol):
    return Descriptors.MolLogP(mol)
def tpsa(mol):
    return Descriptors.TPSA(mol)
def hbond_donors(mol):
    return Descriptors.NumHDonors(mol)
def hbond_acceptors(mol):
    return Descriptors.NumHAcceptors(mol)
