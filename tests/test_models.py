"""Tests for the models configuration module."""

import sys
import json
import tempfile
from pathlib import Path

import pytest

# Add the src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from token_vision.models import (
    MODELS,
    get_model_info,
    get_provider_for_model,
    load_custom_models
)

# Store original models for reset
ORIGINAL_MODELS = MODELS.copy()

def reset_models():
    """Reset models to original state."""
    MODELS.clear()
    MODELS.update(ORIGINAL_MODELS)

@pytest.fixture(autouse=True)
def reset_models_after_test():
    """Reset models after each test."""
    yield
    reset_models()

def test_models_structure():
    """Test that MODELS dictionary has the expected structure."""
    required_provider_keys = {"name", "max_images", "models"}
    required_model_keys = {"name", "input_rate"}
    
    for provider, provider_info in MODELS.items():
        # Test provider structure
        assert isinstance(provider, str)
        assert all(key in provider_info for key in required_provider_keys)
        
        # Test model structure
        for model_name, model_info in provider_info["models"].items():
            assert isinstance(model_name, str)
            assert all(key in model_info for key in required_model_keys)
            assert isinstance(model_info["input_rate"], (int, float))

def test_get_model_info():
    """Test get_model_info function."""
    # Test valid model
    model_info = get_model_info("claude-3-opus")
    assert model_info["name"] == "Claude 3 Opus"
    assert "input_rate" in model_info
    assert "output_rate" in model_info
    
    # Test invalid model
    with pytest.raises(ValueError):
        get_model_info("nonexistent-model")

def test_get_provider_for_model():
    """Test get_provider_for_model function."""
    # Test valid models
    assert get_provider_for_model("claude-3-opus") == "claude"
    assert get_provider_for_model("gpt-4-vision") == "openai"
    assert get_provider_for_model("gemini-1-5-pro") == "gemini"
    
    # Test invalid model
    with pytest.raises(ValueError):
        get_provider_for_model("nonexistent-model")

def test_load_custom_models(tmp_path):
    """Test loading custom models from JSON."""
    # Create a test config file
    config = {
        "custom-provider": {
            "name": "Custom Provider",
            "max_images": 5,
            "models": {
                "custom-model-v1": {
                    "name": "Custom Model V1",
                    "input_rate": 0.001,
                    "output_rate": 0.005
                }
            }
        }
    }
    
    config_path = tmp_path / "custom_models.json"
    with open(config_path, "w") as f:
        json.dump(config, f)
    
    # Load custom models
    loaded_models = load_custom_models(str(config_path))
    
    # Verify loaded models
    assert "custom-provider" in MODELS
    assert MODELS["custom-provider"]["name"] == "Custom Provider"
    assert "custom-model-v1" in MODELS["custom-provider"]["models"]
    
    # Test using custom model
    model_info = get_model_info("custom-model-v1")
    assert model_info["name"] == "Custom Model V1"
    assert model_info["input_rate"] == 0.001
    
    # Test invalid config file
    with pytest.raises(FileNotFoundError):
        load_custom_models("nonexistent.json")

def test_model_rates():
    """Test that model rates are reasonable."""
    for provider_info in MODELS.values():
        for model_info in provider_info["models"].values():
            # Input rates should be positive and reasonable
            assert 0 < model_info["input_rate"] < 1.0
            
            # Output rates should be non-negative if present
            if "output_rate" in model_info:
                assert 0 < model_info["output_rate"] < 1.0

def test_max_images_limits():
    """Test that max_images limits are reasonable."""
    assert MODELS["openai"]["max_images"] == 1  # OpenAI supports single image
    assert MODELS["claude"]["max_images"] > 1  # Claude supports multiple images
    assert MODELS["gemini"]["max_images"] > 1  # Gemini supports multiple images 