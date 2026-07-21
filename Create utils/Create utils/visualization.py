from rdkit.Chem import Draw
from rdkit import Chem
import io
def molecule_image(mol):
    Chem.rdDepictor.Compute2DCoords(mol)
    image = Draw.MolToImage(
        mol,
        size=(350,350)
    )

    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    return buffer.getvalue()
