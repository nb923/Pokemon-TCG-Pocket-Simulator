import pytest
from unittest.mock import MagicMock
from pokemon_file_reader import PokemonFileReader

@pytest.fixture
def reader():
    """Creates an instance of PokemonFileReader."""

    return PokemonFileReader()

@pytest.fixture
def mock_import(monkeypatch):
    """Attaches a mock function for importlib.import_module using monkeypatch."""

    def _mock_import(input_file):
        """Creates a mock function for importlib.import_module with example module functions."""

        mock_standard = MagicMock()
        mock_custom = MagicMock()
    
        def mock_effect_function_one():
            return "Thunderbolt Attack"
    
        def mock_effect_function_two():
            return "Fire Blast Attack"
    
        def mock_effect_function_three():
            return "Blizzard Attack"
    
        def mock_effect_function_four():
            return "Proton Beam Attack"
    
        def mock_effect_function_five():
            return "Crystal Rush Attack"
    
        mock_standard.thunderbolt_effect = mock_effect_function_one
        mock_standard.fire_blast_effect = mock_effect_function_two
        mock_standard.blizzard_effect = mock_effect_function_three
        mock_custom.proton_beam_effect = mock_effect_function_four
        mock_custom.crystal_rush_effect = mock_effect_function_five

        if input_file == "pokemon_standard_move_effect_list":
            return mock_standard
        elif input_file == "pokemon_custom_move_effect_list":
            return mock_custom
        else:
            raise Exception("Invalid input file")
    
    monkeypatch.setattr("importlib.import_module", _mock_import)

@pytest.fixture
def mock_files(monkeypatch):
    """Returns a dynamic version of a mock for if each file exists and the contents of each file."""

    def _mock_files(file_exists_map):
        """Creates a mock function for pathlib.Path.exists."""

        def mock_exists(path):
            """Mimics pathlib.Path.exists using file_exists_map."""

            return file_exists_map.get(str(path), False)
        
        monkeypatch.setattr("pathlib.Path.exists", mock_exists)
    
    return _mock_files

def test_perfect_format_standard_move_effect(reader, mock_import, mock_files):
    """Test if format string is perfect and effect function is in standard"""
    move_text = "Move Name: Thunderbolt, Energies: Electric; Electric, Damage: 50, Effect Function: thunderbolt_effect"
    reader.types = {"Electric"}
    file_exists_map = {
        "pokemon_standard_move_effect_list.py": True,
        "pokemon_custom_move_effect_list.py": True,
    }

    mock_files(file_exists_map)
    move = reader.read_move(move_text)

    assert move is not None
    assert move.name == "Thunderbolt"
    assert move.energy == ["Electric", "Electric"]
    assert move.damage == 50
    assert move.effect() == "Thunderbolt Attack"

def test_perfect_format_custom_move_effect(reader, mock_import, mock_files):
    """Test if format string is perfect and effect function is in custom"""
    move_text = "Move Name: Crystal Rush, Energies: Crystal; Crystal; Colorless, Damage: 70, Effect Function: crystal_rush_effect"
    reader.types = {"Crystal", "Colorless"}
    file_exists_map = {
        "pokemon_standard_move_effect_list.py": True,
        "pokemon_custom_move_effect_list.py": True,
    }

    mock_files(file_exists_map)
    move = reader.read_move(move_text)

    assert move is not None
    assert move.name == "Crystal Rush"
    assert move.energy == ["Crystal", "Crystal", "Colorless"]
    assert move.damage == 70
    assert move.effect() == "Crystal Rush Attack"

def test_perfect_format_no_move_effect_modules_exist(reader, mock_import, mock_files, caplog):
    """Test if format string is perfect and effect function modules are missing"""
    move_text = "Move Name: Crystal Rush, Energies: Crystal; Crystal; Colorless, Damage: 70, Effect Function: crystal_rush_effect"
    reader.types = {"Crystal", "Colorless"}
    file_exists_map = {
        "pokemon_standard_move_effect_list.py": False,
        "pokemon_custom_move_effect_list.py": False,
    }

    mock_files(file_exists_map)

    with caplog.at_level("DEBUG"):
        move = reader.read_move(move_text)

    assert move is None
    assert "Move effect modules are not present" in caplog.text

def test_perfect_format_move_effect_not_in_standard(reader, mock_import, mock_files, caplog):
    """Test if format string is perfect and effect function not in standard"""
    move_text = "Move Name: Crystal Rush, Energies: Crystal; Crystal; Colorless, Damage: 70, Effect Function: crystal_rush_effect"
    reader.types = {"Crystal", "Colorless"}
    file_exists_map = {
        "pokemon_standard_move_effect_list.py": True,
        "pokemon_custom_move_effect_list.py": False,
    }

    mock_files(file_exists_map)

    with caplog.at_level("DEBUG"):
        move = reader.read_move(move_text)

    assert move is None
    assert f"Move effect function does not exist for move: {move_text}" in caplog.text

def test_perfect_format_move_effect_not_in_custom(reader, mock_import, mock_files, caplog):
    """Test if format string is perfect and effect function not in custom"""
    move_text = "Move Name: Thunderbolt, Energies: Electric; Electric, Damage: 50, Effect Function: thunderbolt_effect"
    reader.types = {"Electric"}
    file_exists_map = {
        "pokemon_standard_move_effect_list.py": False,
        "pokemon_custom_move_effect_list.py": True,
    }

    mock_files(file_exists_map)

    with caplog.at_level("DEBUG"):
        move = reader.read_move(move_text)

    assert move is None
    assert f"Move effect function does not exist for move: {move_text}" in caplog.text

def test_perfect_format_move_effect_not_in_modules(reader, mock_import, mock_files, caplog):
    """Test if format string is perfect and effect function not in either module"""
    move_text = "Move Name: Zap Cannon, Energies: Electric; Electric, Damage: 100, Effect Function: zap_cannon_effect"
    reader.types = {"Electric"}
    file_exists_map = {
        "pokemon_standard_move_effect_list.py": True,
        "pokemon_custom_move_effect_list.py": True,
    }

    mock_files(file_exists_map)

    with caplog.at_level("DEBUG"):
        move = reader.read_move(move_text)

    assert move is None
    assert f"Move effect function does not exist for move: {move_text}" in caplog.text

def test_perfect_format_move_effect_is_none(reader, mock_import, mock_files):
    """Test if format string is perfect and effect function is None"""
    move_text = "Move Name: Thunderbolt, Energies: Electric; Electric, Damage: 50, Effect Function: None"
    reader.types = {"Electric"}
    file_exists_map = {
        "pokemon_standard_move_effect_list.py": True,
        "pokemon_custom_move_effect_list.py": True,
    }

    mock_files(file_exists_map)
    move = reader.read_move(move_text)

    assert move is not None
    assert move.name == "Thunderbolt"
    assert move.energy == ["Electric", "Electric"]
    assert move.damage == 50
    assert move.effect == None

def test_damage_value_is_not_digit(reader, mock_import, mock_files, caplog):
    """Test if damage value is not a digit"""
    move_text = "Move Name: Thunderbolt, Energies: Electric; Electric, Damage: not_digit, Effect Function: thunderbolt_effect"
    reader.types = {"Electric"}
    file_exists_map = {
        "pokemon_standard_move_effect_list.py": True,
        "pokemon_custom_move_effect_list.py": True,
    }

    mock_files(file_exists_map)

    with caplog.at_level("DEBUG"):
        move = reader.read_move(move_text)

    assert move is None
    assert f"Move damage value is not digit for move: {move_text}" in caplog.text

def test_perfect_format_energy_is_none(reader, mock_import, mock_files):
    """Test if format string is perfect and energy is none"""
    move_text = "Move Name: Thunderbolt, Energies: None, Damage: 50, Effect Function: thunderbolt_effect"
    reader.types = {"Electric"}
    file_exists_map = {
        "pokemon_standard_move_effect_list.py": True,
        "pokemon_custom_move_effect_list.py": True,
    }

    mock_files(file_exists_map)
    move = reader.read_move(move_text)

    assert move is not None
    assert move.name == "Thunderbolt"
    assert move.energy == []
    assert move.damage == 50
    assert move.effect() == "Thunderbolt Attack"

def test_illegal_energy_value(reader, mock_import, mock_files, caplog):
    """Test if energy used is not a valid type"""
    move_text = "Move Name: Thunderbolt, Energies: Electric; Nuclear, Damage: 50, Effect Function: thunderbolt_effect"
    reader.types = {"Electric"}
    file_exists_map = {
        "pokemon_standard_move_effect_list.py": True,
        "pokemon_custom_move_effect_list.py": True,
    }

    mock_files(file_exists_map)

    with caplog.at_level("DEBUG"):
        move = reader.read_move(move_text)

    assert move is None
    assert f"Illegal energy type used in move: {move_text}" in caplog.text

def test_no_name_given_for_move(reader, mock_import, mock_files, caplog):
    """Test if no move name is given"""
    move_text = "Move Name: , Energies: Electric; Electric, Damage: 50, Effect Function: thunderbolt_effect"
    reader.types = {"Electric"}
    file_exists_map = {
        "pokemon_standard_move_effect_list.py": True,
        "pokemon_custom_move_effect_list.py": True,
    }

    mock_files(file_exists_map)

    with caplog.at_level("DEBUG"):
        move = reader.read_move(move_text)

    assert move is None
    assert f"No name is given for move: {move_text}" in caplog.text

def test_effect_function_substring_is_invalid(reader, mock_import, mock_files, caplog):
    """Test if effect function substring "Effect Function: [funct]" is not structured properly"""
    move_text = "Move Name: Thunderbolt, Energies: Electric; Electric, Damage: 50, Efdsafdsafdsfsafdsafdsafdsa"
    reader.types = {"Electric"}
    file_exists_map = {
        "pokemon_standard_move_effect_list.py": True,
        "pokemon_custom_move_effect_list.py": True,
    }

    mock_files(file_exists_map)

    with caplog.at_level("DEBUG"):
        move = reader.read_move(move_text)

    assert move is None
    assert f"Error in formatting of move function for move: {move_text}" in caplog.text

def test_energy_substring_is_invalid(reader, mock_import, mock_files, caplog):
    """Test if energy substring "Energies: [Energies]" is not structured properly"""
    move_text = "Move Name: Thunderbolt, Efdsafdsafdsafdsafdsfasfsda, Damage: 50, Effect Function: thunderbolt_effect"
    reader.types = {"Electric"}
    file_exists_map = {
        "pokemon_standard_move_effect_list.py": True,
        "pokemon_custom_move_effect_list.py": True,
    }

    mock_files(file_exists_map)

    with caplog.at_level("DEBUG"):
        move = reader.read_move(move_text)

    assert move is None
    assert f"Error in formatting of move energy for move: {move_text}" in caplog.text

def test_damage_substring_is_invalid(reader, mock_import, mock_files, caplog):
    """Test if damage substring "Damage: [num]" is not structured properly"""
    move_text = "Move Name: Thunderbolt, Energies: Electric; Electric, Dadafdsafdsafdsa, Effect Function: thunderbolt_effect"
    reader.types = {"Electric"}
    file_exists_map = {
        "pokemon_standard_move_effect_list.py": True,
        "pokemon_custom_move_effect_list.py": True,
    }

    mock_files(file_exists_map)

    with caplog.at_level("DEBUG"):
        move = reader.read_move(move_text)

    assert move is None
    assert f"Error in formatting of move damage for move: {move_text}" in caplog.text

def test_move_substring_is_invalid(reader, mock_import, mock_files, caplog):
    """Test if move name substring "Move Name: [name]" is not structured properly"""
    move_text = "Mofddsafdsafdsafdsa, Energies: Electric; Electric, Damage: 50, Effect Function: thunderbolt_effect"
    reader.types = {"Electric"}
    file_exists_map = {
        "pokemon_standard_move_effect_list.py": True,
        "pokemon_custom_move_effect_list.py": True,
    }

    mock_files(file_exists_map)

    with caplog.at_level("DEBUG"):
        move = reader.read_move(move_text)

    assert move is None
    assert f"Error in formatting of move name for move: {move_text}" in caplog.text

def test_input_string_is_invalid_four_commas(reader, mock_import, mock_files, caplog):
    """Test if input_string is invalid but has 4 commas"""
    move_text = "Mofddsafdsafdsafdsa, fdsajflkd;sdsajf, fjdksafjdsl;afjdsa, fjdskalfjsafjdsa"
    reader.types = {"Electric"}
    file_exists_map = {
        "pokemon_standard_move_effect_list.py": True,
        "pokemon_custom_move_effect_list.py": True,
    }

    mock_files(file_exists_map)

    with caplog.at_level("DEBUG"):
        move = reader.read_move(move_text)

    assert move is None
    assert f"Error in formatting of move name for move: {move_text}" in caplog.text

def test_input_string_is_invalid_not_four_commas(reader, mock_import, mock_files, caplog):
    """Test if input_string is invalid and doesn't have 4 commas"""
    move_text = "fdsafdsafdsaaaaaaaaaaaaaaaaaaafdafdsafdsfdsafdsafds,dsaf,afjdsa"
    reader.types = {"Electric"}
    file_exists_map = {
        "pokemon_standard_move_effect_list.py": True,
        "pokemon_custom_move_effect_list.py": True,
    }

    mock_files(file_exists_map)

    with caplog.at_level("DEBUG"):
        move = reader.read_move(move_text)

    assert move is None
    assert f"Error in formatting of move: {move_text}" in caplog.text