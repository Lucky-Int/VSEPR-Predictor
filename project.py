
# Try writing Double and Triple bond code. And create the final lewis structure.
# VSEPR Predictor and Modeler
# rename property so variable names don't collide
from mendeleev import element as get_element
import re
import sys
from chemicals import search_chemical

def main():
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
    # Error Checking and input
    print(
    "Welcome to VSEPR Predictor! "
    )
    raw_input = input("Molecule: ")
    if not validate_formula(raw_input):
        sys.exit("Not a valid molecule (please disclude starting coefficient, if applicable)")
    molecule = raw_input

    me = range(1)
    for motivation in me:
        lock_in(motivation)

    print("-" * 120)

    # Count the number of Valence Electrons in the compound-- consider the charge as well.



    # Perhaps uneccesary to find coefficient ^^^
    elements_and_nums = parse_atoms_subscripts(molecule)
    ve_total = calculate_total_valence(molecule)
    try:
        central_atom = determine_central_atom(molecule)
    except ValueError:
        sys.exit("There must be a central atom present. If there are only 2 elements in the given input, know that the molecular geometry of the shape is Linear.")

    central_lone_pairs, terminal_atoms = fetch_structure_data(elements_and_nums, ve_total, central_atom)
    num_terminal_atoms = len(terminal_atoms)
    steric_number = central_lone_pairs + num_terminal_atoms
    if steric_number > 6:
        sys.exit("Sorry, pick a molecule with less than 7 electron groups / with one central atom. Try picking a molecule with less elements.")






    # go on with adding double or triple bonds. (If formal_charge_central != 0).









    # Search all data.
    if central_lone_pairs == 1:
        vsepr_form = f"AX{num_terminal_atoms}E"

        e_geo = vsepr_table[vsepr_form]["electron_geometry"]

    elif central_lone_pairs != 0:
        vsepr_form = f"AX{num_terminal_atoms}E{central_lone_pairs}"
        e_geo = vsepr_table[vsepr_form]["electron_geometry"]

    else:
        vsepr_form = f"AX{num_terminal_atoms}E"

        e_geo = vsepr_table[vsepr_form]["electron_geometry"]


    mol_geo = vsepr_table[vsepr_form]["molecular_geometry"]
    hybridization = vsepr_table[vsepr_form]["hybridization"]
    bond_angles = vsepr_table[vsepr_form]["bond_angles"]

    element_one = elements_and_nums[0]['Element']
    sub_element_one = int(elements_and_nums[0]['Subscript'])
    element_two = elements_and_nums[1]['Element']
    sub_element_two = int(elements_and_nums[1]['Subscript'])

    print(f"""Alright, first we have to calculate the total number of valence electrons we have.
   """)
    while True:
        ve_input = int(input("Can you calculate the total number of Valence Electrons? Answer Here: "))
        if ve_input == ve_total:
            break
        elif ve_input == "HINT":
             print(f"""We see that we have {sub_element_one} {element_one} molecules and {sub_element_two} {element_two} molecules.
We can then calculate the valence electrons for each part. Looking at a periodic table, {element_one} has {get_element(element_one).nvalence()} valence electrons
and we have {sub_element_one} of them. Therefore, we multiply {get_element(element_one).nvalence()} valence electrons per molecule by {sub_element_one} molecule(s) to get {sub_element_one * get_element(element_one).nvalence()} valence electrons.
The same process goes straight-forwardly for the other parts, and we get the total number of Valence Electrons: ???)""")

        elif ve_input == "SKIP":
            print(f"The total amount of valence electrons is {ve_total}!")
            break
        else:
            print("That is incorrect! Try again, or type HINT for a hint; SKIP to reveal the answer (these keywords will work for any time in this program when you need them).")

    print("""Great! Now that we have the total number of valence electrons, we can use this to create out partial lewis structure, and then figure out our lone pairs and electron groups.
    Now, let's go step by step. First, we have to find the central atom of our molecule.""")

    while True:
        central_atom_input = input("Now, can you find the Central Atom for our molecule? Central Atom (Type here): ")
        if central_atom_input == central_atom:
            print(f"Correct! Our central atom is indeed {central_atom}.")
            break
        elif central_atom_input == "HINT":
            print("""Okay, you asked for a hint. The central atom is the atom which is least electronegative amoung all the elements present in the molecule.
            To figure this out, you need to look at a periodic table and remember the patterns in them, or you can use your knowledge about electronegativites if you have it.
            If this is difficult for you, use an electronegativites chart (like the Pauling Scale periodic table of electronegativites) or type SKIP if it is too difficult!""")
        elif central_atom_input == "SKIP":
            print(f""""The central atom of this molecule is {central_atom}.
            We can figure this out by know""" )



    print(elements_and_nums)
    print(f"Valence Electrons: {ve_total}")
    print(f"Central Atom: {central_atom}")
    print("Lone Pairs:", central_lone_pairs)
    print("Electron Groups / Steric Number:", steric_number)
    print("Terminal Atoms:", terminal_atoms)
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

def fetch_structure_data(elements_and_nums, ve_total, central_atom,):
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

        central_lone_pairs = int(track_ve / 2)

        track_ve = 0
        central_electrons = central_lone_pairs * 2 + num_terminal_atoms
    # check formal charge of central atom
        central_atom_valence = get_element(central_atom).nvalence()
        central_formal_charge = central_atom_valence - central_electrons
        # ^^ Might use central_formal_charge for creating the double and triple bonds later

    else:
        central_electrons = num_terminal_atoms
        central_formal_charge = get_element(central_atom).nvalence() - central_electrons
        central_lone_pairs = 0
    return central_lone_pairs, terminal_atoms


def determine_central_atom(molecule):
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

def calculate_total_valence(molecule):
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

def parse_atoms_subscripts(molecule):

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
        search_chemical(formula)
        return True
    except ValueError:
        return False


# ex: [{'Element': 'H', 'Subscript': '2'}, {'Element': 'O', 'Subscript': '1'}]
if __name__ == "__main__":
    main()
