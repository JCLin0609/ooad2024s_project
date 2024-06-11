from app.models.fuzzConfig import FuzzConfig


def test_fuzzConfig():
    # Arrange
    fuzz_config = FuzzConfig(is_input_by_file=True)
    # Act
    result = fuzz_config.is_input_by_file
    # Assert
    assert result == True


def test_fuzzConfig_from_json():
    # Arrange
    json_str = '{"isInputByFile": true}'
    # Act
    result = FuzzConfig.from_json(json_str)
    # Assert
    assert result.is_input_by_file == True
