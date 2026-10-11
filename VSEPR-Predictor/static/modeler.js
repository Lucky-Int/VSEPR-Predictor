
        // 3Dmol.js documentation and connect to PubChem API so user can type mol names like H2O or CO32-
        // Google searches for things like spinning molecule-- prioritized documentation.
        const viewerElement = document.getElementById('moleculeViewer');
        const viewer = $3Dmol.createViewer(viewerElement, { backgroundColor: '#ffffff' });

        document.getElementById('submitBtn').addEventListener('click', async () => {
            const input = document.getElementById('moleculeInput').value.trim();
            if (!input) return;

           
            let cid = await fetchCID(`https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/${encodeURIComponent(input)}/cids/JSON`);
            
            
            if (!cid) {
                cid = await fetchCID(`https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/formula/${encodeURIComponent(input)}/cids/JSON`);
            }

            if (cid) {
                viewer.clear();
                
                $3Dmol.download(`cid:${cid}`, viewer, { record_type: "3d" }, function() {
                    viewer.setStyle({}, { stick: { radius: 0.15 }, sphere: { scale: 0.25 } });
                    viewer.zoomTo();
                    viewer.render();
                    viewer.spin(true); 
                }, function() {
                
                    $3Dmol.download(`cid:${cid}`, viewer, {}, function() {
                        viewer.setStyle({}, { stick: { radius: 0.15 }, sphere: { scale: 0.25 } });
                        viewer.zoomTo();
                        viewer.render();
                    });
                });
            }
        });

       
        async function fetchCID(url) {
            try {
                const response = await fetch(url);
                if (!response.ok) return null;
                const data = await response.json();
                return data.IdentifierList.CID[0];
            } catch (e) {
                return null;
            }
        }
    