import pytest
from project import calculate_total_valence
from project import parse_atoms_subscripts
from project import determine_central_atom
from project import validate_formula
from project import fetch_structure_data

def test_parse_atoms_subscripts():
    assert parse_atoms_subscripts("NO3-") == [{'Element': 'N', 'Subscript': '1'}, {'Element': 'O', 'Subscript': '3'}]
    assert parse_atoms_subscripts("H2O") == [{'Element': 'H', 'Subscript': '2'}, {'Element': 'O', 'Subscript': '1'}]
    assert parse_atoms_subscripts("CO2") == [{'Element': "C", 'Subscript': '1'},{'Element': 'O', 'Subscript': '2'}]


def test_calculate_total_valence():
    assert calculate_total_valence("NH4+") == 8
    assert calculate_total_valence("H2O") == 8
    assert calculate_total_valence("CO32-") == 24

def test_determine_central_atom():
    assert determine_central_atom("H2O") == "O"
    assert determine_central_atom("NO3-") == "N"
    assert determine_central_atom("CH4") == "C"
    assert determine_central_atom("XeF4") == "Xe"

def test_validate_formula():
    assert validate_formula("NH4+") == True
    assert validate_formula("H2O") == True
    assert validate_formula("CO2") == True
    assert validate_formula("NH3") == True

    assert validate_formula("HAPPY") == False
    assert validate_formula("HA2PP6Y1") == False
    assert validate_formula("asjdhsa@&@&;") == False

def test_fetch_structure_data():
    assert fetch_structure_data([{'Element': 'H', 'Subscript': '2'}, {'Element': 'O', 'Subscript': '1'}], 8, "O") == (2, ['H','H'])
    assert fetch_structure_data([{'Element': 'N', 'Subscript': '1'}, {'Element': 'H', 'Subscript': '3'}], 8, "N") == (1, ['H', 'H', 'H'])
    assert fetch_structure_data([{'Element': 'C', 'Subscript': '1'}, {'Element': 'H', 'Subscript': '4'}], 8, "C") == (0, ['H', 'H', 'H', 'H'])
    assert fetch_structure_data([{'Element': 'C', 'Subscript': '1'}, {'Element': 'O', 'Subscript': '2'}], 16, "C") == (0, ['O', 'O'])
    assert fetch_structure_data([{'Element': 'B', 'Subscript': '1'}, {'Element': 'F', 'Subscript': '3'}], 24, "B") == (0, ['F', 'F', 'F'])

# test_fetch_structure_data(elements_and_nums, ve_total, central_atom)
# returns lone_pairs and terminal atoms
