document.addEventListener('DOMContentLoaded', () => {
    
    const API_URL = '/predict';
    const submitBtn = document.getElementById('submitBtn');
    const moleculeInput = document.getElementById('moleculeInput');
    const resultDashboard = document.getElementById('resultDashboard');

    
    const safeUpdateText = (id, text) => {
        try {
            const element = document.getElementById(id);
            if (element) {
                element.innerText = text;
            }
        } catch (e) {
            console.warn(`Skipped missing HTML ID: ${id}`);
        }
    };

    if (moleculeInput) {
        moleculeInput.addEventListener('keydown', (event) => {
            if (event.key === 'Enter') {
                event.preventDefault();
                if (submitBtn) submitBtn.click();
            }
        });
    }

    if (submitBtn) {
        submitBtn.addEventListener('click', async (event) => {
            event.preventDefault();

            if (!moleculeInput) return;
            const moleculeValue = moleculeInput.value.trim();
            if (!moleculeValue) {
                alert("Please enter a molecule (e.g. H2O, SF6)");
                return;
            }

            submitBtn.disabled = true;
            submitBtn.innerText = "Analyzing... ⏳";

            
            const outputFields = [
                'centralAtomOutput', 'valenceElectronsOutput', 'stericNumberOutput',
                'lonePairsOutput', 'electronGeoOutput', 'molecularGeoOutput',
                'hybridizationOutput', 'bondAngleOutput', 'terminalAtomsOutput', 'rawElementsOutput'
            ];
            outputFields.forEach(id => safeUpdateText(id, "Calculating..."));
                
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

                
                safeUpdateText('centralAtomOutput', responseData.central_atom);
                safeUpdateText('valenceElectronsOutput', responseData.valence_electrons);
                safeUpdateText('stericNumberOutput', responseData.steric_number);
                safeUpdateText('lonePairsOutput', responseData.lone_pairs);
                safeUpdateText('electronGeoOutput', responseData.electron_geometry);
                safeUpdateText('molecularGeoOutput', responseData.molecular_geometry);
                safeUpdateText('hybridizationOutput', responseData.hybridization);
                safeUpdateText('bondAngleOutput', responseData.bond_angles);

                if (resultDashboard) {
                    resultDashboard.style.display = 'block';
                    resultDashboard.style.animation = 'none';
                    resultDashboard.offsetHeight;
                    resultDashboard.style.animation = 'fadeInSlide 0.4s ease-out forwards';
                    resultDashboard.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
                }

                submitBtn.innerText = "Done! ✅";
                setTimeout(() => {
                    submitBtn.disabled = false;
                    submitBtn.innerText = "Submit";
                }, 1200);

            } catch (error) {
                console.error("Request failed:", error);
                safeUpdateText('molecularGeoOutput', "Error");
                alert(`Error: ${error.message}`);
                
                submitBtn.disabled = false;
                submitBtn.innerText = "Submit";
            }
        });
    }
});
