REACTIONS = {

    "Fischer Esterification": {
        "smarts": "[CX3:1](=[O:2])[OH].[OX2H:3]>>[CX3:1](=[O:2])[O:3]",
        "reactants": ["CC(=O)O", "CCO"],
        "dH": -15.4,
        "dS": -42.3,
        "catalyst": "H₂SO₄",
        "solvent": "Ethanol",
        "temperature": "60–80 °C",
        "mechanism": [
            "Protonation of carbonyl oxygen",
            "Nucleophilic attack by alcohol",
            "Formation of tetrahedral intermediate",
            "Elimination of water",
            "Deprotonation to give ester"
        ]
    },

    "Amide Formation": {
        "smarts": "[CX3:1](=[O:2])[OH].[NX3H2:3]>>[CX3:1](=[O:2])[N:3]",
        "reactants": ["CC(=O)O", "CN"],
        "dH": -25.8,
        "dS": -35.5,
        "catalyst": "DCC / EDC",
        "solvent": "DMF",
        "temperature": "25 °C",
        "mechanism": [
            "Activation of carboxylic acid",
            "Nucleophilic attack by amine",
            "Formation of tetrahedral intermediate",
            "Elimination of water",
            "Amide formation"
        ]
    },

    "SN1 Reaction": {
        "smarts": "...",
        "reactants": ["CC(C)Br", "O"],
        "dH": -18.0,
        "dS": 15.0,
        "catalyst": "None",
        "solvent": "Water",
        "temperature": "25 °C",
        "mechanism": [
            "Leaving group departs",
            "Carbocation formation",
            "Nucleophilic attack",
            "Deprotonation"
        ]
    }
}
