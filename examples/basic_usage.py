"""
Basic usage examples for Token Vision.
"""

from pathlib import Path
from token_vision import ImageTokenCalculator

def main():
    # Initialize calculator with default settings
    calculator = ImageTokenCalculator()

    # Get sample image path
    sample_image = next(Path("examples/sample_images").glob("*.jpg"))

    # Calculate tokens for a single image
    try:
        tokens = calculator.calculate(sample_image)
        print(f"\nAnalyzing image: {sample_image.name}")
        print(f"Tokens required: {tokens:,}")
        print(f"Cost: ${calculator.get_cost(tokens):.6f}")
    except ValueError as e:
        print(f"Error processing image: {e}")

    # Try different models
    models = [
        "gpt-4o",
        "gpt-4o-2024-05-13",
        "claude-3-opus",
        "gemini-1.5-pro"
    ]

    print("\nComparison across models:")
    print("-" * 50)
    for model in models:
        try:
            tokens = calculator.calculate(
                sample_image,
                model=model
            )
            cost = calculator.get_cost(tokens, model)
            print(f"{model}:")
            print(f"  Tokens: {tokens:,}")
            print(f"  Cost: ${cost:.6f}")
        except ValueError as e:
            print(f"{model}: Error - {e}")
        print("-" * 50)

    # Batch processing example
    print("\nBatch Processing Example:")
    print("-" * 50)
    try:
        # Get all sample images
        image_paths = list(Path("examples/sample_images").glob("*.jpg"))
        print(f"Processing {len(image_paths)} images...")
        
        # Calculate tokens for each image
        tokens_list = calculator.calculate_batch(image_paths)
        
        # Print results
        for image_path, tokens in zip(image_paths, tokens_list):
            cost = calculator.get_cost(tokens)
            print(f"\nImage: {image_path.name}")
            print(f"Tokens: {tokens:,}")
            print(f"Cost: ${cost:.6f}")
        
        # Print total
        total_tokens = sum(tokens_list)
        total_cost = calculator.get_cost(total_tokens)
        print("\nTotal:")
        print(f"Total Tokens: {total_tokens:,}")
        print(f"Total Cost: ${total_cost:.6f}")
        
    except ValueError as e:
        print(f"Error in batch processing: {e}")

if __name__ == "__main__":
    main() 