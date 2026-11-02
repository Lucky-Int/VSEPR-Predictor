from fastapi import FastAPI, Body, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, Response
import os
import sys

# CRITICAL: Force Vercel to append the root folder to python path
# This prevents the module/pipeline import errors completely
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    import VSEPR
except ImportError:
    try:
        from api import VSEPR
    except ImportError:
        import sys
        raise ImportError(f"Could not load VSEPR pipeline. Current sys.path: {sys.path}")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Robust path engine that handles file retrieval safely
def get_file_content(filename: str, binary: bool = False):
    api_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(api_dir)
    
    paths_to_check = [
        os.path.join(root_dir, filename),
        os.path.join(api_dir, filename),
        os.path.join(root_dir, "public", filename)
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
        raise HTTPException(status_code=404, detail="index.html not found")
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
@app.post("/api/predict")
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
        ) = VSEPR.main(molecule_from_web=molecule)
        
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
