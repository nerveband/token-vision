"""
Example demonstrating Token Vision usage with different LLM models.
This example shows how to:
1. Use the default models (Anthropic, OpenAI, Google)
2. Load your own model configurations
3. Calculate tokens and costs for different models
"""

from pathlib import Path
from token_vision import ImageTokenCalculator
from token_vision.models import load_models, reset_models

def main():
    # Initialize calculator with default models from examples/models.json
    calculator = ImageTokenCalculator()

    # Get sample image path
    sample_image = next(Path("examples/sample_images").glob("*.jpg"))

    print("\nAnthropic Models:")
    print("-" * 50)
    for model in ["claude-3-opus", "claude-3-sonnet", "claude-3-haiku"]:
        try:
            tokens = calculator.calculate(sample_image, model=model)
            cost = calculator.get_cost(tokens, model=model)
            print(f"{model}:")
            print(f"  Tokens: {tokens:,}")
            print(f"  Cost: ${cost:.6f}")
            print("-" * 30)
        except ValueError as e:
            print(f"Error with {model}: {e}")
            print("-" * 30)

    print("\nOpenAI Models:")
    print("-" * 50)
    for model in ["gpt-4o", "gpt-4o-2024-11-20"]:
        try:
            tokens = calculator.calculate(sample_image, model=model)
            cost = calculator.get_cost(tokens, model=model)
            print(f"{model}:")
            print(f"  Tokens: {tokens:,}")
            print(f"  Cost: ${cost:.6f}")
            print("-" * 30)
        except ValueError as e:
            print(f"Error with {model}: {e}")
            print("-" * 30)

    print("\nGoogle Models:")
    print("-" * 50)
    for model in ["gemini-1-5-pro", "gemini-1-5-flash"]:
        try:
            tokens = calculator.calculate(sample_image, model=model)
            cost = calculator.get_cost(tokens, model=model)
            print(f"{model}:")
            print(f"  Tokens: {tokens:,}")
            print(f"  Cost: ${cost:.6f}")
            print("-" * 30)
        except ValueError as e:
            print(f"Error with {model}: {e}")
            print("-" * 30)

    # Example: Loading your own model configuration
    print("\nLoading Custom Configuration:")
    print("-" * 50)
    print("To use your own models, create a JSON file with your model configurations")
    print("and load it using load_models('/path/to/your/models.json')")
    print("\nExample JSON structure:")
    print("""{
    "your_provider": {
        "name": "Your Provider Name",
        "max_images": 1000,
        "models": {
            "your-model-name": {
                "name": "Your Model Display Name",
                "provider": "your_provider",
                "input_rate": 1.0,
                "output_rate": 2.0,
                "batch_input_rate": 0.5,
                "batch_output_rate": 1.0,
                "cached_input_rate": 0.25,
                "cached_output_rate": 0.5
            }
        }
    }
}""")

if __name__ == "__main__":
    main() 