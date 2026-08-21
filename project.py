# Next up --> Clean up code to create functions like get_valence_total() and get_central_atom()
# Next up --> start creating abstract lewis structure: central atom to terminal atoms covalent bonds. 2 V.E each.

# FIX +- CHARGE LOGIC; SUBSCRIPTS COLLIDING. URGENCY: !!!
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




    for _ in range(120):
        print("-", end = "")
    print()

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



        ve = get_element(element).nvalence()
        try:
            ve_part = ve * int(subscript)
        except ValueError:
            ve_part = ve * 1
        pure_ve_total += ve_part
    if charge_matches := re.search(r"(\d)?(\+|-)$", molecule):
            if charge_matches.group(1) is None:
                charge_mag = 1
            else:
                charge_mag = int(charge_matches.group(1))
            charge_sign = charge_matches.group(2)
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


    # Consider 2 electrons used for each bond shared between the core atom and another one.

    # If there are still leftover electrons assign them to the outer atoms as lone pairs.

    # If there are still more leftover electrons assign them to the central atom as lone pairs

    # If the central atom does not have enough electrons, needing at least 8, create more covalent bonds.

    # Check formal charges and if they can be reduced closer 0 do as that.



# Count the amount of electron pairs/clouds around the central atom; give the compounds its electron-group geo.
# ignore lone pairs and consider the greater space they take up to predict the molecular geometry.
if __name__ == "__main__":
    main()
