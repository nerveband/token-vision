"""Test configuration for Token Vision."""

import sys
from pathlib import Path

import pytest

# Add the src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

@pytest.fixture(autouse=True)
def setup_test_env():
    """Set up the test environment."""
    # Ensure the sample images directory exists
    sample_images_dir = Path(__file__).parent.parent / "examples" / "sample_images"
    assert sample_images_dir.exists(), "Sample images directory not found"
    
    # Ensure the models.json file exists
    models_json = Path(__file__).parent.parent / "examples" / "models.json"
    assert models_json.exists(), "Models configuration file not found" 