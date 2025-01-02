from token_vision import ImageTokenCalculator, MODELS
import numpy as np
from PIL import Image

def create_test_image(width, height):
    """Create a test image with given dimensions."""
    return np.zeros((height, width, 3), dtype=np.uint8)

def test_models():
    """Test different models and providers."""
    calculator = ImageTokenCalculator()
    
    # Create a test image
    test_image = create_test_image(1024, 1024)
    
    print("\nTesting different models:")
    print("-" * 50)
    
    for provider, info in MODELS.items():
        print(f"\n{info['name']} Models:")
        for model_name in info['models']:
            result = calculator.calculate(test_image, model=model_name)
            cost = calculator.get_cost(result.tokens, model=model_name)
            print(f"  {model_name}:")
            print(f"    Tokens: {result.tokens:,}")
            print(f"    Cost: ${cost:.6f}")
            if result.warnings:
                print("    Warnings:")
                for warning in result.warnings:
                    print(f"      - {warning}")

def test_dimensions():
    """Test different image dimensions."""
    calculator = ImageTokenCalculator()
    
    print("\nTesting different dimensions:")
    print("-" * 50)
    
    dimensions = [
        (384, 384),    # Small
        (1024, 1024),  # Medium
        (2048, 2048),  # Large
        (4096, 4096),  # Very large
    ]
    
    for width, height in dimensions:
        test_image = create_test_image(width, height)
        result = calculator.calculate(test_image)
        cost = calculator.get_cost(result.tokens)
        print(f"\n{width}x{height}:")
        print(f"  Tokens: {result.tokens:,}")
        print(f"  Cost: ${cost:.6f}")
        if result.warnings:
            print("  Warnings:")
            for warning in result.warnings:
                print(f"    - {warning}")

def test_batch():
    """Test batch processing."""
    calculator = ImageTokenCalculator()
    
    print("\nTesting batch processing:")
    print("-" * 50)
    
    # Create test images
    images = [
        create_test_image(1024, 1024),
        create_test_image(2048, 1024),
        create_test_image(512, 512),
    ]
    
    results = calculator.calculate_batch(images)
    total_cost = calculator.get_cost_batch([r.tokens for r in results])
    
    print(f"\nBatch Results:")
    for i, result in enumerate(results):
        print(f"  Image {i+1}:")
        print(f"    Tokens: {result.tokens:,}")
        if result.warnings:
            print("    Warnings:")
            for warning in result.warnings:
                print(f"      - {warning}")
    print(f"Total Cost: ${total_cost:.6f}")

if __name__ == "__main__":
    print("Testing token-vision package...")
    test_models()
    test_dimensions()
    test_batch() 