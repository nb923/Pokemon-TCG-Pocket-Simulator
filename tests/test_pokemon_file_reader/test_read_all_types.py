import pytest
from unittest.mock import MagicMock
from pokemon_file_reader import PokemonFileReader

@pytest.fixture
def reader():
    return PokemonFileReader()

@pytest.fixture
def mock_files(monkeypatch):
    def _mock_files(file_exists_map, file_content_map):
        def mock_exists(path):
            return file_exists_map.get(str(path), False)
        
        monkeypatch.setattr("pathlib.Path.exists", mock_exists)

        def mock_open(path, mode="r"):
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

def test_both_files_exist_both_have_text(reader, mock_files, caplog):
    file_exists_map = {
        "pokemon_standard_types.txt": True,
        "pokemon_custom_types.txt": True,
    }

    file_contents_map = {
        "pokemon_standard_types.txt": """Fire
Fighting
Lightning
Water
Grass
Psychic
Metal
Darkness
Dragon
Colorless
""",
        "pokemon_custom_types.txt": """Nuclear
Crystal
Sound
""",
    }

    mock_files(file_exists_map, file_contents_map)

    with caplog.at_level("DEBUG"):
        types = reader.read_all_types()

    expected_types = {
        "Fire", 
        "Fighting", 
        "Lightning", 
        "Water", 
        "Grass", 
        "Psychic", 
        "Metal", 
        "Darkness", 
        "Dragon", 
        "Colorless",
        "Nuclear", 
        "Crystal", 
        "Sound"
    }

    assert types == expected_types

    assert "Imported standard types from file" in caplog.text
    assert "Imported custom types from file" in caplog.text

def test_both_files_exist_only_standard_has_text(reader, mock_files, caplog):
    file_exists_map = {
        "pokemon_standard_types.txt": True,
        "pokemon_custom_types.txt": True,
    }

    file_contents_map = {
        "pokemon_standard_types.txt": """Fire
Fighting
Lightning
Water
Grass
Psychic
Metal
Darkness
Dragon
Colorless
""",
        "pokemon_custom_types.txt": """""",
    }

    mock_files(file_exists_map, file_contents_map)

    with caplog.at_level("DEBUG"):
        types = reader.read_all_types()

    expected_types = {
        "Fire", 
        "Fighting", 
        "Lightning", 
        "Water", 
        "Grass", 
        "Psychic", 
        "Metal", 
        "Darkness", 
        "Dragon", 
        "Colorless"
    }

    assert types == expected_types

    assert "Imported standard types from file" in caplog.text
    assert "Imported custom types from file" in caplog.text

def test_both_files_exist_only_custom_has_text(reader, mock_files, caplog):
    file_exists_map = {
        "pokemon_standard_types.txt": True,
        "pokemon_custom_types.txt": True,
    }

    file_contents_map = {
        "pokemon_standard_types.txt": """""",
        "pokemon_custom_types.txt": """Nuclear
Crystal
Sound
""",
    }

    mock_files(file_exists_map, file_contents_map)

    with caplog.at_level("DEBUG"):
        types = reader.read_all_types()

    expected_types = {
        "Nuclear",
        "Crystal",
        "Sound"
    }

    assert types == expected_types

    assert "Imported standard types from file" in caplog.text
    assert "Imported custom types from file" in caplog.text

def test_both_files_exist_both_are_empty(reader, mock_files, caplog):
    file_exists_map = {
        "pokemon_standard_types.txt": True,
        "pokemon_custom_types.txt": True,
    }

    file_contents_map = {
        "pokemon_standard_types.txt": """""",
        "pokemon_custom_types.txt": """""",
    }

    mock_files(file_exists_map, file_contents_map)

    with caplog.at_level("DEBUG"):
        types = reader.read_all_types()

    expected_types = set()

    assert types == expected_types

    assert "Imported standard types from file" in caplog.text
    assert "Imported custom types from file" in caplog.text

def test_no_custom_file_standard_has_text(reader, mock_files, caplog):
    file_exists_map = {
        "pokemon_standard_types.txt": True,
        "pokemon_custom_types.txt": False,
    }

    file_contents_map = {
        "pokemon_standard_types.txt": """Fire
Fighting
Lightning
Water
Grass
Psychic
Metal
Darkness
Dragon
Colorless
""",
    }

    mock_files(file_exists_map, file_contents_map)

    with caplog.at_level("DEBUG"):
        types = reader.read_all_types()

    expected_types = {
        "Fire", 
        "Fighting", 
        "Lightning", 
        "Water", 
        "Grass", 
        "Psychic", 
        "Metal", 
        "Darkness", 
        "Dragon", 
        "Colorless"
    }

    assert types == expected_types

    assert "Imported standard types from file" in caplog.text
    assert "Cannot locate custom types file, pokemon_custom_types.txt, did not import any custom types" in caplog.text

def test_no_custom_file_standard_is_empty(reader, mock_files, caplog):
    file_exists_map = {
        "pokemon_standard_types.txt": True,
        "pokemon_custom_types.txt": False,
    }

    file_contents_map = {
        "pokemon_standard_types.txt": """""",
    }

    mock_files(file_exists_map, file_contents_map)

    with caplog.at_level("DEBUG"):
        types = reader.read_all_types()

    expected_types = set()

    assert types == expected_types

    assert "Imported standard types from file" in caplog.text
    assert "Cannot locate custom types file, pokemon_custom_types.txt, did not import any custom types" in caplog.text

def test_no_standard_file_custom_has_text(reader, mock_files, caplog):
    file_exists_map = {
        "pokemon_standard_types.txt": False,
        "pokemon_custom_types.txt": True,
    }

    file_contents_map = {
        "pokemon_custom_types.txt": """Nuclear
Crystal
Sound
""",
    }

    mock_files(file_exists_map, file_contents_map)

    with caplog.at_level("DEBUG"):
        types = reader.read_all_types()

    expected_types = set()

    assert types == expected_types

    assert "Cannot locate standard types file, pokemon_standard_types.txt, did not import any types" in caplog.text

def test_no_standard_file_custom_is_empty(reader, mock_files, caplog):
    file_exists_map = {
        "pokemon_standard_types.txt": False,
        "pokemon_custom_types.txt": True,
    }

    file_contents_map = {
        "pokemon_custom_types.txt": """""",
    }

    mock_files(file_exists_map, file_contents_map)

    with caplog.at_level("DEBUG"):
        types = reader.read_all_types()

    expected_types = set()

    assert types == expected_types

    assert "Cannot locate standard types file, pokemon_standard_types.txt, did not import any types" in caplog.text

def test_both_files_do_not_exist(reader, mock_files, caplog):
    file_exists_map = {
        "pokemon_standard_types.txt": False,
        "pokemon_custom_types.txt": False,
    }

    file_contents_map = {}

    mock_files(file_exists_map, file_contents_map)

    with caplog.at_level("DEBUG"):
        types = reader.read_all_types()

    expected_types = set()

    assert types == expected_types

    assert "Cannot locate standard types file, pokemon_standard_types.txt, did not import any types" in caplog.text