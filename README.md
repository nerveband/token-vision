![Token Vision Banner](token-vision-banner.jpg)

> **Warning**: This is an experimental alpha release. APIs and functionality may change significantly between versions.

# Token Vision

A fast, offline token calculator for images with various AI models (Claude, OpenAI, Google). Calculate image tokens and costs without making API calls or hitting rate limits.

## Author
Ashraf Ali (ashrafali.net)

## Advantages

- **Offline Operation**: Calculate tokens without internet connectivity or API keys
- **No Rate Limits**: Process unlimited images without worrying about API quotas
- **Ultra Fast**: Get instant results without network latency
- **Cost Efficient**: Plan and estimate costs without spending API credits
- **Multi-Model Support**: One library for all major vision models
- **Accurate**: Uses the same tiling and scaling algorithms as the official implementations
- **Developer Friendly**: Clean API with type hints and comprehensive documentation
- **Extensible**: Support for custom models and pricing configurations

## Installation

```bash
pip install token-vision
```

## Quick Start

```python
from token_vision import ImageTokenCalculator

# Initialize calculator
calculator = ImageTokenCalculator()

# Calculate tokens and get warnings
result = calculator.calculate("image.jpg")
print(f"Tokens: {result.tokens:,}")
print(f"Warnings: {result.warnings}")  # List of any size/optimization warnings

# Get cost
cost = calculator.get_cost(result.tokens)
print(f"Cost: ${cost:.6f}")
```

## Return Values

The library provides clean, typed return values for easy integration:

```python
# TokenResult named tuple contains:
result = calculator.calculate("image.jpg")
result.tokens    # int: Number of tokens
result.warnings  # list[str]: Any warnings about size/optimization

# Direct numerical values
cost = calculator.get_cost(result.tokens)  # float: Cost in USD

# Batch processing returns lists
results = calculator.calculate_batch(["img1.jpg", "img2.jpg"])
for result in results:
    print(f"Tokens: {result.tokens}")
    print(f"Warnings: {result.warnings}")

# Get total cost for batch
total_cost = calculator.get_cost_batch([r.tokens for r in results])
```

### Example Use Cases

```python
# Cost-based decision making
def process_if_affordable(image_path, budget=0.01):
    calculator = ImageTokenCalculator()
    result = calculator.calculate(image_path)
    cost = calculator.get_cost(result.tokens)
    
    return {
        "can_process": cost <= budget,
        "tokens": result.tokens,
        "cost": cost,
        "needs_optimization": bool(result.warnings)
    }

# Model comparison
def find_cheapest_model(image_path):
    calculator = ImageTokenCalculator()
    models = ["claude-3-opus", "gpt-4-vision", "gemini-1-5-pro"]
    
    costs = {
        model: calculator.get_cost(
            calculator.calculate(image_path, model=model).tokens,
            model=model
        )
        for model in models
    }
    
    return min(costs.items(), key=lambda x: x[1])
```

## Features

- Support for multiple AI models:
  - Claude (3.5 Sonnet, 3.5 Haiku, 3 Opus, 3 Sonnet, 3 Haiku)
  - OpenAI (Latest, Nov 2024, Aug 2024, May 2024)
  - Google (Gemini 1.5 Pro, 1.5 Flash)
- Accurate token calculation based on image dimensions
- Cost estimation for both input and output tokens
- Support for various image input formats:
  - File paths (str/Path)
  - NumPy arrays
  - PIL Images
- Batch processing capabilities
- Memory efficient processing
- Custom model configuration support
- Smart image size handling:
  - No automatic resizing - calculates tokens for original dimensions
  - Provides warnings when images exceed model-specific optimal sizes
  - Suggests optimizations to reduce bandwidth costs

## Documentation

### Image Size Handling

The library calculates tokens based on your original image dimensions while providing helpful warnings:

```python
from token_vision import ImageTokenCalculator

calculator = ImageTokenCalculator()

# Calculate tokens for a large image
result = calculator.calculate("large_image.jpg")
print(f"Tokens: {result.tokens:,}")

# Check for any size-related warnings
if result.warnings:
    print("\nWarnings:")
    for warning in result.warnings:
        print(f"- {warning}")
```

Example output for a 4096x4096 image:
```
Tokens: 12,545
Warnings:
- Image dimensions (4096x4096) exceed recommended size. The model will automatically scale this down. Consider resizing to max 2048px on the longest side to reduce bandwidth costs.
```

The library will:
1. Calculate tokens for your original image size
2. Warn you if the image exceeds model-specific optimal dimensions
3. Explain how the model will handle the image
4. Suggest optimizations to reduce bandwidth costs

This approach gives you full control while providing the information needed to optimize your usage.

### Supported Models

The library supports the following models with their respective token calculation methods:

#### Claude Models
- claude-3-5-sonnet-20241022
- claude-3-5-haiku-20241022
- claude-3-opus-20240229
- claude-3-sonnet-20240229
- claude-3-haiku-20240307

#### OpenAI Models
- gpt-4o
- gpt-4o-2024-11-20
- gpt-4o-2024-08-06
- gpt-4o-2024-05-13

#### Google Models
- gemini-1-5-pro
- gemini-1-5-flash (default)

### Custom Models

You can add your own models or override existing ones using a JSON configuration file:

```python
from token_vision import ImageTokenCalculator
from token_vision.models import load_custom_models

# Load custom models
load_custom_models("path/to/custom_models.json")

# Use custom model
calculator = ImageTokenCalculator()
tokens = calculator.calculate("image.jpg", model="custom-model-v1")
```

Example custom_models.json:
```json
{
    "custom-provider": {
        "name": "Custom Provider",
        "max_images": 10,
        "token_multiplier": 1.0,
        "models": {
            "custom-model-v1": {
                "name": "Custom Model V1",
                "input_rate": 15000,
                "output_rate": 75000,
                "batch_input_rate": 7500,
                "batch_output_rate": 37500,
                "cached_input_rate": 1500,
                "cached_output_rate": 7500
            }
        }
    }
}
```

### Advanced Usage

```python
# Custom configuration
calculator = ImageTokenCalculator(
    default_model="gemini-1-5-flash",
    detail_level="high"
)

# Process multiple images
results = calculator.calculate_batch([
    "image1.jpg",
    "image2.jpg"
])

# Get batch costs (uses batch rates)
costs = calculator.get_cost_batch(results)

# Using numpy arrays
import numpy as np
image_array = np.array(...)  # Your image data
result = calculator.calculate(
    image=image_array,
    model="gemini-1-5-flash",
    detail_level="low"
)
```

## Development

### Setup

1. Clone the repository:
```bash
git clone https://github.com/nerveband/token-vision.git
cd token-vision
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install development dependencies:
```bash
pip install -e ".[dev]"
```

### Running Tests

```bash
pytest
```

## License

This project is licensed under the MIT License - see the LICENSE file for details. 