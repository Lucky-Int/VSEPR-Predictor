from fastapi import FastAPI, Body, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from VSEPR import main as run_vsepr_pipeline  

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/predict")
def predict_vsepr(payload: dict = Body(...)):
    molecule = payload.get("molecule")
    if not molecule:
        raise HTTPException(status_code=400, detail="Please enter a molecule.")
    
    try:
        (
            central_atom, 
            ve_total, 
            central_lone_pairs, 
            elements_and_nums, 
            steric_number, 
            terminal_atoms, 
            e_geo, 
            mol_geo, 
            hybridization, 
            bond_angles
        ) = run_vsepr_pipeline(molecule_from_web=molecule)
        
    except SystemExit as err:
        # Convert any sys.exit from VSEPR.py into a clean 400 error
        raise HTTPException(status_code=400, detail=str(err))
    except Exception as err:
        raise HTTPException(status_code=400, detail=str(err))

    return {
        "central_atom": central_atom,
        "valence_electrons": ve_total,
        "lone_pairs": central_lone_pairs,
        "elements_and_nums": elements_and_nums,
        "steric_number": steric_number,
        "terminal_atoms": terminal_atoms,
        "electron_geometry": e_geo,
        "molecular_geometry": mol_geo,
        "hybridization": hybridization,
        "bond_angles": bond_angles
    }