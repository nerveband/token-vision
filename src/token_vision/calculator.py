from typing import Union, Dict, Any, Tuple, NamedTuple
from pathlib import Path
import math
import warnings
import numpy as np
from PIL import Image

from .models import MODELS, get_model_info, get_provider_for_model

class TokenResult(NamedTuple):
    """Result of token calculation containing token count and any warnings."""
    tokens: int
    warnings: list[str]

class ImageTokenCalculator:
    def __init__(self, default_model: str = "gemini-1-5-flash", detail_level: str = "high"):
        self.default_model = default_model
        self.detail_level = detail_level
        
    def _get_image_dimensions(self, image_path: Union[str, Path, np.ndarray]) -> Tuple[int, int]:
        """Get image dimensions from various input types."""
        if isinstance(image_path, (str, Path)):
            with Image.open(image_path) as img:
                return img.size
        elif isinstance(image_path, np.ndarray):
            return image_path.shape[1], image_path.shape[0]  # width, height
        else:
            raise ValueError("Unsupported image input type")
            
    def _calculate_claude_tokens(self, width: int, height: int) -> TokenResult:
        """Calculate tokens for Claude models."""
        warnings = []
        if width * height <= 384 * 384:
            return TokenResult(258, warnings)
            
        if width > 2048 or height > 2048:
            warnings.append(
                f"Image dimensions ({width}x{height}) exceed Claude's optimal size. "
                "The model will automatically scale this down. Consider resizing to max 2048px "
                "on the longest side to reduce bandwidth costs."
            )
            
        tile_size = min(max(256, min(width, height) / 1.5), 768)
        tiles_x = math.ceil(width / tile_size)
        tiles_y = math.ceil(height / tile_size)
        return TokenResult(tiles_x * tiles_y * 258, warnings)
        
    def _calculate_other_tokens(self, width: int, height: int) -> TokenResult:
        """Calculate tokens for OpenAI and Gemini models."""
        warnings = []
        if self.detail_level == "low":
            return TokenResult(85, warnings)
            
        if width > 2048 or height > 2048:
            warnings.append(
                f"Image dimensions ({width}x{height}) exceed recommended size. "
                "The model will automatically scale this down. Consider resizing to max 2048px "
                "on the longest side to reduce bandwidth costs."
            )
            
        # Calculate tiles based on original dimensions
        tiles_x = math.ceil(width / 512)
        tiles_y = math.ceil(height / 512)
        total_tiles = tiles_x * tiles_y
        
        return TokenResult(total_tiles * 170 + 85, warnings)
        
    def calculate(self, 
                 image_path: Union[str, Path, np.ndarray],
                 model: str = None,
                 detail_level: str = None) -> TokenResult:
        """
        Calculate tokens for an image.
        
        Returns:
            TokenResult: A named tuple containing:
                - tokens: The number of tokens required
                - warnings: List of warnings about image size and scaling
        """
        model = model or self.default_model
        self.detail_level = detail_level or self.detail_level
        
        # Get image dimensions
        width, height = self._get_image_dimensions(image_path)
        
        # Get provider
        provider = get_provider_for_model(model)
        
        # Calculate tokens based on provider
        if provider == "claude":
            return self._calculate_claude_tokens(width, height)
        else:
            return self._calculate_other_tokens(width, height)
            
    def get_cost(self, tokens: int, model: str = None) -> float:
        """Calculate cost for given tokens."""
        model = model or self.default_model
        model_info = get_model_info(model)
        
        input_cost = tokens * model_info["input_rate"] / 1_000_000
        output_cost = tokens * model_info.get("output_rate", 0) / 1_000_000
        
        return input_cost + output_cost
        
    def calculate_batch(self, image_paths: list, model: str = None) -> list[TokenResult]:
        """Calculate tokens for multiple images."""
        model = model or self.default_model
        provider = get_provider_for_model(model)
        max_images = MODELS[provider]["max_images"]
        
        if len(image_paths) > max_images:
            raise ValueError(f"Maximum {max_images} images allowed for {provider}")
            
        return [self.calculate(img, model) for img in image_paths]
        
    def get_cost_batch(self, tokens: list[int], model: str = None) -> float:
        """Calculate total cost for batch of images."""
        return sum(self.get_cost(t, model) for t in tokens)

__all__ = ["ImageTokenCalculator", "TokenResult"]
