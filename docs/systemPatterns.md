# System Patterns

## System Architecture
1. **Core Components**
   - ImageTokenCalculator (main class)
   - Model definitions and configurations
   - Token calculation algorithms
   - Cost estimation utilities
   - Image processing utilities

2. **Directory Structure**
   ```
   token-vision/
   ├── token_vision/
   │   ├── __init__.py
   │   ├── calculator.py
   │   ├── models.py
   │   └── utils/
   ├── tests/
   ├── docs/
   ├── examples/
   └── dist/
   ```

## Key Technical Decisions
1. **Type System**
   - Comprehensive type hints throughout
   - Named tuples for structured returns
   - Clear interface definitions

2. **Error Handling**
   - Custom exceptions for specific error cases
   - Informative error messages
   - Graceful fallbacks

3. **Image Processing**
   - No automatic resizing
   - Original dimension preservation
   - Warning system for optimization

4. **Token Calculation**
   - Model-specific algorithms
   - Accurate tiling implementation
   - Efficient memory usage

5. **Cost Estimation**
   - Per-model pricing
   - Batch rate support
   - Custom rate configuration

## Architecture Patterns
1. **Clean Architecture**
   - Separation of concerns
   - Dependency injection
   - Interface-based design

2. **Factory Pattern**
   - Model creation
   - Calculator instantiation
   - Configuration loading

3. **Strategy Pattern**
   - Token calculation strategies
   - Cost calculation strategies
   - Image processing strategies

4. **Builder Pattern**
   - Calculator configuration
   - Model configuration
   - Result construction

5. **Observer Pattern**
   - Warning collection
   - Progress tracking
   - Event handling

## Development Practices
1. **Code Quality**
   - Type checking with mypy
   - Linting with flake8
   - Formatting with black
   - Import sorting with isort

2. **Testing**
   - pytest for unit tests
   - Coverage reporting
   - Integration tests
   - Performance benchmarks

3. **Documentation**
   - Docstrings
   - Type hints
   - README
   - API reference

4. **Version Control**
   - Semantic versioning
   - Feature branches
   - Pull request workflow
   - Release tagging 