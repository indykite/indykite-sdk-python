from utils.deserialize_digital_twin_with_token_info import deserialize_digital_twin_with_token_info

def test_no_response():
    # Prepare
    response = None

    # Act
    result = deserialize_digital_twin_with_token_info(response)

    # Assert
    assert result == None
