import pytest
from unittest.mock import MagicMock
from pokemon_file_reader import PokemonFileReader

@pytest.fixture
def reader():
    """Creates an instance of PokemonFileReader"""

    return PokemonFileReader()

@pytest.fixture
def mock_files(monkeypatch):
    """Returns a dynamic version of a mock for if each file exists and the contents of each file."""

    def _mock_files(file_exists_map, file_content_map):
        """Creates a mock function for pathlib.Path.exists and builtins.open."""
        
        def mock_exists(path):
            """Mimics pathlib.Path.exists using file_exists_map."""
            return file_exists_map.get(str(path), False)
        
        monkeypatch.setattr("pathlib.Path.exists", mock_exists)

        def mock_open(path, mode="r"):
            """Mimics builtins.open by using file_content_map."""
            file_path = str(path)

            if file_path in file_content_map:
                content = file_content_map[file_path]

                mock_file = MagicMock()

                mock_file.__enter__.return_value = iter(content.splitlines(keepends=True))
                mock_file.__exit__.return_value = False

                return mock_file
            
            raise FileNotFoundError(f"File not found: {file_path}")
        
        monkeypatch.setattr("builtins.open", mock_open)

    return _mock_files

@pytest.fixture
def mock_import(monkeypatch):
    """Attaches a mock function for importlib.import_module using monkeypatch."""

    def _mock_import(input_file):
        """Creates a mock function for importlib.import_module."""

        mock_standard = MagicMock()
        mock_custom = MagicMock()

        if input_file == "pokemon_standard_move_effect_list":
            return mock_standard
        elif input_file == "pokemon_custom_move_effect_list":
            return mock_custom
        else:
            raise Exception("Invalid input file")
    
    monkeypatch.setattr("importlib.import_module", _mock_import)

def test_both_files_exist_both_have_valid_text(reader, mock_files, caplog):
    """Test if both files exist and have valid content."""

    file_exists_map = {
        "pokemon_standard_abilities.txt": True,
        "pokemon_custom_abilities.txt": True,
    }

    file_contents_map = {
        "pokemon_standard_abilities.txt": """Ability Name: Frost Armor, Type: Passive, Activation Function: None, Effect Function: None
Ability Name: Solar Flare, Type: Active, Activation Function: None, Effect Function: None
Ability Name: Venom Strike, Type: Active, Activation Function: None, Effect Function: None
Ability Name: Mystic Shield, Type: Passive, Activation Function: None, Effect Function: None
Ability Name: Arcane Surge, Type: Active, Activation Function: None, Effect Function: None
""",
        "pokemon_custom_abilities.txt": """Ability Name: Flame Burst, Type: Active, Activation Function: None, Effect Function: None
Ability Name: Iron Will, Type: Passive, Activation Function: None, Effect Function: None
Ability Name: Healing Rain, Type: Active, Activation Function: None, Effect Function: None
Ability Name: Shadow Veil, Type: Passive, Activation Function: None, Effect Function: None
Ability Name: Thunder Strike, Type: Active, Activation Function: None, Effect Function: None
""",
    }

    mock_files(file_exists_map, file_contents_map)

    with caplog.at_level("DEBUG"):
        abilities = reader.read_all_abilities()

    expected_abilities = dict()

    expected_abilities["Flame Burst"] = reader.read_ability("Ability Name: Flame Burst, Type: Active, Activation Function: None, Effect Function: None")  
    expected_abilities["Iron Will"] = reader.read_ability("Ability Name: Iron Will, Type: Passive, Activation Function: None, Effect Function: None")  
    expected_abilities["Healing Rain"] = reader.read_ability("Ability Name: Healing Rain, Type: Active, Activation Function: None, Effect Function: None")  
    expected_abilities["Shadow Veil"] = reader.read_ability("Ability Name: Shadow Veil, Type: Passive, Activation Function: None, Effect Function: None")  
    expected_abilities["Thunder Strike"] = reader.read_ability("Ability Name: Thunder Strike, Type: Active, Activation Function: None, Effect Function: None")  
    expected_abilities["Frost Armor"] = reader.read_ability("Ability Name: Frost Armor, Type: Passive, Activation Function: None, Effect Function: None")  
    expected_abilities["Solar Flare"] = reader.read_ability("Ability Name: Solar Flare, Type: Active, Activation Function: None, Effect Function: None")  
    expected_abilities["Venom Strike"] = reader.read_ability("Ability Name: Venom Strike, Type: Active, Activation Function: None, Effect Function: None")  
    expected_abilities["Mystic Shield"] = reader.read_ability("Ability Name: Mystic Shield, Type: Passive, Activation Function: None, Effect Function: None")  
    expected_abilities["Arcane Surge"] = reader.read_ability("Ability Name: Arcane Surge, Type: Active, Activation Function: None, Effect Function: None")  

    assert abilities == expected_abilities

    assert "Imported standard abilities from file" in caplog.text
    assert "Imported custom abilities from file" in caplog.text

def test_only_standard_exists_and_has_valid_text(reader, mock_files, caplog):
    """Test if only standard file exists and have valid content."""

    file_exists_map = {
        "pokemon_standard_abilities.txt": True,
        "pokemon_custom_abilities.txt": False,
    }

    file_contents_map = {
        "pokemon_standard_abilities.txt": """Ability Name: Frost Armor, Type: Passive, Activation Function: None, Effect Function: None
Ability Name: Solar Flare, Type: Active, Activation Function: None, Effect Function: None
Ability Name: Venom Strike, Type: Active, Activation Function: None, Effect Function: None
Ability Name: Mystic Shield, Type: Passive, Activation Function: None, Effect Function: None
Ability Name: Arcane Surge, Type: Active, Activation Function: None, Effect Function: None
""",
        "pokemon_custom_abilities.txt": """Ability Name: Flame Burst, Type: Active, Activation Function: None, Effect Function: None
Ability Name: Iron Will, Type: Passive, Activation Function: None, Effect Function: None
Ability Name: Healing Rain, Type: Active, Activation Function: None, Effect Function: None
Ability Name: Shadow Veil, Type: Passive, Activation Function: None, Effect Function: None
Ability Name: Thunder Strike, Type: Active, Activation Function: None, Effect Function: None
""",
    }

    mock_files(file_exists_map, file_contents_map)

    with caplog.at_level("DEBUG"):
        abilities = reader.read_all_abilities()

    expected_abilities = dict()

    expected_abilities["Frost Armor"] = reader.read_ability("Ability Name: Frost Armor, Type: Passive, Activation Function: None, Effect Function: None")  
    expected_abilities["Solar Flare"] = reader.read_ability("Ability Name: Solar Flare, Type: Active, Activation Function: None, Effect Function: None")  
    expected_abilities["Venom Strike"] = reader.read_ability("Ability Name: Venom Strike, Type: Active, Activation Function: None, Effect Function: None")  
    expected_abilities["Mystic Shield"] = reader.read_ability("Ability Name: Mystic Shield, Type: Passive, Activation Function: None, Effect Function: None")  
    expected_abilities["Arcane Surge"] = reader.read_ability("Ability Name: Arcane Surge, Type: Active, Activation Function: None, Effect Function: None")  

    assert abilities == expected_abilities

    assert "Imported standard abilities from file" in caplog.text
    assert "Cannot locate custom abilities file, pokemon_custom_abilities.txt, did not import any custom abilities" in caplog.text

def test_only_custom_exists_and_has_valid_text(reader, mock_files, caplog):
    """Test if only standard file exists and have valid content."""

    file_exists_map = {
        "pokemon_standard_abilities.txt": False,
        "pokemon_custom_abilities.txt": True,
    }

    file_contents_map = {
        "pokemon_standard_abilities.txt": """Ability Name: Frost Armor, Type: Passive, Activation Function: None, Effect Function: None
Ability Name: Solar Flare, Type: Active, Activation Function: None, Effect Function: None
Ability Name: Venom Strike, Type: Active, Activation Function: None, Effect Function: None
Ability Name: Mystic Shield, Type: Passive, Activation Function: None, Effect Function: None
Ability Name: Arcane Surge, Type: Active, Activation Function: None, Effect Function: None
""",
        "pokemon_custom_abilities.txt": """Ability Name: Flame Burst, Type: Active, Activation Function: None, Effect Function: None
Ability Name: Iron Will, Type: Passive, Activation Function: None, Effect Function: None
Ability Name: Healing Rain, Type: Active, Activation Function: None, Effect Function: None
Ability Name: Shadow Veil, Type: Passive, Activation Function: None, Effect Function: None
Ability Name: Thunder Strike, Type: Active, Activation Function: None, Effect Function: None
""",
    }

    mock_files(file_exists_map, file_contents_map)

    with caplog.at_level("DEBUG"):
        abilities = reader.read_all_abilities()

    expected_abilities = dict()

    assert abilities == expected_abilities

    assert "Cannot locate standard abilities file, pokemon_standard_abilities.txt, did not import any abilities" in caplog.text

def test_no_files_exist(reader, mock_files, caplog):
    """Test if no files exist."""

    file_exists_map = {
        "pokemon_standard_abilities.txt": False,
        "pokemon_custom_abilities.txt": False,
    }

    file_contents_map = {
        "pokemon_standard_abilities.txt": """Ability Name: Frost Armor, Type: Passive, Activation Function: None, Effect Function: None
Ability Name: Solar Flare, Type: Active, Activation Function: None, Effect Function: None
Ability Name: Venom Strike, Type: Active, Activation Function: None, Effect Function: None
Ability Name: Mystic Shield, Type: Passive, Activation Function: None, Effect Function: None
Ability Name: Arcane Surge, Type: Active, Activation Function: None, Effect Function: None
""",
        "pokemon_custom_abilities.txt": """Ability Name: Flame Burst, Type: Active, Activation Function: None, Effect Function: None
Ability Name: Iron Will, Type: Passive, Activation Function: None, Effect Function: None
Ability Name: Healing Rain, Type: Active, Activation Function: None, Effect Function: None
Ability Name: Shadow Veil, Type: Passive, Activation Function: None, Effect Function: None
Ability Name: Thunder Strike, Type: Active, Activation Function: None, Effect Function: None
""",
    }

    mock_files(file_exists_map, file_contents_map)

    with caplog.at_level("DEBUG"):
        abilities = reader.read_all_abilities()

    expected_abilities = dict()

    assert abilities == expected_abilities

    assert "Cannot locate standard abilities file, pokemon_standard_abilities.txt, did not import any abilities" in caplog.text

def test_both_files_exist_both_have_some_invalid_abilities(reader, mock_files, caplog):
    """Test if both files exist and some are invalid lines."""

    file_exists_map = {
        "pokemon_standard_abilities.txt": True,
        "pokemon_custom_abilities.txt": True,
    }

    file_contents_map = {
        "pokemon_standard_abilities.txt": """Ability Name: Frost Armor, Type: Passive, Activation Function: None, Effect Function: None
Ability Name: Solar Flare, Type: Active, Activation Function: None, Effect Function: None
Ability Name: Venom dfasfdsafdsa Function: None, Effect Function: None
Ability Name: Mystic Shield, Type: Passive, Activation Fufdsfdse, Effect Function: None
Ability Name: Arcane Surge, Type: Active, Activation Function: None, Effect Function: None
""",
        "pokemon_custom_abilities.txt": """Ability Name: Flame Burst, Type: Active, Activation Function: None, Effect Function: None
Ability Name: Iron Will, Type: Passive, Activation Function: None, Effect Function: None
Ability Name: Healing Rain, Type: None, Activation Function: None, Effect Function: None
Ability Name: Shadow Veil, Type: Passive, Activation Function: None, Effect Function: None
Ability Name: Thunder Strike, Type: Active, Activation Function: None, Effect Function: None
""",
    }

    mock_files(file_exists_map, file_contents_map)

    with caplog.at_level("DEBUG"):
        abilities = reader.read_all_abilities()

    expected_abilities = dict()

    expected_abilities["Flame Burst"] = reader.read_ability("Ability Name: Flame Burst, Type: Active, Activation Function: None, Effect Function: None")  
    expected_abilities["Iron Will"] = reader.read_ability("Ability Name: Iron Will, Type: Passive, Activation Function: None, Effect Function: None")  
    expected_abilities["Shadow Veil"] = reader.read_ability("Ability Name: Shadow Veil, Type: Passive, Activation Function: None, Effect Function: None")  
    expected_abilities["Thunder Strike"] = reader.read_ability("Ability Name: Thunder Strike, Type: Active, Activation Function: None, Effect Function: None")  
    expected_abilities["Frost Armor"] = reader.read_ability("Ability Name: Frost Armor, Type: Passive, Activation Function: None, Effect Function: None")  
    expected_abilities["Solar Flare"] = reader.read_ability("Ability Name: Solar Flare, Type: Active, Activation Function: None, Effect Function: None")  
    expected_abilities["Arcane Surge"] = reader.read_ability("Ability Name: Arcane Surge, Type: Active, Activation Function: None, Effect Function: None")  

    assert abilities == expected_abilities

    assert "Imported standard abilities from file" in caplog.text
    assert "Imported custom abilities from file" in caplog.text