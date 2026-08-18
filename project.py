# VSEPR Predictor and Modeler
# rename property so variable names don't collide
from mendeleev import element as get_element
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
    coefficient = int(matches.group(1))
    no_c_molecule = molecule[1:]
else:
    coefficient = 1
    no_c_molecule = molecule


matches = re.findall(r"([A-Z][a-z]?)(\d*)" ,no_c_molecule)
elements = []
elements_and_nums = []
ve_total = 0
for element, subscript in matches:
    if subscript == "":
        subscript = "1"
    elements.append(element)
    element_w_num = {
         "Element": element,
         "Subscript": subscript,
         }
    elements_and_nums.append(element_w_num)

    # calculate valence electron total
    ve = get_element(element).nvalence()
    ve_part = ve * int(subscript)
    ve_total += ve_part
# ACCOUNT FOR OVERALL CHARGE (POLYATOMIC ATOMS) URGENCY: !!!
# find element with lowest electronegativity (central atom)
electronegativities = []
no_h_elements = [e for e in elements if e != "H"]
for element in no_h_elements:
        element = get_element(element)
        electronegativities.append(element.electronegativity())

lowest_eneg = min(electronegativities)
position = electronegativities.index(lowest_eneg)
central_atom = no_h_elements[position]


print(elements_and_nums)
print(f"Valence Electrons: {ve_total}")
print(f"Central Atom: {central_atom}")

# ex: [{'Element': 'H', 'Subscript': '2'}, {'Element': 'O', 'Subscript': '1'}]


    # Consider 2 electrons used for each bond shared between the core atom and another one.

    # If there are still leftover electrons assign them to the outer atoms as lone pairs.

    # If there are still more leftover electrons assign them to the central atom as lone pairs

    # If the central atom does not have enough electrons, needing at least 8, create more covalent bonds.

    # Check formal charges and if they can be reduced closer 0 do as that. """



# Count the amount of electron pairs/clouds around the central atom; give the compounds its electron-group geo.
# ignore lone pairs and consider the greater space they take up to predict the molecular geometry.

