
# Try writing Double and Triple bond code. And create the final lewis structure.
# VSEPR Predictor and Modeler
# rename property so variable names don't collide
from mendeleev import element as get_element
import re
import sys
from chemicals import search_chemical

def main():
    raw_input = input("Molecule: ")
    if not validate_formula(raw_input):
        sys.exit("Not a valid molecule")
    molecule = raw_input

    me = range(1)


    for motivation in me:
        lock_in(motivation)





    print("-" * 120)

    # Count the number of Valence Electrons in the compound-- consider the charge as well.


    if matches := re.search(r"^(\d)", molecule):
        coefficient = int(matches.group(1))
        no_c_molecule = molecule[1:]
    else:
        coefficient = 1
        no_c_molecule = molecule
    # Maybe uneccesary to find coefficient ^^^
    elements_and_nums = get_atoms_subscripts(no_c_molecule)
    ve_total = get_total_valence(no_c_molecule)
    central_atom = get_central_atom(no_c_molecule)


    print(elements_and_nums)
    print(f"Valence Electrons: {ve_total}")
    print(f"Central Atom: {central_atom}")

    num_terminal_atoms = 0
    terminal_atoms = []
    for part in elements_and_nums:
        if part['Element'] != central_atom:
            num_terminal_atoms += int(part['Subscript'])
            for _ in range(int(part['Subscript'])):
                terminal_atoms.append(part["Element"])

        track_ve = ve_total - 2 * num_terminal_atoms
        if track_ve != 0:
            for terminal_atom in terminal_atoms:
                if terminal_atom != "H":
                    track_ve -= 6
    # add lone pairs if needed
    if track_ve != 0:
        electron_groups = num_terminal_atoms
        central_lone_pairs = int(track_ve / 2)
        electron_groups += central_lone_pairs
        track_ve = 0
        central_electrons = central_lone_pairs * 2 + num_terminal_atoms
    # check formal charge of central atom
        central_atom_valence = get_element(central_atom).nvalence()
        central_formal_charge = central_atom_valence - central_electrons
    else:
        electron_groups = num_terminal_atoms
        central_electrons = num_terminal_atoms
        central_formal_charge = get_element(central_atom).nvalence() - central_electrons
        central_lone_pairs = 0

    # go on with adding double or triple bonds. (If formal_charge_central != 0).


    try:
        print("Lone Pairs:", central_lone_pairs)
    except UnboundLocalError:
        pass
    print("Electron Groups / Steric Number:", electron_groups)
    print("Terminal Atoms:", terminal_atoms)




    vsepr_table = {
    "AX2": {
        "steric_number": 2,
        "bonding_groups": 2,
        "lone_pairs": 0,
        "electron_geometry": "Linear",
        "molecular_geometry": "Linear",
        "bond_angles": "180",
        "hybridization": "sp"
    },
    "AX3": {
        "steric_number": 3,
        "bonding_groups": 3,
        "lone_pairs": 0,
        "electron_geometry": "Trigonal Planar",
        "molecular_geometry": "Trigonal Planar",
        "bond_angles": "120",
        "hybridization": "sp2"
    },
    "AX2E": {
        "steric_number": 3,
        "bonding_groups": 2,
        "lone_pairs": 1,
        "electron_geometry": "Trigonal Planar",
        "molecular_geometry": "Bent",
        "bond_angles": "<120",
        "hybridization": "sp2"
    },
    "AX4": {
        "steric_number": 4,
        "bonding_groups": 4,
        "lone_pairs": 0,
        "electron_geometry": "Tetrahedral",
        "molecular_geometry": "Tetrahedral",
        "bond_angles": "109.5",
        "hybridization": "sp3"
    },
    "AX3E": {
        "steric_number": 4,
        "bonding_groups": 3,
        "lone_pairs": 1,
        "electron_geometry": "Tetrahedral",
        "molecular_geometry": "Trigonal Pyramidal",
        "bond_angles": "~107",
        "hybridization": "sp3"
    },
    "AX2E2": {
        "steric_number": 4,
        "bonding_groups": 2,
        "lone_pairs": 2,
        "electron_geometry": "Tetrahedral",
        "molecular_geometry": "Bent",
        "bond_angles": "~104.5",
        "hybridization": "sp3"
    },
    "AX5": {
        "steric_number": 5,
        "bonding_groups": 5,
        "lone_pairs": 0,
        "electron_geometry": "Trigonal Bipyramidal",
        "molecular_geometry": "Trigonal Bipyramidal",
        "bond_angles": "90, 120, 180",
        "hybridization": "sp3d"
    },
    "AX4E": {
        "steric_number": 5,
        "bonding_groups": 4,
        "lone_pairs": 1,
        "electron_geometry": "Trigonal Bipyramidal",
        "molecular_geometry": "Seesaw",
        "bond_angles": "<90, <120",
        "hybridization": "sp3d"
    },
    "AX3E2": {
        "steric_number": 5,
        "bonding_groups": 3,
        "lone_pairs": 2,
        "electron_geometry": "Trigonal Bipyramidal",
        "molecular_geometry": "T-Shaped",
        "bond_angles": "<90",
        "hybridization": "sp3d"
    },
    "AX2E3": {
        "steric_number": 5,
        "bonding_groups": 2,
        "lone_pairs": 3,
        "electron_geometry": "Trigonal Bipyramidal",
        "molecular_geometry": "Linear",
        "bond_angles": "180",
        "hybridization": "sp3d"
    },
    "AX6": {
        "steric_number": 6,
        "bonding_groups": 6,
        "lone_pairs": 0,
        "electron_geometry": "Octahedral",
        "molecular_geometry": "Octahedral",
        "bond_angles": "90, 180",
        "hybridization": "sp3d2"
    },
    "AX5E": {
        "steric_number": 6,
        "bonding_groups": 5,
        "lone_pairs": 1,
        "electron_geometry": "Octahedral",
        "molecular_geometry": "Square Pyramidal",
        "bond_angles": "<90",
        "hybridization": "sp3d2"
    },
    "AX4E2": {
        "steric_number": 6,
        "bonding_groups": 4,
        "lone_pairs": 2,
        "electron_geometry": "Octahedral",
        "molecular_geometry": "Square Planar",
        "bond_angles": "90",
        "hybridization": "sp3d2"
    }
}
    if central_lone_pairs != 0:
        vsepr_form = f"AX{num_terminal_atoms}E{central_lone_pairs}"
    else:
        vsepr_form = f"AX{num_terminal_atoms}"
    e_geo = vsepr_table[vsepr_form]["electron_geometry"]
    mol_geo = vsepr_table[vsepr_form]["molecular_geometry"]
    hybridization = vsepr_table[vsepr_form]["hybridization"]
    bond_angles = vsepr_table[vsepr_form]["bond_angles"]

    print("Electron Geometry:", e_geo)
    print("Molecular Geometry:", mol_geo)
    print("Bond Hybridization:", hybridization)
    print("Bond Angle(s):", bond_angles)

    # [{'Element': 'H', 'Subscript': '2'}, {'Element': 'O', 'Subscript': '1'}]
   # Consider 2 electrons used for each bond shared between the core atom and another one.

    # If there are still leftover electrons assign them to the outer atoms as lone pairs.

    # If there are still more leftover electrons assign them to the central atom as lone pairs

    # If the central atom does not have enough electrons, needing at least 8, create more covalent bonds.

    # Check formal charges and if they can be reduced closer 0 do as that.



# Count the amount of electron pairs/clouds around the central atom; give the compounds its electron-group geo.
# ignore lone pairs and consider the greater space they take up to predict the molecular geometry.
def get_central_atom(molecule):
    matches = re.findall(r"([A-Z][a-z]?)(\d?)" ,molecule)

    elements = [atom for atom, _, in matches if atom]



    electronegativities = []
    no_h_elements = [e for e in elements if e != "H"]
    for element in no_h_elements:
            element_obj = get_element(element)
            electronegativities.append(element_obj.electronegativity())

    lowest_eneg = min(electronegativities)
    position = electronegativities.index(lowest_eneg)
    central_atom = no_h_elements[position]
    return central_atom

def get_total_valence(molecule):
    pure_ve_total = 0
    atom_matches = re.findall(r"([A-Z][a-z]?)(\d?)" ,molecule)
    for element, subscript, in atom_matches:
        if not element:
            continue


        try:
            ve = get_element(element).nvalence()

        except ValueError:
            sys.exit("Invalid Molecule")
        try:
            ve_part = ve * int(subscript)
        except ValueError:
            ve_part = ve * 1
        pure_ve_total += ve_part
    if charge_matches := re.search(r"(\d)?(\d)?(\+|-)$", molecule):
            if charge_matches.group(2) is None:
                charge_mag = 1
            else:
                charge_mag = int(charge_matches.group(2))
            charge_sign = charge_matches.group(3)
            if charge_sign == "+":
                ve_total = pure_ve_total - charge_mag
            else:
                ve_total = pure_ve_total + charge_mag
    else:
        ve_total = pure_ve_total
    return ve_total

def get_atoms_subscripts(molecule):

    matches = re.findall(r"([A-Z][a-z]?)(\d?)" ,molecule)
    elements_and_nums = []
    for element, subscript, in matches:

        if not element:
            continue

        if subscript == "":
            subscript = "1"

        element_w_num = {
            "Element": element,
            "Subscript": subscript,
            }
        elements_and_nums.append(element_w_num)
    return elements_and_nums
def lock_in(m):
    return None

def validate_formula(formula):
    try:
        result = search_chemical(formula)
        return True
    except ValueError:
        return False


# ex: [{'Element': 'H', 'Subscript': '2'}, {'Element': 'O', 'Subscript': '1'}]
if __name__ == "__main__":
    main()
