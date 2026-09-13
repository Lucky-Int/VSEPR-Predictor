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
            "hybridization": "sp",
        },
        "AX3": {
            "steric_number": 3,
            "bonding_groups": 3,
            "lone_pairs": 0,
            "electron_geometry": "Trigonal Planar",
            "molecular_geometry": "Trigonal Planar",
            "bond_angles": "120",
            "hybridization": "sp2",
        },
        "AX2E": {
            "steric_number": 3,
            "bonding_groups": 2,
            "lone_pairs": 1,
            "electron_geometry": "Trigonal Planar",
            "molecular_geometry": "Bent",
            "bond_angles": "<120",
            "hybridization": "sp2",
        },
        "AX4": {
            "steric_number": 4,
            "bonding_groups": 4,
            "lone_pairs": 0,
            "electron_geometry": "Tetrahedral",
            "molecular_geometry": "Tetrahedral",
            "bond_angles": "109.5",
            "hybridization": "sp3",
        },
        "AX3E": {
            "steric_number": 4,
            "bonding_groups": 3,
            "lone_pairs": 1,
            "electron_geometry": "Tetrahedral",
            "molecular_geometry": "Trigonal Pyramidal",
            "bond_angles": "~107",
            "hybridization": "sp3",
        },
        "AX2E2": {
            "steric_number": 4,
            "bonding_groups": 2,
            "lone_pairs": 2,
            "electron_geometry": "Tetrahedral",
            "molecular_geometry": "Bent",
            "bond_angles": "~104.5",
            "hybridization": "sp3",
        },
        "AX5": {
            "steric_number": 5,
            "bonding_groups": 5,
            "lone_pairs": 0,
            "electron_geometry": "Trigonal Bipyramidal",
            "molecular_geometry": "Trigonal Bipyramidal",
            "bond_angles": "90, 120, 180",
            "hybridization": "sp3d",
        },
        "AX4E": {
            "steric_number": 5,
            "bonding_groups": 4,
            "lone_pairs": 1,
            "electron_geometry": "Trigonal Bipyramidal",
            "molecular_geometry": "Seesaw",
            "bond_angles": "<90, <120",
            "hybridization": "sp3d",
        },
        "AX3E2": {
            "steric_number": 5,
            "bonding_groups": 3,
            "lone_pairs": 2,
            "electron_geometry": "Trigonal Bipyramidal",
            "molecular_geometry": "T-Shaped",
            "bond_angles": "<90",
            "hybridization": "sp3d",
        },
        "AX2E3": {
            "steric_number": 5,
            "bonding_groups": 2,
            "lone_pairs": 3,
            "electron_geometry": "Trigonal Bipyramidal",
            "molecular_geometry": "Linear",
            "bond_angles": "180",
            "hybridization": "sp3d",
        },
        "AX6": {
            "steric_number": 6,
            "bonding_groups": 6,
            "lone_pairs": 0,
            "electron_geometry": "Octahedral",
            "molecular_geometry": "Octahedral",
            "bond_angles": "90, 180",
            "hybridization": "sp3d2",
        },
        "AX5E": {
            "steric_number": 6,
            "bonding_groups": 5,
            "lone_pairs": 1,
            "electron_geometry": "Octahedral",
            "molecular_geometry": "Square Pyramidal",
            "bond_angles": "<90",
            "hybridization": "sp3d2",
        },
        "AX4E2": {
            "steric_number": 6,
            "bonding_groups": 4,
            "lone_pairs": 2,
            "electron_geometry": "Octahedral",
            "molecular_geometry": "Square Planar",
            "bond_angles": "90",
            "hybridization": "sp3d2",
        },
    }
    # Error Checking and input
    print("Welcome to VSEPR Predictor! ")
    molecule = input("Molecule: ")
    if not validate_formula(molecule):
        sys.exit(
            "Not a valid molecule (please disclude starting coefficient, if applicable)"
        )

    print("-" * 120)

    # Count the number of Valence Electrons in the compound-- consider the charge as well.

    elements_and_nums = parse_atoms_subscripts(molecule)
    ve_total = calculate_total_valence(molecule)
    try:
        central_atom = determine_central_atom(molecule)
    except ValueError:
        sys.exit(
            "There must be a central atom present. If there are only 2 elements in the given input, know that the molecular geometry of the shape is Linear."
        )
    try:
        central_lone_pairs, terminal_atoms = fetch_structure_data(
            elements_and_nums, ve_total, central_atom
        )
    except ValueError:
        sys.exit(
            f"""{molecule} is a radical. This means the molecule has a lone electron around the central electron, due to the odd number of valence electrons.
Unfortunately, simple VSEPR theory cannot reliably predict the shapes of these radicals; as, a single electron repels, but not as much as a lone pair.
As a result, experimental data or otherwise strict quantum mechanics is needed to mathematically predict the shape of this molecule."""
        )
    if not terminal_atoms:
        sys.exit(
            f"{molecule} has no terminal atoms. Diatomic molecules, including this one, are Linear by definition."
        )
    num_terminal_atoms = len(terminal_atoms)
    steric_number = central_lone_pairs + num_terminal_atoms
    if steric_number > 6:
        sys.exit(
            "Sorry, pick a molecule with less than 7 electron groups / with one central atom. Try picking a molecule with less elements."
        )

    # go on with adding double or triple bonds. (If formal_charge_central != 0).

    # Search all data.
    if central_lone_pairs == 1:
        vsepr_form = f"AX{num_terminal_atoms}E"

    elif central_lone_pairs != 0:
        vsepr_form = f"AX{num_terminal_atoms}E{central_lone_pairs}"

    else:
        vsepr_form = f"AX{num_terminal_atoms}"

    try:
        e_geo = vsepr_table[vsepr_form]["electron_geometry"]
    except KeyError:
        sys.exit(
            f"Sorry, {molecule} has no defined central atom. By definition, these diatomic molecules have a Linear geometry."
        )

    no_h_terminal_atoms = [a for a in terminal_atoms if a != "H"]
    mol_geo = vsepr_table[vsepr_form]["molecular_geometry"]
    hybridization = vsepr_table[vsepr_form]["hybridization"]
    bond_angles = vsepr_table[vsepr_form]["bond_angles"]

    element_one = elements_and_nums[0]["Element"]
    sub_element_one = int(elements_and_nums[0]["Subscript"])
    element_two = elements_and_nums[1]["Element"]
    sub_element_two = int(elements_and_nums[1]["Subscript"])

    print(f"""
    Alright, first we have to calculate the total number of valence electrons we have.
    """)
    all_skip = False
    while all_skip == False:
        while True:

            ve_input = input(
                "\nCan you calculate the total number of Valence Electrons? Answer Here: "
            )

            if ve_input.isalpha() and ve_input.upper().strip() == "HINT":
                print(
                    f"""
    We see that we have {sub_element_one} {element_one} molecule(s) and {sub_element_two} {element_two} molecule(s).
We can then calculate the valence electrons for each part. Looking at a periodic table, {element_one} has {get_element(element_one).nvalence()} valence electrons
and we have {sub_element_one} of them. Therefore, we multiply {get_element(element_one).nvalence()} valence electrons per molecule by {sub_element_one} molecule(s) to get {sub_element_one * get_element(element_one).nvalence()} valence electrons.
The same process goes straight-forwardly for the other parts, and we get the total number of Valence Electrons: ???)"""
                )
            elif ve_input.isalpha() and ve_input.upper().strip() == "SKIP":
                print(f"\nThe total amount of valence electrons is {ve_total}!")
                break

            elif ve_input.isdigit() and int(ve_input) == ve_total:
                print("\nWow, that's correct!")
                break
            elif str(ve_input).upper().strip() == "ALL SKIP":
                all_skip = True
                break
            else:
                print(
                    "\nThat is incorrect! Please try again, or type HINT for a hint; SKIP to reveal the answer; ALL SKIP to skip all questions (these keywords will work for any time in this program when you need them)."
                )
        if all_skip:
            break

        print(f"""
    {"-" * 50}
    Great! Now that we have the total number of valence electrons, we can use this to create out partial lewis structure, and then figure out our lone pairs and electron groups.
First, we have to find the central atom of our molecule.
    {"-" * 50}""")

        while True:

            central_atom_input = input(
                "\nNow, can you find the Central Atom for our molecule? Central Atom (Type here): "
            )

            if central_atom_input == central_atom:
                print(f"\nCorrect! Our central atom is indeed {central_atom}.")
                break

            elif (
                central_atom_input.isalpha()
                and central_atom_input.upper().strip() == "HINT"
            ):
                print("""
    Okay, you asked for a hint. The central atom is the atom which is least electronegative amoung all the elements present in the molecule.
    To figure this out, you need to look at a periodic table and remember the patterns in them, or you can use your knowledge about electronegativites if you have it.
    If this is difficult for you, use an electronegativites chart (like the Pauling Scale periodic table of electronegativites) or type SKIP if it is too difficult!
    Note that Hydrogen is never a central atom.""")

            elif (
                central_atom_input.isalpha()
                and central_atom_input.upper().strip() == "SKIP"
            ):
                print(
                    f"""
    The central atom of this molecule is {central_atom}.
    We can figure this out by knowing that {central_atom} is the least electronegative of the elements in this molecule (besides hydrogen)."""
                )
                break

            elif str(central_atom_input).upper().strip() == "ALL SKIP":
                all_skip = True
                break
            else:
                print(
                    "\nThat's unfortunately incorrect! Please try again, or remember that you can: type HINT for a hint; SKIP to reveal the answer; ALL SKIP to skip all questions (these keywords will work for any time in this program when you need them as aforementioned!). "
                )
        if all_skip:
            break
        print(f"""
        {"-" * 50}


        Now, we want the terminal atoms to have 8 valence electrons, fulfulling the 'octet-rule'. This is true for all atoms but hydrogen, which
only needs 2 valence electrons to become stable.

        We will add lone pairs of electrons (2 per) to these terminal atoms that need it, to reach the octet rule.
        {"-" * 50}""")

        while True:
            track_ve = input(
                "\nWhen we do this process, fulfulling octet rules for every terminal atom (except for hydrogen), how many electrons do we have after the process? Answer here: "
            )

            if track_ve.upper().strip() == "HINT":
                print(
                    "\nYou want a hint?-- You get a hint! Remember that these terminal atoms need to have 8 electrons. Right now, they have 2!"
                    "So we have to add 6 electrons for each one of those terminal atoms. Then, subtract our original total from the number used to assign to the terminal atoms in order to get the correct answer."
                )

            elif track_ve.upper().strip() == "SKIP":
                print(
                    f"""\nThe correct answer is {ve_total - 6*len(no_h_terminal_atoms)} valence electrons.
We get this by knowing that we need 6 more electrons for every terminal atom but hydrogen, yielding us 6 times the number of terminal atoms
that are not hydrogen as how many valence electrons we used. We then subract this number from our original valence electron total to get our answer."""
                )
                break

            elif track_ve.upper().strip() == "ALL SKIP":
                all_skip = True
                break

            elif track_ve == str(ve_total - 6 * len(no_h_terminal_atoms)):
                print(
                    f"""Amazing! That's correct-- we will indeed have {ve_total - 6*len(no_h_terminal_atoms)} valence electrons left."""
                )
                break

            else:
                print(
                    f"""Sorry, your answer is incorrect. Please try again, or type: HINT for a hint; SKIP to skip; ALL SKIP to skip all questions."""
                )
        if all_skip:
            break

        if ve_total - 6 * len(no_h_terminal_atoms) == 0:
            print(f"""
            {"-" * 50}
            Since we have 0 valence electrons left, we are DONE! We have what we need and we can now count electron groups and lone pairs.
            {"-"*50}""")

        else:

            print(f"""
            {"-" * 50}
            Since we still have valence electrons left, we still have more to go. We will now assign these leftover electrons to the central atom.
            We will do this in lone pairs (2 per*).

            * Remember that lone pairs have 2 electrons in them.
            {"-"*50}""")
            while True:
                ans_lone_pairs = input(
                    "\nHow many lone pairs will we have on the central atom? Answer Here: "
                )

                if ans_lone_pairs == str(central_lone_pairs):
                    print(
                        f"""\nNice! Just as you stated, we have {central_lone_pairs} lone pairs."""
                    )
                    break

                elif ans_lone_pairs.upper().strip() == "HINT":
                    print(
                        f"""\nHere's hint for you! We have {ve_total - 6*len(no_h_terminal_atoms)} left,
                so we will assign all of them and therefore there will be ??? lone pairs around the central atom."""
                    )

                elif ans_lone_pairs.upper().strip() == "SKIP":
                    print(
                        f"""\nThat's alright! The correct answer is {(ve_total - 6*len(no_h_terminal_atoms))/2} Lone Pairs.
    This is because we had {(ve_total - 6*len(no_h_terminal_atoms))} left, therefore we have to assign all
    of those electrons to the central atom in lone pairs (pairs of 2). To put it simply, divide the amount of valence electrons
    we previously had by 2 to get our answer! """
                    )
                    break

                elif ans_lone_pairs.upper().strip() == "ALL SKIP":
                    all_skip = True
                    break

                else:
                    print(
                        """\nYour answer is close (I hope)! Remember that you can type: 'HINT' for a hint; 'SKIP' to skip;
                    'ALL SKIP' to skip all questions."""
                    )
                if all_skip:
                    break
        print(
            f"""We are done drawing our partial lewis structure, leaving out triple and double bonds.
Steric number/ electron groups = bonding terminal atoms + lone pairs.
We have {steric_number}  electron groups, which is also our steric number.

This means that-- by looking at a table, by memorization, or by intuition-- the molecular geometry is {mol_geo}
and when accounting for the lone pairs (if any), the electron geometry is {e_geo}
Below is the summarized info as well as more we can figure out using the steric number and the knowledge we gained:
 """
        )
        break

    print()
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


def fetch_structure_data(
    elements_and_nums,
    ve_total,
    central_atom,
):
    num_terminal_atoms = 0
    terminal_atoms = []
    for part in elements_and_nums:
        if part["Element"] != central_atom:
            num_terminal_atoms += int(part["Subscript"])
            for _ in range(int(part["Subscript"])):
                terminal_atoms.append(part["Element"])

        track_ve = ve_total - 2 * num_terminal_atoms
        if track_ve != 0:
            for terminal_atom in terminal_atoms:
                if terminal_atom != "H":
                    track_ve -= 6

    # add lone pairs if needed
    if track_ve > 0:

        central_lone_pairs, extra_electrons = divmod(track_ve, 2)

        track_ve = 0
        if extra_electrons != 0:
            raise ValueError(
                "This molecule is a radical. VSEPR Theory cannot reliably calculate the geometries of these molecules; please try a different molecule."
            )

        # central_electrons = central_lone_pairs * 2 + num_terminal_atoms

    # check formal charge of central atom
    # central_electrons = (central_lone_pairs * 2) + extra_electrons + num_terminal_atoms
    # central_atom_valence = get_element(central_atom).nvalence()
    # central_formal_charge = central_atom_valence - central_electrons
    # ^^ Might use central_formal_charge for creating the double and triple bonds later

    else:
        central_lone_pairs = 0
    return central_lone_pairs, terminal_atoms


def determine_central_atom(molecule):
    matches = re.findall(r"([A-Z][a-z]?)(\d?)", molecule)

    elements = [atom for atom, _, in matches if atom]
    no_h_elements = [e for e in elements if e != "H"]
    if not no_h_elements:
        raise ValueError("no non-hydrogen atom available")
    # use set to remove duplicates
    if len(set(elements)) < 2:
        raise ValueError(f"{molecule} has no distinct central atom.")

    electronegativities = []
    for element in no_h_elements:
        element_obj = get_element(element)
        electronegativities.append(element_obj.electronegativity())

    lowest_eneg = min(electronegativities)
    position = electronegativities.index(lowest_eneg)
    central_atom = no_h_elements[position]
    return central_atom


def calculate_total_valence(molecule):
    pure_ve_total = 0
    atom_matches = re.findall(r"([A-Z][a-z]?)(\d?)", molecule)
    for (
        element,
        subscript,
    ) in atom_matches:
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

    matches = re.findall(r"([A-Z][a-z]?)(\d?)", molecule)
    elements_and_nums = []
    for (
        element,
        subscript,
    ) in matches:

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


def validate_formula(formula):
    try:
        search_chemical(formula)
        return True
    except ValueError:
        return False


# ex: [{'Element': 'H', 'Subscript': '2'}, {'Element': 'O', 'Subscript': '1'}]
if __name__ == "__main__":
    main()
