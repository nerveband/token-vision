# Technical Context

## Technologies Used
1. **Core Technologies**
   - Python 3.8+
   - NumPy for array operations
   - PIL/Pillow for image processing
   - typing for type hints
   - dataclasses for data structures

2. **Development Tools**
   - pytest for testing
   - mypy for type checking
   - black for code formatting
   - flake8 for linting
   - isort for import sorting
   - coverage.py for test coverage

3. **Build Tools**
   - setuptools for packaging
   - build for distribution
   - twine for PyPI uploads
   - wheel for binary distribution

## Development Setup
1. **Environment Setup**
   ```bash
   # Create virtual environment
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows

   # Install dependencies
   pip install -r requirements.txt
   pip install -e .  # Install in editable mode
   ```

2. **Testing Setup**
   ```bash
   # Run tests
   pytest tests/
   
   # Run with coverage
   pytest --cov=token_vision tests/
   
   # Type checking
   mypy token_vision/
   ```

3. **Code Quality**
   ```bash
   # Format code
   black token_vision/
   
   # Sort imports
   isort token_vision/
   
   # Lint code
   flake8 token_vision/
   ```

## Technical Constraints
1. **Performance Requirements**
   - Fast token calculation (< 100ms per image)
   - Efficient memory usage
   - Scalable batch processing

2. **Compatibility**
   - Python 3.8+ support
   - Cross-platform compatibility
   - No external runtime dependencies

3. **Memory Management**
   - Efficient image loading
   - Stream processing for large files
   - Memory-efficient batch operations

4. **Error Handling**
   - Graceful error recovery
   - Informative error messages
   - Type safety

5. **Security**
   - No API key storage
   - Safe file handling
   - Input validation

## Dependencies
1. **Required Dependencies**
   ```
   numpy>=1.19.0
   Pillow>=8.0.0
   typing-extensions>=4.0.0
   ```

2. **Development Dependencies**
   ```
   pytest>=6.0.0
   pytest-cov>=2.0.0
   mypy>=0.800
   black>=21.0
   flake8>=3.9.0
   isort>=5.0.0
   ```

3. **Optional Dependencies**
   ```
   tqdm>=4.0.0  # for progress bars
   requests>=2.25.0  # for URL support
   ``` 