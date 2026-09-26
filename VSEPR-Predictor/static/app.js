document.addEventListener('DOMContentLoaded', () => {

    const API_URL = 'https://supreme-space-potato-gx4664rv5j542xv9-8000.app.github.dev/predict';
    const submitBtn = document.getElementById('submitBtn');
    const moleculeInput = document.getElementById('moleculeInput');
    const resultDashboard = document.getElementById('resultDashboard');

    
    moleculeInput.addEventListener('keydown', (event) => {
        if (event.key === 'Enter') {
            event.preventDefault();
            submitBtn.click();
        }
    });

    submitBtn.addEventListener('click', async (event) => {
        event.preventDefault();

        const moleculeValue = moleculeInput.value.trim();
        if (!moleculeValue) {
            alert("Please enter a molecule (e.g. H2O, SF6)");
            return;
        }

        
        submitBtn.disabled = true;
        submitBtn.innerText = "Analyzing... ⏳";
        document.getElementById('centralAtomOutput').innerText = "Calculating...";
    document.getElementById('valenceElectronsOutput').innerText = "Calculating...";
    document.getElementById('stericNumberOutput').innerText = "Calculating...";
    document.getElementById('lonePairsOutput').innerText = "Calculating...";
    document.getElementById('electronGeoOutput').innerText = "Calculating...";
    document.getElementById('molecularGeoOutput').innerText = "Calculating...";
    document.getElementById('hybridizationOutput').innerText = "Calculating...";
    document.getElementById('bondAngleOutput').innerText = "Calculating...";

    document.getElementById('terminalAtomsOutput').innerText = "Calculating...";
    document.getElementById('rawElementsOutput').innerText = "Calculating...";
            
        
        try {
            const response = await fetch(API_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    molecule: moleculeValue
                })
            });
            

            let responseData;
            const contentType = response.headers.get("content-type");
            if (contentType && contentType.includes("application/json")) {
                responseData = await response.json();
            } else {
                const text = await response.text();
                throw new Error(text || `HTTP Error ${response.status}`);
            }

            if (!response.ok) {
                throw new Error(responseData.detail || "Server computation error");
            }

            
            document.getElementById('centralAtomOutput').innerText = responseData.central_atom;
            document.getElementById('valenceElectronsOutput').innerText = responseData.valence_electrons;
            document.getElementById('stericNumberOutput').innerText = responseData.steric_number;
            document.getElementById('lonePairsOutput').innerText = responseData.lone_pairs;
            document.getElementById('electronGeoOutput').innerText = responseData.electron_geometry;
            document.getElementById('molecularGeoOutput').innerText = responseData.molecular_geometry;
            document.getElementById('hybridizationOutput').innerText = responseData.hybridization;
            document.getElementById('bondAngleOutput').innerText = responseData.bond_angles;

            document.getElementById('terminalAtomsOutput').innerText = JSON.stringify(responseData.terminal_atoms);
            document.getElementById('rawElementsOutput').innerText = JSON.stringify(responseData.elements_and_nums);

            
            resultDashboard.style.display = 'block';
            resultDashboard.style.animation = 'none';
            resultDashboard.offsetHeight;
            resultDashboard.style.animation = 'fadeInSlide 0.4s ease-out forwards';

            
            resultDashboard.scrollIntoView({ behavior: 'smooth', block: 'nearest' });

           
            submitBtn.innerText = "Done! ✅";
            setTimeout(() => {
                submitBtn.disabled = false;
                submitBtn.innerText = "Submit";
            }, 1200);

        } catch (error) {
            console.error("Request failed:", error);
            document.getElementById('molecularGeoOutput').innerText = "Error";
            alert(`Error: ${error.message}`);
            
            submitBtn.disabled = false;
            submitBtn.innerText = "Submit";
        }
    });
});
