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
        "pokemon_standard_moves.txt": True,
        "pokemon_custom_moves.txt": True,
    }

    file_contents_map = {
        "pokemon_standard_moves.txt": """Move Name: Thunderbolt, Energies: Electric; Electric, Damage: 50, Effect Function: None
Move Name: Flamethrower, Energies: Fire; Fire; Colorless, Damage: 90, Effect Function: None
Move Name: Hydro Pump, Energies: Water; Water; Colorless, Damage: 80, Effect Function: None
Move Name: Solar Beam, Energies: Grass; Grass; Grass, Damage: 120, Effect Function: None
Move Name: Shadow Ball, Energies: Psychic; Colorless; Colorless, Damage: 70, Effect Function: None
""",
        "pokemon_custom_moves.txt": """Move Name: Gamma Ray, Energies: Nuclear; Nuclear, Damage: 110, Effect Function: None
Move Name: Half Life, Energies: Nuclear; Colorless, Damage: 60, Effect Function: None
Move Name: Crystal Rush, Energies: Crystal; Crystal, Damage: 90, Effect Function: None
Move Name: Holy Beam, Energies: Holy; Holy, Damage: 100, Effect Function: None
""",
    }

    reader.types = {"Electric", "Colorless", "Fire", "Water", "Grass", "Psychic", "Nuclear", "Crystal", "Holy"}

    mock_files(file_exists_map, file_contents_map)

    with caplog.at_level("DEBUG"):
        moves = reader.read_all_moves()

    expected_moves = dict()

    expected_moves["Thunderbolt"] = reader.read_move("Move Name: Thunderbolt, Energies: Electric; Electric, Damage: 50, Effect Function: None")
    expected_moves["Flamethrower"] = reader.read_move("Move Name: Flamethrower, Energies: Fire; Fire; Colorless, Damage: 90, Effect Function: None")
    expected_moves["Hydro Pump"] = reader.read_move("Move Name: Hydro Pump, Energies: Water; Water; Colorless, Damage: 80, Effect Function: None")
    expected_moves["Solar Beam"] = reader.read_move("Move Name: Solar Beam, Energies: Grass; Grass; Grass, Damage: 120, Effect Function: None")
    expected_moves["Shadow Ball"] = reader.read_move("Move Name: Shadow Ball, Energies: Psychic; Colorless; Colorless, Damage: 70, Effect Function: None")
    expected_moves["Gamma Ray"] = reader.read_move("Move Name: Gamma Ray, Energies: Nuclear; Nuclear, Damage: 110, Effect Function: None")
    expected_moves["Half Life"] = reader.read_move("Move Name: Half Life, Energies: Nuclear; Colorless, Damage: 60, Effect Function: None")
    expected_moves["Crystal Rush"] = reader.read_move("Move Name: Crystal Rush, Energies: Crystal; Crystal, Damage: 90, Effect Function: None")
    expected_moves["Holy Beam"] = reader.read_move("Move Name: Holy Beam, Energies: Holy; Holy, Damage: 100, Effect Function: None")

    assert moves == expected_moves

    assert "Imported standard moves from file" in caplog.text
    assert "Imported custom moves from file" in caplog.text

def test_only_standard_exists_and_has_valid_text(reader, mock_files, caplog):
    """Test if only standard file exists and have valid content."""

    file_exists_map = {
        "pokemon_standard_moves.txt": True,
        "pokemon_custom_moves.txt": False,
    }

    file_contents_map = {
        "pokemon_standard_moves.txt": """Move Name: Thunderbolt, Energies: Electric; Electric, Damage: 50, Effect Function: None
Move Name: Flamethrower, Energies: Fire; Fire; Colorless, Damage: 90, Effect Function: None
Move Name: Hydro Pump, Energies: Water; Water; Colorless, Damage: 80, Effect Function: None
Move Name: Solar Beam, Energies: Grass; Grass; Grass, Damage: 120, Effect Function: None
Move Name: Shadow Ball, Energies: Psychic; Colorless; Colorless, Damage: 70, Effect Function: None
""",
        "pokemon_custom_moves.txt": """Move Name: Gamma Ray, Energies: Nuclear; Nuclear, Damage: 110, Effect Function: None
Move Name: Half Life, Energies: Nuclear; Colorless, Damage: 60, Effect Function: None
Move Name: Crystal Rush, Energies: Crystal; Crystal, Damage: 90, Effect Function: None
Move Name: Holy Beam, Energies: Holy; Holy, Damage: 100, Effect Function: None
""",
    }

    reader.types = {"Electric", "Colorless", "Fire", "Water", "Grass", "Psychic"}

    mock_files(file_exists_map, file_contents_map)

    with caplog.at_level("DEBUG"):
        moves = reader.read_all_moves()

    expected_moves = dict()

    expected_moves["Thunderbolt"] = reader.read_move("Move Name: Thunderbolt, Energies: Electric; Electric, Damage: 50, Effect Function: None")
    expected_moves["Flamethrower"] = reader.read_move("Move Name: Flamethrower, Energies: Fire; Fire; Colorless, Damage: 90, Effect Function: None")
    expected_moves["Hydro Pump"] = reader.read_move("Move Name: Hydro Pump, Energies: Water; Water; Colorless, Damage: 80, Effect Function: None")
    expected_moves["Solar Beam"] = reader.read_move("Move Name: Solar Beam, Energies: Grass; Grass; Grass, Damage: 120, Effect Function: None")
    expected_moves["Shadow Ball"] = reader.read_move("Move Name: Shadow Ball, Energies: Psychic; Colorless; Colorless, Damage: 70, Effect Function: None")

    assert moves == expected_moves

    assert "Imported standard moves from file" in caplog.text
    assert "Cannot locate custom moves file, pokemon_custom_moves.txt, did not import any custom moves" in caplog.text

def test_only_custom_exists_and_has_valid_text(reader, mock_files, caplog):
    """Test if only standard file exists and have valid content."""

    file_exists_map = {
        "pokemon_standard_moves.txt": False,
        "pokemon_custom_moves.txt": True,
    }

    file_contents_map = {
        "pokemon_standard_moves.txt": """Move Name: Thunderbolt, Energies: Electric; Electric, Damage: 50, Effect Function: None
Move Name: Flamethrower, Energies: Fire; Fire; Colorless, Damage: 90, Effect Function: None
Move Name: Hydro Pump, Energies: Water; Water; Colorless, Damage: 80, Effect Function: None
Move Name: Solar Beam, Energies: Grass; Grass; Grass, Damage: 120, Effect Function: None
Move Name: Shadow Ball, Energies: Psychic; Colorless; Colorless, Damage: 70, Effect Function: None
""",
        "pokemon_custom_moves.txt": """Move Name: Gamma Ray, Energies: Nuclear; Nuclear, Damage: 110, Effect Function: None
Move Name: Half Life, Energies: Nuclear; Colorless, Damage: 60, Effect Function: None
Move Name: Crystal Rush, Energies: Crystal; Crystal, Damage: 90, Effect Function: None
Move Name: Holy Beam, Energies: Holy; Holy, Damage: 100, Effect Function: None
""",
    }

    reader.types = {"Electric", "Colorless", "Fire", "Water", "Grass", "Psychic"}

    mock_files(file_exists_map, file_contents_map)

    with caplog.at_level("DEBUG"):
        moves = reader.read_all_moves()

    expected_moves = dict()

    assert moves == expected_moves

    assert "Cannot locate standard moves file, pokemon_standard_moves.txt, did not import any moves" in caplog.text

def test_no_files_exist(reader, mock_files, caplog):
    """Test if no files exist."""

    file_exists_map = {
        "pokemon_standard_moves.txt": False,
        "pokemon_custom_moves.txt": False,
    }

    file_contents_map = {
        "pokemon_standard_moves.txt": """Move Name: Thunderbolt, Energies: Electric; Electric, Damage: 50, Effect Function: None
Move Name: Flamethrower, Energies: Fire; Fire; Colorless, Damage: 90, Effect Function: None
Move Name: Hydro Pump, Energies: Water; Water; Colorless, Damage: 80, Effect Function: None
Move Name: Solar Beam, Energies: Grass; Grass; Grass, Damage: 120, Effect Function: None
Move Name: Shadow Ball, Energies: Psychic; Colorless; Colorless, Damage: 70, Effect Function: None
""",
        "pokemon_custom_moves.txt": """Move Name: Gamma Ray, Energies: Nuclear; Nuclear, Damage: 110, Effect Function: None
Move Name: Half Life, Energies: Nuclear; Colorless, Damage: 60, Effect Function: None
Move Name: Crystal Rush, Energies: Crystal; Crystal, Damage: 90, Effect Function: None
Move Name: Holy Beam, Energies: Holy; Holy, Damage: 100, Effect Function: None
""",
    }

    reader.types = {"Electric", "Colorless", "Fire", "Water", "Grass", "Psychic"}

    mock_files(file_exists_map, file_contents_map)

    with caplog.at_level("DEBUG"):
        moves = reader.read_all_moves()

    expected_moves = dict()

    assert moves == expected_moves

    assert "Cannot locate standard moves file, pokemon_standard_moves.txt, did not import any moves" in caplog.text

def test_both_files_exist_both_have_some_invalid_moves(reader, mock_files, caplog):
    """Test if both files exist and some are invalid lines."""

    file_exists_map = {
        "pokemon_standard_moves.txt": True,
        "pokemon_custom_moves.txt": True,
    }

    file_contents_map = {
        "pokemon_standard_moves.txt": """Move Name: Thunderbolt, Energies: Electric; Electric, Damage: 50, Effect Function: None
Move Name: Flamefdsafsddsfadsfasdflorless, fdasfect Function: None
Move Name: Hydro Pump, Energies: Water; Water; Colorless, Damage: 80, Effect Function: None
Move Name: Solar Beam, Energies: Grass; Grass; Grass, Damage: 120, Effect Function: None
Move Name: ShfdsafsdfsdaColorless; Colorfdsa 70, Effect Function: None
""",
        "pokemon_custom_moves.txt": """Move Name: Gamma Ray, Energies: Nuclear; Nuclear, Damage: 110, Effect Function: None
Move Name: Half Life, Energies: Nuclear; Colorless, Damage: 60, Effect Function: None
Move Name: Crystal Rush, Enfdsafdsact Function: None
Move Name: Holy Beam, Energies: Holy; Holy, Damage: 100, Effect Function: None
""",
    }

    reader.types = {"Electric", "Colorless", "Fire", "Water", "Grass", "Psychic", "Nuclear", "Crystal", "Holy"}

    mock_files(file_exists_map, file_contents_map)

    with caplog.at_level("DEBUG"):
        moves = reader.read_all_moves()

    expected_moves = dict()

    expected_moves["Thunderbolt"] = reader.read_move("Move Name: Thunderbolt, Energies: Electric; Electric, Damage: 50, Effect Function: None")
    expected_moves["Hydro Pump"] = reader.read_move("Move Name: Hydro Pump, Energies: Water; Water; Colorless, Damage: 80, Effect Function: None")
    expected_moves["Solar Beam"] = reader.read_move("Move Name: Solar Beam, Energies: Grass; Grass; Grass, Damage: 120, Effect Function: None")
    expected_moves["Gamma Ray"] = reader.read_move("Move Name: Gamma Ray, Energies: Nuclear; Nuclear, Damage: 110, Effect Function: None")
    expected_moves["Half Life"] = reader.read_move("Move Name: Half Life, Energies: Nuclear; Colorless, Damage: 60, Effect Function: None")
    expected_moves["Holy Beam"] = reader.read_move("Move Name: Holy Beam, Energies: Holy; Holy, Damage: 100, Effect Function: None")

    assert moves == expected_moves

    assert "Imported standard moves from file" in caplog.text
    assert "Imported custom moves from file" in caplog.text