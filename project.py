# Next up --> Clean up code to create functions like get_valence_total() and get_central_atom()
# Next up --> start creating abstract lewis structure: central atom to terminal atoms covalent bonds. 2 V.E each.


# VSEPR Predictor and Modeler
# rename property so variable names don't collide
from mendeleev import element as get_element
import re
import sys
from chemicals import search_chemical

def main():
    molecule = input("Molecule: ")
    if not validate_formula(molecule):
        sys.exit("Not a valid molecule")


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
    matches = re.findall(r"([A-Z][a-z]?)(\d?)" ,no_c_molecule)
    elements = []
    elements_and_nums = []
    pure_ve_total = 0
    for element, subscript, in matches:
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
        pure_ve_total += ve_part
    if matches := re.search(r"(\d)?(\+|-)$", molecule):
        if matches.group(1) is None:
            charge_mag = 1
        else:
            charge_mag = int(matches.group(1))
        charge_sign = matches.group(2)
        if charge_sign == "+":
            ve_total = pure_ve_total - charge_mag
        else:
            ve_total = pure_ve_total + charge_mag
    else:
        ve_total = pure_ve_total
    # find element with lowest electronegativity (central atom, excluding hydrogen)
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


def get_central_atom():
    ...

def get_total_valence():
    ...
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
