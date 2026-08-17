# VSEPR Predictor and Modeler
import re
molecule = input("Molecule: ")
# ERROR CHECK ^^^
# ex input: CH3OH
# Create a molecular diagram; use RDKit.
# convert molecule into necessary type.

# draw diagram of molecule

    # Count the number of Valence Electrons in the compound (consider the charge as well)

# check the coefficient of the molecule
if matches := re.search(r"^(\d)", molecule):
    coefficient = matches.group(1)
    no_c_molecule = molecule[1:]
else:
    coefficient = "1"
    no_c_molecule = molecule

elements = []
subscripts = []
for a in no_c_molecule:
    if a.isalpha():
        elements.append(a)

    else:
        subscripts.append(a)

matches = re.findall(r"([A-Z][a-z]?)(\d*)" ,no_c_molecule)

elements_and_nums = []
for element, subscript in matches:
    if subscript == "":
        subscript = "1"

    element_w_num = {
         "Element": element,
         "Subscript": subscript,
         }
    elements_and_nums.append(element_w_num)

print(elements_and_nums)



    # Consider 2 electrons used for each bond shared between the core atom and another one.

    # If there are still leftover electrons assign them to the outer atoms as lone pairs.

    # If there are still more leftover electrons assign them to the central atom as lone pairs

    # If the central atom does not have enough electrons, needing at least 8, create more covalent bonds.

    # Check formal charges and if they can be reduced closer 0 do as that. """



# Count the amount of electron pairs/clouds around the central atom; give the compounds its electron-group geo.
# ignore lone pairs and consider the greater space they take up to predict the molecular geometry.

