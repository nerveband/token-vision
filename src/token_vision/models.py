from typing import Dict, Any
import json
from pathlib import Path

MODELS = {
    "claude": {
        "name": "Claude",
        "max_images": 3000,
        "models": {
            "claude-3-sonnet": {
                "name": "Claude 3.5 Sonnet",
                "input_rate": 0.003,
                "output_rate": 0.015
            },
            "claude-3-haiku": {
                "name": "Claude 3.5 Haiku",
                "input_rate": 0.0008,
                "output_rate": 0.004
            },
            "claude-3-opus": {
                "name": "Claude 3 Opus",
                "input_rate": 0.015,
                "output_rate": 0.075
            }
        }
    },
    "openai": {
        "name": "OpenAI",
        "max_images": 1,
        "models": {
            "gpt-4-vision": {
                "name": "GPT-4V",
                "input_rate": 0.01
            },
            "gpt-4o": {
                "name": "GPT-4o",
                "input_rate": 0.00250
            }
        }
    },
    "gemini": {
        "name": "Google Gemini",
        "max_images": 3000,
        "models": {
            "gemini-1-5-pro": {
                "name": "Gemini 1.5 Pro",
                "input_rate": 0.00125,
                "output_rate": 0.005
            },
            "gemini-1-5-flash": {
                "name": "Gemini 1.5 Flash",
                "input_rate": 0.000075,
                "output_rate": 0.0003
            }
        }
    }
}

def get_model_info(model_name: str) -> Dict[str, Any]:
    """Get model information by model name."""
    for provider in MODELS.values():
        if model_name in provider["models"]:
            return provider["models"][model_name]
    raise ValueError(f"Model {model_name} not found")

def get_provider_for_model(model_name: str) -> str:
    """Get provider name for a given model."""
    for provider_name, provider in MODELS.items():
        if model_name in provider["models"]:
            return provider_name
    raise ValueError(f"Provider not found for model {model_name}")

def load_custom_models(config_path: str) -> Dict[str, Any]:
    """Load custom model configurations from a JSON file."""
    path = Path(config_path)
    if not path.exists():
        raise FileNotFoundError(f"Model config file not found: {config_path}")
        
    with open(path) as f:
        custom_models = json.load(f)
        # Merge with existing models
        MODELS.update(custom_models)
        return custom_models

__all__ = ["MODELS", "get_model_info", "get_provider_for_model", "load_custom_models"]
