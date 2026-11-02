from fastapi import FastAPI, Body, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, Response
import os

try:
    from VSEPR import main as run_vsepr_pipeline
except ImportError:
    from api.VSEPR import main as run_vsepr_pipeline

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Robust path handler to find files whether they are in / or /public relative to the api/ folder
def get_file_content(filename: str, binary: bool = False):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    paths_to_check = [
        os.path.join(base_dir, "..", filename),          # Directly in the root directory
        os.path.join(base_dir, "..", "public", filename), # Inside a public directory if it exists
        os.path.join(base_dir, filename)                  # Inside the api/ directory itself
    ]
    for path in paths_to_check:
        if os.path.exists(path):
            mode = "rb" if binary else "r"
            encoding = None if binary else "utf-8"
            with open(path, mode, encoding=encoding) as f:
                return f.read()
    return None

# --- FRONTEND ROUTING ---

@app.get("/", response_class=HTMLResponse)
def read_index():
    content = get_file_content("index.html")
    if not content:
        raise HTTPException(status_code=404, detail="index.html not found in root directory")
    return content

@app.get("/style.css")
def read_css():
    content = get_file_content("style.css")
    if not content:
        return Response(status_code=404)
    return Response(content=content, media_type="text/css")

@app.get("/app.js")
def read_js():
    content = get_file_content("app.js")
    if not content:
        return Response(status_code=404)
    return Response(content=content, media_type="application/javascript")

@app.get("/modeler.js")
def read_modeler_js():
    content = get_file_content("modeler.js")
    if not content:
        return Response(status_code=404)
    return Response(content=content, media_type="application/javascript")

@app.get("/electronegativitychart.jpg")
def read_chart_image():
    content = get_file_content("electronegativitychart.jpg", binary=True)
    if not content:
        return Response(status_code=404)
    return Response(content=content, media_type="image/jpeg")

# --- BACKEND API ROUTING ---

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
