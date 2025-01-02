"""Tests for the ImageTokenCalculator class."""

import os
import sys
from pathlib import Path

import pytest
from PIL import Image
import numpy as np

# Add the src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from token_vision import ImageTokenCalculator, TokenResult
from token_vision.models import get_model_info

# Get the path to the sample images directory
SAMPLE_IMAGES_DIR = Path(__file__).parent.parent / "examples" / "sample_images"

@pytest.fixture
def calculator():
    return ImageTokenCalculator()

@pytest.fixture
def test_image():
    return np.zeros((1024, 1024, 3), dtype=np.uint8)

def test_token_result_structure(calculator, test_image):
    """Test that TokenResult contains the expected attributes."""
    result = calculator.calculate(test_image)
    assert isinstance(result, TokenResult)
    assert hasattr(result, 'tokens')
    assert hasattr(result, 'warnings')
    assert isinstance(result.tokens, int)
    assert isinstance(result.warnings, list)

def test_small_image_tokens(calculator):
    """Test token calculation for small images."""
    small_image = np.zeros((384, 384, 3), dtype=np.uint8)
    result = calculator.calculate(small_image)
    assert result.tokens == 255  # Base token count
    assert not result.warnings  # Should have no warnings

def test_large_image_warning(calculator):
    """Test warnings for large images."""
    large_image = np.zeros((4096, 4096, 3), dtype=np.uint8)
    result = calculator.calculate(large_image)
    assert result.tokens > 0
    assert len(result.warnings) > 0
    assert "exceed recommended size" in result.warnings[0]

def test_different_models(calculator, test_image):
    """Test token calculation across different models."""
    models = {
        "claude-3-opus": (1000, True),    # (min_expected_tokens, has_output_cost)
        "gpt-4-vision": (500, False),
        "gemini-1-5-pro": (500, True)
    }
    
    for model, (min_tokens, has_output) in models.items():
        result = calculator.calculate(test_image, model=model)
        cost = calculator.get_cost(result.tokens, model=model)
        
        assert result.tokens >= min_tokens
        assert cost > 0
        if has_output:
            model_info = get_model_info(model)
            assert "output_rate" in model_info

def test_batch_processing(calculator):
    """Test batch processing functionality."""
    images = [
        np.zeros((512, 512, 3), dtype=np.uint8),
        np.zeros((1024, 1024, 3), dtype=np.uint8),
        np.zeros((2048, 2048, 3), dtype=np.uint8)
    ]
    
    results = calculator.calculate_batch(images)
    assert len(results) == 3
    assert all(isinstance(r, TokenResult) for r in results)
    assert results[0].tokens < results[1].tokens < results[2].tokens

def test_cost_calculation(calculator, test_image):
    """Test cost calculation accuracy."""
    result = calculator.calculate(test_image, model="claude-3-opus")
    cost = calculator.get_cost(result.tokens, model="claude-3-opus")
    
    # Claude-3-opus rates: input=0.015, output=0.075
    expected_input_cost = result.tokens * 0.015 / 1_000_000
    expected_output_cost = result.tokens * 0.075 / 1_000_000
    expected_total = expected_input_cost + expected_output_cost
    
    assert cost == pytest.approx(expected_total, rel=1e-6)

def test_detail_level(calculator, test_image):
    """Test detail level affects token count."""
    high_detail = calculator.calculate(test_image, detail_level="high")
    low_detail = calculator.calculate(test_image, detail_level="low")
    
    assert high_detail.tokens > low_detail.tokens

def test_input_validation(calculator):
    """Test input validation and error handling."""
    with pytest.raises(ValueError):
        calculator.calculate(None)
    
    with pytest.raises((ValueError, FileNotFoundError)):
        calculator.calculate("nonexistent.jpg")
    
    with pytest.raises(ValueError):
        calculator.calculate(test_image, model="nonexistent-model")

def test_max_images_limit(calculator):
    """Test max images limit in batch processing."""
    # OpenAI has max_images=1
    images = [np.zeros((512, 512, 3), dtype=np.uint8)] * 2
    
    with pytest.raises(ValueError) as exc_info:
        calculator.calculate_batch(images, model="gpt-4-vision")
    assert "Maximum 1 images allowed" in str(exc_info.value) 