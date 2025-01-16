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

        mock_standard_activation = MagicMock()
        mock_custom_activation = MagicMock()
        mock_standard_effect = MagicMock()
        mock_custom_effect = MagicMock()
    
        # Ability activation condition mock functions
        def mock_effect_function_one():
            return True
    
        def mock_effect_function_two():
            return False
    
        def mock_effect_function_three(should_it_activate):
            return should_it_activate
    
        mock_standard_activation.wash_out_activation = mock_effect_function_two
        mock_standard_activation.fragrance_trap_activation = mock_effect_function_three
        mock_custom_activation.pixilate_activation = mock_effect_function_one
        mock_custom_activation.battle_bond_activation = mock_effect_function_three

        # Ability effect mock functions
        def mock_effect_function_four():
            return "Ability did damage"
        def mock_effect_function_five():
            return "Ability did not do damage"
        def mock_effect_function_six(should_it_do_damage):
            return "Ability did damage" if should_it_do_damage else "Ability did not do damage"
        
        mock_standard_effect.wash_out_effect = mock_effect_function_five
        mock_standard_effect.fragrance_trap_effect = mock_effect_function_six
        mock_custom_effect.pixilate_effect = mock_effect_function_four
        mock_custom_effect.battle_bond_effect = mock_effect_function_six
        

        if input_file == "pokemon_standard_ability_activation_list":
            return mock_standard_activation
        elif input_file == "pokemon_custom_ability_activation_list":
            return mock_custom_activation
        elif input_file == "pokemon_standard_ability_effect_list":
            return mock_standard_effect
        elif input_file == "pokemon_custom_ability_effect_list":
            return mock_custom_effect
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

def test_perfect_format_standard_ability(reader, mock_import, mock_files):
    """Test if format string is perfect and effect function is in standard"""
    ability_text = "Ability Name: Wash Out, Type: Active, Activation Function: wash_out_activation, Effect Function: wash_out_effect"

    file_exists_map = {
        "pokemon_standard_ability_activation_list.py": True,
        "pokemon_custom_ability_activation_list.py": True,
        "pokemon_standard_ability_effect_list.py": True,
        "pokemon_custom_ability_effect_list.py": True
    }

    mock_files(file_exists_map)
    ability = reader.read_ability(ability_text)

    assert ability is not None
    assert ability.name == "Wash Out"
    assert ability.passive == False
    assert ability.activation_condition() == False
    assert ability.usable == False
    assert ability.effect() == "Ability did not do damage"

def test_perfect_format_custom_ability(reader, mock_import, mock_files):
    """Test if format string is perfect and effect function is in custom"""
    ability_text = "Ability Name: Pixilate, Type: Passive, Activation Function: pixilate_activation, Effect Function: pixilate_effect"

    file_exists_map = {
        "pokemon_standard_ability_activation_list.py": True,
        "pokemon_custom_ability_activation_list.py": True,
        "pokemon_standard_ability_effect_list.py": True,
        "pokemon_custom_ability_effect_list.py": True
    }

    mock_files(file_exists_map)
    ability = reader.read_ability(ability_text)

    assert ability is not None
    assert ability.name == "Pixilate"
    assert ability.passive == True
    assert ability.activation_condition() == True
    assert ability.usable == False
    assert ability.effect() == "Ability did damage"

def test_standard_ability_effect_none_file_does_not_exist(reader, mock_import, mock_files):
    """Test if format string is perfect, effect function is None and effect function file doesn't exist for standard"""
    ability_text = "Ability Name: Wash Out, Type: Active, Activation Function: wash_out_activation, Effect Function: None"

    file_exists_map = {
        "pokemon_standard_ability_activation_list.py": True,
        "pokemon_custom_ability_activation_list.py": True,
        "pokemon_standard_ability_effect_list.py": False,
        "pokemon_custom_ability_effect_list.py": False
    }

    mock_files(file_exists_map)
    ability = reader.read_ability(ability_text)

    assert ability is not None
    assert ability.name == "Wash Out"
    assert ability.passive == False
    assert ability.activation_condition() == False
    assert ability.usable == False
    assert ability.effect == None

def test_custom_ability_effect_none_file_does_not_exist(reader, mock_import, mock_files):
    """Test if format string is perfect, effect function is None and effect function file doesn't exist for custom"""
    ability_text = "Ability Name: Pixilate, Type: Passive, Activation Function: pixilate_activation, Effect Function: None"

    file_exists_map = {
        "pokemon_standard_ability_activation_list.py": True,
        "pokemon_custom_ability_activation_list.py": True,
        "pokemon_standard_ability_effect_list.py": False,
        "pokemon_custom_ability_effect_list.py": False
    }

    mock_files(file_exists_map)
    ability = reader.read_ability(ability_text)

    assert ability is not None
    assert ability.name == "Pixilate"
    assert ability.passive == True
    assert ability.activation_condition() == True
    assert ability.usable == False
    assert ability.effect == None

def test_standard_ability_activation_none_file_does_not_exist(reader, mock_import, mock_files):
    """Test if format string is perfect, activation function is None and activation function file doesn't exist for standard"""
    ability_text = "Ability Name: Wash Out, Type: Active, Activation Function: None, Effect Function: wash_out_effect"

    file_exists_map = {
        "pokemon_standard_ability_activation_list.py": False,
        "pokemon_custom_ability_activation_list.py": False,
        "pokemon_standard_ability_effect_list.py": True,
        "pokemon_custom_ability_effect_list.py": True
    }

    mock_files(file_exists_map)
    ability = reader.read_ability(ability_text)

    assert ability is not None
    assert ability.name == "Wash Out"
    assert ability.passive == False
    assert ability.activation_condition == None
    assert ability.usable == False
    assert ability.effect() == "Ability did not do damage"

def test_custom_ability_activation_none_file_does_not_exist(reader, mock_import, mock_files):
    """Test if format string is perfect, activation function is None and activation function file doesn't exist for custom"""
    ability_text = "Ability Name: Pixilate, Type: Passive, Activation Function: None, Effect Function: pixilate_effect"

    file_exists_map = {
        "pokemon_standard_ability_activation_list.py": False,
        "pokemon_custom_ability_activation_list.py": False,
        "pokemon_standard_ability_effect_list.py": True,
        "pokemon_custom_ability_effect_list.py": True
    }

    mock_files(file_exists_map)
    ability = reader.read_ability(ability_text)

    assert ability is not None
    assert ability.name == "Pixilate"
    assert ability.passive == True
    assert ability.activation_condition == None
    assert ability.usable == False
    assert ability.effect() == "Ability did damage"

def test_standard_ability_effect_not_none_file_does_not_exist(reader, mock_import, mock_files, caplog):
    """Test if format string is perfect, effect function is not None and effect function file doesn't exist for standard"""
    ability_text = "Ability Name: Wash Out, Type: Active, Activation Function: wash_out_activation, Effect Function: wash_out_effect"

    file_exists_map = {
        "pokemon_standard_ability_activation_list.py": True,
        "pokemon_custom_ability_activation_list.py": True,
        "pokemon_standard_ability_effect_list.py": False,
        "pokemon_custom_ability_effect_list.py": False
    }

    mock_files(file_exists_map)
    ability = reader.read_ability(ability_text)

    assert ability is None
    assert f"Ability effect function does not exist for ability: {ability_text}" in caplog.text

def test_custom_ability_effect_not_none_file_does_not_exist(reader, mock_import, mock_files, caplog):
    """Test if format string is perfect, effect function is not None and effect function file doesn't exist for custom"""
    ability_text = "Ability Name: Pixilate, Type: Passive, Activation Function: pixilate_activation, Effect Function: pixilate_effect"

    file_exists_map = {
        "pokemon_standard_ability_activation_list.py": True,
        "pokemon_custom_ability_activation_list.py": True,
        "pokemon_standard_ability_effect_list.py": False,
        "pokemon_custom_ability_effect_list.py": False
    }

    mock_files(file_exists_map)
    ability = reader.read_ability(ability_text)

    assert ability is None
    assert f"Ability effect function does not exist for ability: {ability_text}" in caplog.text

def test_standard_ability_activation_not_none_file_does_not_exist(reader, mock_import, mock_files, caplog):
    """Test if format string is perfect, activation function is not None and activation function file doesn't exist for standard"""
    ability_text = "Ability Name: Wash Out, Type: Active, Activation Function: wash_out_activation, Effect Function: wash_out_effect"

    file_exists_map = {
        "pokemon_standard_ability_activation_list.py": False,
        "pokemon_custom_ability_activation_list.py": False,
        "pokemon_standard_ability_effect_list.py": True,
        "pokemon_custom_ability_effect_list.py": True
    }

    mock_files(file_exists_map)
    ability = reader.read_ability(ability_text)

    assert ability is None
    assert f"Ability activation function does not exist for ability: {ability_text}" in caplog.text

def test_custom_ability_activation_not_none_file_does_not_exist(reader, mock_import, mock_files, caplog):
    """Test if format string is perfect, activation function is not None and activation function file doesn't exist for custom"""
    ability_text = "Ability Name: Pixilate, Type: Passive, Activation Function: pixilate_activation, Effect Function: pixilate_effect"

    file_exists_map = {
        "pokemon_standard_ability_activation_list.py": False,
        "pokemon_custom_ability_activation_list.py": False,
        "pokemon_standard_ability_effect_list.py": True,
        "pokemon_custom_ability_effect_list.py": True
    }

    mock_files(file_exists_map)
    ability = reader.read_ability(ability_text)

    assert ability is None
    assert f"Ability activation function does not exist for ability: {ability_text}" in caplog.text

def test_no_name_one_space_standard_ability(reader, mock_import, mock_files, caplog):
    """Test if ability has no name for standard ability"""
    ability_text = "Ability Name: , Type: Active, Activation Function: wash_out_activation, Effect Function: wash_out_effect"

    file_exists_map = {
        "pokemon_standard_ability_activation_list.py": True,
        "pokemon_custom_ability_activation_list.py": True,
        "pokemon_standard_ability_effect_list.py": True,
        "pokemon_custom_ability_effect_list.py": True
    }

    mock_files(file_exists_map)
    ability = reader.read_ability(ability_text)

    assert ability is None
    assert f"No name is given for ability: {ability_text}" in caplog.text

def test_no_name_no_space_custom_ability(reader, mock_import, mock_files, caplog):
    """Test if ability has no name for custom ability"""
    ability_text = "Ability Name:, Type: Passive, Activation Function: pixilate_activation, Effect Function: pixilate_effect"

    file_exists_map = {
        "pokemon_standard_ability_activation_list.py": True,
        "pokemon_custom_ability_activation_list.py": True,
        "pokemon_standard_ability_effect_list.py": True,
        "pokemon_custom_ability_effect_list.py": True
    }

    mock_files(file_exists_map)
    ability = reader.read_ability(ability_text)

    assert ability is None
    assert f"No name is given for ability: {ability_text}" in caplog.text

def test_type_not_active_or_passive(reader, mock_import, mock_files, caplog):
    """Test if type of ability is not active or passive"""
    ability_text = "Ability Name: Wash Out, Type: Hybrid, Activation Function: wash_out_activation, Effect Function: wash_out_effect"

    file_exists_map = {
        "pokemon_standard_ability_activation_list.py": True,
        "pokemon_custom_ability_activation_list.py": True,
        "pokemon_standard_ability_effect_list.py": True,
        "pokemon_custom_ability_effect_list.py": True
    }

    mock_files(file_exists_map)
    ability = reader.read_ability(ability_text)

    assert ability is None
    assert f"Type value for ability is not passive or active in ability: {ability_text}" in caplog.text

def test_standard_ability_activation_not_in_file(reader, mock_import, mock_files, caplog):
    """Test if standard ability activation not in file"""
    ability_text = "Ability Name: Wash Out, Type: Active, Activation Function: wash_out_wrong_activation, Effect Function: wash_out_effect"

    file_exists_map = {
        "pokemon_standard_ability_activation_list.py": True,
        "pokemon_custom_ability_activation_list.py": True,
        "pokemon_standard_ability_effect_list.py": True,
        "pokemon_custom_ability_effect_list.py": True
    }

    mock_files(file_exists_map)
    ability = reader.read_ability(ability_text)

    assert ability is None
    assert f"Ability activation function does not exist for ability: {ability_text}" in caplog.text

def test_custom_ability_activation_not_in_file(reader, mock_import, mock_files, caplog):
    """Test if custom ability activation not in file"""
    ability_text = "Ability Name: Pixilate, Type: Passive, Activation Function: pixilate_wrong_activation, Effect Function: pixilate_effect"

    file_exists_map = {
        "pokemon_standard_ability_activation_list.py": True,
        "pokemon_custom_ability_activation_list.py": True,
        "pokemon_standard_ability_effect_list.py": True,
        "pokemon_custom_ability_effect_list.py": True
    }

    mock_files(file_exists_map)
    ability = reader.read_ability(ability_text)

    assert ability is None
    assert f"Ability activation function does not exist for ability: {ability_text}" in caplog.text

def test_standard_ability_effect_not_in_file(reader, mock_import, mock_files, caplog):
    """Test if standard ability effect not in file"""
    ability_text = "Ability Name: Wash Out, Type: Active, Activation Function: wash_out_activation, Effect Function: wash_out_wrong_effect"

    file_exists_map = {
        "pokemon_standard_ability_activation_list.py": True,
        "pokemon_custom_ability_activation_list.py": True,
        "pokemon_standard_ability_effect_list.py": True,
        "pokemon_custom_ability_effect_list.py": True
    }

    mock_files(file_exists_map)
    ability = reader.read_ability(ability_text)

    assert ability is None
    assert f"Ability effect function does not exist for ability: {ability_text}" in caplog.text

def test_custom_ability_effect_not_in_file(reader, mock_import, mock_files, caplog):
    """Test if custom ability effect not in file"""
    ability_text = "Ability Name: Pixilate, Type: Passive, Activation Function: pixilate_activation, Effect Function: pixilate_wrong_effect"

    file_exists_map = {
        "pokemon_standard_ability_activation_list.py": True,
        "pokemon_custom_ability_activation_list.py": True,
        "pokemon_standard_ability_effect_list.py": True,
        "pokemon_custom_ability_effect_list.py": True
    }

    mock_files(file_exists_map)
    ability = reader.read_ability(ability_text)

    assert ability is None
    assert f"Ability effect function does not exist for ability: {ability_text}" in caplog.text

def test_name_substring_is_invalid(reader, mock_import, mock_files, caplog):
    """Test if name substring is not structured properly"""
    ability_text = "Ability Ndfasfdsafut, Type: Active, Activation Function: wash_out_activation, Effect Function: wash_out_effect"

    file_exists_map = {
        "pokemon_standard_ability_activation_list.py": True,
        "pokemon_custom_ability_activation_list.py": True,
        "pokemon_standard_ability_effect_list.py": True,
        "pokemon_custom_ability_effect_list.py": True
    }

    mock_files(file_exists_map)
    ability = reader.read_ability(ability_text)

    assert ability is None
    assert f"Error in formatting of ability name for ability: {ability_text}" in caplog.text

def test_type_substring_is_invalid(reader, mock_import, mock_files, caplog):
    """Test if type substring is not structured properly"""
    ability_text = "Ability Name: Wash Out, Tydasfdsafdsafdsae, Activation Function: wash_out_activation, Effect Function: wash_out_effect"

    file_exists_map = {
        "pokemon_standard_ability_activation_list.py": True,
        "pokemon_custom_ability_activation_list.py": True,
        "pokemon_standard_ability_effect_list.py": True,
        "pokemon_custom_ability_effect_list.py": True
    }

    mock_files(file_exists_map)
    ability = reader.read_ability(ability_text)

    assert ability is None
    assert f"Error in formatting of ability type for ability: {ability_text}" in caplog.text

def test_activation_substring_is_invalid(reader, mock_import, mock_files, caplog):
    """Test if activation substring is not structured properly"""
    ability_text = "Ability Name: Wash Out, Type: Active, Activatfdsaftivation, Effect Function: wash_out_effect"

    file_exists_map = {
        "pokemon_standard_ability_activation_list.py": True,
        "pokemon_custom_ability_activation_list.py": True,
        "pokemon_standard_ability_effect_list.py": True,
        "pokemon_custom_ability_effect_list.py": True
    }

    mock_files(file_exists_map)
    ability = reader.read_ability(ability_text)

    assert ability is None
    assert f"Error in formatting of ability activation function for ability: {ability_text}" in caplog.text

def test_effect_substring_is_invalid(reader, mock_import, mock_files, caplog):
    """Test if effect substring is not structured properly"""
    ability_text = "Ability Name: Wash Out, Type: Active, Activation Function: wash_out_activation, Effect Ffdasfeffect"

    file_exists_map = {
        "pokemon_standard_ability_activation_list.py": True,
        "pokemon_custom_ability_activation_list.py": True,
        "pokemon_standard_ability_effect_list.py": True,
        "pokemon_custom_ability_effect_list.py": True
    }

    mock_files(file_exists_map)
    ability = reader.read_ability(ability_text)

    assert ability is None
    assert f"Error in formatting of ability effect function for ability: {ability_text}" in caplog.text

def test_input_string_is_invalid_four_commas(reader, mock_import, mock_files, caplog):
    """Test if input_string is invalid but has 4 commas"""
    ability_text = "Abilifdsafdsah Out, Tfdsafdsive, Activfdsafd_activation, Efffdsafsfeffect"

    file_exists_map = {
        "pokemon_standard_ability_activation_list.py": True,
        "pokemon_custom_ability_activation_list.py": True,
        "pokemon_standard_ability_effect_list.py": True,
        "pokemon_custom_ability_effect_list.py": True
    }

    mock_files(file_exists_map)
    ability = reader.read_ability(ability_text)

    assert ability is None
    assert f"Error in formatting of ability name for ability: {ability_text}" in caplog.text

def test_input_string_is_invalid_not_four_commas(reader, mock_import, mock_files, caplog):
    """Test if input_string is invalid and doesn't have 4 commas"""
    ability_text = "Abilifdsaffdsafdsafdsafdsdfsafdsdsafd_activatdsfadfdsafdssfeffect"

    file_exists_map = {
        "pokemon_standard_ability_activation_list.py": True,
        "pokemon_custom_ability_activation_list.py": True,
        "pokemon_standard_ability_effect_list.py": True,
        "pokemon_custom_ability_effect_list.py": True
    }

    mock_files(file_exists_map)
    ability = reader.read_ability(ability_text)

    assert ability is None
    assert f"Error in formatting of ability: {ability_text}" in caplog.text