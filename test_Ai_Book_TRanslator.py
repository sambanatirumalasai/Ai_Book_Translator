import pytest
import tempfile
import os
from unittest.mock import MagicMock, patch
from project import convert_txt_to_dict, check_api_key, translate_block



# 1. Test convert_txt_to_dict()

def test_convert_txt_to_dict_basic():
    content = "{-Intro-}\n\nThis is the first paragraph.\n\nThis is the second paragraph.\n\n{-Chapter One-}\n\nAnother paragraph."

    with tempfile.NamedTemporaryFile("w+", delete=False, encoding="utf-8") as tmp:
        tmp.write(content)
        tmp_filename = tmp.name

    result = convert_txt_to_dict(tmp_filename)

    assert "Intro" in result
    assert "Chapter One" in result
    assert result["Intro"] == ["This is the first paragraph.", "This is the second paragraph."]
    assert result["Chapter One"] == ["Another paragraph."]

    os.remove(tmp_filename)  # cleanup



# 2. Test check_api_key() with mocking

@patch("project.genai")
def test_check_api_key_valid(mock_genai):
    mock_model = MagicMock()
    mock_model.generate_content.return_value.text = "Hello!"
    mock_genai.GenerativeModel.return_value = mock_model

    result = check_api_key("fake_api_key")
    assert result is False  # means key is valid


@patch("project.genai")
def test_check_api_key_invalid(mock_genai):
    mock_genai.GenerativeModel.side_effect = Exception("Invalid API key")
    result = check_api_key("bad_key")
    assert result is True  # means key is invalid



# 3. Test translate_block() with mocking

def test_translate_block_success():
    mock_model = MagicMock()
    mock_model.generate_content.return_value.text = "Bonjour!"
    text = "Hello!"
    result = translate_block(mock_model, text)
    assert isinstance(result, str)
    assert "Bonjour" in result


def test_translate_block_failure():
    mock_model = MagicMock()
    mock_model.generate_content.side_effect = Exception("Network error")

    with pytest.raises(ValueError):
        translate_block(mock_model, "Hello!")
