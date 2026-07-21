REACTIONS = {

    "Fischer Esterification": {
        "smarts": "[CX3:1](=[O:2])[OH].[OX2H:3]>>[CX3:1](=[O:2])[O:3]",
        "reactants": ["CC(=O)O", "CCO"]
    },

    "Amide Formation": {
        "smarts": "[CX3:1](=[O:2])[OH].[NX3H2:3]>>[CX3:1](=[O:2])[N:3]",
        "reactants": ["CC(=O)O", "CN"]
    },

    "SN1 Reaction": {
        "smarts": "",
        "reactants": ["CC(C)Br", "O"]
    },

    "SN2 Reaction": {
        "smarts": "[C:1][Br].[O-:2]>>[C:1][O:2]",
        "reactants": ["CCBr", "[OH-]"]
    },

    "E1 Elimination": {
        "smarts": "",
        "reactants": ["CC(C)Br", "O"]
    },

    "E2 Elimination": {
        "smarts": "",
        "reactants": ["CCBr", "[OH-]"]
    },

    "Grignard Reaction": {
        "smarts": "",
        "reactants": ["CC(=O)C", "CC[Mg]Br"]
    },

    "Aldol Condensation": {
        "smarts": "",
        "reactants": ["CC=O", "CC=O"]
    },

    "Friedel-Crafts Alkylation": {
        "smarts": "",
        "reactants": ["c1ccccc1", "CCl"]
    },

    "Diels-Alder Reaction": {
        "smarts": "",
        "reactants": ["C=CC=C", "C=C"]
    }

}
