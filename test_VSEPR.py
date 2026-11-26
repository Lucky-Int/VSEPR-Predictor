import sys
from api.VSEPR import (
    calculate_total_valence,
    parse_atoms_subscripts,
    determine_central_atom,
    validate_formula,
    fetch_structure_data,
)

def test_parse_atoms_subscripts():
    assert parse_atoms_subscripts("NO3-") == [{'Element': 'N', 'Subscript': '1'}, {'Element': 'O', 'Subscript': '3'}]
    assert parse_atoms_subscripts("H2O") == [{'Element': 'H', 'Subscript': '2'}, {'Element': 'O', 'Subscript': '1'}]
    assert parse_atoms_subscripts("CO2") == [{'Element': "C", 'Subscript': '1'}, {'Element': 'O', 'Subscript': '2'}]

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
    assert fetch_structure_data([{'Element': 'H', 'Subscript': '2'}, {'Element': 'O', 'Subscript': '1'}], 8, "O") == (2, ['H', 'H'])
    assert fetch_structure_data([{'Element': 'N', 'Subscript': '1'}, {'Element': 'H', 'Subscript': '3'}], 8, "N") == (1, ['H', 'H', 'H'])
    assert fetch_structure_data([{'Element': 'C', 'Subscript': '1'}, {'Element': 'H', 'Subscript': '4'}], 8, "C") == (0, ['H', 'H', 'H', 'H'])
    assert fetch_structure_data([{'Element': 'C', 'Subscript': '1'}, {'Element': 'O', 'Subscript': '2'}], 16, "C") == (0, ['O', 'O'])
    assert fetch_structure_data([{'Element': 'B', 'Subscript': '1'}, {'Element': 'F', 'Subscript': '3'}], 24, "B") == (0, ['F', 'F', 'F'])

def run_self_tests():
    assertions = [
        ("parse_atoms_subscripts (NO3-)", lambda: parse_atoms_subscripts("NO3-") == [{'Element': 'N', 'Subscript': '1'}, {'Element': 'O', 'Subscript': '3'}]),
        ("parse_atoms_subscripts (H2O)", lambda: parse_atoms_subscripts("H2O") == [{'Element': 'H', 'Subscript': '2'}, {'Element': 'O', 'Subscript': '1'}]),
        ("parse_atoms_subscripts (CO2)", lambda: parse_atoms_subscripts("CO2") == [{'Element': "C", 'Subscript': '1'}, {'Element': 'O', 'Subscript': '2'}]),
        ("calculate_total_valence (NH4+)", lambda: calculate_total_valence("NH4+") == 8),
        ("calculate_total_valence (H2O)", lambda: calculate_total_valence("H2O") == 8),
        ("calculate_total_valence (CO32-)", lambda: calculate_total_valence("CO32-") == 24),
        ("determine_central_atom (H2O)", lambda: determine_central_atom("H2O") == "O"),
        ("determine_central_atom (NO3-)", lambda: determine_central_atom("NO3-") == "N"),
        ("determine_central_atom (CH4)", lambda: determine_central_atom("CH4") == "C"),
        ("determine_central_atom (XeF4)", lambda: determine_central_atom("XeF4") == "Xe"),
        ("validate_formula (NH4+)", lambda: validate_formula("NH4+") is True),
        ("validate_formula (H2O)", lambda: validate_formula("H2O") is True),
        ("validate_formula (CO2)", lambda: validate_formula("CO2") is True),
        ("validate_formula (NH3)", lambda: validate_formula("NH3") is True),
        ("validate_formula (HAPPY)", lambda: validate_formula("HAPPY") is False),
        ("validate_formula (HA2PP6Y1)", lambda: validate_formula("HA2PP6Y1") is False),
        ("validate_formula (invalid chars)", lambda: validate_formula("asjdhsa@&@&;") is False),
        ("fetch_structure_data (H2O)", lambda: fetch_structure_data([{'Element': 'H', 'Subscript': '2'}, {'Element': 'O', 'Subscript': '1'}], 8, "O") == (2, ['H', 'H'])),
        ("fetch_structure_data (NH3)", lambda: fetch_structure_data([{'Element': 'N', 'Subscript': '1'}, {'Element': 'H', 'Subscript': '3'}], 8, "N") == (1, ['H', 'H', 'H'])),
        ("fetch_structure_data (CH4)", lambda: fetch_structure_data([{'Element': 'C', 'Subscript': '1'}, {'Element': 'H', 'Subscript': '4'}], 8, "C") == (0, ['H', 'H', 'H', 'H'])),
        ("fetch_structure_data (CO2)", lambda: fetch_structure_data([{'Element': 'C', 'Subscript': '1'}, {'Element': 'O', 'Subscript': '2'}], 16, "C") == (0, ['O', 'O'])),
        ("fetch_structure_data (BF3)", lambda: fetch_structure_data([{'Element': 'B', 'Subscript': '1'}, {'Element': 'F', 'Subscript': '3'}], 24, "B") == (0, ['F', 'F', 'F'])),
    ]

    passed = 0
    failed = 0
    for name, check in assertions:
        try:
            assert check(), f"Assertion failed for {name}"
            passed += 1
        except Exception as e:
            failed += 1
            print(f"FAIL: {name} -> {e}")

    print(f"Passed: {passed}/{len(assertions)} | Failed: {failed}")
    sys.exit(1 if failed else 0)

if __name__ == "__main__":
    if "--test" in sys.argv:
        run_self_tests()
